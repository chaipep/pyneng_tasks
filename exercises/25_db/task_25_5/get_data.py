# -*- coding: utf-8 -*-
"""
Задание 25.4

Для заданий 25 раздела нет тестов!

Скопировать файл get_data из задания 25.2.
Добавить в скрипт поддержку столбца active, который мы добавили в задании 25.3.

Теперь, при запросе информации, сначала должны отображаться активные записи,
а затем, неактивные. Если неактивных записей нет, не отображать
заголовок "Неактивные записи".

Примеры выполнения итогового скрипта
$ python get_data.py
В таблице dhcp такие записи:

Активные записи:

-----------------  ----------  --  ----------------  ---  -
00:09:BB:3D:D6:58  10.1.10.2   10  FastEthernet0/1   sw1  1
00:04:A3:3E:5B:69  10.1.15.2   15  FastEthernet0/15  sw1  1
00:05:B3:7E:9B:60  10.1.5.4     5  FastEthernet0/9   sw1  1
00:07:BC:3F:A6:50  10.1.10.6   10  FastEthernet0/5   sw1  1
00:E9:BC:3F:A6:50  100.1.1.6    3  FastEthernet0/20  sw3  1
00:E9:22:11:A6:50  100.1.1.7    3  FastEthernet0/21  sw3  1
00:A9:BB:3D:D6:58  10.1.10.20  10  FastEthernet0/7   sw2  1
00:B4:A3:3E:5B:69  10.1.5.20    5  FastEthernet0/5   sw2  1
00:A9:BC:3F:A6:50  10.1.10.65  20  FastEthernet0/2   sw2  1
00:A9:33:44:A6:50  10.1.10.77  10  FastEthernet0/4   sw2  1
-----------------  ----------  --  ----------------  ---  -

Неактивные записи:

-----------------  ---------------  -  ---------------  ---  -
00:09:BC:3F:A6:50  192.168.100.100  1  FastEthernet0/7  sw1  0
00:C5:B3:7E:9B:60  10.1.5.40        5  FastEthernet0/9  sw2  0
-----------------  ---------------  -  ---------------  ---  -

$ python get_data.py vlan 5

Информация об устройствах с такими параметрами: vlan 5

Активные записи:

-----------------  ---------  -  ---------------  ---  -
00:05:B3:7E:9B:60  10.1.5.4   5  FastEthernet0/9  sw1  1
00:B4:A3:3E:5B:69  10.1.5.20  5  FastEthernet0/5  sw2  1
-----------------  ---------  -  ---------------  ---  -

Неактивные записи:

-----------------  ---------  -  ---------------  ---  -
00:C5:B3:7E:9B:60  10.1.5.40  5  FastEthernet0/9  sw2  0
-----------------  ---------  -  ---------------  ---  -


$ python get_data.py vlan 10

Информация об устройствах с такими параметрами: vlan 10

Активные записи:

-----------------  ----------  --  ---------------  ---  -
00:09:BB:3D:D6:58  10.1.10.2   10  FastEthernet0/1  sw1  1
00:07:BC:3F:A6:50  10.1.10.6   10  FastEthernet0/5  sw1  1
00:A9:BB:3D:D6:58  10.1.10.20  10  FastEthernet0/7  sw2  1
00:A9:33:44:A6:50  10.1.10.77  10  FastEthernet0/4  sw2  1
-----------------  ----------  --  ---------------  ---  -
"""

import sqlite3
import sys

db_name = 'dhcp_snooping.db'
keys = ['mac', 'ip', 'vlan', 'interface', 'switch', 'active', 'last_active']


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


def query_2_args(db_name):
    key, value = sys.argv[1:]
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


def query_0_args(db_name):
    con = sqlite3.connect(db_name)
    con.row_factory = sqlite3.Row
    print('\nВ таблице dhcp такие записи:')
    print('-' * 100)
    query = 'select * from dhcp'
    result = con.execute(query)
    print_active_inactive(con, result)
    con.close()


if len(sys.argv) == 3:
    query_2_args(db_name)
elif len(sys.argv) == 1:
    query_0_args(db_name)
else:
    print('Пожалуйста, введите два или ноль аргументов')

