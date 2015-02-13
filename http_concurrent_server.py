#!/usr/bin/env python
from __future__ import print_function
import email.utils
import os


def server(socket, address):
    buffersize = 32

    try:
        while True:

            # conn, addr = server_socket.accept()
            try:
                while True:
                    recieve_total = ""
                    finished = 0
                    while not finished:
                        recieve = socket.recv(buffersize)
                        if len(recieve) < buffersize:
                            recieve_total += recieve
                            finished = 1
                        else:
                            recieve_total += recieve

                    if recieve_total:
                        try:
                            uri = parse_request(recieve_total)
                            info = resolve_uri(uri)
                            response = response_ok(info)
                        except RequestError, msg:
                            errors = str(msg).strip("'").split(' ', 1)
                            response = response_error(errors[0], errors[1])
                        socket.sendall(response)
                    else:
                        socket.shutdown(socket.SHUT_RDWR)
                        break
            finally:
                socket.close()
    except KeyboardInterrupt:
        socket.close()


def response_ok(*args):
    first_line = 'HTTP/1.1 200 OK'
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: {}'.format(args[0][0])
    body = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format(args[0][1])
    response_list = [first_line, timestamp, content_header, ' ', body, '\r\n']
    return '\r\n'.join(response_list)


def response_error(error_code, error_message):
    first_line = 'HTTP/1.1 {} {}'.format(error_code, error_message)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    body = '{} {}\n'.format(error_code, error_message)
    body = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format(body)
    response_list = [first_line, timestamp, content_header, ' ', body, '\r\n']
    return '\r\n'.join(response_list)


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
        body = gen_list(uri)
        content_type = 'text/html'
        info = (content_type, body)
    elif os.path.isfile(uri):
        body = gen_text(uri)
        content_type = 'text/html'
        info = (content_type, body)
    else:
        error_key = '404'
        msg = "{} {}".format(error_key, 'Not Found')
        raise RequestError(msg)
    return info


def gen_list(uri):
    path_list = os.listdir(uri)
    dir_list = ""
    for i in path_list:
        dir_list += "<li>"+i+"</li>\n"
    body = "<ul>\n{}</ul>\n".format(dir_list)
    return body


def gen_text(uri):
    fo = open(uri, "r")
    body = fo.read();
    fo.close()
    return body


class RequestError(Exception):
    """Exception raised for errors in the request."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

if __name__ == '__main__':
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    server = StreamServer(('127.0.0.1', 50000), server)
    print('Starting http server on port 50000')
    server.serve_forever()
