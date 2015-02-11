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
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    body = '200 OK'
    response_list = [first_line, timestamp, content_header, ' ', body, '\r\n']
    assert es.response_ok() == '\r\n'.join(response_list)


def test_response_error():
    ''' Test error response message. '''
    error_code = '404'
    error_message = 'Not Found'
    first_line = 'HTTP/1.1 {} {}'.format(error_code, error_message)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    body = '{} {}'.format(error_code, error_message)
    response_list = [first_line, timestamp, content_header, ' ', body, '\r\n']
    assert es.response_error(error_code, error_message) == '\r\n'.join(response_list)


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


def test_parse_request_405():
    ''' Test parse request with a 405 error. '''
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
    body = '{} {}'.format(error_code, error_message)
    response_list = [first_line, timestamp, content_header, ' ', body, '\r\n']
    assert es.parse_request('\r\n'.join(client_request)) == '\r\n'.join(response_list)


def test_parse_request_505():
    ''' Test parse request with a 505 error. '''
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
    body = '{} {}'.format(error_code, error_message)
    response_list = [first_line, timestamp, content_header, ' ', body, '\r\n']
    assert es.parse_request('\r\n'.join(client_request)) == '\r\n'.join(response_list)


def test_client_socket_function_ok():
    ''' Test a good request'''
    method = 'GET'
    uri = '/index.html'
    protocol = 'HTTP/1.1'
    first_line = '{} {} {}'.format(method, uri, protocol)
    timestamp = 'Date: ' + email.utils.formatdate(usegmt=True)
    header = 'Host: www.example.com'
    client_request = [first_line, timestamp, header, ' ', '\r\n']

    response = uri

    recieve = ec.client_socket_function('\r\n'.join(client_request))
    assert recieve == response


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
    body = '{} {}'.format(error_code, error_message)
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
    body = '{} {}'.format(error_code, error_message)
    response_list = [first_line, timestamp, content_header, ' ', body, '\r\n']

    recieve = ec.client_socket_function('\r\n'.join(client_request))
    assert recieve == '\r\n'.join(response_list)
