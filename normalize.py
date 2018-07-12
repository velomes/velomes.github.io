#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import os

from fuzzywuzzy import process

MAGIC_RATIO = 80
LENGTH_MISMATCH = 9

# ([\d▲▼-]+\t)+([^\t]+)\t.*

def normalize_names(results, names):
    if results['type'] == 'road':
        _normalize_keys(results, names, ['Stg','Spr', 'hc', 'cat1', 'Bky'])
    _normalize_keys(results, names, ['GC', 'PC', 'KOM', 'abandons'])


def normalize_teams(results, teams):
    if results['type'] == 'ttt':
        _normalize_keys(results, teams, ['Stg'])
    if 'assists' in results:
        _normalize_keys(results['assists'], teams, ['TC'])


def _normalize_keys(results, data, keys):
    for key in keys:
        print(f'Processing {key}...', end='')
        if key not in results:
            print('SKIP')
            continue

        for i, entry in enumerate(results[key]):
            if entry in data:
                continue

            match, ratio = process.extractOne(entry.title(), data.keys())
            if ratio < MAGIC_RATIO or abs(len(match) - len(entry)) > LENGTH_MISMATCH:
                print('Uknown entry: "{}" (matched "{}" @{})'.format(entry, match, ratio))
                continue

            results[key][i] = match

        print('DONE')


if __name__ == '__main__':
    directory = sys.argv[1] if len(sys.argv) > 1 else './results'
    files = []
    for filename in os.listdir(directory):
        if filename.endswith('.raw.json') and not os.path.isfile(os.path.join(directory, filename.split('.')[0] + '.fix.json')):
            files.append(os.path.join(directory, filename))

    with open('riders.json', 'r', encoding='utf-8') as r:
        riders = json.load(r)

    names = {rider['name']: True for rider in riders}
    teams = {rider['team']: True for rider in riders}

    print('Loaded {} unique riders from {} teams'.format(len(names), len(teams)))

    for result_file in files:
        print('Processing "{}"...'.format(result_file))
        with open(result_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
            normalize_names(results, names)
            normalize_teams(results, teams)

        out_file = result_file.split('.')[0] + '.fix.json'
        print(f'Saving to "{out_file}"')
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(results, f)
