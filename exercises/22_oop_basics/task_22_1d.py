# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Соединение с одним из портов существует"


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

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Соединение с одним из портов существует


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

    def add_link(self, link_src, link_dst):
        duple = 0
        res_topo = self.topology
        for key, value in self.topology.items():
            if (link_src == key and link_dst == value) or (link_dst == key and link_src == value):
                duple = 2
            elif link_src == key or link_src == value or link_dst == key or link_dst == value:
                duple = 1
        if duple == 0:
            self.topology[link_src] = link_dst
        elif duple == 1:
            print('Соединение с одним из портов существует')
        else:
            print('Такое соединение существует')

    def delete_node(self, device):
        res_topo = self.topology
        del_keys = []
        for key, value in self.topology.items():
            if device in key or device in value:
                del_keys.append(key)
        [res_topo.pop(key) for key in del_keys]
        if del_keys:
            self.topology = res_topo
        else:
            print('Такого устройства нет')


if __name__ == "__main__":
    new_topology = Topology(topology_example)
    print(new_topology.topology)
    new_topology.add_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))
    print(new_topology.topology)
