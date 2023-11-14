# -*- coding: utf-8 -*-
"""
Задание 25.1

Для заданий 25 раздела нет тестов!

Необходимо создать два скрипта:

1. create_db.py
2. add_data.py


1 скрипт create_db.py - в этот скрипт должна быть вынесена функциональность по созданию БД:
* должна выполняться проверка наличия файла БД
* если файла нет, согласно описанию схемы БД в файле dhcp_snooping_schema.sql,
  должна быть создана БД
* имя файла бд - dhcp_snooping.db

В БД должно быть две таблицы (схема описана в файле dhcp_snooping_schema.sql):
 * switches - в ней находятся данные о коммутаторах
 * dhcp - тут хранится информация полученная из вывода sh ip dhcp snooping binding

Пример выполнения скрипта, когда файла dhcp_snooping.db нет:
$ python create_db.py
Создаю базу данных...

После создания файла:
$ python create_db.py
База данных существует
"""

import sqlite3
import os
import re

db_exists = os.path.exists('dhcp_snooping.db')


def create_db(db_name, db_scheme):
    con = sqlite3.connect(db_name)
    if not db_exists:
        print('Создаю базу данных...')
        with open(db_scheme, 'r')as f:
            schema = f.read()
            con.executescript(schema)
            print('База данных успешно создана')
    else:
        print('База данных существует')
    con.close()


if __name__ == "__main__":
    db_name = 'dhcp_snooping.db'
    db_scheme = './new_data/dhcp_snooping_schema.sql'

    create_db(db_name, db_scheme)
