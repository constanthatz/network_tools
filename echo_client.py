#!/usr/bin/env python
from __future__ import print_function
import socket
import sys


def client_socket_function(message):
    client_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM,
                                  socket.IPPROTO_IP)
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall(message)
    client_socket.shutdown(socket.SHUT_WR)

    recieve_total = ""
    buffersize = 32
    finished = 0
    while not finished:
        recieve = client_socket.recv(buffersize)
        if len(recieve) < buffersize:
            client_socket.close()
            finished = 1
        recieve_total += recieve

    return recieve_total

if __name__ == '__main__':
    recieve = client_socket_function(sys.argv[1])
    print(recieve)
