import unittest
import git_utils
import logging
import yaml
# import subprocess

CHANGED_FILES_PASS = ['resource_config/projects/001/nonp/iam/roles.yaml',
                      'resource_config/projects/001/nonp/policies.yaml']
CHANGED_FILES_FAIL = ['fail.yaml']


class TestGitUtils(unittest.TestCase):
    def test_is_git_repo(self):
        repo_path = './data/repo'
        repo_path_fail = '../..'
        self.assertFalse(git_utils.is_git_repo(repo_path_fail))
        self.assertTrue(git_utils.is_git_repo(repo_path))

    def test_get_changed_files(self):
        repo_path = './data/repo'
        self.assertEqual(git_utils.get_changed_files(repo_path), CHANGED_FILES_PASS)
        self.assertNotEqual(git_utils.get_changed_files(repo_path), CHANGED_FILES_FAIL)

    def test_get_changed_files_invalid_path(self):
        repo_path = './invalid_repository_path'
        with self.assertRaises(FileNotFoundError):
            git_utils.get_changed_files(repo_path)

    def test_get_changed_files_not_git_repo(self):
        repo_path = '../..'
        result = git_utils.is_git_repo(repo_path)
        result = git_utils.get_changed_files(repo_path)
        self.assertEqual(result, [])

    def test_output_files_csv(self):
        repo_path = './data/repo'
        output_format = 'csv'
        output_file = 'foo'
        logger = logging.getLogger(__name__)
        files = git_utils.get_changed_files(repo_path)
        output_files = git_utils.output_files(
            files, output_format, output_file, logger)
        expected_output_files = 'resource_config/projects/001/nonp/iam/roles.yaml,resource_config/projects/001/nonp/policies.yaml'
        print(output_files)
        print(expected_output_files)
        self.assertEqual(output_files, expected_output_files)

    def test_output_files_yaml(self):
        repo_path = './data/repo'
        output_format = 'yaml'
        output_file = 'foo'
        logger = logging.getLogger(__name__)
        files = git_utils.get_changed_files(repo_path)
        output_files = git_utils.output_files(files, output_format, output_file, logger)
        expected_output_files = yaml.dump(CHANGED_FILES_PASS)
        self.assertEqual(output_files, expected_output_files)
