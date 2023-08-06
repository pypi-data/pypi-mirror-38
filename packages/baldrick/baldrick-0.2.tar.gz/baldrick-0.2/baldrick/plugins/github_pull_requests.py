from flask import current_app

from baldrick.github.github_api import RepoHandler, PullRequestHandler
from baldrick.blueprints.github import github_webhook_handler

__all__ = ['pull_request_handler']

PULL_REQUEST_CHECKS = []


def pull_request_handler(func):
    """
    A decorator to add functions to the pull request checker.

    Functions decorated with this decorator will be passed events which match
    the following actions:

    * unlabeled
    * labeled
    * synchronize
    * opened
    * milestoned
    * demilestoned

    They will be passed ``(pr_handler, repo_handler)`` and are expected to
    return a dictionary where the key is a unique string that refers to the
    specific check that has been made, and the values are dictionaries with
    the following keys:

    * ``status`` is a string giving the state for the latest commit (one of
      ``success``, ``failure``, ``error``, or ``pending``).
    * ``message``: the message to be shown in the status
    * ``target_url`` (optional): a URL to link to in the status
    """
    PULL_REQUEST_CHECKS.append(func)
    return func


@github_webhook_handler
def handle_pull_requests(repo_handler, payload, headers):
    """
    Handle pull request events which match the following event types:
    """

    event = headers['X-GitHub-Event']

    if event not in ('pull_request', 'issues'):
        return "Not a pull_request or issues event"

    # We only need to listen to certain kinds of events:
    if event == 'pull_request':
        if payload['action'] not in ('unlabeled', 'labeled', 'synchronize', 'opened'):
            return "Action '" + payload['action'] + "' does not require action"
    elif event == 'issues':
        if payload['action'] not in ('milestoned', 'demilestoned'):
            return "Action '" + payload['action'] + "' does not require action"

    if event == 'pull_request':
        number = payload['pull_request']['number']
    elif event == 'issues':
        number = payload['issue']['number']
    else:
        return "Not an issue or pull request"

    return process_pull_request(repo_handler.repo, number, repo_handler.installation)


def process_pull_request(repository, number, installation):

    # TODO: cache handlers and invalidate the internal cache of the handlers on
    # certain events.
    pr_handler = PullRequestHandler(repository, number, installation)

    pr_config = pr_handler.get_config_value("pull_requests", {})
    if not pr_config.get("enabled", False):
        return "Skipping PR checks, disabled in config."

    post_comment = pr_config.get("post_pr_comment", False)
    pull_request_substring = pr_config.get('pull_request_substring', '')

    # Disable if the config is not present
    if pr_config is None:
        return

    # Don't comment on closed PR
    if pr_handler.is_closed:
        return "Pull request already closed, no need to check"

    repo_handler = RepoHandler(pr_handler.head_repo_name,
                               pr_handler.head_branch, installation)

    def is_previous_comment(message):
        if len(pull_request_substring) > 0:
            return pull_request_substring in message
        else:
            return True

    # Find previous comments by this app
    comment_ids = pr_handler.find_comments(f'{current_app.bot_username}[bot]',
                                           filter_keep=is_previous_comment)

    if len(comment_ids) == 0:
        comment_id = None
    else:
        comment_id = comment_ids[-1]

    # First check whether there are labels that indicate the checks should be
    # skipped

    skip_labels = pr_config.get("skip_labels", [])
    skip_fails = pr_config.get("skip_fails", True)

    for label in pr_handler.labels:
        if label in skip_labels:
            if post_comment:
                skip_message = pr_config.get("skip_message", "Pull request checks have "
                                             "been skipped as this pull request has been "
                                             f"labelled as **{label}**")
                skip_message = skip_message.format(pr_handler=pr_handler, repo_handler=repo_handler)
                pr_handler.submit_comment(skip_message, comment_id=comment_id)
            if skip_fails:
                pr_handler.set_status('failure', "Skipping checks due to {0} label".format(label), current_app.bot_username)
            return

    results = {}
    for function in PULL_REQUEST_CHECKS:
        result = function(pr_handler, repo_handler)
        # Ignore skipped checks
        if result is not None:
            results.update(result)

    failures = [details['description'] for details in results.values() if details['state'] in ('error', 'failure')]

    if post_comment:

        # Post all failures in a comment, and have a single status check

        if failures:

            pull_request_prologue = pr_config.get('fail_prologue', '')
            pull_request_epilogue = pr_config.get('fail_epilogue', '')

            fail_status = pr_config.get('fail_status', 'Failed some checks')

            message = pull_request_prologue.format(pr_handler=pr_handler, repo_handler=repo_handler)
            for failure in failures:
                message += f'* {failure}\n'
            message += pull_request_epilogue.format(pr_handler=pr_handler, repo_handler=repo_handler)
            comment_url = pr_handler.submit_comment(message, comment_id=comment_id, return_url=True)

            pr_handler.set_status('failure', fail_status, current_app.bot_username, target_url=comment_url)

        else:

            pass_status = pr_config.get('pass_status', 'Passed all checks')

            all_passed_message = pr_config.get('all_passed_message', '')
            all_passed_message = all_passed_message.format(pr_handler=pr_handler, repo_handler=repo_handler)

            if all_passed_message:
                pr_handler.submit_comment(all_passed_message, comment_id=comment_id)

            pr_handler.set_status('success', pass_status, current_app.bot_username)

    else:

        # Post each failure as a status

        existing_statuses = pr_handler.list_statuses()

        for context, details in sorted(results.items()):

            full_context = current_app.bot_username + ':' + context

            # NOTE: we could in principle check if the status has been posted
            # before, and if so not post it again, but we had this in the past
            # and there were some strange caching issues where GitHub would
            # return old status messages, so we avoid doing that.

            pr_handler.set_status(details['state'], details['description'],
                                  full_context,
                                  target_url=details.get('target_url'))

        # For statuses that have been skipped this time but existed before, set
        # status to pass and set message to say skipped

        for full_context in existing_statuses:

            if full_context.startswith(current_app.bot_username + ':'):
                context = full_context[len(current_app.bot_username) + 1:]
                if context not in results:
                    pr_handler.set_status('success', 'This check has been skipped',
                                          current_app.bot_username + ':' + context)

            # Also set the general 'single' status check as a skipped check if it
            # is present
            if full_context == current_app.bot_username:
                pr_handler.set_status('success', 'This check has been skipped',
                                      current_app.bot_username)

        # If a comment has been posted before, and to be careful only if it is
        # a comment that matches the specified substring, we edit the comment.
        if len(pull_request_substring) > 0 and len(comment_ids) > 0:
            for comment_id in comment_ids:
                pr_handler.submit_comment(f'Check results are now reported in the '
                                          'status checks at the bottom of this page.',
                                          comment_id=comment_id)

    return 'Finished pull requests checks'
