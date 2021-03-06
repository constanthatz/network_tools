#!/usr/bin/env python
from __future__ import print_function
import socket
import email.utils


def server_socket_function():
    server_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM,
                                  socket.IPPROTO_IP)
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)

    try:
        while True:
            conn, addr = server_socket.accept()
            message = conn.recv(4096)
            if message:
                response = parse_request(message)
                conn.sendall(response)
            conn.close()
    except KeyboardInterrupt:
        server_socket.close()


def response_ok():
    first_line = 'HTTP/1.1 200 OK'
    timestamp = email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    crlf = '<CRLF>'
    response = ('{}\nDate: {}\n{}\n{}').format(
        first_line, timestamp, content_header, crlf)
    return response


def response_error(error_code, error_message):
    first_line = 'HTTP/1.1 {} {}'.format(error_code, error_message)
    timestamp = email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    crlf = '<CRLF>'
    response = ('{}\nDate: {}\n{}\n{}').format(
        first_line, timestamp, content_header, crlf)
    return response


def parse_request(request):
    mup_line = request.splitlines()[0]
    mup = mup_line.split(' ')

    if mup[0] != 'GET':
        return response_error('405', 'Method Not Allowed')
    elif mup[2] != 'HTTP/1.1':
        return response_error('505', 'HTTP Version Not Supported')

    return mup[1]

if __name__ == '__main__':
    server_socket_function()
    # server_socket = socket.socket(socket.AF_INET,
    #                               socket.SOCK_STREAM,
    #                               socket.IPPROTO_IP)
    # server_socket.listen(1)
    # conn, addr = server_socket.accept()
    # conn.close()
    # server_socket.close()
