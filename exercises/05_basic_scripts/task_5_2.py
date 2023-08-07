# -*- coding: utf-8 -*-
"""
Задание 5.2

Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24

Затем вывести информацию о сети и маске в таком формате:

Network:
10        1         1         0
00001010  00000001  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Вывод сети и маски должен быть упорядочен также, как в примере:
- столбцами
- ширина столбца 10 символов (в двоичном формате
  надо добавить два пробела между столбцами
  для разделения октетов между собой)

Подсказка: Получить маску в двоичном формате можно так:
In [1]: "1" * 28 + "0" * 4
Out[1]: '11111111111111111111111111110000'


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

ip_address = input('Введите IP адрес и маску сети в формате X.X.X.X/Y ')
ip_list = ip_address.split('/')
ip = (ip_list[0]).split('.')
mask = int(ip_list[1])
mask_zero = 32-mask
mask_bin = '1'*mask+'0'*mask_zero
mask_bin_oct = [mask_bin[0:8], mask_bin[8:16], mask_bin[16:24], mask_bin[24:32]]
mask_dec = [int(mask_bin_oct[0], 2), int(mask_bin_oct[1], 2), int(mask_bin_oct[2], 2),
            int(mask_bin_oct[3], 2)]

ip_template = '''

Network:
{0:<8}  {1:<8}  {2:<8}  {3:<8}
{0:>08b}  {1:>08b}  {2:>08b}  {3:>08b}

Mask:
/{4}
{5:<8}  {6:<8}  {7:<8}  {8:<8}
{5:>08b}  {6:>08b}  {7:>08b}  {8:>08b}
'''

print(ip_template.format(int(ip[0]), int(ip[1]), int(ip[2]), int(ip[3]), mask,
                         int(mask_dec[0]), int(mask_dec[1]), int(mask_dec[2]),
                         int(mask_dec[3])))

