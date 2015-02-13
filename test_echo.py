from echo_client import client_socket_function
import subprocess
import pytest


@pytest.fixture(scope='module')
def server(request):
    """set up and tear down a server"""

    process = subprocess.Popen('./echo_server.py', shell=True)

    def cleanup():
        process.kill()

    request.addfinalizer(cleanup)

    return process


def test_client_socket_function_short():
    ''' 16 byte message. Short response'''
    message = "Can you hear me?"
    recieve = client_socket_function(message)
    assert recieve == message


def test_client_socket_function_long():
    ''' 74 byte message. '''
    message = "Can you hear me? I am waiting for you to respond. Come on, where are you?!"
    recieve = client_socket_function(message)
    assert recieve == message


def test_client_socket_function_unicode():
    ''' Unicode. '''
    message = u"Can you hear me? I am waiting for you to respond. Come on, where are you?!"
    recieve = client_socket_function(message)
    assert recieve == message
