#!/usr/bin/env python3
#
# Usage: ./parse.py
# Converts the 'advent_2020.py' Python script into 'README.md' markdown text file.

from pathlib import Path
import os


def main():
    lines = read_file(Path(__file__).resolve().parent / 'advent_2020.py')
    lines2 = [a for a in lines[lines.index('###\n'):lines.index('# ###\n')] if not a.startswith(('###\n', '#\n', 'IN_'))]
    lines3 = [b.strip() for b in ''.join(f'\r{a}' if a.startswith(('##', "'''", 'def')) else a for a in lines2).split('\r') if b]
    lines4 = [f'## {a.title()[4:]}' if a.startswith('##') else (f'```text\n{a[3:-3]}\n```' if a.startswith("'''") else f'```python\n{a}\n```') for a in lines3]
    text = '\n\n'.join(['# Advent of Code 2020'] + lines4)
    write_to_file('README.md', text)
    os.popen('./parse.js')


###
##  UTIL
#

def read_file(filename):
    with open(filename, encoding='utf-8') as file:
        return file.readlines()


def write_to_file(filename, text):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


if __name__ == '__main__':
    main()
