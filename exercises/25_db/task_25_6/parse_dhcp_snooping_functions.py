# -*- coding: utf-8 -*-

import sqlite3
import os
import re
import yaml
import sys
from datetime import datetime, timedelta

keys = ['mac', 'ip', 'vlan', 'interface', 'switch', 'active', 'last_active']


def create_db(db_name, db_scheme):
    db_exists = os.path.exists(db_name)
    con = sqlite3.connect(db_name)
    if not db_exists:
        print('Создаю базу данных...')
        with open(db_scheme, 'r') as f:
            schema = f.read()
            con.executescript(schema)
            print('База данных успешно создана')
    else:
        print('База данных существует')
    con.close()


def add_data_switches(db_name, sw_list):
    for sw_file in sw_list:
        with open(str(sw_file), 'r') as f:
            switches = yaml.safe_load(f)['switches']
        print('Добавляю данные в таблицу switches...')
        con = sqlite3.connect(db_name)
        for key, value in switches.items():
            row = tuple([key, value])
            try:
                with con:
                    query = '''insert into switches (hostname, location)
                               values (?, ?)'''
                    con.execute(query, row)
            except sqlite3.IntegrityError as e:
                print('При добавлении данных:', row, 'Возникла ошибка:', e)
        con.close()


def add_data(db_name, data_list):
    regex_dhcp = re.compile('(\S+)\s+(\S+)\s+\d+\s+\S+\s+(\S+)\s+(\S+)\s+')
    dhcp_data = []
    for file in data_list:
        with open(file, 'r') as data:
            for line in data:
                match = regex_dhcp.search(line)
                if match:
                    dhcp_data.append(tuple(list(match.groups())+[file.split('/')[-1].split('_')[0]]))
    con = sqlite3.connect(db_name)
    print('Добавляю данные в таблицу dhcp...')
    for row in dhcp_data:
        try:
            with con:
                query = '''replace into dhcp (mac, ip, vlan, interface, switch, active, last_active)
                           values (?, ?, ?, ?, ?, 1, datetime('now'))'''
                con.execute(query, row)
        except sqlite3.IntegrityError as e:
            print('При добавлении данных:', row, 'Возникла ошибка:', e)
    con.close()


def print_active_inactive(con, result):
    active = []
    inactive = []
    for row in result:
        line = []
        for k in keys:
            line.append(row[k])
        if row['active'] == 1:
            active.append(line)
        else:
            inactive.append(line)
    print('\nАктивные записи:\n')
    print('-' * 100)
    for line in active:
        print('{}  {:16}  {:6}  {:24}  {:4}  {}  {:16}'.format(*line))
    print('-' * 100)
    con.close()
    print('\nНеактивные записи:\n')
    print('-' * 100)
    for line in inactive:
        print('{}  {:16}  {:6}  {:24}  {:4}  {}  {:16}'.format(*line))
    print('-' * 100)


def get_data(db_name, key, value):
    if key not in keys:
        print('Данный параметр не поддерживается.')
        print('Допустимые значения параметров: mac, ip, vlan, interface, switch, active, last_active')
    else:
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        print('\nИнформация об устройствах с такими параметрами:', key, value)
        print('-'*100)
        query = 'select * from dhcp where {} = ?'.format(key)
        result = con.execute(query, (value, ))
        print_active_inactive(con, result)
        con.close()


def get_all_data(db_name):
    con = sqlite3.connect(db_name)
    con.row_factory = sqlite3.Row
    print('\nВ таблице dhcp такие записи:')
    print('-' * 100)
    query = 'select * from dhcp'
    result = con.execute(query)
    print_active_inactive(con, result)
    con.close()
