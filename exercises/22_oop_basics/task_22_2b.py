# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

"""

from telnetlib import Telnet
from textfsm import TextFSM, clitable


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.con = Telnet(ip, 23, 10)
        self.con.read_until(b'Username: ')
        self._write_line(username)
        self.con.read_until(b'Password: ')
        self._write_line(password)
        self.con.expect([b'[>#]'])
        self._write_line('enable')
        self.con.read_until(b'Password: ')
        self._write_line(secret)
        self.con.expect([b'[#]'])
        self._write_line('terminal length 0')
        self.con.expect([b'[#]'])

    def _write_line(self, line):
        self.con.write(line.encode('ascii') + b'\n')

    def send_config_commands(self, commands):
        self._write_line('conf t')
        self.con.expect([b'[#]'])
        if isinstance(commands, str):
            self._write_line(commands)
            return self.con.read_until(b'#').decode('utf-8')
        else:
            result_list = []
            result = None
            for command in commands:
                self._write_line(command)
                result_list.append(self.con.read_until(b'#').decode('utf-8'))
                result = '\n'.join(result_list)
            return result

    def send_show_command(self, command, parse=True, templates='templates', index='index'):
        self._write_line(command)
        attributes_dict = {'Command': command, 'Vendor': 'cisco_ios'}
        output = self.con.read_until(b'#').decode('utf-8')
        if parse:
            cli_table = clitable.CliTable(index, templates)
            cli_table.ParseCmd(output, attributes_dict)
            header = list(cli_table.header)
            result = [list(row) for row in cli_table]
            result_list = []
            for value in result:
                res_dict = {}
                for key, item in zip(header, value):
                    res_dict[key] = item
                result_list.append(res_dict)
            return result_list
        else:
            return output


if __name__ == "__main__":

    r1_params = {
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'}
    com = 'sh ip int br'
    coms = ['int Fa1/15', 'speed 100', 'duplex full', 'exit', 'do sh run int Fa1/15']
    # coms = 'do sh ip int br'

    r1 = CiscoTelnet(**r1_params)
    # print(r1.send_show_command(com))
    print(r1.send_config_commands(coms))
