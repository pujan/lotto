#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request
import datetime
import sqlite3

print('-- START: {} --'.format(datetime.datetime.now()))

url = "http://www.lotto.pl/lotto/wyniki-i-wygrane/ostatnie-wyniki"
data = urllib.request.urlopen(url)

if data.status != 200:
    print('status:', data.status)
    exit()

charset = data.getheader('Content-Type').split('=')[1]
content = data.read().decode(charset, 'ignore')
soup = BeautifulSoup(content, "html.parser")
data = []
table = soup.find('table', attrs={'class': 'ostatnie-wyniki-table'})
tbody = table.find('tbody')

for row in tbody.find_all('tr'):
    for col in [el for el in row.find_all('td')]:
        img = col.find('img')
        if img and img.attrs['alt'] == 'Lotto':
            td = img.next_element
            id_ = td.text
            td = td.next_sibling
            date = datetime.datetime.strptime(td.text.split(',')[0], '%d-%m-%y').date()
            td = td.next_sibling
            div = td.find('div', class_='{}-kolejnosc'.format(id_))
            numbers = [el.text.strip() for el in div.find_all('div', class_='number')]
            numbers = ','.join(numbers)
            print('id: {}, date: {}, numbers: {}'.format(id_, date, numbers))
            data.append([id_, date, numbers])

conn = sqlite3.connect('draws.db')
c = conn.cursor()

for row in data:
    c.execute('SELECT * FROM losowania WHERE id_losowania = ? AND data = ?', tuple(row[:2]))
    res = c.fetchone()

    if not res:
        print('add:', row)
        c.execute('INSERT INTO losowania (id_losowania,data,liczby) VALUES (?,?,?)', tuple(row))
        conn.commit()

c.close()

print('-- STOP: {} --'.format(datetime.datetime.now()))
