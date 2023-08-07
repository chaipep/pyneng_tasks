# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

ip_correct = False
while not ip_correct:
    ip = input('Введите ip адрес: ')
    ip_octets = ip.split('.')
    if len(ip_octets) == 4 and ip_octets[0].isdigit() and ip_octets[1].isdigit() \
            and ip_octets[2].isdigit() and ip_octets[3].isdigit() and 0 <= int(ip_octets[0]) <= 255 \
            and int(ip_octets[1]) <= 255 and int(ip_octets[2]) <= 255 \
            and int(ip_octets[3]) <= 255:
        if ip == '0.0.0.0':
            print('unassigned')
            ip_correct = True
        elif ip == '255.255.255.255':
            print('local broadcast')
            ip_correct = True
        else:
            oct1 = int(ip_octets[0])
            if 0 < oct1 < 224:
                print('unicast')
                ip_correct = True
            elif 223 < oct1 < 240:
                print('multicast')
                ip_correct = True
            else:
                print('unused')
                ip_correct = True
    else:
        print("Неправильный IP-адрес")
