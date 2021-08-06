#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import requests
import datetime
import sqlite3
import argparse

DB_DIR = os.environ.get('HOME', os.environ.get('HOMEPATH'))
DB_NAME = 'lotto_draws.db3'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
GAMES = [
    'Lotto',  # 'Lotto', 'LottoPlus', 'SuperSzansa'
]


def argv():
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                     description='Pobiera losowania z lotto.pl')
    parser.add_argument('--game', default='Lotto', type=str, choices=GAMES, help='Games kind')
    # parser.add_argument('--id-draw', default=0, type=int, help='System Lotto ID draw')
    # parser.add_argument('--date-draw', type=str, help='Date of draw')
    parser.add_argument('--size-result', type=int, default=10, help='Count results')
    parser.add_argument('--page', default=1, type=int, help='Page number of result')
    parser.add_argument('--db-file', type=str, help='Path to DB exists file')

    return parser.parse_args()


# sort for drawDate and drawSystemId is the same result, sort for gameType the server return status code 500
URL_GAMETYPE_FMT = 'https://www.lotto.pl/api/lotteries/draw-results/by-gametype?game={game}&index={page}&size={size}' \
    '&sort=drawDate&order=DESC'
HEADERS = {
    'authority': 'www.lotto.pl',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"\\Not\"A;Brand";v="99", "Chromium";v="84"',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.56'
    'Safari/537.36 OPR/70.0.3728.8',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.lotto.pl/lotto/wyniki-i-wygrane',
    'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'}


def download(url):
    """Maybe download, maybe get, maybe from_api."""
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print('status:', response.status_code)
        exit()

    return response.json()


def main():
    options = argv()
    url = URL_GAMETYPE_FMT.format(game=options.game, page=options.page, size=options.size_result)
    data = download(url)

    dbfilename = os.path.join(DB_DIR, DB_NAME)

    if options.db_file:
        dbfilename = options.db_file

    conn = sqlite3.connect(dbfilename)
    c = conn.cursor()

    for row in data.get('items', []):
        for result in row['results']:
            date = datetime.datetime.strptime(result['drawDate'], DATE_FORMAT)
            sys_id = result['drawSystemId']
            game_type = result['gameType']
            numbers = ','.join(map(str, result['resultsJson']))

            c.execute(f'SELECT * FROM {game_type.lower()} WHERE system_id = ? AND date = ?', (sys_id, date))

            if not c.fetchone():
                print(f'add {game_type}[{sys_id}]: {numbers}, {date}')
                c.execute(f'INSERT INTO {game_type.lower()} (system_id,date,numbers) VALUES (?,?,?)',
                          (sys_id, date, numbers))
                conn.commit()

    c.close()


if __name__ == '__main__':
    print('-- START: {} --'.format(datetime.datetime.now()))
    main()
    print('-- STOP: {} --'.format(datetime.datetime.now()))
