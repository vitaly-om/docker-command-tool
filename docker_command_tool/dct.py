import sys

from docker_command_tool.cli import parse_and_run
from docker_command_tool.build import load_containers
from docker_command_tool.utils import get_config


def main():
    config = get_config()
    load_containers(config)
    parse_and_run(config)


if __name__ == '__main__':
    main()
