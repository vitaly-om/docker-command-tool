from docker_command_tool.utils import hash_func


def test_hash_func():
    check_hash = 'fc5e038d38a57032085441e7fe7010b0'
    assert hash_func('helloworld') == check_hash
