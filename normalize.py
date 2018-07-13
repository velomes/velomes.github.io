#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import os

from fuzzywuzzy import process

MAGIC_RATIO = 80
LENGTH_MISMATCH = 9

# ([\d▲▼-]+\t)+([^\t]+)\t.*

team_codes = {
  "AG2R La Mondiale": "ALM",
  "Astana Pro Team": "AST",
  "Bahrain Merida Pro Cycling Team": "TBM",
  "BMC Racing Team": "BMC",
  "BORA - hansgrohe": "BOH",
  "Groupama - FDJ": "GFC",
  "Lotto Soudal": "LTS",
  "Mitchelton-Scott": "MTS",
  "Movistar Team": "MOV",
  "Quick-Step Floors": "QST",
  "Dimension Data": "DDD",
  "EF Education First-Drapac p/b Cannondale": "EFD",
  "Team Katusha - Alpecin": "TKA",
  "Team LottoNL-Jumbo": "TLJ",
  "Team Sky": "SKY",
  "Team Sunweb": "SUN",
  "Trek - Segafredo": "TFS",
  "UAE-Team Emirates": "UAD",
  "Fortuneo - Samsic": "FST",
  "Wanty - Groupe Gobert": "WGG",
  "Direct Energie": "TDE",
  "Cofidis Solutions Crédits": "COF",
}

def swap_team_code(entries, key):
    entries[key] = [t if t in team_codes.values() else team_codes[t] for t in entries[key]]


def normalize_names(results, names):
    if results['type'] == 'road':
        _normalize_keys(results, names, ['Stg','Spr', 'hc', 'cat1', 'Bky'])
    _normalize_keys(results, names, ['GC', 'PC', 'KOM', 'abandons'])


def normalize_teams(results):
    if results['type'] == 'ttt':
        _normalize_keys(results, team_codes, ['Stg'])
        swap_team_code(results, 'Stg')
    if 'Ass' in results:
        _normalize_keys(results['Ass'], team_codes, ['TC'])
        swap_team_code(results['Ass'], 'TC')


def _normalize_keys(results, data, keys):
    for key in keys:
        print(f'Processing {key}...', end='')
        if key not in results:
            print('SKIP')
            continue

        for i, entry in enumerate(results[key]):
            if entry in data:
                continue

            if entry in data.values():
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
            normalize_teams(results)

        out_file = result_file.split('.')[0] + '.fix.json'
        print(f'Saving to "{out_file}"')
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(results, f)
