# -*- coding: utf-8 -*-
import csv
import re
"""
Задание 17.1

Создать функцию write_dhcp_snooping_to_csv, которая обрабатывает вывод
команды show dhcp snooping binding из разных файлов и записывает обработанные
данные в csv файл.

Аргументы функции:
* filenames - список с именами файлов с выводом show dhcp snooping binding
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Например, если как аргумент был передан список с одним файлом sw3_dhcp_snooping.txt:
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:E9:BC:3F:A6:50   100.1.1.6        76260       dhcp-snooping   3    FastEthernet0/20
00:E9:22:11:A6:50   100.1.1.7        76260       dhcp-snooping   3    FastEthernet0/21
Total number of bindings: 2

В итоговом csv файле должно быть такое содержимое:
switch,mac,ip,vlan,interface
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21

Первый столбец в csv файле имя коммутатора надо получить из имени файла,
остальные - из содержимого в файлах.

Проверить работу функции на содержимом файлов sw1_dhcp_snooping.txt,
sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.

"""


def write_dhcp_snooping_to_csv(filenames, output):
    data = []
    data.append(['switch', 'mac', 'ip', 'vlan', 'interface'])
    for file in filenames:
        with open(file, 'r') as f:
            n_lines = 0
            for n in f:
                n_lines += 1
        with open(file, 'r') as f:
            switchname = re.search(r'(\w+\d+)_', file).group(1)
            i = 0
            for string in f:
                i = i + 1
                if i != 1 and i != 2 and i != n_lines:
                    line = string.split()
                    line = [switchname, line[0], line[1], line[4], line[5]]
                    data.append(line)
    with open(output, 'w') as out:
        writer = csv.writer(out)
        for row in data:
            writer.writerow(row)


fileslist = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']
write_dhcp_snooping_to_csv(fileslist, 'output.csv')
