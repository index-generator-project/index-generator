#!/usr/bin/env python3
# *-- coding: utf-8 --*
import sys
import time

import jinja2
import argparse
import os

from index_generator.models.entries import Entry
from index_generator.models.exceptions import IndexGeneratorException
from . import *


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
    parser.add_argument('path', type=str, default='.', help='Path')
    arguments = parser.parse_args(sys.argv[1:])
    app(arguments)


def app(args):
    if args.version:
        print(APP_NAME + ' ' + APP_VERSION + ' ' + APP_URL)
        sys.exit(0)
    if args.no_recursive:
        generate_once(args.template, args.path, args.name, args.print)
    else:
        raise IndexGeneratorException(IndexGeneratorException.NOT_IMPLEMENTED)


def generate_once(template_dir, path='.', name='index.html', if_print=False):
    environment = jinja2.Environment(
        loader=jinja2.PackageLoader('index_generator', template_dir),
        autoescape=jinja2.select_autoescape(['html', 'htm'])
    )
    template = environment.get_template(name)
    entries = list(map(lambda f: Entry(f), os.listdir(path)))
    files = []
    for entry in entries:
        files.append({
            'path':     entry.path,
            'name':     entry.name,
            'size':     entry.size,
            'modified': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry.modified)),
            'mime':     entry.mime
        })
    html = template.render(ig={
        'currentPath': '/',
        'files': files
    })
    if if_print:
        print(html)
    else:
        raise IndexGeneratorException(IndexGeneratorException.NOT_IMPLEMENTED)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
