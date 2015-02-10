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


def test_client_socket_function_short():
    ''' 16 byte message. Short response'''
    recieve = ec.client_socket_function("Can you hear me?")
    assert recieve == "I recieved your message. Stop talking to me. You are annoying."


def test_client_socket_function_long():
    ''' 74 byte message. '''
    recieve = ec.client_socket_function("Can you hear me? I am waiting for you to respond. Come on, where are you?!")
    assert recieve == "I recieved your message. Stop talking to me. You are annoying."


def test_client_socket_function_unicode():
    ''' Unicode. '''
    recieve = ec.client_socket_function(u"Can you hear me? I am waiting for you to respond. Come on, where are you?!")
    assert recieve == "I recieved your message. Stop talking to me. You are annoying."


def test_response_ok():
    ''' Test ok response message'''
    first_line = 'HTTP/1.1 200 OK'
    timestamp = email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    crlf = '<CRLF>'
    response = ('{}\nDate: {}\n{}\n{}').format(
        first_line, timestamp, content_header, crlf)
    assert es.response_ok() == response


def test_response_error():
    ''' Test error response message'''
    error_code = '404'
    error_text = 'Not Found'
    first_line = 'HTTP/1.1 {} {}'.format(error_code, error_text)
    timestamp = email.utils.formatdate(usegmt=True)
    content_header = 'Content-Type: text/plain'
    crlf = '<CRLF>'
    response = ('{}\nDate: {}\n{}\n{}').format(
        first_line, timestamp, content_header, crlf)
    assert es.response_error() == response
