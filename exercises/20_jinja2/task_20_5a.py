# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""

import yaml
from jinja2 import Environment, FileSystemLoader
from task_20_5 import create_vpn_config
from netmiko import (ConnectHandler, NetmikoTimeoutException, NetMikoAuthenticationException)
import re
from time import time


def configure_vpn(src_device_params, dst_device_params,
                  src_template, dst_template, vpn_data_dict):
    try:
        device_list = [src_device_params, dst_device_params]
        tunnels = []
        for dev in device_list:
            with ConnectHandler(**dev) as ssh:
                ssh.enable()
                show = ssh.send_command('sh run | include Tunnel')
                if show:
                    for string in show.split('\n'):
                        tun = re.search(r'\d+', string).group(0)
                        tunnels.append(int(tun))
        tunnels = list(set(tunnels))
        if tunnels:
            for i in range(4097):
                if i not in tunnels:
                    vpn_data_dict["tun_num"] = i
                    break
        else:
            vpn_data_dict["tun_num"] = 0
        commands = create_vpn_config(src_template, dst_template, vpn_data_dict)
        print('------------------------------------------------------------')
        with ConnectHandler(**src_device_params) as ssh:
            ssh.enable()
            srs_result = ssh.send_config_set(commands[0].split('\n'))
        print(srs_result)
        print('------------------------------------------------------------')
        with ConnectHandler(**dst_device_params) as ssh:
            ssh.enable()
            dst_result = ssh.send_config_set(commands[1].split('\n'))
        print(dst_result)
        print('------------------------------------------------------------')
        return srs_result, dst_result
    except TypeError as error:
        print(error)


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    data = {
        "tun_num": None,
        "wan_ip_1": "192.168.100.1",
        "wan_ip_2": "192.168.100.2",
        "tun_ip_1": "10.0.1.1 255.255.255.252",
        "tun_ip_2": "10.0.1.2 255.255.255.252",
    }
    src_device = devices[0]
    dst_device = devices[1]
    template_file1 = "templates/gre_ipsec_vpn_1.txt"
    template_file2 = "templates/gre_ipsec_vpn_2.txt"
    print(configure_vpn(src_device, dst_device, template_file1, template_file2, data))
