#!/usr/bin/env python
from __future__ import print_function
import socket
import email.utils

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


def response_ok(conn):
    first_line = 'HTTP/1.1 200 OK'
    timestamp = email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    crlf = '<CRLF>'
    response = ('{}\nDate: {}\n{}\n{}').format(
        first_line, timestamp, content_header, crlf)
    conn.sendall(response)
    return


def response_error():
    return


def parse_request():
    return


if __name__ == '__main__':
    server_socket_function()
