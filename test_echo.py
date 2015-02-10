from echo_client import client_socket_funciton
from echo_server import server_socket_function


def test_client_socket_function_short():
    ''' Test client/server interaction. '''

    ''' 16 byte message. '''
    recieve = client_socket_funciton("Can you hear me?")
    assert recieve == "I recieved your message. Stop talking to me. You are annoying."


def test_client_socket_function_long():
    ''' Test client/server interaction. '''
    ''' 74 byte message. '''
    recieve = client_socket_funciton("Can you hear me? I am waiting for you to respond. Come on, where are you?!")
    assert recieve == "I recieved your message. Stop talking to me. You are annoying."


def test_client_socket_function_unicode():
    ''' Test client/server interaction. '''
    ''' Unicode. '''
    recieve = client_socket_funciton(u"Can you hear me? I am waiting for you to respond. Come on, where are you?!")
    assert recieve == "I recieved your message. Stop talking to me. You are annoying."
