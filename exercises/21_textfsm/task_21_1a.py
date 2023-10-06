# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM.
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt
и шаблоне templates/sh_ip_int_br.template.
"""

import textfsm
from netmiko import ConnectHandler
from textfsm import TextFSM


def parse_output_to_dict(template, command_output):
    with open(template) as f:
        re_table = textfsm.TextFSM(f)
        header = re_table.header
        result = re_table.ParseText(command_output)
    result_list = []
    for value in result:
        dict = {}
        for key, item in zip(header, value):
            dict[key] = item
        result_list.append(dict)
    return result_list


if __name__ == "__main__":
    r1_params = {
        "device_type": "cisco_ios",
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    with open('output/sh_ip_int_br.txt') as f:
        output = f.read()
    result = parse_output_to_dict("templates/sh_ip_int_br.template", output)
    print(result)
