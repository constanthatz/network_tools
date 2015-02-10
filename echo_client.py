#!/usr/bin/env python
from __future__ import print_function
from __future__ import unicode_literals
import socket
import sys


def client_socket_funciton(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall(message)
    client_socket.shutdown(socket.SHUT_WR)
    recieve = client_socket.recv(32)
    client_socket.close()
    return recieve

if __name__ == '__main__':
    recieve = client_socket_funciton(sys.argv[1])
    print(recieve)
