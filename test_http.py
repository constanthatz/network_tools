import http_client as ec
import http_concurrent_server as es
import subprocess
import os
import pytest
import email.utils


# @pytest.fixture(scope='module')
# def server(request):
#     """set up and tear down a server"""
#     import multiprocessing

#     p = multiprocessing.Process(target=es)
#     p.start()
#     # subprocess.Popen('./http_concurrent_server.py', shell=True)

#     def cleanup(p=p):
#         p.terminate()

#     request.addfinalizer(cleanup)


def test_response_ok_dir():
    ''' Test ok response message to a dir request. '''
    uri = 'webroot/'
    body = es.gen_list(uri)
    content_type = 'text/html'
    info = (content_type, body)
    first_line = 'HTTP/1.1 200 OK'
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: {}'.format(content_type)
    body = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format(body)
    response_list = [first_line, timestamp, content_header, ' ', body, '\r\n']
    assert es.response_ok(info) == '\r\n'.join(response_list)


def test_response_ok_file():
    ''' Test ok response message to a dir request. '''
    uri = 'webroot/sample.txt'
    fo = open(uri, "r")
    body = fo.read();
    fo.close()
    content_type = 'text/html'
    info = (content_type, body)
    first_line = 'HTTP/1.1 200 OK'
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: {}'.format(content_type)
    body = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format(body)
    response_list = [first_line, timestamp, content_header, ' ', body, '\r\n']
    assert es.response_ok(info) == '\r\n'.join(response_list)


def test_response_error():
    ''' Test error response message. '''
    error_code = '404'
    error_message = 'Not Found'
    first_line = 'HTTP/1.1 {} {}'.format(error_code, error_message)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    body = '{} {}\n'.format(error_code, error_message)
    body = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format(body)
    response_list = [first_line, timestamp, content_header, ' ', body, '\r\n']
    assert es.response_error(
        error_code, error_message) == '\r\n'.join(response_list)


def test_parse_request_uri():
    ''' Test parse request with a good request. '''
    method = 'GET'
    uri = '/index.html'
    protocol = 'HTTP/1.1'
    first_line = '{} {} {}'.format(method, uri, protocol)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    header = 'Host: www.example.com'
    client_request = [first_line, timestamp, header, ' ', '\r\n']
    assert es.parse_request('\r\n'.join(client_request)) == '/index.html'


def test_client_socket_function_ok():
    ''' Test a good request'''
    method = 'GET'
    uri = 'webroot/'
    protocol = 'HTTP/1.1'
    first_line = '{} {} {}'.format(method, uri, protocol)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    header = 'Host: www.example.com'
    client_request = [first_line, timestamp, header, ' ', '\r\n']

    body = es.gen_list(uri)
    content_type = 'text/html'
    first_line = 'HTTP/1.1 200 OK'
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: {}'.format(content_type)
    body = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format(body)
    response_list = [first_line, timestamp, content_header, ' ', body, '\r\n']

    recieve = ec.client_socket_function('\r\n'.join(client_request))
    assert recieve == '\r\n'.join(response_list)


def test_client_socket_function_405():
    ''' Test a 405 error'''
    method = 'PUSH'
    uri = '/index.html'
    protocol = 'HTTP/1.1'
    first_line = '{} {} {}'.format(method, uri, protocol)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    header = 'Host: www.example.com'
    client_request = [first_line, timestamp, header, ' ', '\r\n']

    error_code = '405'
    error_message = 'Method Not Allowed'
    first_line = 'HTTP/1.1 {} {}'.format(error_code, error_message)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    body = '{} {}\n'.format(error_code, error_message)
    body = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format(body)
    response_list = [first_line, timestamp, content_header, ' ', body, '\r\n']

    recieve = ec.client_socket_function('\r\n'.join(client_request))
    assert recieve == '\r\n'.join(response_list)


def test_client_socket_function_505():
    ''' Test a 505 error'''
    method = 'GET'
    uri = '/index.html'
    protocol = 'HTTP/1.0'
    first_line = '{} {} {}'.format(method, uri, protocol)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    header = 'Host: www.example.com'
    client_request = [first_line, timestamp, header, ' ', '\r\n']

    error_code = '505'
    error_message = 'HTTP Version Not Supported'
    first_line = 'HTTP/1.1 {} {}'.format(error_code, error_message)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    body = '{} {}\n'.format(error_code, error_message)
    body = '''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n{}</body>\n</html>'''.format(body)
    response_list = [first_line, timestamp, content_header, ' ', body, '\r\n']

    recieve = ec.client_socket_function('\r\n'.join(client_request))
    assert recieve == '\r\n'.join(response_list)


def test_resolve_uri():
    ''' Test a good dir uri '''
    uri = 'webroot/'
    body = es.gen_list(uri)
    content_type = 'text/html'
    info = (content_type, body)
    assert es.resolve_uri(uri) == info

    ''' Test a good file uri '''
    uri = 'webroot/sample.txt'
    body = es.gen_text(uri)
    content_type = 'text/html'
    info = (content_type, body)
    assert es.resolve_uri(uri) == info


class RequestError(Exception):
    """Exception raised for errors in the request."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
