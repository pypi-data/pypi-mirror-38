import json
from copy import copy
from unittest.mock import MagicMock, patch, PropertyMock

from baldrick.github.github_api import cfg_cache
from baldrick.plugins.github_pull_requests import pull_request_handler, PULL_REQUEST_CHECKS

test_hook = MagicMock()


CONFIG_TEMPLATE = """
[ tool.testbot ]
[ tool.testbot.pull_requests ]
enabled = true
post_pr_comment = {post_pr_comment}
all_passed_message = '{all_passed_message}'
fail_prologue = '{fail_prologue}'
fail_epilogue = '{fail_epilogue}'
"""


def setup_module(module):
    module.PULL_REQUEST_CHECKS_ORIG = copy(PULL_REQUEST_CHECKS)
    pull_request_handler(test_hook)


def teardown_module(module):
    PULL_REQUEST_CHECKS[:] = module.PULL_REQUEST_CHECKS_ORIG[:]


class TestPullRequestHandler:

    def setup_method(self, method):

        test_hook.resetmock()

        self.pr_comments = []
        self.existing_statuses = []
        self.pr_open = True

        self.requests_get_mock = patch('requests.get', self._requests_get)
        self.requests_post_mock = patch('requests.post')
        self.get_file_contents_mock = patch('baldrick.github.github_api.GitHubHandler.get_file_contents')
        self.get_installation_token_mock = patch('baldrick.github.github_auth.get_installation_token')
        self.labels_mock = patch('baldrick.github.github_api.PullRequestHandler.labels',
                                 new_callable=PropertyMock)

        self.requests_get = self.requests_get_mock.start()
        self.requests_post = self.requests_post_mock.start()
        self.get_file_contents = self.get_file_contents_mock.start()
        self.get_installation_token = self.get_installation_token_mock.start()
        self.labels = self.labels_mock.start()

        self.get_installation_token.return_value = 'abcdefg'
        self.labels.return_value = []

        cfg_cache.clear()

    def teardown_method(self, method):
        self.requests_get_mock.stop()
        self.requests_post_mock.stop()
        self.get_file_contents_mock.stop()
        self.get_installation_token_mock.stop()
        self.labels = self.labels_mock.stop()

    def _requests_get(self, url, headers=None):
        req = MagicMock()
        req.ok = True
        if url == 'https://api.github.com/repos/test-repo/pulls/1234':
            req.json.return_value = {'base': {'ref': 'master'},
                                     'state': 'open' if self.pr_open else 'closed',
                                     'head': {'ref': 'custom', 'sha': 'abc464aa',
                                              'repo': {'full_name': 'contributor/test'}}}
            return req
        elif url == 'https://api.github.com/repos/test-repo/issues/1234/comments':
            req.json.return_value = self.pr_comments
        elif url == 'https://api.github.com/repos/test-repo/commits/abc464aa/statuses':
            req.json.return_value = self.existing_statuses
        else:
            raise ValueError('Unexepected URL: {0}'.format(url))
        return req

    def send_event(self, client):

        data = {'pull_request': {'number': '1234'},
                'repository': {'full_name': 'test-repo'},
                'action': 'synchronize',
                'installation': {'id': '123'}}

        headers = {'X-GitHub-Event': 'pull_request'}

        client.post('/github', data=json.dumps(data), headers=headers,
                    content_type='application/json')

    def test_empty_default(self, app, client):

        # Test case where the config doesn't give a default message, and the
        # registered handlers don't return any checks

        test_hook.return_value = {}
        self.get_file_contents.return_value = CONFIG_TEMPLATE.format(post_pr_comment='true',
                                                                     all_passed_message="''",
                                                                     fail_prologue='', fail_epilogue='')

        self.send_event(client)

        assert self.requests_post.call_count == 1

        args, kwargs = self.requests_post.call_args
        assert args[0] == 'https://api.github.com/repos/test-repo/statuses/abc464aa'
        assert kwargs['json'] == {'state': 'success',
                                  'description': 'Passed all checks',
                                  'context': 'testbot'}

    def test_empty_with_message(self, app, client):

        # As above, but a default message is given

        test_hook.return_value = {}
        self.get_file_contents.return_value = CONFIG_TEMPLATE.format(post_pr_comment='true',
                                                                     all_passed_message='All checks passed',
                                                                     fail_prologue='', fail_epilogue='')

        self.send_event(client)

        assert self.requests_post.call_count == 2

        args, kwargs = self.requests_post.call_args_list[0]
        assert args[0] == 'https://api.github.com/repos/test-repo/issues/1234/comments'
        assert kwargs['json'] == {'body': 'All checks passed'}

        args, kwargs = self.requests_post.call_args_list[1]
        assert args[0] == 'https://api.github.com/repos/test-repo/statuses/abc464aa'
        assert kwargs['json'] == {'state': 'success',
                                  'description': 'Passed all checks',
                                  'context': 'testbot'}

    def test_all_passed(self, app, client):

        # As above, but a default message is given

        test_hook.return_value = {'test1': {'description': 'No problem', 'state': 'success'},
                                  'test2': {'description': 'All good here', 'state': 'success'}}

        self.get_file_contents.return_value = CONFIG_TEMPLATE.format(post_pr_comment='false',
                                                                     all_passed_message='All checks passed',
                                                                     fail_prologue='', fail_epilogue='')

        self.send_event(client)

        assert self.requests_post.call_count == 2

        args, kwargs = self.requests_post.call_args_list[0]
        assert args[0] == 'https://api.github.com/repos/test-repo/statuses/abc464aa'
        assert kwargs['json'] == {'state': 'success',
                                  'description': 'No problem',
                                  'context': 'testbot:test1'}

        args, kwargs = self.requests_post.call_args_list[1]
        assert args[0] == 'https://api.github.com/repos/test-repo/statuses/abc464aa'
        assert kwargs['json'] == {'state': 'success',
                                  'description': 'All good here',
                                  'context': 'testbot:test2'}

    def test_all_passed_with_comment(self, app, client):

        # As above, but a default message is given

        test_hook.return_value = {'test1': {'description': 'No problem', 'state': 'success'},
                                  'test2': {'description': 'All good here', 'state': 'success'}}

        self.get_file_contents.return_value = CONFIG_TEMPLATE.format(post_pr_comment='true',
                                                                     all_passed_message='All checks passed',
                                                                     fail_prologue='', fail_epilogue='')

        self.send_event(client)

        assert self.requests_post.call_count == 2

        args, kwargs = self.requests_post.call_args_list[0]
        assert args[0] == 'https://api.github.com/repos/test-repo/issues/1234/comments'
        assert kwargs['json'] == {'body': 'All checks passed'}

        args, kwargs = self.requests_post.call_args_list[1]
        assert args[0] == 'https://api.github.com/repos/test-repo/statuses/abc464aa'
        assert kwargs['json'] == {'state': 'success',
                                  'description': 'Passed all checks',
                                  'context': 'testbot'}

    def test_one_failure(self, app, client):

        # As above, but a default message is given

        test_hook.return_value = {'test1': {'description': 'Problems here', 'state': 'failure'},
                                  'test2': {'description': 'All good here', 'state': 'success'}}

        self.get_file_contents.return_value = CONFIG_TEMPLATE.format(post_pr_comment='false',
                                                                     all_passed_message='All checks passed',
                                                                     fail_prologue='', fail_epilogue='')

        self.send_event(client)

        assert self.requests_post.call_count == 2

        args, kwargs = self.requests_post.call_args_list[0]
        assert args[0] == 'https://api.github.com/repos/test-repo/statuses/abc464aa'
        assert kwargs['json'] == {'state': 'failure',
                                  'description': 'Problems here',
                                  'context': 'testbot:test1'}

        args, kwargs = self.requests_post.call_args_list[1]
        assert args[0] == 'https://api.github.com/repos/test-repo/statuses/abc464aa'
        assert kwargs['json'] == {'state': 'success',
                                  'description': 'All good here',
                                  'context': 'testbot:test2'}

    def test_one_failure_with_comment(self, app, client):

        # As above, but a default message is given

        test_hook.return_value = {'test1': {'description': 'Problems here', 'state': 'failure'},
                                  'test2': {'description': 'All good here', 'state': 'success'}}

        self.get_file_contents.return_value = CONFIG_TEMPLATE.format(post_pr_comment='true',
                                                                     all_passed_message='All checks passed',
                                                                     fail_prologue='', fail_epilogue='')

        self.send_event(client)

        assert self.requests_post.call_count == 2

        args, kwargs = self.requests_post.call_args_list[0]
        assert args[0] == 'https://api.github.com/repos/test-repo/issues/1234/comments'
        assert kwargs['json'] == {'body': '* Problems here\n'}

        args, kwargs = self.requests_post.call_args_list[1]
        assert args[0] == 'https://api.github.com/repos/test-repo/statuses/abc464aa'
        assert kwargs['json']['state'] == 'failure'
        assert kwargs['json']['description'] == 'Failed some checks'
        assert kwargs['json']['context'] == 'testbot'

    def test_one_failure_with_comment_prologue_epilogue(self, app, client):

        # As above, but a default message is given

        test_hook.return_value = {'test1': {'description': 'Problems here', 'state': 'failure'},
                                  'test2': {'description': 'All good here', 'state': 'success'}}

        self.get_file_contents.return_value = CONFIG_TEMPLATE.format(post_pr_comment='true',
                                                                     all_passed_message='All checks passed',
                                                                     fail_prologue='The prologue - ',
                                                                     fail_epilogue=' - The epilogue')

        self.send_event(client)

        assert self.requests_post.call_count == 2

        args, kwargs = self.requests_post.call_args_list[0]
        assert args[0] == 'https://api.github.com/repos/test-repo/issues/1234/comments'
        assert kwargs['json'] == {'body': 'The prologue - * Problems here\n - The epilogue'}

        args, kwargs = self.requests_post.call_args_list[1]
        assert args[0] == 'https://api.github.com/repos/test-repo/statuses/abc464aa'
        assert kwargs['json']['state'] == 'failure'
        assert kwargs['json']['description'] == 'Failed some checks'
        assert kwargs['json']['context'] == 'testbot'

    def test_skip_existing_statuses(self, app, client):

        # If statuses already exist, don't post them again

        test_hook.return_value = {'test1': {'description': 'Problems here', 'state': 'failure'},
                                  'test2': {'description': 'All good here', 'state': 'success'}}

        self.get_file_contents.return_value = CONFIG_TEMPLATE.format(post_pr_comment='false',
                                                                     all_passed_message='All checks passed',
                                                                     fail_prologue='', fail_epilogue='')

        self.existing_statuses = [{'context': 'testbot:test1',
                                   'description': 'Problems here',
                                   'state': 'failure'}]

        self.send_event(client)

        assert self.requests_post.call_count == 1

        args, kwargs = self.requests_post.call_args_list[0]
        assert args[0] == 'https://api.github.com/repos/test-repo/statuses/abc464aa'
        assert kwargs['json'] == {'state': 'success',
                                  'description': 'All good here',
                                  'context': 'testbot:test2'}

    def test_no_skip_existing_different_statuses(self, app, client):

        # If statuses already exist but has some differences, post again

        test_hook.return_value = {'test1': {'description': 'Problems here', 'state': 'failure'},
                                  'test2': {'description': 'All good here', 'state': 'success'}}

        self.get_file_contents.return_value = CONFIG_TEMPLATE.format(post_pr_comment='false',
                                                                     all_passed_message='All checks passed',
                                                                     fail_prologue='', fail_epilogue='')

        self.existing_statuses = [{'context': 'testbot:test1',
                                   'description': 'Problems here',
                                   'state': 'pending'},
                                  {'context': 'testbot:test2',
                                   'description': 'All good here (extra comment)',
                                   'state': 'success'},
                                  {'context': 'travis',
                                   'description': 'An unrelated status',
                                   'state': 'failure'}]

        self.send_event(client)

        assert self.requests_post.call_count == 2

        args, kwargs = self.requests_post.call_args_list[0]
        assert args[0] == 'https://api.github.com/repos/test-repo/statuses/abc464aa'
        assert kwargs['json'] == {'state': 'failure',
                                  'description': 'Problems here',
                                  'context': 'testbot:test1'}

        args, kwargs = self.requests_post.call_args_list[1]
        assert args[0] == 'https://api.github.com/repos/test-repo/statuses/abc464aa'
        assert kwargs['json'] == {'state': 'success',
                                  'description': 'All good here',
                                  'context': 'testbot:test2'}

    def test_skip_on_labels(self, app, client):

        # Test case where the config doesn't give a default message, and the
        # registered handlers don't return any checks

        test_hook.return_value = {}
        self.get_file_contents.return_value = (CONFIG_TEMPLATE.format(post_pr_comment='true',
                                                                      all_passed_message='',
                                                                      fail_prologue='',
                                                                      fail_epilogue='') +
                                               'skip_labels = [ "Experimental" ]\n' +
                                               "skip_message = 'All checks have been skipped'\n")

        self.labels.return_value = ['Experimental']

        self.send_event(client)

        assert self.requests_post.call_count == 2

        args, kwargs = self.requests_post.call_args_list[0]
        assert args[0] == 'https://api.github.com/repos/test-repo/issues/1234/comments'
        assert kwargs['json'] == {'body': 'All checks have been skipped'}

        args, kwargs = self.requests_post.call_args_list[1]
        assert args[0] == 'https://api.github.com/repos/test-repo/statuses/abc464aa'
        assert kwargs['json'] == {'state': 'failure',
                                  'description': 'Skipping checks due to Experimental label',
                                  'context': 'testbot'}

    def test_update_existing_comment(self, app, client):

        # There is already a comment that should be updated

        self.pr_comments = [{'id': 14431, 'body': 'I like apples', 'user': {'login': 'testbot[bot]'}}]

        test_hook.return_value = {}
        self.get_file_contents.return_value = (CONFIG_TEMPLATE.format(post_pr_comment='true',
                                                                      all_passed_message='All checks passed',
                                                                      fail_prologue='',
                                                                      fail_epilogue='') +
                                               'pull_request_substring = "apples"\n')

        self.send_event(client)

        assert self.requests_post.call_count == 2

        args, kwargs = self.requests_post.call_args_list[0]
        assert args[0] == 'https://api.github.com/repos/test-repo/issues/comments/14431'
        assert kwargs['json'] == {'body': 'All checks passed'}

        args, kwargs = self.requests_post.call_args_list[1]
        assert args[0] == 'https://api.github.com/repos/test-repo/statuses/abc464aa'
        assert kwargs['json'] == {'state': 'success',
                                  'description': 'Passed all checks',
                                  'context': 'testbot'}

    def test_check_returns_none(self, app, client):
        """
        Test that a check can return None to skip itself.
        """

        test_hook.return_value = None
        self.send_event(client)
        assert self.requests_post.call_count == 0
