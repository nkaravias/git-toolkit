import unittest
import git_utils
import logging
import json
import yaml

CHANGED_FILES_PASS = ['resource_config/projects/001/nonp/iam/roles.yaml',
                      'resource_config/projects/001/nonp/policies.yaml']
CHANGED_FILES_FAIL = ['i_dont_exist_in_the_commit.yaml']
COMMIT_PASS = '33e9807e'
REPO_PATH = './data/repo'
NOT_GIT_REPO_PATH = '../..'
INVALID_REPO_PATH = './does_not_exist'
LOGGER = logging.getLogger(__name__)


class TestGitUtils(unittest.TestCase):
    def test_is_git_repo(self):
        self.assertFalse(git_utils.is_git_repo(NOT_GIT_REPO_PATH))
        self.assertTrue(git_utils.is_git_repo(REPO_PATH))

    def test_get_changed_files(self):
        self.assertEqual(git_utils.get_changed_files(REPO_PATH, COMMIT_PASS), CHANGED_FILES_PASS)
        self.assertNotEqual(git_utils.get_changed_files(
            REPO_PATH, COMMIT_PASS), CHANGED_FILES_FAIL)

    def test_get_changed_files_invalid_path(self):
        with self.assertRaises(FileNotFoundError):
            git_utils.get_changed_files(INVALID_REPO_PATH, COMMIT_PASS)

    def test_get_changed_files_not_git_repo(self):
        result = git_utils.is_git_repo(NOT_GIT_REPO_PATH)
        result = git_utils.get_changed_files(NOT_GIT_REPO_PATH, COMMIT_PASS)
        self.assertEqual(result, [])

    def test_output_files_csv(self):
        output_format = 'csv'
        output_file = 'foo'
        files = git_utils.get_changed_files(REPO_PATH, COMMIT_PASS)
        output_files = git_utils.output_files(
            files, output_format, output_file, LOGGER)
        expected_output_files = ','.join(CHANGED_FILES_PASS)
        self.assertEqual(output_files, expected_output_files)

    def test_output_files_yaml(self):
        output_format = 'yaml'
        output_file = 'foo'
        files = git_utils.get_changed_files(REPO_PATH, COMMIT_PASS)
        output_files = git_utils.output_files(files, output_format, output_file, LOGGER)
        expected_output_files = yaml.dump(CHANGED_FILES_PASS)
        self.assertEqual(output_files, expected_output_files)

    def test_output_files_json(self):
        output_format = 'json'
        output_file = 'foo'
        files = git_utils.get_changed_files(REPO_PATH, COMMIT_PASS)
        output_files = git_utils.output_files(files, output_format, output_file, LOGGER)
        expected_output_files = json.dumps(CHANGED_FILES_PASS)
        self.assertEqual(output_files, expected_output_files)

    def test_output_files_text(self):
        output_format = 'text'
        output_file = 'foo'
        files = git_utils.get_changed_files(REPO_PATH, COMMIT_PASS)
        output_files = git_utils.output_files(files, output_format, output_file, LOGGER)
        expected_output_files = '\n'.join(CHANGED_FILES_PASS)
        self.assertEqual(output_files, expected_output_files)

    def test_invalid_output_format(self):
        with self.assertRaises(ValueError):
            git_utils.output_files([], 'invalid_format', None, LOGGER)
