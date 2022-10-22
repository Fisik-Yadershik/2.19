#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import json
import pathlib


def selecting(line, flights, nom):
    """Выбор рейсов по типу самолёта"""
    count = 0
    print(line)
    print(
        '| {:^4} | {:^20} | {:^15} | {:^16} |'.format(
            "№",
            "Место прибытия",
            "Номер самолёта",
            "Тип"))
    print(line)
    for i, num in enumerate(flights, 1):
        if nom == num.get('value', ''):
            count += 1
            print(
                '| {:<4} | {:<20} | {:<15} | {:<16} |'.format(
                    count,
                    num.get('stay', ''),
                    num.get('number', ''),
                    num.get('value', 0)))
    print(line)


def table(line, flights):
    """Вывод скиска рейсов"""
    print(line)
    print(
        '| {:^4} | {:^20} | {:^15} | {:^16} |'.format(
            "№",
            "Место прибытия",
            "Номер самолёта",
            "Тип"))
    print(line)
    for i, num in enumerate(flights, 1):
        print(
            '| {:<4} | {:<20} | {:<15} | {:<16} |'.format(
                i,
                num.get('stay', ''),
                num.get('number', ''),
                num.get('value', 0)
            )
        )
    print(line)


def adding(flights, stay, number, value):
    flights.append(
        {
            'stay': stay,
            'number': number,
            'value': value
        }
    )
    return flights


def saving(file_name, flights):
    with open(file_name, "w", encoding="utf-8") as file_out:
        json.dump(flights, file_out, ensure_ascii=False, indent=4)
    work_dir = pathlib.Path.cwd()/file_name
    work_dir.replace(pathlib.Path.home()/file_name)


def opening(file_name):
    with open(file_name, "r", encoding="utf-8") as f_in:
        return json.load(f_in)


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",)
    parser = argparse.ArgumentParser("flights")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0")
    subparsers = parser.add_subparsers(dest="command")
    add = subparsers.add_parser(
        "add",
        parents=[file_parser])
    add.add_argument(
        "-s",
        "--stay",
        action="store",
        required=True,)
    add.add_argument(
        "-v",
        "--value",
        action="store",
        required=True,)
    add.add_argument(
        "-n",
        "--number",
        action="store",
        required=True,)
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],)
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],)
    select.add_argument(
        "-t",
        "--type",
        action="store",
        required=True,)
    args = parser.parse_args(command_line)
    is_dirty = False
    name = args.filename
    home = pathlib.Path.home()/name

    if home.exists():
        flights = opening(home)
    else:
        flights = []

    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 20,
        '-' * 15,
        '-' * 16)

    if args.command == "add":
        flights = adding(flights, args.stay, args.number, args.value)
        is_dirty = True
    elif args.command == 'display':
        table(line, flights)
    elif args.command == "select":
        selecting(line, flights, args.type)
    if is_dirty:
        saving(args.filename, flights)


if __name__ == '__main__':
    main()
