# -*- coding: utf-8 -*-

"""
Задание 22.1b

Изменить класс Topology из задания 22.1a или 22.1.

Добавить метод delete_link, который удаляет указанное соединение.
Метод должен удалять и "обратное" соединение, если оно есть (ниже пример).

Если такого соединения нет, выводится сообщение "Такого соединения нет".

Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление линка:
In [9]: t.delete_link(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление "обратного" линка:
в словаре есть запись ``('R3', 'Eth0/2'): ('R5', 'Eth0/0')``, но вызов delete_link
с указанием ключа и значения в обратном порядке, должно удалять соединение:

In [11]: t.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))

In [12]: t.topology
Out[12]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3')}

Если такого соединения нет, выводится сообщение:
In [13]: t.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))
Такого соединения нет

"""

topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}


class Topology:
    def _normalize(self, topo):
        topo_copy = topo
        dup_keys = []
        for key1, value1 in topo.items():
            for key2, value2 in topo_copy.items():
                if key1 == value2 and value1 == key2:
                    dup_keys.append(key1)
        del (dup_keys[:int(len(dup_keys) / 2)])
        [topo.pop(key) for key in dup_keys]
        return topo

    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def delete_link(self, link_src, link_dst):
        res_topo = self.topology
        if link_src in self.topology.keys():
            res_topo.pop(link_src)
        elif link_dst in self.topology.keys():
            res_topo.pop(link_dst)
        else:
            print('Такого соединения нет')
        self.topology = res_topo


if __name__ == "__main__":
    new_topology = Topology(topology_example)
    print(new_topology.topology)
    new_topology.delete_link(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
    print(new_topology.topology)
    new_topology.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/5'))
