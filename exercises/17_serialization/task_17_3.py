# -*- coding: utf-8 -*-
import re
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""


def parse_sh_cdp_neighbors(sh_cdp_ne):
    split_cdp = sh_cdp_ne.split('\n')
    hostname = sh_cdp_ne.split('>')[0].strip()
    cdp = {hostname: {}}
    for i in range(len(split_cdp)):
        if 'Device ID' in split_cdp[i]:
            i += 1
            for n in range(len(split_cdp)-i-1):
                if len(split_cdp[i+n]) > 1:
                    match = re.search(r'(\w+\d+) +(\w+ \d+/\d+) +\d+.* (\w+ +\d+/\d+)$', split_cdp[i+n])
                    dev_id = match.group(1)
                    local_if = match.group(2)
                    remote_if = match.group(3)
                    cdp[hostname].update({local_if: {dev_id: remote_if}})
    return cdp


if __name__ == "__main__":
    with open('sh_cdp_n_r2.txt', 'r') as f:
        text = f.read()
        print(parse_sh_cdp_neighbors(text))
