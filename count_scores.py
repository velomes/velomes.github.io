#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict

import json
import sys
import os

SCORE_DATA = {
    'Stg': [200, 150, 120, 100, 80, 70, 60, 50, 40, 30, 25, 20, 15, 10, 5],
    'Spr': [15, 12, 10, 8, 6, 5, 4, 3, 2, 1],
    'Bky': [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
    'hc': [30, 25, 20, 15, 10, 6, 4, 2],
    'cat1': [15, 10, 6, 4, 2],

    'GC': [25, 22, 20, 18, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    'PC': [10, 6, 4, 3, 2, 1],
    'KOM': [10, 6, 4, 3, 2, 1],

    'Ass': [6, 4, 2],

    'TTT': [40, 35, 30, 25, 20, 15, 10, 5],

    'final': {
        'GC': [500, 400, 350, 300, 260, 220, 200, 180, 160, 140, 130, 120, 110, 100, 90, 80, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5],
        'PC': [100, 80, 60, 50, 40, 30, 20, 15, 10, 5],
        'KOM': [100, 80, 60, 50, 40, 30, 20, 15, 10, 5],
        'Ass': [40, 30, 20, 10, 5],
    },
}

DONT_CHECK = ['Bky', 'KOM']

YEAR = 2019


def score_key(results, score_data, check=True):
    if check and len(results) > 0 and len(results) != len(score_data):
        print('Error: invalid results {} != {}'.format(len(results), len(score_data)))
        return

    scores = {}
    for pos, rider in enumerate(results):
        scores[rider] = score_data[pos]

    return scores


def add_points(scores, key, points):
    for rider in points.keys():
        scores[rider][key] += points[rider]


def calculate_ttt(scores, results):
    print('TTT', end=' ')
    key = 'Stg'
    score = score_key(results[key], SCORE_DATA['TTT'], True)
    add_points(scores, key, score)
    print('DONE')


def calculate_final(scores, results):
    print('Final', end=' ')
    for key in ['GC', 'PC', 'KOM']:
        print(key, end=' ')
        score = score_key(results[key], SCORE_DATA['final'][key])
        add_points(scores['riders'], key, score)


def calculate_fina_ass(teamscores, results):
    score = score_key(results['Ass']['TC'], SCORE_DATA['final']['Ass'], True)
    add_points(teamscores, 'Ass', score)


def calculate_stage(scores, results):
    print('Stage results: ', end='')
    for key in ['Stg', 'Spr', 'Bky']:
        print(key, end=' ')
        score = score_key(results[key], SCORE_DATA[key], key not in DONT_CHECK)
        add_points(scores['riders'], key, score)

    for key in ['hc', 'cat1']:
        print(key, end=' ')
        for hill in results['Sum'][key]:
            score = score_key(hill, SCORE_DATA[key])
            add_points(scores['riders'], 'Sum', score)

    print('DONE')


def calculate_daily(scores, results):
    print('Daily points: ', end='')
    for key in ['GC', 'PC', 'KOM']:
        print(key, end=' ')
        score = score_key(results[key], SCORE_DATA[key], key not in DONT_CHECK)
        add_points(scores['riders'], key, score)

    print('DONE')


def calculate_assists(teamscores, assistscores, results):
    print('Assists: ', end='')
    ass = 'Ass'
    key = 'TC'
    print(key, end=' ')
    score = score_key(results[ass][key], SCORE_DATA[ass], True)
    add_points(teamscores, ass, score)

    for key in ['Stg', 'GC']:
        print(key, end=' ')
        score = score_key(results[key][:3], SCORE_DATA[ass], True)
        add_points(assistscores, ass, score)

    print('DONE')


def main(riders, stages):
    rider_list = [{'name': rider, 'team': riders[rider]['team']} for rider in riders]

    for stage in stages:
        print(f'Processing stage {stage}...')
        with open(f'./results/{YEAR}/{stage}.fix.json', 'r', encoding='utf-8') as f:
            results = json.load(f)

        # add up scores
        teamscores = defaultdict(lambda: defaultdict(int))
        assistscores = defaultdict(lambda: defaultdict(int))
        scores = {
            'stage': results['stage'],
            'type': results['type'],
            'riders': defaultdict(lambda: defaultdict(int)),
        }
        if results['type'] == 'ttt':
            calculate_ttt(teamscores, results)

        if results['type'] == 'road':
            calculate_stage(scores, results)
            calculate_assists(teamscores, assistscores, results)

        if results['type'] == 'tt':
            calculate_stage(scores, results)

        if results['type'] == 'final':
            calculate_final(scores, results)
            calculate_fina_ass(teamscores, results)

        if results['type'] != 'final':
            calculate_daily(scores, results)

        # convert team/assist points
        abandons = set(results['abandons'])
        for rider in rider_list:
            if rider['name'] in abandons:
                continue

            if rider['team'] in teamscores:
                for key, value in teamscores[rider['team']].items():
                    scores['riders'][rider['name']][key] += value
                # scores['riders'][rider['name']]['Ass'] += teamscores[rider['team']]['Ass']

            for mate in assistscores:
                if mate == rider['name']:
                    continue
                if riders[mate]['team'] == riders[rider['name']]['team']:
                    scores['riders'][rider['name']]['Ass'] += assistscores[mate]['Ass']

        total = 0
        for rider in scores['riders']:
            score = sum([v for v in scores['riders'][rider].values()])
            total += score
        print('Stage {}: {} riders scored total of {} points'.format(stage, len(scores['riders']), total))

        with open(f'./scores/{YEAR}/{stage}.json', 'w', encoding='utf-8') as f:
            json.dump(scores, f)


if __name__ == '__main__':
    #         riders.json
    with open(sys.argv[1], 'r', encoding='utf-8') as r:
        riders = json.load(r)

    main(riders, sys.argv[2:])
