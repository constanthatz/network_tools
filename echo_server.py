#!/usr/bin/env python
from __future__ import print_function
import socket


def server_socket_function():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)

    try:
        while True:
            conn, addr = server_socket.accept()
            message = conn.recv(32)
            if message:
                conn.sendall("I recieved your message. Stop talking to me. You are annoying.")
    except KeyboardInterrupt:
        conn.close()


if __name__ == '__main__':
    server_socket_function()
