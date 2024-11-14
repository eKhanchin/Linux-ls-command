import argparse
import os


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=('List information about the FILEs (the current directory'
                     ' by default).'),
        usage='ls [OPTION]... [FILE]...'
    )

    parser.add_argument(
        'target_path',
        metavar='PATH',
        default=os.getcwd(),
        type=str,
        nargs='?',
        help=argparse.SUPPRESS
    )

    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='Do not ignore entries starting with .'
    )

    parser.add_argument(
        '-A', '--almost-all',
        action='store_true',
        help='Do not list implied . and ..'
    )

    parser.add_argument(
        '-b', '--escape',
        action='store_true',
        help='Print C-style escapes for non-graphic characters'
    )

    parser.add_argument(
        '-B', '--ignore-backups',
        action='store_true',
        help='Do not list implied entries ending with ~'
    )

    arguments = parser.parse_args()

    return arguments
