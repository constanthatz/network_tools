import echo_client as ec
import echo_server as es
import subprocess
import pytest
import email.utils


@pytest.fixture(scope='module')
def server(request):
    """set up and tear down a server"""

    process = subprocess.Popen('./echo_server.py', shell=True)

    def cleanup():
        process.kill()

    request.addfinalizer(cleanup)

    return process


def test_response_ok():
    ''' Test ok response message. '''
    first_line = 'HTTP/1.1 200 OK'
    timestamp = email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    crlf = '<CRLF>'
    response = ('{}\nDate: {}\n{}\n{}').format(
        first_line, timestamp, content_header, crlf)
    assert es.response_ok() == response


def test_response_error():
    ''' Test error response message. '''
    error_code = '404'
    error_message = 'Not Found'
    first_line = 'HTTP/1.1 {} {}'.format(error_code, error_message)
    timestamp = email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    crlf = '<CRLF>'
    response = ('{}\nDate: {}\n{}\n{}').format(
        first_line, timestamp, content_header, crlf)
    assert es.response_error(error_code, error_message) == response


def test_parse_request_uri():
    ''' Test parse request with a good request. '''
    method = 'GET'
    uri = '/index.html'
    protocol = 'HTTP/1.1'
    header = 'Host: www.example.com'
    crlf = '<CRLF>'
    client_request = '{} {} {}\n{}\n{}'.format(method,
                                               uri,
                                               protocol,
                                               header,
                                               crlf)
    assert es.parse_request(client_request) == '/index.html'


def test_parse_request_405():
    ''' Test parse request with a 405 error. '''
    method = 'PUSH'
    uri = '/index.html'
    protocol = 'HTTP/1.1'
    header = 'Host: www.example.com'
    crlf = '<CRLF>'
    client_request = '{} {} {}\n{}\n{}'.format(method,
                                               uri,
                                               protocol,
                                               header,
                                               crlf)

    first_line = 'HTTP/1.1 405 Method Not Allowed'
    timestamp = email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    crlf = '<CRLF>'
    response = ('{}\nDate: {}\n{}\n{}').format(
        first_line, timestamp, content_header, crlf)
    assert es.parse_request(client_request) == response


def test_parse_request_505():
    ''' Test parse request with a 505 error. '''
    method = 'GET'
    uri = '/index.html'
    protocol = 'HTTP/1.0'
    header = 'Host: www.example.com'
    crlf = '<CRLF>'
    client_request = '{} {} {}\n{}\n{}'.format(method,
                                               uri,
                                               protocol,
                                               header,
                                               crlf)

    first_line = 'HTTP/1.1 505 HTTP Version Not Supported'
    timestamp = email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    crlf = '<CRLF>'
    response = ('{}\nDate: {}\n{}\n{}').format(
        first_line, timestamp, content_header, crlf)
    assert es.parse_request(client_request) == response


def test_client_socket_function_ok():
    ''' Test a good request'''
    method = 'GET'
    uri = '/index.html'
    protocol = 'HTTP/1.1'
    header = 'Host: www.example.com'
    crlf = '<CRLF>'
    client_request = '{} {} {}\n{}\n{}'.format(method,
                                               uri,
                                               protocol,
                                               header,
                                               crlf)

    response = uri

    recieve = ec.client_socket_function(client_request)
    assert recieve == response


def test_client_socket_function_405():
    ''' Test a 405 error'''
    method = 'PUSH'
    uri = '/index.html'
    protocol = 'HTTP/1.1'
    header = 'Host: www.example.com'
    crlf = '<CRLF>'
    client_request = '{} {} {}\n{}\n{}'.format(method,
                                               uri,
                                               protocol,
                                               header,
                                               crlf)

    first_line = 'HTTP/1.1 405 Method Not Allowed'
    timestamp = email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    crlf = '<CRLF>'
    response = ('{}\nDate: {}\n{}\n{}').format(
        first_line, timestamp, content_header, crlf)

    recieve = ec.client_socket_function(client_request)
    assert recieve == response


def test_client_socket_function_505():
    ''' Test a 505 error'''
    method = 'GET'
    uri = '/index.html'
    protocol = 'HTTP/1.0'
    header = 'Host: www.example.com'
    crlf = '<CRLF>'
    client_request = '{} {} {}\n{}\n{}'.format(method,
                                               uri,
                                               protocol,
                                               header,
                                               crlf)

    first_line = 'HTTP/1.1 505 HTTP Version Not Supported'
    timestamp = email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    crlf = '<CRLF>'
    response = ('{}\nDate: {}\n{}\n{}').format(
        first_line, timestamp, content_header, crlf)

    recieve = ec.client_socket_function(client_request)
    assert recieve == response
