from echo_client import client_socket_function
from echo_server import server_socket_function
import pytest


# @pytest.yield_fixture(scope='module')
# def server(request):
#     """set up and tear down a server"""

#     process = subprocess.Popen('./echo_server.py', shell=True)

#     def cleanup():
#         process.kill()

#     request.addfinalizer(cleanup)

#     yield process

@pytest.yield_fixture(scope='module')
def start_server():
    """set up and tear down a server"""
    import threading
    target = server_socket_function
    server_thread = threading.Thread(target=target)
    server_thread.daemon = True
    server_thread.start()
    yield


def test_client_socket_function_short(start_server):
    ''' 16 byte message. Short response'''
    message = "Can you hear me?"
    recieve = client_socket_function(message)
    assert recieve == message


def test_client_socket_function_long(start_server):
    ''' 74 byte message. '''
    message = "Can you hear me? I am waiting for you to respond. Come on, where are you?!"
    recieve = client_socket_function(message)
    assert recieve == message


def test_client_socket_function_unicode(start_server):
    ''' Unicode. '''
    message = u"Can you hear me? I am waiting for you to respond. Come on, where are you?!"
    recieve = client_socket_function(message)
    assert recieve == message
