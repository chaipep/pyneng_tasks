# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]
with open('/home/yudkinds/tools/pyneng_tasks/exercises/07_files/config_sw1.txt', 'r') as config, \
        open('/tmp/pytest-of-yudkinds/pytest-0/test_task0/test_tasks/task_7_2b.txt', 'w') as result:
    for string in config:
        if '!' in string:
            continue
        else:
            string_ignore = False
            for word in ignore:
                if word in string:
                    string_ignore = True
            if not string_ignore:
                result.writelines(string)
