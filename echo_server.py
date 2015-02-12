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
                except RequestError, msg:
                    errors = str(msg).strip("'").split(' ', 1)
                    response = response_error(errors[0], errors[1])
                conn.sendall(response)
            conn.close()
    except KeyboardInterrupt:
        server_socket.close()


def response_ok():
    first_line = 'HTTP/1.1 200 OK'
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    body = '200 OK'
    response_list = [first_line, timestamp, content_header, ' ', body, '\r\n']
    return '\r\n'.join(response_list)


def response_error(error_code, error_message):
    first_line = 'HTTP/1.1 {} {}'.format(error_code, error_message)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    body = '{} {}'.format(error_code, error_message)
    response_list = [first_line, timestamp, content_header, ' ', body, '\r\n']
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
        msg = "{} {}".format(error_key, http_response_codes[error_key])
        raise RequestError(msg)
    elif mup[2] != 'HTTP/1.1':
        error_key = '505'
        msg = "{} {}".format(error_key, http_response_codes[error_key])
        raise RequestError(msg)
    else:
        return mup[1]


def resolve_uri(uri):
    if os.path.isdir(uri):
        response = gen_list(uri)
    elif os.path.isfile(uri):
        response = gen_text(uri)
    else:
        raise EnvironmentError
    return response


def gen_list(uri):
    path_list = os.listdir(uri)
    dir_list = ""
    for i in path_list:
        dir_list += "<li>"+i+"</li>\n"
    body = "<ul>\n{}</ul>\n".format(dir_list)
    html = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format(body)
    return html


def gen_text(uri):
    fo = open(uri, "r")
    file_text = fo.read();
    fo.close()
    html = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format(file_text)
    return html


class RequestError(Exception):
    """Exception raised for errors in the request."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

if __name__ == '__main__':
    # server_socket_function()
    print(resolve_uri())
