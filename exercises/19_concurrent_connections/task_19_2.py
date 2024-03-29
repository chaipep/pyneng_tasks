# -*- coding: utf-8 -*-
"""
Задание 19.2

Создать функцию send_show_command_to_devices, которая отправляет одну и ту же
команду show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя текстового файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в обычный текстовый файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
"""

from concurrent.futures import ThreadPoolExecutor
import yaml
import netmiko
from netmiko import (ConnectHandler, NetmikoTimeoutException, NetMikoAuthenticationException)


threads = 5


def send_show_command_to_devices(devices, command, filename, limit):
    with ThreadPoolExecutor(max_workers=limit):
        result = []
        for dev in devices:
            with netmiko.ConnectHandler(**dev) as ssh:
                ssh.enable()
                result.append('\n' + ssh.find_prompt() + command + '\n')
                result.append(ssh.send_command(command))
        with open(filename, 'w') as file:
            for string in result:
                file.write(string)


if __name__ == "__main__":
    show = "sh ip int br"
    name = "sh_ip_in_br.txt"

    with open("devices.yaml") as f:
        device_list = yaml.safe_load(f)
    send_show_command_to_devices(device_list, show, name, threads)
