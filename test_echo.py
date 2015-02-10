from echo_client import client_socket_funciton


def test_client_socket_function():
    recieve = echo_client("Can you hear me?")
    assert recieve == "I received your message."
