import sys

from docker_command_tool.commands_docker import run_command
from docker_command_tool.constants import DOCKER_PARAMS_FLAG, SUCCESS_CODE
from docker_command_tool.build import build_container


def parse_and_run(config, argv):

    command = argv[1]
    command_desc = config['commands'][command]
    command_container = command_desc['container']

    if DOCKER_PARAMS_FLAG in argv:
        docker_params = argv[argv.index(DOCKER_PARAMS_FLAG) + 1]
    else:
        docker_params = ''

    if build_container(command_container) != SUCCESS_CODE:
        print('Container build is failed')
        sys.exit(1)

    run_command(
        command_container,
        command_desc['cmd'],
        command_desc.get('volumes'),
        command_desc.get('ports'),
        docker_params,
    )
