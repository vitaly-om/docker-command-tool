import os
import sys
import yaml
import hashlib

CONFIG_PATH = 'dct.yaml'
DOCKERFILE_DIR = '.dockerfiles'
DOCKER_PARAMS_FLAG = r'dp'

SUCCESS_CODE = 0


def get_config():
    with open(CONFIG_PATH, 'r') as config_file:
        return yaml.load(config_file)


def get_dockerfile_path(container_name):
    return os.path.join('.', DOCKERFILE_DIR, container_name)


def load_containers(dct_config):
        if not os.path.exists(DOCKERFILE_DIR):
            os.mkdir(DOCKERFILE_DIR)

        containers = dct_config['containers']
        for container_name, container_desc in containers.items():
            dockerfile_path = get_dockerfile_path(container_name)
            with open(dockerfile_path, 'w') as dockerfile:
                dockerfile.write(container_desc)


def hash_func(content):
    md5_hash = hashlib.md5()
    md5_hash.update(''.join(content.split()).encode())
    return md5_hash.hexdigest()


def _rewrite_hash_if_needed(container_name):
    hashes_path = os.path.join('.', DOCKERFILE_DIR, 'hashes.yaml')
    if not os.path.exists(hashes_path):
        open(hashes_path, 'a').close()

    dockerfile_path = get_dockerfile_path(container_name)

    with open(dockerfile_path, 'r') as dockerfile:
        dockerfile_content = dockerfile.read()
        new_hash_value = hash_func(dockerfile_content)

    with open(hashes_path, 'r+') as hashes_store:
        hashes_items = yaml.load(hashes_store) or {}
        current_hash_value = hashes_items.get(container_name)
        if current_hash_value != new_hash_value:
            hashes_items[container_name] = new_hash_value
            hashes_store.truncate(0)
            hashes_store.seek(0)
            hashes_store.write(yaml.dump(hashes_items))
            return True

    return False


def build_container(container_name):
    if _rewrite_hash_if_needed(container_name):
        return os.system(f'docker build -t {container_name} '
                         f'-f {DOCKERFILE_DIR}/{container_name} .')
    return SUCCESS_CODE


def run_command(container_name, command, docker_params):
    commands = command.split('\n')
    formatted_commands = ' && '.join(commands)
    os.system(
        f'docker run -it --rm {docker_params} {container_name} '
        f'/bin/bash -c "{formatted_commands}"'
    )


if __name__ == '__main__':
    config = get_config()
    load_containers(config)

    argv = sys.argv
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

    run_command(command_container, command_desc['cmd'], docker_params)
