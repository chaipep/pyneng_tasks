# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""
import os
from concurrent.futures import ThreadPoolExecutor

list_ip = [
        '192.168.100.1',
        '192.168.100.2',
        '192.168.100.3',
        '192.168.100.4',
        '192.168.100.5',
        '192.168.100.6',
        '192.168.100.7',
        '192.168.100.8',
        '192.168.100.9',
        '192.168.100.10',
        '192.168.100.100'
    ]
threads = 5


def ping_ip_addresses(ip_list, limit=3):
    with ThreadPoolExecutor(max_workers=limit):
        response = []
        notresponse = []
        for ip in ip_list:
            result = (os.system("ping -c 1 " + ip))
            if result == 0:
                response.append(ip)
            else:
                notresponse.append(ip)
        return response, notresponse


if __name__ == "__main__":
    print(ping_ip_addresses(list_ip, threads))
