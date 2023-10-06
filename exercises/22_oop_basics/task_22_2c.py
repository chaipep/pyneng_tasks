# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

"""

from telnetlib import Telnet
from textfsm import TextFSM, clitable
from time import sleep


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.ip = ip
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

    def send_config_commands(self, commands, strict=True):
        self._write_line('conf t')
        self.con.expect([b'[#]'])
        if isinstance(commands, str):
            self._write_line('\n')
            self._write_line(commands)
            sleep(1)
            output = self.con.read_very_eager().decode('utf-8')
            clear_output = '\n'.join(output.split('\n')[2:-1])
            if '%' in output:
                error = output.split('% ')[-1].split('\n')[0]
                if strict:
                    raise ValueError('При выполнении команды "' + commands +
                                     '" на устройстве ' + self.ip + ' возникла ошибка -> ' + error)
                else:
                    print('При выполнении команды "' + commands +
                          '" на устройстве ' + self.ip + ' возникла ошибка -> ' + error)
                    return clear_output
            else:
                return clear_output
        else:
            result_list = []
            errors_list = []
            for command in commands:
                self._write_line('\n')
                self._write_line(command)
                sleep(1)
                output = self.con.read_very_eager().decode('utf-8')
                clear_output = '\n'.join(output.split('\n')[2:-1])
                if '%' in output:
                    error = output.split('% ')[-1].split('\n')[0]
                    if strict:
                        raise ValueError('При выполнении команды "' + command +
                                         '" на устройстве ' + self.ip + ' возникла ошибка -> ' + error)
                    else:
                        errors_list.append('При выполнении команды "' + command +
                                           '" на устройстве ' + self.ip + ' возникла ошибка -> ' + error)
                        result_list.append(clear_output)
                else:
                    result_list.append(clear_output)
            return '\n'.join(errors_list) + '\n' + '\n'.join(result_list)

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
    # coms = ['int Fa1/15', 'speed 100', 'duplex full', 'exit', 'd0o sh run int Fa1/15']
    # coms = 'do sh ip int br'
    commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
    correct_commands = ['logging buffered 20010', 'ip http server']
    commands_list = commands_with_errors + correct_commands
    # commands_list = 'a'
    r1 = CiscoTelnet(**r1_params)
    # print(r1.send_show_command(com))
    print(r1.send_config_commands(commands_list))
