# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping (запуск ping через subprocess).
IP-адрес считается доступным, если выполнение команды ping отработало с кодом 0 (returncode).
Нюансы: на Windows returncode может быть равен 0 не только, когда ping был успешен,
но для задания нужно проверять именно код. Это сделано для упрощения тестов.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import subprocess


def ping_ip_addresses(ip_list):
    av_ip = []
    unav_ip = []
    for ip in ip_list:
        result = subprocess.run(['ping', '-c', '1', ip],
                                stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            av_ip.append(ip)
        else:
            unav_ip.append(ip)
    return av_ip, unav_ip


if __name__ == "__main__":
    ip_list = [
        '192.168.1.1',
        '100.91.0.1',
        '100.81.0.110',
        '100.81.0.114',
        '10.100.105.106',
        '100.93.0.1'
    ]
    print(ping_ip_addresses(ip_list))
