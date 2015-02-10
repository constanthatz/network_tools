from echo_client import client_socket_function
import subprocess
import os
import signal


def test_client_socket_function_short():
    ''' Test client/server interaction. '''

    process = subprocess.Popen('./echo_server.py', shell=True)
    ''' 16 byte message. '''
    recieve = client_socket_function("Can you hear me?")
    assert recieve == "I recieved your message. Stop talking to me. You are annoying."
    process.kill()


def test_client_socket_function_long():
    ''' Test client/server interaction. '''

    process = subprocess.Popen('./echo_server.py', shell=True)
    ''' 74 byte message. '''
    recieve = client_socket_function("Can you hear me? I am waiting for you to respond. Come on, where are you?!")
    assert recieve == "I recieved your message. Stop talking to me. You are annoying."
    process.kill()


def test_client_socket_function_unicode():
    ''' Test client/server interaction. '''

    process = subprocess.Popen('./echo_server.py', shell=True)
    ''' Unicode. '''
    recieve = client_socket_function(u"Can you hear me? I am waiting for you to respond. Come on, where are you?!")
    assert recieve == "I recieved your message. Stop talking to me. You are annoying."
    process.kill()
