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

            recieve_total = ""
            buffersize = 32
            finished = 0
            while not finished:
                recieve = conn.recv(buffersize)
                if len(recieve) < buffersize:
                    recieve_total += recieve
                    finished = 1
                else:
                    recieve_total += recieve

            if recieve_total:
                try:
                    response = parse_request(recieve_total)
                    response = response_ok()
                except RequestError as error:
                    response = response_error(error)
                conn.sendall(response)
            conn.close()
    except KeyboardInterrupt:
        server_socket.close()


def response_ok():
    first_line = 'HTTP/1.1 200 OK'
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/html'
    body = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format('200 OK')
    response_list = [first_line, timestamp, content_header, '', body, '\r\n']
    return '\r\n'.join(response_list)


def response_error(error):
    first_line = 'HTTP/1.1 {} {}'.format(error.code, error.msg)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    body = '{} {}'.format(error.code, error.msg)
    body = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format(body)
    response_list = [first_line, timestamp, content_header, '', body, '\r\n']
    return '\r\n'.join(response_list)


def parse_request(client_request):
    mup_line = client_request.splitlines()[0]
    mup = mup_line.split(' ')

    answer = error_mup(mup)

    return answer


def error_mup(mup):

    http_response_codes = {'405': 'Method Not Allowed',
                           '505': 'HTTP Version Not Supported'}

    if mup[0] != 'GET':
        error_key = '405'
        raise RequestError(error_key, http_response_codes[error_key])
    elif mup[2] != 'HTTP/1.1':
        error_key = '505'
        raise RequestError(error_key, http_response_codes[error_key])
    else:
        return mup[1]


class RequestError(Exception):
    """Exception raised for errors in the request."""
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return "{} {}".format(self.code, self.msg)


if __name__ == '__main__':
    server_socket_function()
