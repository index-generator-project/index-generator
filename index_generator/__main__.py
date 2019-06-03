#!/usr/bin/env python3
# *-- coding: utf-8 --*
import sys

import jinja2
import argparse


def main():
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


def generate(templateDir):
    environment = jinja2.Environment(
        loader=jinja2.PackageLoader('index_generator', templateDir),
        autoescape=jinja2.select_autoescape(['html', 'htm'])
    )
    template = environment.get_template('index.html')
    print(template.render(ig={
        'currentPath': '/example',
        'files': [
            {
                'name': 'test.txt',
                'modified': '-',
                'size': '12'
            }
        ]
    }))


if __name__ == '__main__':
    main()
