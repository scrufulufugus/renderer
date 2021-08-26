#!/usr/bin/env python3

import os.path as path
import re
import sys
import argparse
import csv

def main(t_file, m_file, i_files, o_path):
    with open(t_file, 'r') as f:
        template = f.read()

    content = {}

    for item in i_files:
        prog = re.compile(r'(?<=<!--#\+BEGIN:\sitems-->).+(?=<!--#\+END:\sitems-->)', flags=re.I|re.M|re.S)
        match = prog.search(template)
        if match:
            template = prog.sub(' ', template)
        else:
            break
        sub_template = match.group(0)
        with open(item, 'r') as f:
            reader = csv.DictReader(f, delimiter=',', quotechar='"')
            for row in reader:
                if row["id"] not in content:
                    content[row["id"]] = []
                content[row["id"]].append(replaceKeys(sub_template, row))

    #template = prog.sub('', template)
    outfiles = {}

    with open(m_file, 'r') as f:
        reader = csv.DictReader(f, delimiter=',', quotechar='"')
        #main_data_vars = reader.fieldnames
        for row in reader:
            outfiles[row['id']] = [row['title'], replaceKeys(template, row)]
            if row["id"] in content:
                outfiles[row['id']][1] = outfiles[row['id']][1].replace('<!--#+BEGIN: items-->',
                                                              ''.join(content[row['id']]))

        for file_id, file_array in outfiles.items():
            with open(o_path + '/' + file_array[0].replace('/', '_') + '.html', 'w') as f:
                f.write(file_array[1])

    #print(main_data_vars)

def replaceKeys(template, data_dict):
    for key, value in data_dict.items():
        template = template.replace('{' + key + '}', value)
    return template

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
