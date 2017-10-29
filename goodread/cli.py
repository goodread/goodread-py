# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import sys
import click
import traceback
from emoji import emojize


# Helpers

def parse_document(path):
    elements = []
    codeblock = ''
    capture = False

    # Parse file lines
    with io.open(path, encoding='utf-8') as file:
        for line in file:

            # Heading
            if line.startswith('#'):
                heading = line.strip(' #\n')
                level = len(line) - len(line.lstrip('#'))
                if (elements and
                    elements[-1]['type'] == 'heading' and
                    elements[-1]['level'] == level):
                    continue
                elements.append({
                    'type': 'heading',
                    'value': heading,
                    'level': level,
                })

            # Codeblock
            if line.startswith('```python'):
                if 'goodread' in line:
                    capture = True
                codeblock = ''
                continue
            if line.startswith('```'):
                if capture:
                    elements.append({
                        'type': 'codeblock',
                        'value': codeblock,
                    })
                capture = False
            if capture:
                codeblock += line
                continue

    return elements


def test_document(elements):
    scope = {}
    passed = 0
    failed = 0
    skipped = 0
    title = None
    exception = None

    # Test elements
    for element in elements:

        # Heading
        if element['type'] == 'heading':
            report(element['value'], type='heading', level=element['level'])
            if title is None:
                title = element['value']
                report(None, type='separator')

        # Codeblock
        elif element['type'] == 'codeblock':
            exception_line = 1000  # infinity
            try:
                exec(instrument(element['value']), scope)
            except Exception:
                _, exception, tb = sys.exc_info()
                exception_line = traceback.extract_tb(tb)[-1][1]
            for line_number, line in enumerate(element['value'].strip().split('\n'), start=1):
                if line_number < exception_line:
                    report(line, type='success')
                    passed += 1
                elif line_number == exception_line:
                    report(line, type='failure', exception=exception)
                    failed += 1
                elif line_number > exception_line:
                    report(line, type='skipped')
                    skipped += 1

    # Report summary
    if title is not None:
        report(title, type='summary', passed=passed, failed=failed, skipped=skipped)

    return exception is None


def instrument(codeblock):
    lines = []
    for line in codeblock.strip().split('\n'):
        if ' # ' in line:
            left, right = line.split(' # ')
            left = left.strip()
            right = right.strip()
            if left and right:
                message = '%s != %s' % (left, right)
                line = 'assert %s == %s, "%s"' % (left, right, message)
        lines.append(line)
    return '\n'.join(lines)


state = {'prev_type': None}
def report(text, type, level=None, exception=None, passed=None, failed=None, skipped=None):
    message = None
    if type == 'blank':
        return click.echo('')
    elif type == 'separator':
        message = click.style(emojize(':heavy_minus_sign:'*3, use_aliases=True))
    elif type == 'heading':
        message = click.style(emojize(' %s  ' % ('#' * (level or 1)), use_aliases=True))
        message += click.style('%s' % text, bold=True)
    elif type == 'success':
        message = click.style(emojize(' :heavy_check_mark:  ', use_aliases=True), fg='green')
        message += click.style('%s' % text)
    elif type == 'failure':
        message = click.style(emojize(' :x:  ', use_aliases=True), fg='red')
        message += click.style('%s\n' % text)
        message += click.style('Exception: %s\n' % exception, fg='red', bold=True)
    elif type == 'skipped':
        message = click.style(emojize(' :heavy_minus_sign:  ', use_aliases=True), fg='yellow')
        message += click.style('%s' % text)
    elif type == 'summary':
        color = 'green'
        message = click.style(emojize(' :heavy_check_mark:  ', use_aliases=True), fg='green', bold=True)
        if (failed + skipped) > 0:
            color = 'red'
            message = click.style(emojize(' :x:  ', use_aliases=True), fg='red', bold=True)
        message += click.style('%s: %s/%s' % (text, passed, passed + failed + skipped), bold=True, fg=color)
    if message:
        if state['prev_type'] != type:
            message = '\n' + message
        click.echo(message)
    state['prev_type'] = type


# Main program

@click.command()
@click.argument('paths', nargs=-1)
def cli(paths=['README.md']):
    success = True
    for path_number, path in enumerate(paths, start=1):
        elements = parse_document(path)
        success = success and test_document(elements)
        if path_number < len(paths):
            report(None, type='separator')
    report(None, type='blank')
    if not success:
        exit(1)


if __name__ == '__main__':
    cli()
