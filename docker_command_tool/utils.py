import hashlib
import yaml

from docker_command_tool.constants import CONFIG_PATH


def get_config():
    with open(CONFIG_PATH, 'r') as config_file:
        return yaml.load(config_file)


def hash_func(content):
    md5_hash = hashlib.md5()
    md5_hash.update(''.join(content.split()).encode())
    return md5_hash.hexdigest()