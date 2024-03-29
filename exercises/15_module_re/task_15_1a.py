# -*- coding: utf-8 -*-
import re
"""
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом,
чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""


def get_ip_from_cfg(cfg_file):
    with open(cfg_file, 'r') as file:
        result = {}
        for line in file:
            if line.startswith('interface'):
                inter = re.search(r'(\S+)$', line)
            if line.startswith(' ip address'):
                ipaddr = re.search(r'(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)', line)
                result[inter.group()] = ipaddr.groups()
    return result


print(get_ip_from_cfg('config_r1.txt'))
