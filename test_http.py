import http_client as ec
import http_concurrent_server as es
import HTTP_server as hs
import pytest
import email.utils
import os


@pytest.yield_fixture(scope='module')
def start_server():
    """set up and tear down a server"""
    import threading
    target = es.start
    server_thread = threading.Thread(target=target)
    server_thread.daemon = True
    server_thread.start()
    yield


def test_parse_request_uri():
    ''' Test parse request with a good request. '''
    client_request = 'GET /index.html HTTP/1.1\r\n'
    assert es.parse_request(client_request) == '/index.html'


def test_response_ok():
    ''' Test ok response message. '''
    body = '<li>Test</li>'
    content_type = 'text/html'
    info = (content_type, body)
    actual = es.response_ok(info)
    assert body in actual
    assert content_type in actual


def test_response_error():
    ''' Test error response message. '''
    class error_test():
        def __init__(self, code, msg):
            self.code = code
            self.msg = msg

    error = error_test('404', 'Not Found')
    actual = es.response_error(error)
    assert error.code in actual
    assert error.msg in actual


def test_gen_list():
    uri = os.path.join(os.getcwd(), 'webroot')
    assert 'sample.txt' in hs.gen_list(uri)


def test_gen_text():
    uri = os.path.join(os.getcwd(), 'webroot/sample.txt')
    assert 'simple text file' in hs.gen_text(uri)


def test_resolve_uri_dir():
    ''' Test a good dir uri '''
    uri = os.path.join('/')
    assert 'text/html' in es.resolve_uri(uri)


def test_resolve_uri_file():
    ''' Test a good file uri '''
    uri = ('sample.txt')
    assert 'text/html' in es.resolve_uri(uri)


def test_handler_ok(start_server):
    ''' Test a 404'''
    client_request = 'GET / HTTP/1.1\r\n'
    actual = ec.client_socket_function(client_request)

    assert '200' in actual
    assert 'OK' in actual


def test_handler_404(start_server):
    ''' Test a 404'''
    client_request = 'GET /index.html HTTP/1.1\r\n'
    error = {"code": '404', "msg": 'Not Found'}
    actual = ec.client_socket_function(client_request)

    assert error['code'] in actual
    assert error['msg'] in actual


def test_handler_405(start_server):
    ''' Test a 405 error'''
    client_request = 'PUSH /index.html HTTP/1.1\r\n'
    error = {"code": '405', "msg": 'Method Not Allowed'}
    actual = ec.client_socket_function(client_request)

    assert error['code'] in actual
    assert error['msg'] in actual


def test_handler_505(start_server):
    ''' Test a 505 error'''
    client_request = 'GET /index.html HTTP/1.0\r\n'
    error = {"code": '505', "msg": 'HTTP Version Not Supported'}
    actual = ec.client_socket_function(client_request)

    assert error['code'] in actual
    assert error['msg'] in actual
