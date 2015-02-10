#!/usr/bin/env python
from __future__ import print_function
from __future__ import unicode_literals
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)

client_socket.connect(('127.0.0.1', 50000))

client_socket.sendall("Hey, can you hear me?")
client_socket.shutdown(socket.SHUT_WR)

client_socket.recv(32)
client_socket.close()
