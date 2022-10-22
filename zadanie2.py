#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import pathlib
import colorama
from colorama import Fore, Back, Style


def tree(directory):
    print(Fore.RED + f'|-- {directory}')
    for path in sorted(directory.glob('*')):
        depth = len(path.relative_to(directory).parts)
        spacer = '\t' * depth
        print(Fore.YELLOW + f'{spacer}|-- \033 {path.name}')
        for new_path in sorted(directory.joinpath(path).glob('*')):
            depth = len(new_path.relative_to(directory.joinpath(path)).parts)
            spacer = '\t\t' * depth
            print(Fore.BLUE + f'{spacer}|-- \033 {new_path.name}')



def main(command_line=None):
    colorama.init()
    way = pathlib.Path.cwd()
    file_parser = argparse.ArgumentParser(add_help=False)
    parser = argparse.ArgumentParser("flights")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0")
    subparsers = parser.add_subparsers(dest="command")
    mv = subparsers.add_parser(
        "cd",
        parents=[file_parser])
    mv.add_argument(
        'filename',
        action="store")
    mv = subparsers.add_parser(
        "back",
        parents=[file_parser])
    mv.add_argument(
        'filename',
        action="store")
    args = parser.parse_args(command_line)
    if args.command == 'cd':
        way = way/args.filename
        tree(way)
    elif args.command == 'back':
        if '\\' in args.filename:
            lst = args.filename.split('\\')
            for i in lst:
               way = way.parent
        else:
            way = way.parent
        tree(way)
    elif args.command == None:
        tree(way)


if __name__ == "__main__":
    main()