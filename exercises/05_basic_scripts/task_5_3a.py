# -*- coding: utf-8 -*-
"""
Задание 5.3a

Дополнить скрипт из задания 5.3 таким образом, чтобы, в зависимости
от выбранного режима, задавались разные вопросы в запросе о номере
VLANа или списка VLANов:
* для access: 'Введите номер VLAN:'
* для trunk: 'Введите разрешенные VLANы:'

Ограничение: Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if и циклов for/while.
"""

access_template = [
    "switchport mode access",
    "switchport access vlan {}",
    "switchport nonegotiate",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable",
]

trunk_template = [
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk allowed vlan {}",
]

int_mode = input('Введите режим работы интерфейса (access/trunk): ')
int_name = input('Введите тип и номер интерфейса: ')
quest = {'access': 'Введите номер VLAN: ', 'trunk': 'Введите разрешенные VLANы: '}
int_vlan = input(quest[int_mode])

access_template[1] = access_template[1].format(int_vlan)
trunk_template[2] = trunk_template[2].format(int_vlan)
result = {'access': access_template, 'trunk': trunk_template}

access_print = '''{0}
{1}
{2}
{3}
{4}
'''

trunk_print = '''{0}
{1}
{2}
'''

print_template = {'access': access_print, 'trunk': trunk_print}

print('interface', int_name)
print(print_template[int_mode].format(*result[int_mode]))
