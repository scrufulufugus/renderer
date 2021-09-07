#!/usr/bin/env python3
"""
Copyright (C) 2021 Samuel Monson <smonson at irbash dot net>

This file is part of renderer.

    renderer is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    renderer is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with renderer.  If not, see <https://www.gnu.org/licenses/>.
"""

import os.path as path
from io import IOBase
import sys
import argparse
import csv
from mako.template import Template

class TemplateRenderer(object):
    def __init__(self, template: str, main_data: IOBase, items: dict):
        self.template = Template(template, format_exceptions=True)

        self.main_data = csv.DictReader(main_data, dialect=self.checkCSV(main_data))
        self.items_data = {}
        for key, item in items.items():
            self.items_data[key] = csv.DictReader(item, dialect=self.checkCSV(item))

    def checkCSV(self, csv_io: IOBase) -> csv.Dialect:
        dialect = csv.Sniffer().sniff(csv_io.read(1024))
        csv_io.seek(0)
        return dialect

    def render(self, **kwargs) -> dict:
        self.id_col = kwargs.get("id", "id")
        self.title_col = kwargs.get("title", "title")

        context_tree = {}

        for row in self.main_data:
            context_tree[row[self.id_col]] = row
            for item in self.items_data.keys():
                context_tree[row[self.id_col]][item] = []

        for item, reader in self.items_data.items():
            for row in reader:
                if row[self.id_col] in context_tree.keys():
                    context_tree[row[self.id_col]][item].append(DictMap(row))

        out_files = {}
        for row in context_tree.values():
            out_files[row[self.title_col]] = self.template.render_unicode(**row)

        return out_files

class DictMap(dict):
    __getattr__ = dict.get

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fill template based off spreadsheets.')
    parser.add_argument('-t', '--template', dest='template', required=True)
    parser.add_argument('-m', '--main-data', dest='main', required=True)
    parser.add_argument('-o', '--out-path', dest='out', required=True)
    parser.add_argument('-i', '--item-data', dest='items', nargs=2, action='append', default=[])
    args = parser.parse_args()

    if path.isfile(args.template):
        f = open(args.template, 'r')
        template = f.read()
        f.close()
    else:
        print("Invalid template: {}".format(args.template))
        sys.exit(2)
    if path.isfile(args.main):
        main_file = open(args.main, 'r', errors='replace', encoding='utf-8')
    else:
        print("Invalid main: {}".format(args.main))
        sys.exit(2)
    if not path.isdir(args.out):
        print("Invalid out path: {}".format(args.out))
        sys.exit(2)
    items = {}
    for item in args.items:
        if not path.isfile(item[1]):
            print("Invalid item path: {}".format(item[1]))
            sys.exit(2)
        if item[0] in items.keys():
            print("Duplicate item: {}".format(item[0]))
            sys.exit(2)
        items[item[0]] = open(item[1], 'r', errors='replace', encoding='utf-8')

    renderer = TemplateRenderer(template, main_file, items)
    out_files = renderer.render()
    main_file.close()
    for item in items.values():
        item.close()
    for filename, contents in out_files.items():
        with open(args.out + '/' + filename.replace('/', '_') + '.html', 'w', encoding='utf-8') as f:
            f.write(contents)
