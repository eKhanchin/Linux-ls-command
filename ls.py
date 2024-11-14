"""
This module implements the functionality of Linux's "ls" command.
"""


import re
import os
from argparse import Namespace
from cli_parser import parse_arguments


WHITESPACE_CHARACTER = re.compile(r'\s+')


def main():
    arguments = parse_arguments()
    list_directory_contents(arguments)


class DirColoring:
    """
    Defines color codes for printing directories.
    """

    start = '\033[94m\033[1m'
    end = '\033[0m'


def list_directory_contents(arguments: Namespace):
    """ Lists information about the FILEs.

    Params
        arguments - Namespace that includes all provided options
    """

    regexes = []
    target_path = arguments.target_path
    items = sorted(os.listdir(target_path), key=sort_item)

    if not arguments.almost_all:
        items = add_special_directories(items)

    if not (arguments.all or arguments.almost_all):
        regexes.append(r'^\.')  # Starts with .

    if arguments.ignore_backups:
        regexes.append('~$')  # Ends with ~

    items = filter_items(items, regexes)

    if arguments.escape:
        items = [escape_whitespace_characters(item) for item in items]

    for item in items:
        if os.path.isdir(f'{target_path}/{item}'):
            item = add_directory_color(item)
        print(item)


def sort_item(item: str) -> tuple:
    """ Sort files and directories in alphabetical order, where
    priorities are next:
    1 - Files and directories that start with ".".
    2 - Directories.
    3 - Files.

    Params
        item - File or directory name

    Returns
        A tuple of priority code and the item for the alphabetical sort.

    """

    if item.startswith('.'):
        return 0, item
    elif os.path.isdir(item):
        return 1, item

    return 2, item


def add_special_directories(items: list) -> list:
    """ Adds current '.' and parent '..' directories. """

    return ['.', '..'] + items


def filter_items(items: list, regexes: list) -> list:
    """ Filters files and directories names by given regular expressions.

    Params
        items - List of functions and directories names.
        regexes - List of regular expressions.

    Returns
        Filtered list of items.
    """

    if regexes:
        pattern = re.compile(r'|'.join(regexes))
        items = [item for item in items if not re.search(pattern, item)]

    return items


def escape_whitespace_characters(item: str) -> str:
    """ Escapes whitespaces in the names of files and directories. """

    matches = re.finditer(WHITESPACE_CHARACTER, item)
    offset = 0
    for match in matches:
        i = match.start()
        item = item[:i+offset] + '\\' + item[i+offset:]
        offset += 1

    return item


def add_directory_color(directory: str) -> str:
    """ Adds color code for printing. """

    return f'{DirColoring.start}{directory}{DirColoring.end}'


if __name__ == '__main__':
    main()
