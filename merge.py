#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict

import json
import sys
import os


def add_totals(totals, stage):
    for rider in stage:
        for key in stage[rider]:
            totals[rider][key] += stage[rider][key]


def sum_team(scores, team):
    total = 0
    for rider in team:
        total += sum([v for v in scores['totals'][rider].values()])

    return total


def print_league(league, scores):
    results = []
    max_len = 0
    for team in league:
        results.append((team['name'], sum_team(scores, team['team'])))
        max_len = max(max_len, len(team['name']))

    results.sort(key=lambda x: x[1], reverse=True)

    for n, score in enumerate(results[:50], start=1):
        print(f'{n:>3d}. {score[0]:{max_len+1}} {score[1]}')
    if len(results) > 50:
        print('...')


def print_leaderboard(scores, limit=10):
    top = []
    max_len = 0
    print('Leaderboard:')
    for rider in scores['totals']:
        top.append((rider, sum([v for v in scores['totals'][rider].values()])))
        max_len = max(max_len, len(rider))
    top.sort(key=lambda x: x[1], reverse=True)
    total = 0
    for n, score in enumerate(top[:limit], start=1):
        total += score[1]
        print(f'{n:>3d}. {score[0]:{max_len+1}} {score[1]}')

    print(f'Total: {total}')


def main(scores_dir, teams=None):
    files = []
    for filename in os.listdir(scores_dir):
        if filename.endswith('.json'):
            files.append(os.path.join(scores_dir, filename))

    print('Found {} score files'.format(len(files)))

    scores = {
        'stages': {},
        'totals': defaultdict(lambda: defaultdict(int))
    }
    for filename in files:
        print('Processing "{}"...'.format(filename))
        with open(filename, 'r', encoding='utf-8') as f:
            stage = json.load(f)

        if stage['stage'] in scores['stages']:
            print(f'Error: Stage {stage["stage"]} already loaded, aborting')
            return

        scores['stages'][stage['stage']] = stage
        add_totals(scores['totals'], stage['riders'])

    with open('scores.json', 'w', encoding='utf-8') as f:
        json.dump(scores, f)

    print_leaderboard(scores)
    if teams:
        print_league(teams, scores)

if __name__ == '__main__':
    league = None
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            league = json.load(f)

    main(sys.argv[1], league['teams'])
