#!/usr/bin/env python3

import os.path as path
import re
import sys
import argparse
import csv
from mako.template import Template
from mako.runtime import Context

def main(t_file, m_file, i_files, o_path):
    template = Template(filename=t_file, format_exceptions=True)

    content = {}

    #template = prog.sub('', template)
    outfiles = {}

    with open(m_file, 'r') as f:
        reader = csv.DictReader(f, delimiter=',', quotechar='"')
        #main_data_vars = reader.fieldnames
        for row in reader:
            outfiles[row['id']] = [row['title'], template.render_unicode(**row)]

        for file_id, file_array in outfiles.items():
            with open(o_path + '/' + file_array[0].replace('/', '_') + '.html', 'w') as f:
                f.write(file_array[1])

if __name__ == __name__:
    parser = argparse.ArgumentParser(description='Fill templated based off spreadsheets.')
    parser.add_argument('-t', '--template', dest='template', required=True)
    parser.add_argument('-m', '--main-data', dest='main', required=True)
    parser.add_argument('-o', '--out-path', dest='out', required=True)
    parser.add_argument('-i', '--item-data', dest='items', nargs='*', default=[])
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
    for i, item in enumerate(args.items):
        if not path.isfile(item):
            print("Invalid item: {}".format(item))
            sys.exit(2)
        args.items[i] = path.abspath(item)

    main(path.abspath(args.template), path.abspath(args.main),
         args.items, path.abspath(args.out))
