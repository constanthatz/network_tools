#!/usr/bin/env python
from __future__ import print_function
import socket
import email.utils
import os


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
            finished = False
            while not finished:
                recieve = conn.recv(buffersize)
                if len(recieve) < buffersize:
                    finished = True
                recieve_total += recieve

            if recieve_total:
                try:
                    uri = parse_request(recieve_total)
                    info = resolve_uri(uri)
                    response = response_ok(info)
                except RequestError as error:
                    response = response_error(error)
                conn.sendall(response)
            conn.close()
    except KeyboardInterrupt:
        server_socket.close()


def parse_request(client_request):
    mup_line = client_request.splitlines()[0]
    mup = mup_line.split(' ')
    uri = error_mup(mup)
    return uri


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


def resolve_uri(uri):
    uri = uri.lstrip("/")
    here = os.getcwd()
    home = 'webroot'
    webhome = os.path.join(here, home)

    actual_path = os.path.join(webhome, uri)

    if os.path.isdir(actual_path):
        body = gen_list(actual_path)
        content_type = 'text/html'
        info = (content_type, body)
    elif os.path.isfile(actual_path):
        body = gen_text(actual_path)
        content_type = 'text/html'
        info = (content_type, body)
    else:
        error_key = '404'
        raise RequestError(error_key, 'Not Found')
    return info


def gen_list(uri):
    path_list = os.listdir(uri)
    dir_list = ""
    for i in path_list:
        dir_list += "<li>"+i+"</li>\n"
    body = "<ul>\n{}</ul>\n".format(dir_list)
    return body


def gen_text(uri):
    with open(uri, "rb") as fo:
        body = fo.read()
    return body


def response_ok(*args):
    first_line = 'HTTP/1.1 200 OK'
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: {}'.format(args[0][0])
    body = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format(args[0][1])
    content_length = 'Content-Length: {}'.format(len(body.encode('utf-8')))
    response_list = [first_line, timestamp, content_header, content_length, '', body]
    return '\r\n'.join(response_list)


def response_error(error):
    first_line = 'HTTP/1.1 {} {}'.format(error.code, error.msg)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/html'
    body = '{} {}\n'.format(error.code, error.msg)
    body = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format(body)
    content_length = 'Content-Length: {}'.format(len(body.encode('utf-8')))
    response_list = [first_line, timestamp, content_header, content_length, '', body]
    return '\r\n'.join(response_list)


class RequestError(Exception):
    """Exception raised for errors in the request."""

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return "{} {}".format(self.code, self.msg)

if __name__ == '__main__':
    server_socket_function()
