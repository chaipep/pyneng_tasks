# -*- coding: utf-8 -*-
import graphviz
from draw_network_graph import draw_topology
import yaml

"""
Задание 17.3b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий
для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно,
чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии,
но и удалять "дублирующиеся" соединения (их лучше всего видно на схеме, которую
генерирует функция draw_topology из файла draw_network_graph.py).
Тут "дублирующиеся" соединения, это ситуация когда в словаре есть два соединения:
    ("R1", "Eth0/0"): ("SW1", "Eth0/1")
    ("SW1", "Eth0/1"): ("R1", "Eth0/0")

Из-за того что один и тот же линк описывается дважды, на схеме будут лишние соединения.
Задача оставить только один из этих линков в итоговом словаре, не важно какой.

Проверить работу функции на файле topology.yaml (должен быть создан в задании 17.3a).
На основании полученного словаря надо сгенерировать изображение топологии
с помощью функции draw_topology.
Не копировать код функции draw_topology из файла draw_network_graph.py.

Результат должен выглядеть так же, как схема в файле task_17_3b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть "дублирующихся" линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

"""


def transform_topology(yaml_file):
    with open(yaml_file) as f:
        topo_dict = yaml.safe_load(f)
        temp_dict = {}
        new_dict = {}
        for hostname, cdp_ne in topo_dict.items():
            for local_if, remote_dev_if in cdp_ne.items():
                key = (hostname, local_if)
                for dev_id, remote_if in remote_dev_if.items():
                    temp_dict[key] = (dev_id, remote_if)
                    new_dict.update(temp_dict)
        copy_dict = new_dict
        dup_keys = []
        for key1, value1 in new_dict.items():
            for key2, value2 in copy_dict.items():
                if key1 == value2 and value1 == key2:
                    dup_keys.append(key1)
        del (dup_keys[:int(len(dup_keys) / 2)])
        [new_dict.pop(key) for key in dup_keys]
        return new_dict


if __name__ == "__main__":
    draw_topology(transform_topology('topology.yaml'), 'task_17_3b_new_topology')
