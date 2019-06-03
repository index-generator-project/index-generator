#!/usr/bin/env python3
# *-- coding: utf-8 --*
import sys

import os
import os.path as path
from datetime import datetime

import jinja2
import argparse

indexIgnore=['index.html', 'templates']

def main():
    global template
    global arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-V', action='store_true', default=False,
                        help='Print version infomation and quit.')
    parser.add_argument('--template', '-t', type=str, default='templates/default',
                        help='Select template to generate html.')
    parser.add_argument('--no-recursive', action='store_true', default=False, help='Do not generate recursively.')
    parser.add_argument('--name', '-n', type=str, default='index.html',
                        help='Default output filename.')
    parser.add_argument('--print', '-p', action='store_true', default=False, help='Whether to print to stdout.')
    arguments = parser.parse_args(sys.argv[1:])
    environment = jinja2.Environment(
        loader=jinja2.PackageLoader('index_generator', arguments.template),
        autoescape=jinja2.select_autoescape(['html', 'htm'])
    )
    template = environment.get_template('index.html')
    
    generate()


def generate(currentDir=''):
    filelist=[]
    dirlist=[]
    for file in os.listdir():
        if file in indexIgnore:
            continue
        if path.isdir(file):
            dirlist.append({
                'name': file,
                'modified': datetime.fromtimestamp(path.getmtime(file)).strftime('%Y-%m-%d %H:%M')
                })
        else:
            filelist.append({
                'name': file,
                'modified': datetime.fromtimestamp(path.getmtime(file)).strftime('%Y-%m-%d %H:%M'),
                'size': path.getsize(file)
                })
    
    index = template.render(ig={
            'currentPath': currentDir,
            'dirs': dirlist,
            'files': filelist
            })
    if arguments.print:
        print(index)

    with open('index.html','w') as f:
        print(index, file=f)

    if not arguments.no_recursive and dirlist:
        for file in dirlist:
            if arguments.print:
                print('------------------------------------------------')
            os.chdir(file['name'])
            generate(currentDir+'/'+file['name'])
    
    os.chdir('..')

if __name__ == '__main__':
    main()