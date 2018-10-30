import os
import yaml

from docker_command_tool.utils import hash_func
from docker_command_tool.constants import (
    DOCKERFILE_DIR,
    SUCCESS_CODE,
)


def load_containers(dct_config):
    if not os.path.exists(DOCKERFILE_DIR):
        os.mkdir(DOCKERFILE_DIR)

    containers = dct_config['containers']
    for container_name, container_desc in containers.items():
        dockerfile_path = get_dockerfile_path(container_name)
        with open(dockerfile_path, 'w') as dockerfile:
            dockerfile.write(container_desc)


def get_dockerfile_path(container_name):
    return os.path.join('.', DOCKERFILE_DIR, container_name)


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
