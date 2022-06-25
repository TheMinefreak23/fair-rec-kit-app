"""This module tests to see if the server is online.

test_greeting_example(client): test the server greeting.
test_ping(client): test ping route.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

URL_PREFIX = '/api'


def test_greeting_example(client):
    """Test the server greeting."""
    response = client.get(URL_PREFIX+'/greeting')
    assert b'Greetings from the backend' in response.data


def test_ping(client):
    """Test ping route."""
    response = client.get(URL_PREFIX)
    assert b'Server online' in response.data
