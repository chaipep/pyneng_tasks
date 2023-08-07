# -*- coding: utf-8 -*-
from task_12_1 import ping_ip_addresses
from task_12_2 import convert_ranges_to_ip_list
from tabulate import tabulate
"""
Задание 12.3

Создать функцию print_ip_table, которая отображает таблицу доступных
и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

"""


def print_ip_table(reach, unreach):
    ping_result = {'Reachable': reach,
                   'Unreachable': unreach}
    print(tabulate(ping_result, headers='keys'))


if __name__ == "__main__":
    reach = [
        '100.91.1.1',
        '100.91.1.2',
        '100.91.2.1',
        '100.91.2.2',
        '100.81.0.110',
        '100.81.0.111',
        '100.81.0.114',
        '100.81.0.115'
    ]
    unreach = [
        '192.168.1.1',
        '10.100.105.106',
        '100.93.0.1'
    ]
    print_ip_table(reach, unreach)
