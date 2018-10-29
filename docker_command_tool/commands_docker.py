import os


class Command:
    def __init__(self, command):
        self.command = command

    def add_name(self, name):
        self.command += f' {name}'

    def add_volumes(self, volumes):
        for volume in volumes.split(' '):
            self.command += f' -v {volume}'

    def add_commands(self, commands):
        self.command += f' /bin/bash -c "{commands}"'


def run_command(container_name, command, volumes, docker_params):
    commands = command.strip('\n').split('\n')
    formatted_commands = ' && '.join(commands)

    docker_command = Command(f'docker run -it --rm {docker_params}')
    docker_command.add_volumes(volumes)
    docker_command.add_name(container_name)
    docker_command.add_commands(formatted_commands)

    # final_command = f'docker run -it --rm {docker_params} {container_name} ' \
    #                 f'/bin/bash -c "{formatted_commands}"'
    #
    # final_command = add_volumes(final_command, volumes)
    print(docker_command.command)
    os.system(
        docker_command.command
    )



