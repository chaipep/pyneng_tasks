# -*- coding: utf-8 -*-

"""
Задание 22.1a

Скопировать класс Topology из задания 22.1 и изменить его.

Перенести функциональность удаления "дублей" в метод _normalize.
При этом метод __init__ должен выглядеть таким образом:
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


if __name__ == "__main__":
    new_topology = Topology(topology_example)
    print(new_topology.topology)
