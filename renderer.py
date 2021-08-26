#!/usr/bin/env python3

import os.path as path
import re
import sys
import argparse
import csv
from mako.template import Template

def main(t_file, m_file, i_files, o_path, id_col="id", title_col="title"):
    template = Template(filename=t_file, format_exceptions=True)

    context_tree = {}

    with open(m_file, 'r') as f:
        reader = csv.DictReader(f, delimiter=',', quotechar='"')
        for row in reader:
            context_tree[row[id_col]] = row

    for item, filename in i_files.items():
        with open(filename) as f:
            reader = csv.DictReader(f, delimiter=',', quotechar='"')
            for row in reader:
                if row[id_col] in context_tree.keys():
                    if item in context_tree[row[id_col]].keys():
                        context_tree[row[id_col]][item].append(row)
                    else:
                        context_tree[row[id_col]][item] = [row]

    out_files = {}
    for row in context_tree.values():
        out_files[row[title_col]] = template.render_unicode(**row)

    for filename, contents in out_files.items():
        with open(o_path + '/' + filename.replace('/', '_') + '.html', 'w') as f:
            f.write(contents)

def parse_items(i_files, context):
    pass

if __name__ == __name__:
    parser = argparse.ArgumentParser(description='Fill template based off spreadsheets.')
    parser.add_argument('-t', '--template', dest='template', required=True)
    parser.add_argument('-m', '--main-data', dest='main', required=True)
    parser.add_argument('-o', '--out-path', dest='out', required=True)
    parser.add_argument('-i', '--item-data', dest='items', nargs=2, action='append', default=[])
    args = parser.parse_args()

    if not path.isfile(args.template):
        print("Invalid template: {}".format(args.template))
        sys.exit(2)
    if not path.isfile(args.main):
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
        items[item[0]] = path.abspath(item[1])

    main(path.abspath(args.template), path.abspath(args.main),
         items, path.abspath(args.out))
