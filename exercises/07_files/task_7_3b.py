# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

vlan = int(input('Enter VLAN number: '))
with open('/home/yudkinds/tools/pyneng_tasks/exercises/07_files/CAM_table.txt', 'r') as file:
    i = 0
    result = []
    for string in file:
        line = string.split()
        if len(line) != 0:
            if line[0].isdigit() and int(line[0]) == vlan:
                line = [int(line[0]), line[1], line[3]]
                result.append(line)
                i += 1
result.sort()
template = '''{0:<8} {1}      {2}'''
for num in result:
    print(template.format(*num))
