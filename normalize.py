#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import os

from fuzzywuzzy import process

MAGIC_RATIO = 80
LENGTH_MISMATCH = 9

# ([\d▲▼-]+\t)+([^\t]+)\t.*

teams = {
  "ALM": "Ag2r La Mondiale",
  "AST": "Astana Pro Team",
  "BOH": "BORA - hansgrohe",
  "CCC": "CCC Team",
  "COF": "Cofidis, solutions crédits",
  "DQT": "Deceuninck-Quick Step",
  "EF1": "EF Education First",
  "FST": "Fortuneo - Samsic",
  "GFC": "Groupama-FDJ",
  "INS": "Team Ineos",
  "LTS": "Lotto Soudal",
  "MOV": "Movistar Team",
  "MTS": "Mitchelton-Scott",
  "PCB": "Team Arkéa-Samsic",
  "SUN": "Team Sunweb",
  "TBM": "Bahrain - Merida",
  "TDD": "Team Dimension Data",
  "TDE": "Total Direct Energie",
  "TFS": "Trek - Segafredo",
  "TJV": "Team Jumbo-Visma",
  "TKA": "Team Katusha - Alpecin",
  "TLJ": "Team LottoNL-Jumbo",
  "UAD": "UAE-Team Emirates",
  "WGG": "Wanty - Gobert Cycling Team"
}

team_codes = {name: code for code, name in teams.items()}


def swap_team_code(entries, key):
    entries[key] = [t if t in team_codes.values() else team_codes[t] for t in entries[key]]


def normalize_names(results, names):
    if results['type'] == 'road' or results['type'] == 'tt':
        _normalize_keys(results, names, ['Stg', 'Spr', 'Bky'])
        cat1 = []
        for i, entries in enumerate(results['Sum']['cat1']):
            print('Processing cat1...')
            cat1.append(_normalize_list(entries, names))
        results['Sum']['cat1'] = cat1

        hc = []
        for i, entries in enumerate(results['Sum']['hc']):
            print('Processing hc...')
            hc.append(_normalize_list(entries, names))
        results['Sum']['hc'] = hc

    _normalize_keys(results, names, ['GC', 'PC', 'KOM', 'abandons'])


def normalize_teams(results):
    if results['type'] == 'ttt':
        _normalize_keys(results, team_codes, ['Stg'])
        swap_team_code(results, 'Stg')
    if 'Ass' in results:
        _normalize_keys(results['Ass'], team_codes, ['TC'])
        swap_team_code(results['Ass'], 'TC')

def _normalize_list(entries, names):
    normalized = []
    for entry in entries:
        if entry in names:
            normalized.append(entry)
            continue

        keys = names.keys() if type(names) is dict else names
        match, ratio = process.extractOne(entry.title(), keys)
        if ratio < MAGIC_RATIO or abs(len(match) - len(entry)) > LENGTH_MISMATCH:
            print('Uknown entry: "{}" (matched "{}" @{})'.format(entry, match, ratio))
            normalized.append(entry)
            continue

        normalized.append(match)

    return normalized


def _normalize_keys(results, data, keys):
    for key in keys:
        print(f'Processing {key}...', end='')
        if key not in results:
            print('SKIP')
            continue

        for i, entry in enumerate(results[key]):
            if entry in data:
                continue

            if type(data) is dict and entry in data.values():
                continue

            keys = data.keys() if type(data) is dict else data
            match, ratio = process.extractOne(entry.title(), keys)
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

    names = set(riders.keys())
    teams = {rider['team'] for rider in riders.values()}

    print('Loaded {} unique riders from {} teams'.format(len(names), len(teams)))

    for result_file in files:
        print('Processing "{}"...'.format(result_file))
        with open(result_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
            normalize_names(results, names)
            normalize_teams(results)

        out_file = result_file.split('.')[0] + '.fix.json'
        print(f'Saving to "{out_file}"')
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(results, f)
