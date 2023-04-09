import argparse
import json
import yaml
import logging
from subprocess import check_output, CalledProcessError


def is_git_repo(directory):
    try:
        check_output(
            ['git', 'rev-parse', '--is-inside-work-tree'], cwd=directory)
        print()
        return True
    except CalledProcessError:
        return False


def get_changed_files(directory, commit):
    if not is_git_repo(directory):
        print(f"{directory} is not a git repository")
        return []

    try:
        # Get the SHA of the latest commit
        sha = check_output(['git', 'rev-parse', commit], cwd=directory).decode().strip()

        # Get a list of changed files since the last commit
        changed_files = check_output(['git', 'diff-tree', '--no-commit-id',
                                     '--name-only', sha, '-r'], cwd=directory).decode().strip().split('\n')

        return changed_files
    except CalledProcessError as e:
        print(f"Error getting changed files: {e}")
        return []


def output_files(files, output_format, output_file, logger):
    if output_format == 'text':
        output = '\n'.join(files)
    elif output_format == 'json':
        output = json.dumps(files)
    elif output_format == 'yaml':
        output = yaml.dump(files, default_flow_style=False)
    elif output_format == 'csv':
        output = ','.join(files)
    else:
        error_msg = f"Invalid output format: {output_format}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(output)
            logger.info(f"Wrote output to file {output_file}")
            logger.info(f"Output:\n{output}")
            return output
    else:
        logger.info(f"Output: {output}")
        return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get a list of files changed in the latest commit of a git repository')
    parser.add_argument('directory', type=str,
                        help='the directory of the git repository')
    parser.add_argument('-o', '--output-format', type=str, default='text',
                        choices=['text', 'csv', 'json', 'yaml'],
                        help='the format to output the list of files (default: text)')
    parser.add_argument('-f', '--output-file', type=str,
                        help='the file to write the output to')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='print verbose output to stdout'),
    parser.add_argument('-c', '--commit', type=str, default='HEAD',
                        help='commit sha (default: HEAD)')
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('output.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if args.verbose:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    changed_files = get_changed_files(args.directory, args.commit)
    output_files(changed_files, args.output_format, args.output_file, logger)
