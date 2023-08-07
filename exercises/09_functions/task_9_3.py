# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""


def get_int_vlan_map(config_filename):
    access = {}
    trunk = {}
    key = None
    value = None
    with open(config_filename) as file:
        for string in file:
            if 'FastEthernet' in string:
                key = string.split()[-1]
            elif 'vlan' in string:
                value = string.split()[-1].split(',')
            elif 'access' in string:
                mode = 'access'
            elif 'trunk' in string:
                mode = 'trunk'
            elif 'duplex' in string and key is not None and value is not None:
                if mode == 'access':
                    access[key] = int(''.join(value))
                elif mode == 'trunk':
                    vlans = list(map(int, value))
                    trunk[key] = vlans
                key = None
                value = None
    return access, trunk


list1, list2 = get_int_vlan_map('/home/yudkinds/tools/pyneng_tasks/exercises/09_functions/config_sw1.txt')
print(list1)
print(list2)
