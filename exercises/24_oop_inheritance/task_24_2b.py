# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку
на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает
вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

"""

from netmiko.cisco.cisco_ios import CiscoIosSSH
from typing import Optional, Union, List, Any, Dict, Sequence, Iterator, TextIO


class ErrorInCommand(Exception):

    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """


class MyNetmiko(CiscoIosSSH):
    def __init__(self, **params):
        super().__init__(**params)
        self.enable()
        self.params = params
        self.ip = params['host']

    def _check_error_in_command(self, command, output):
        for string in output.split('\n'):
            if '%' in string:
                clear_out = string.strip('% ').strip()
        if '%' in output:
            if 'Invalid input detected' in output or 'Incomplete command' in output or 'Ambiguous command' in output:
                raise ErrorInCommand(f'При выполнении команды "{command}" на устройстве {self.ip} возникла ошибка "{clear_out}"')

    def send_command(
        self,
        command_string: str,
        expect_string: Optional[str] = None,
        read_timeout: float = 10.0,
        delay_factor: Optional[float] = None,
        max_loops: Optional[int] = None,
        auto_find_prompt: bool = True,
        strip_prompt: bool = True,
        strip_command: bool = True,
        normalize: bool = True,
        use_textfsm: bool = False,
        textfsm_template: Optional[str] = None,
        use_ttp: bool = False,
        ttp_template: Optional[str] = None,
        use_genie: bool = False,
        cmd_verify: bool = True,
    ) -> Union[str, List[Any], Dict[str, Any]]:
        result = super().send_command(command_string)
        self._check_error_in_command(command_string, result)
        return result

    def send_config_set(
        self,
        config_commands: Union[str, Sequence[str], Iterator[str], TextIO, None] = None,
        *,
        exit_config_mode: bool = True,
        read_timeout: Optional[float] = None,
        delay_factor: Optional[float] = None,
        max_loops: Optional[int] = None,
        strip_prompt: bool = False,
        strip_command: bool = False,
        config_mode_command: Optional[str] = None,
        cmd_verify: bool = True,
        enter_config_mode: bool = True,
        error_pattern: str = "",
        terminator: str = r"#",
        bypass_commands: Optional[str] = None,
    ) -> str:
        resultate = []
        if isinstance(config_commands, list):
            for command_string in config_commands:
                result = super().send_config_set(command_string)
                self._check_error_in_command(command_string, result)
                resultate += result
        else:
            self.config_mode()
            resultate = super().send_command(config_commands)
        self._check_error_in_command(config_commands, resultate)
        return resultate


device_params = {
    "device_type": "cisco_ios",
    "host": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}

if __name__ == "__main__":
    r1 = MyNetmiko(**device_params)
    print(r1.send_config_set(['logging 0255.255.1', 'lo', 'a']))
