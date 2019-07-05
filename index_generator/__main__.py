#!/usr/bin/env python3
# *-- coding: utf-8 --*
import sys
import time
import os
import jinja2
import argparse

from jinja2.exceptions import TemplateNotFound
from index_generator.models.entries import Entry
from index_generator.models.exceptions import IndexGeneratorTemplateNotFound, IndexGeneratorPathNotExists
from . import APP_NAME, APP_URL, APP_VERSION

indexIgnore = ('index.html', 'images', 'favicon.ico')


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--version', '-V', action='store_true', default=False,
                            help='Print version infomation and quit.')
        parser.add_argument('--theme', '-t', type=str, default='default', choices=['default', 'default-dark'],
                            help='Select builtin theme to generate html.')
        parser.add_argument('--template', '-T', type=str, default='', help='Custom template to generate html.')
        parser.add_argument('--no-recursive', action='store_true', default=False, help='Do not generate recursively.')
        parser.add_argument('--name', '-n', type=str, default='index.html',
                            help='Default output filename.')
        parser.add_argument('--print', '-P', action='store_true', default=False, help='Whether to print to stdout.')
        parser.add_argument('--depth', '-d', type=int, default=0, help='Set cutoff depth.')
        parser.add_argument('--root', '-r', type=str, default=os.path.sep, help='Set base root dir.')
        parser.add_argument('--human', action='store_true', default=False, help='Make size human readable.')
        parser.add_argument('path', type=str, default='', help='Path', nargs='?')
        arguments = parser.parse_args()
        app(arguments)
    except BaseException as e:
        if e.__class__.__name__ != 'SystemExit':
            print('[Exception] ' + e.__class__.__name__ + ': ' + str(e))
            if hasattr(e, 'hint'):
                print(e.hint)


def app(args):
    if args.version:
        print(APP_NAME + ' ' + APP_VERSION + ' ' + APP_URL)
        sys.exit(0)
    if not args.path:
        print(APP_NAME + ' ' + APP_VERSION + ' ' + APP_URL)
        print('Usage: index-generator [OPTIONS] PATH.')
        print('See: index-generator --help')
        sys.exit(0)
    if not os.path.exists(args.path):
        raise IndexGeneratorPathNotExists('Path does not exists')
    try:
        if args.no_recursive:
            os.chdir(args.path)
            generate_once(args.theme, '.', os.listdir('.'), args.name, args.print, base=args.root, human=args.human,
                          template=os.path.abspath(args.template) if args.template else '')
        else:
            generate_recursively(args.theme, args.path, args.name, args.print, args.depth, base=args.root, human=args.human,
                                 template=os.path.abspath(args.template) if args.template else '')
    except TemplateNotFound as e:
        raise IndexGeneratorTemplateNotFound(str(e))


def generate_once(theme, root, files, name, if_print, base=os.path.sep, human=False, template='', iconset='material'):
    if not template:
        environment = jinja2.Environment(
            loader=jinja2.PackageLoader('index_generator', 'templates/' + theme),
            autoescape=jinja2.select_autoescape(['html', 'htm'])
        )
    else:
        environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template),
            autoescape=jinja2.select_autoescape(['html', 'htm'])
        )
    template = environment.get_template(name)

    entries = list(map(lambda f1: Entry(f1, root, base=base, human=human), files))
    # entries.sort(key=lambda x: x.isDir, reverse=True)

    filelist = []
    for entry in entries:
        if entry.name in indexIgnore:
            continue
        filelist.append({
            'path': entry.path,
            'name': entry.name,
            'size': entry.size,
            'modified': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry.modified)),
            'mime': entry.mime,
            'isDir': entry.isDir,
            'icon': entry.icon
        })
    html = template.render(ig={
        'root': base + root.lstrip('.*' + os.path.sep),
        'files': filelist,
        'generator': {
            'name': APP_NAME,
            'version': APP_VERSION,
            'url': APP_URL
        }
    })

    if if_print:
        print(html)
    else:
        with open(root + os.path.sep + name, 'w') as f:
            print(html, file=f)


def generate_recursively(theme, path, name, if_print, max_depth=0, base=os.path.sep, human=False, template='', iconset='material'):
    os.chdir(path)
    for root, dirs, files in os.walk('.'):
        if max_depth != 0 and root.count(os.sep) >= max_depth:
            dirs.clear()
            continue

        dirs.sort()
        files.sort()

        if if_print:
            print('-----------------------------------------')
            print('Path: ' + root)
            print('dirs: {}'.format(dirs))
            print('files: {}'.format(files))
            print('-----------------------------------------')

        generate_once(theme, root, dirs + files, name, if_print, base=base, human=human, template=template, iconset=iconset)


if __name__ == '__main__':
    main()
