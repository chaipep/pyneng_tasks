# -*- coding: utf-8 -*-
"""
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса.
Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделенны точкой
   - каждое число в диапазоне от 0 до 255

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'

Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
ip = input('Введите ip адрес: ')
ip_octets = ip.split('.')
if len(ip_octets) == 4 and ip_octets[0].isdigit() and ip_octets[1].isdigit() \
        and ip_octets[2].isdigit() and ip_octets[3].isdigit() and 0 <= int(ip_octets[0]) <= 255 \
        and int(ip_octets[1]) <= 255 and int(ip_octets[2]) <= 255 \
        and int(ip_octets[3]) <= 255:
    if ip == '0.0.0.0':
        print('unassigned')
    elif ip == '255.255.255.255':
        print('local broadcast')
    else:
        oct1 = int(ip_octets[0])
        if 0 < oct1 < 224:
            print('unicast')
        elif 223 < oct1 < 240:
            print('multicast')
        else:
            print('unused')
else:
    print("Неправильный IP-адрес")
