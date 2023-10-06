# -*- coding: utf-8 -*-

"""
Задание 22.1c

Изменить класс Topology из задания 22.1b.

Добавить метод delete_node, который удаляет все соединения с указаным устройством.

Если такого устройства нет, выводится сообщение "Такого устройства нет".

Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

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
    new_topology.delete_node('SW2')
    print(new_topology.topology)
