#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

from collections import defaultdict


TEAM_CODES = {
  "ALM": "AG2R La Mondiale",
  "AST": "Astana Pro Team",
  "TBM": "Bahrain Merida Pro Cycling Team",
  "BMC": "BMC Racing Team",
  "BOH": "BORA - hansgrohe",
  "GFC": "Groupama - FDJ",
  "LTS": "Lotto Soudal",
  "MTS": "Mitchelton-Scott",
  "MOV": "Movistar Team",
  "QST": "Quick-Step Floors",
  "DDD": "Dimension Data",
  "EFD": "EF Education First-Drapac p/b Cannondale",
  "TKA": "Team Katusha - Alpecin",
  "TLJ": "Team LottoNL-Jumbo",
  "SKY": "Team Sky",
  "SUN": "Team Sunweb",
  "TFS": "Trek - Segafredo",
  "UAD": "UAE-Team Emirates",
  "FST": "Fortuneo - Samsic",
  "WGG": "Wanty - Groupe Gobert",
  "TDE": "Direct Energie",
  "COF": "Cofidis Solutions Crédits"
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
        teams[info['team']].append({'name': name, 'cost': info['cost']})

    for team in teams:
        if len(teams[team]) != 8:
            print(f'Invalid rider count in {team}')
        league['teams'].append({
                'user': team,
                'name': TEAM_CODES[team],
                'team': [rider['name'] for rider in sorted(teams[team], key=lambda r: r['cost'])]
            })

    with open('tradeteams.json', 'w', encoding='utf-8') as w:
        json.dump(league, w)
