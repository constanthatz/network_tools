#!/usr/bin/env python
from __future__ import print_function
from HTTP_server import (
    parse_request,
    resolve_uri,
    RequestError,
    response_ok,
    response_error
)


def handler(conn, address):
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


def start():
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    server = StreamServer(('127.0.0.1', 50000), handler)
    print('Starting http server on port 50000')
    server.serve_forever()

if __name__ == '__main__':
    start()
