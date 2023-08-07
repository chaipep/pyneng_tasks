# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт: Скрипт не должен выводить на стандартрый поток вывода команды,
в которых содержатся слова из списка ignore.

При этом скрипт также не должен выводить строки, которые начинаются на !.

Проверить работу скрипта на конфигурационном файле config_sw1.txt.
Имя файла передается как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]
with open('/home/yudkinds/tools/pyneng_tasks/exercises/07_files/config_sw1.txt', 'r') as config:
    for string in config:
        if '!' in string:
            continue
        else:
            string_ignore = False
            for word in ignore:
                if word in string:
                    string_ignore = True
            if not string_ignore:
                print(string.strip('\n'))
