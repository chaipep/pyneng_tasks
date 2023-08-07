# -*- coding: utf-8 -*-
import re
"""
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

"""


def parse_sh_ip_int_br(inputfile):
    with open(inputfile, 'r') as file:
        result = []
        for string in file:
            match = re.search(r'(\w+\d+\/*\d*) +(\S+) +\S+ +\S+ +(\S+ \S*) +(\S+)', string)
            if match:
                result.append((match.group(1),
                               match.group(2),
                               match.group(3).rstrip(),
                               match.group(4)))
    return result


print(parse_sh_ip_int_br('sh_ip_int_br.txt'))
