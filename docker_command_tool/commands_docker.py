import os
import sys

from docker_command_tool.build import build_container
from docker_command_tool.constants import SUCCESS_CODE


class Command:
    def __init__(self, command):
        self.command = command

    def add_name(self, name):
        self.command += f' {name}'

    def add_list_params(self, params_list):
        if params_list:
            for params in params_list:
                for param in params:
                    self.command += param

    def add_commands(self, commands):
        self.command += f' /bin/bash -c "{commands}"'

    def add_docker_params(self, params):
        if params:
            self.command += f' {params}'


def run_command(command, args, config):
    command_desc = config['commands'][command]
    command_container = command_desc['container']

    if build_container(command_container) != SUCCESS_CODE:
        print('Container build is failed')
        sys.exit(1)

    params_list = get_params_list(command_desc)
    docker_run_command(
        command_container,
        command_desc['cmd'],
        params_list,
        args.docker_commands,
    )


def get_params(param, config):
    params = config.get(param['dsl_name'])
    if not params:
        return

    # This is how we get them from yaml
    params = params.split(' ')
    return [param['docker_command'].format(p) for p in params]


def get_params_list(config):
    PARAMS = (
        {'dsl_name': 'volumes', 'docker_command': ' -v {}'},
        {'dsl_name': 'ports', 'docker_command': ' -p {}'},
        {'dsl_name': 'envs', 'docker_command': ' -e {}'},
    )
    params_list = [get_params(p, config) for p in PARAMS]
    return [p for p in params_list if p]


def docker_run_command(
        container_name,
        command,
        params_list,
        docker_params
):
    commands = command.strip('\n').split('\n')
    formatted_commands = ' && '.join(commands)

    docker_command = Command(f'docker run -it --rm')
    docker_command.add_docker_params(docker_params)
    docker_command.add_list_params(params_list)
    docker_command.add_name(container_name)
    docker_command.add_commands(formatted_commands)

    print(docker_command.command)
    os.system(
        docker_command.command
    )



