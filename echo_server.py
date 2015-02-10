#!/usr/bin/env python
from __future__ import print_function
from __future__ import unicode_literals
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
server_socket.bind(('127.0.0.1', 50000))
server_socket.listen(1)
conn, addr = server_socket.accept()

conn.recv(32)

conn.sendall("Yes, I hear you.")
conn.close()

server_socket.close()
