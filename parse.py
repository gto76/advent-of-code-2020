#!/usr/bin/env python3
#
# Usage: ./parse.py
# Converts the 'advent_2020.py' Python script into 'README.md' markdown text file.
# After that it runs 'parse.js' script that converts 'README.md' into 'index.html'.

import os, pathlib, re


TITLES = ['Entries', 'Passwords', 'Trees', 'Passports', 'Seat IDs', 'Answers', 'Bags', 
          'Program', 'Encryption', 'Adapters', 'Seats', 'Navigation', 'Buses', 'Bitmasks',
          'Numbers Game', 'Tickets']

LINKS = '<p class="banner"><sup><a href="https://adventofcode.com/2020">Go to the site' + \
        '</a>, <a href="https://raw.githubusercontent.com/gto76/advent-of-code-2020/' + \
        'master/advent_2020.py">Download Python script</a> or <a href="https://github.com/' + \
        'gto76/advent-of-code-2020">Fork me on GitHub</a>.</sup></p>'
BANNER = '<p class="banner"><img src="web/image_888.png" alt="Advent of Code"></p>'


def main():
    lines_1 = read_file(pathlib.Path(__file__).resolve().parent / 'advent_2020.py')
    lines_2 = lines_1[lines_1.index('###\n'):lines_1.index('# ###\n')] 
    lines_3 = [a for a in lines_2 if not a.startswith(('###\n', '#\n', 'IN_'))]
    lines_4 = [f'\r{a}' if a.startswith(('##', "'''", 'def')) else a for a in lines_3]
    parts_1 = [a.strip() for a in ''.join(lines_4).split('\r') if a]
    parts_2 = [process_title(a) if a.startswith('##') else
                   (f'```text\n{a[3:-3]}\n```' if a.startswith("'''") else process_def(a))
                       for a in parts_1]
    text = '\n\n'.join(['# Advent of Code 2020', LINKS, BANNER] + parts_2)
    write_to_file('README.md', text)
    os.popen('./parse.js')


def process_title(text):
    day = int(re.search('\d+', text).group())
    title = '' if len(TITLES) < day else f': {TITLES[day-1]}'
    return f'## Day {day}{title}'


def process_def(text):
    doc = re.search(r"'''(.+?)'''", text, flags=re.DOTALL).group(1)
    question, answer = doc.rsplit('?', maxsplit=1)
    question = re.sub('\s*\n\s*', ' ', question, flags=re.DOTALL)
    title = f'### {question}?'
    function = re.sub("'''.*?'''", f"'''{answer.strip()}'''", text, flags=re.DOTALL, count=1)
    return f'{title}\n\n```python\n{function}\n```'


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
