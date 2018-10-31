import argparse
import sys

from docker_command_tool.commands_docker import run_command
from docker_command_tool.constants import SUCCESS_CODE
from docker_command_tool.build import build_container

# You can use this arguments in code by its name casted to python var style
# '--docker-commands' ==> 'docker_commands'
#
# args = parser.parse_args()
# print(args.docker_commands)
ARGUMENTS = {
    '--docker-commands': {
        'short_name': '-d',
        'help': 'Additional docker commands',
    }
}


def parse_args(config):
    parser = argparse.ArgumentParser(
        prog='bagga',
        description='BAGGA',
        usage='bagga <command> [<args>]'
    )
    subparsers = parser.add_subparsers()
    for name, desc in config['commands'].items():
        parser_append = subparsers.add_parser(
            name,
            help=desc.get('description', 'No description provided'))
        for arg_name, args in ARGUMENTS.items():
            parser_append.add_argument(
                args['short_name'],
                arg_name,
                help=args['help'],
            )
        parser_append.set_defaults(command=name)
    args = parser.parse_args()
    if not getattr(args, 'command', False):
        parser.print_help()
        exit(1)
    return args


def parse_and_run(config):
    args = parse_args(config)
    command = args.command
    command_desc = config['commands'][command]
    command_container = command_desc['container']

    if build_container(command_container) != SUCCESS_CODE:
        print('Container build is failed')
        sys.exit(1)

    run_command(
        command_container,
        command_desc['cmd'],
        command_desc.get('volumes'),
        command_desc.get('ports'),
        args.docker_commands,
    )
