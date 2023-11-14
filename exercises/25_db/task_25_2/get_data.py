# -*- coding: utf-8 -*-
import sqlite3
import sys

db_name = '../task_25_1/dhcp_snooping.db'
keys = ['mac', 'ip', 'vlan', 'interface', 'switch']


def query_2_args(db_name):
    key, value = sys.argv[1:]
    if key not in keys:
        print('Данный параметр не поддерживается.')
        print('Допустимые значения параметров: mac, ip, vlan, interface, switch')
    else:
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        print('\nИнформация об устройствах с такими параметрами:', key, value)
        print('-'*100)
        query = 'select * from dhcp where {} = ?'.format(key)
        result = con.execute(query, (value, ))
        for row in result:
            line = []
            for k in keys:
                line.append(row[k])
            print('{}  {:16}  {:6}  {:24}  {:4}'.format(*line))
        print('-' * 100)
        con.close()


def query_0_args(db_name):
    con = sqlite3.connect(db_name)
    con.row_factory = sqlite3.Row
    print('\nВ таблице dhcp такие записи:')
    print('-' * 100)
    query = 'select * from dhcp'
    result = con.execute(query)
    for row in result:
        line = []
        for k in keys:
            line.append(row[k])
        print('{}  {:16}  {:6}  {:24}  {:4}'.format(*line))
    print('-' * 100)
    con.close()


if len(sys.argv) == 3:
    query_2_args(db_name)
elif len(sys.argv) == 1:
    query_0_args(db_name)
else:
    print('Пожалуйста, введите два или ноль аргументов')

