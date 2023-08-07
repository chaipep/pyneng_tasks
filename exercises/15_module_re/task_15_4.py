# -*- coding: utf-8 -*-
import re
"""
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример итогового списка:
["Loopback0", "Tunnel0", "Ethernet0/1", "Ethernet0/3.100", "Ethernet1/0"]

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
"""


def get_ints_without_description(cfg_file):
    with open(cfg_file, 'r') as file:
        result = []
        ifwithdes = []
        ifall = []
        for line in file:
            if line.startswith('interface'):
                inter = re.search(r'(\S+)$', line).group()
                ifall.append(inter)
            if line.startswith(' description'):
                ifwithdes.append(inter)
        result = [int for int in ifall if int not in ifwithdes]
    return result


print(get_ints_without_description('config_r1.txt'))
