#!/usr/bin/env python3
# *-- coding: utf-8 --*
import sys
import time
import os
import jinja2
import argparse
from datetime import datetime

from index_generator.models.entries import Entry
from index_generator.models.exceptions import IndexGeneratorException
from . import *

indexIgnore = ('index.html' 'images' 'favicon.ico')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-V', action='store_true', default=False,
                        help='Print version infomation and quit.')
    parser.add_argument('--template', '-t', type=str, default='templates/default',
                        help='Select template to generate html.')
    parser.add_argument('--no-recursive', action='store_true', default=False, help='Do not generate recursively.')
    parser.add_argument('--name', '-n', type=str, default='index.html',
                        help='Default output filename.')
    parser.add_argument('--print', '-P', action='store_true', default=False, help='Whether to print to stdout.')
    parser.add_argument('path', type=str, default='', help='Path')
    parser.add_argument('--depth','-d', type=int, default=0, help='Set cutoff depth.')
    arguments = parser.parse_args(sys.argv[1:])
    app(arguments)


def app(args):
    if args.version:
        print(APP_NAME + ' ' + APP_VERSION + ' ' + APP_URL)
        sys.exit(0)
    if args.no_recursive:
        generate_once(args.template, args.path, os.listdir(args.path), args.name, args.print)
    else:
        generate_recursively(args.template, args.path, args.name, args.print, args.depth)


def generate_once(template_dir, root, files, name, if_print):
    environment = jinja2.Environment(
        loader=jinja2.PackageLoader('index_generator', template_dir),
        autoescape=jinja2.select_autoescape(['html', 'htm'])
    )
    template = environment.get_template(name)

    entries = list(map(lambda f: Entry(f,root), files))
    #entries.sort(key=lambda x: x.isDir, reverse=True)

    filelist=[]
    for entry in entries:
        if entry.name in indexIgnore:
            continue
        filelist.append({
            'path':     entry.path,
            'name':     entry.name,
            'size':     entry.size,
            'modified': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry.modified)),
            'mime':     entry.mime,
            'isDir':    entry.isDir
        })
    html = template.render(ig={
        'root': '/'+root.lstrip('.*/'),
        'files': filelist
        'generator': {
            'name':    APP_NAME,
            'version': APP_VERSION,
            'url':     APP_URL
        }
    })

    if if_print:
        print(html)
    else:
        with open(root+os.path.sep+name, 'w') as f:
            print(html, file=f)

def generate_recursively(template_dir, path, name, if_print, max_depth=0):
    for root, dirs, files in os.walk(path):
        if max_depth != 0 and root.count(os.sep) >= max_depth:
            dirs.clear()
            continue

        dirs.sort()
        files.sort()

        if if_print:
            print('-----------------------------------------')
            print('Path: '+root)
            print('dirs: {}'.format(dirs))
            print('files: {}'.format(files))
            print('-----------------------------------------')

        generate_once(template_dir, root, dirs+files, name, if_print)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
