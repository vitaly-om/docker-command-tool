import argparse

from docker_command_tool.commands_docker import run_command
from docker_command_tool.build import load_containers
from docker_command_tool.utils import get_config
from docker_command_tool.cli import parse_args, parse_default_args


def main():
    parser = argparse.ArgumentParser(
        prog='bagga',
        description='BAGGA',
        usage='bagga <command> [<args>]'
    )

    default_args = parse_default_args(parser)

    if default_args.config:
        config = get_config(default_args.config)
    else:
        config = get_config()

    load_containers(config)

    args = parse_args(parser, config)
    command = args.command
    run_command(command, args, config)


if __name__ == '__main__':
    main()
