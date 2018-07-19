#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import string

from bs4 import BeautifulSoup as bs
import requests

LEAGUE_URL = 'https://www.velogames.com/tour-de-france/2018/leaguescores.php?league={league_id}'
TEAM_URL = 'https://www.velogames.com/tour-de-france/2018/teamroster.php?tid={tid}'


def get_soup(url):
    r = requests.get(url)
    if not r.ok:
        print('Error loading url "{}": {}'.format(url, r.code))

    return bs(r.text, 'html.parser')


def laod_league_name(team_id, league_id):
    url = TEAM_URL.format(tid=team_id)
    soup = get_soup(url)
    valid_chars = string.ascii_lowercase + string.digits

    for a in soup.find_all('a'):
        h = a.get('href')
        if h == 'leaguescores.php?league={}'.format(league_id):
            name = a.string
            break
    else:
        name = str(league_id)

    return name, ''.join(ch for ch in name.lower() if ch in valid_chars)


def load_league(league_id):
    url = LEAGUE_URL.format(league_id=league_id)
    soup = get_soup(url)

    user_list = []
    users = soup.find(id="users")
    for user in users.find_all('li'):
        u = {}

        p = user.find('p', {'class': 'born'}, recursive=False)
        u['user'] = p.string

        h3 = user.find('h3', {'class': 'name'})
        u['name'] = h3.string

        a = h3.find('a')
        href = a.get('href')
        u['tid'] = href.split('tid=')[1]

        user_list.append(u)

    return user_list


def load_team(tid):
    url = TEAM_URL.format(tid=tid)
    soup = get_soup(url)

    riders = []
    for a in soup.find_all('a'):
        h = a.get('href')
        if not h or not h.startswith('riderprofile.php'):
            continue
        riders.append(a.string)

    if len(set(riders)) != 9:
        print('Error: invalid rider count: {} ({})'.format(tid, len(set(riders))))

    return riders


def main(league_id):
    teams = load_league(league_id)
    print('Found {} teams'.format(len(teams)))

    fullname, shortname = laod_league_name(teams[0]['tid'], league_id)

    if os.path.isfile(f'leagues/{shortname}.json'):
        print(f'League "{fullname}" ({shortname}) already exists')
        return

    print(f'Loading league "{fullname}" ({shortname})', end='', flush=True)
    for n, team in enumerate(teams):
        print('.', end='', flush=True)
        team['team'] = load_team(team['tid'])
        time.sleep(0.188)
    print('DONE')

    league = {
        'name': fullname,
        'shortname': shortname,
        'teams': [{k: v for k, v in team.items() if k != 'tid'} for team in teams],
    }

    with open(f'leagues/{shortname}.json', 'w') as f:
        json.dump(league, f)


if __name__ == '__main__':
    main(sys.argv[1])
