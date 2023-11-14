# -*- coding: utf-8 -*-
"""
2 скрипт add_data.py - с помощью этого скрипта, выполняется добавление данных в БД.
Скрипт должен добавлять данные из вывода sh ip dhcp snooping binding
и информацию о коммутаторах

Соответственно, в файле add_data.py должны быть две части:
* информация о коммутаторах добавляется в таблицу switches
 * данные о коммутаторах, находятся в файле switches.yml
* информация на основании вывода sh ip dhcp snooping binding добавляется в таблицу dhcp
 * вывод с трёх коммутаторов:
   * файлы sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt
 * так как таблица dhcp изменилась, и в ней теперь присутствует поле switch, его нужно
   также заполнять. Имя коммутатора определяется по имени файла с данными

Пример выполнения скрипта, когда база данных еще не создана:
$ python add_data.py
База данных не существует. Перед добавлением данных, ее надо создать

Пример выполнения скрипта первый раз, после создания базы данных:
$ python add_data.py
Добавляю данные в таблицу switches...
Добавляю данные в таблицу dhcp...

Пример выполнения скрипта, после того как данные были добавлены в таблицу
(порядок добавления данных может быть произвольным, но сообщения должны
выводиться аналогично выводу ниже):

$ python add_data.py
Добавляю данные в таблицу switches...
При добавлении данных: ('sw1', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
При добавлении данных: ('sw2', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
При добавлении данных: ('sw3', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
Добавляю данные в таблицу dhcp...
При добавлении данных: ('00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:04:A3:3E:5B:69', '10.1.5.2', '5', 'FastEthernet0/10', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:05:B3:7E:9B:60', '10.1.5.4', '5', 'FastEthernet0/9', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:07:BC:3F:A6:50', '10.1.10.6', '10', 'FastEthernet0/3', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:09:BC:3F:A6:50', '192.168.100.100', '1', 'FastEthernet0/7', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:E9:BC:3F:A6:50', '100.1.1.6', '3', 'FastEthernet0/20', 'sw3') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:E9:22:11:A6:50', '100.1.1.7', '3', 'FastEthernet0/21', 'sw3') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:A9:BB:3D:D6:58', '10.1.10.20', '10', 'FastEthernet0/7', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:B4:A3:3E:5B:69', '10.1.5.20', '5', 'FastEthernet0/5', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:C5:B3:7E:9B:60', '10.1.5.40', '5', 'FastEthernet0/9', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:A9:BC:3F:A6:50', '10.1.10.60', '20', 'FastEthernet0/2', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac


На данном этапе, оба скрипта вызываются без аргументов.

Код в скриптах должен быть разбит на функции.
Какие именно функции и как разделить код, надо решить самостоятельно.
Часть кода может быть глобальной.
"""

import sqlite3
import os
import re
import yaml

db_exists = os.path.exists('dhcp_snooping.db')
regex_dhcp = re.compile('(\S+)\s+(\S+)\s+\d+\s+\S+\s+(\S+)\s+(\S+)\s+')
dhcp_data = []


def create_table_dhcp(data_list):
    for file in data_list:
        with open(file, 'r') as data:
            for line in data:
                match = regex_dhcp.search(line)
                if match:
                    dhcp_data.append(tuple(list(match.groups())+[file.split('_')[0]]))
    con = sqlite3.connect(db_name)
    print('Добавляю данные в таблицу dhcp...')
    for row in dhcp_data:
        try:
            with con:
                query = '''insert into dhcp (mac, ip, vlan, interface, switch)
                           values (?, ?, ?, ?, ?)'''
                con.execute(query, row)
        except sqlite3.IntegrityError as e:
            print('При добавлении данных:', row, 'Возникла ошибка:', e)
    con.close()


def create_table_switch(sw_file):
    with open(sw_file, 'r') as f:
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


if __name__ == "__main__":
    db_name = 'dhcp_snooping.db'
    data_list = [
        'sw1_dhcp_snooping.txt',
        'sw2_dhcp_snooping.txt',
        'sw3_dhcp_snooping.txt'
    ]
    sw_file = 'switches.yml'

    create_table_dhcp(data_list)
    create_table_switch(sw_file)
