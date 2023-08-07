# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
template = '''Prefix                {}
AD/Metric             {}
Next-Hop              {}
Last update           {}
Outbound Interface    {}'''

with open('/home/yudkinds/tools/pyneng_tasks/exercises/07_files/ospf.txt', 'r') as ospf:
    for string_num in ospf:
        string = string_num.split()
        string.pop(0)
        string.pop(2)
        string[1] = string[1].strip('[]')
        string[2] = string[2].strip(',')
        string[3] = string[3].strip(',')
        print(template.format(*string))
