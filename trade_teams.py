#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

from collections import defaultdict


TEAM_CODES = {
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


if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8') as r:
        riders = json.load(r)

    league = {
        'name': 'Trade Teams',
        'shortname': 'tradeteams',
        'teams': [],
    }

    teams = defaultdict(list)

    for name, info in riders.items():
        teams[info['team']].append({'name': name, 'cost': info.get('cost', 0)})

    for team in teams:
        if len(teams[team]) != 8:
            print(f'Invalid rider count in {team}')
        league['teams'].append({
            'user': team,
            'name': TEAM_CODES[team],
            'team': [rider['name'] for rider in sorted(teams[team], key=lambda r: r['cost'], reverse=True)]
        })

    with open('tradeteams.json', 'w', encoding='utf-8') as w:
        json.dump(league, w)
