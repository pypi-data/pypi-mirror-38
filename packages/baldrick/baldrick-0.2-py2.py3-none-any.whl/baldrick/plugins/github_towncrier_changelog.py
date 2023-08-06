import os
import re
from collections import OrderedDict

from toml import loads

from .github_pull_requests import pull_request_handler

try:
    from towncrier._settings import parse_toml
except ImportError:  # pragma: nocover
    from towncrier._settings import _template_fname, _start_string, _title_format, _underlines, _default_types

    def parse_toml(config):  # pragma: nocover
        if 'tool' not in config:
            raise ValueError("No [tool.towncrier] section.")

        config = config['tool']['towncrier']

        sections = OrderedDict()
        types = OrderedDict()

        if "section" in config:
            for x in config["section"]:
                sections[x.get('name', '')] = x['path']
        else:
            sections[''] = ''

        if "type" in config:
            for x in config["type"]:
                types[x["directory"]] = {"name": x["name"],
                                         "showcontent": x["showcontent"]}
        else:
            types = _default_types

        return {
            'package': config.get('package', ''),
            'package_dir': config.get('package_dir', '.'),
            'filename': config.get('filename', 'NEWS.rst'),
            'directory': config.get('directory'),
            'sections': sections,
            'types': types,
            'template': config.get('template', _template_fname),
            'start_line': config.get('start_string', _start_string),
            'title_format': config.get('title_format', _title_format),
            'issue_format': config.get('issue_format'),
            'underlines': config.get('underlines', _underlines)
        }


def calculate_fragment_paths(config):

    if config.get("directory"):
        base_directory = config["directory"]
        fragment_directory = None
    else:
        base_directory = os.path.join(config['package_dir'], config['package'])
        fragment_directory = "newsfragments"

    section_dirs = []
    for key, val in config['sections'].items():
        if fragment_directory is not None:
            section_dirs.append(os.path.join(base_directory, val, fragment_directory))
        else:
            section_dirs.append(os.path.join(base_directory, val))

    return section_dirs


def check_sections(filenames, sections):
    """
    Check that a file matches ``<section><issue number>``. Otherwise the root
    dir matches when it shouldn't.
    """
    for section in sections:
        # Make sure the path ends with a /
        if not section.endswith("/"):
            section += "/"
        pattern = section.replace("/", r"\/") + r"\d+.*"
        for fname in filenames:
            match = re.match(pattern, fname)
            if match is not None:
                return fname
    return False


def check_changelog_type(types, matching_file):
    for ty in types:
        if ty in matching_file:
            return True
    return False


def verify_pr_number(pr_number, matching_file):
    # TODO: Make this a regex to check that the number is in the right place etc.
    return pr_number in matching_file


def load_towncrier_config(pr_handler):
    file_content = pr_handler.get_file_contents("pyproject.toml", branch=pr_handler.base_branch)
    config = loads(file_content)
    if "towncrier" in config.get("tool", {}):
        return parse_toml(config)


CHANGELOG_EXISTS = "Changelog file was added in the correct directories."
CHANGELOG_MISSING = "No changelog file was added in the correct directories."

TYPE_CORRECT = "The changelog file that was added is one of the configured types."
TYPE_INCORRECT = "The changelog file that was added is not one of the configured types."

NUMBER_CORRECT = "The number in the changelog file matches this pull request number."
NUMBER_INCORRECT = "The number in the changelog file does not match this pull request number."


@pull_request_handler
def process_towncrier_changelog(pr_handler, repo_handler):

    cl_config = pr_handler.get_config_value('towncrier_changelog', {})

    if not cl_config.get('enabled', False):
        return None

    skip_label = cl_config.get('changelog_skip_label', None)

    config = load_towncrier_config(pr_handler)
    if not config:
        return

    section_dirs = calculate_fragment_paths(config)
    types = config['types'].keys()

    modified_files = pr_handler.get_modified_files()

    matching_file = check_sections(modified_files, section_dirs)

    messages = {}

    if skip_label and skip_label in pr_handler.labels:
        return

    elif not matching_file:

        messages['missing_file'] = {'description': cl_config.get('changelog_missing', CHANGELOG_MISSING),
                                    'state': 'failure'}

    else:

        messages['missing_file'] = {'description': cl_config.get('changelog_exists', CHANGELOG_EXISTS),
                                    'state': 'success'}

        if check_changelog_type(types, matching_file):
            messages['wrong_type'] = {'description': cl_config.get('type_correct', TYPE_CORRECT),
                                      'state': 'success'}
        else:
            messages['wrong_type'] = {'description': cl_config.get('type_incorrect', TYPE_INCORRECT),
                                      'state': 'failure'}

        if cl_config.get('verify_pr_number', False) and not verify_pr_number(pr_handler.number, matching_file):
            messages['wrong_number'] = {'description': cl_config.get('number_incorrect', NUMBER_INCORRECT),
                                        'state': 'failure'}
        else:
            messages['wrong_number'] = {'description': cl_config.get('number_correc', NUMBER_CORRECT),
                                        'state': 'success'}

    # Add help URL
    for message in messages.values():
        message['target_url'] = cl_config.get('help_url', None)

    return messages
