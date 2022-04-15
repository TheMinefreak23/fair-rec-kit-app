# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

url_prefix = '/api'

# Test the server greeting
def test_greeting_example(client):
    response = client.get(url_prefix+'/greeting')
    assert b'Greetings from the backend' in response.data


# Test ping route
def test_ping(client):
    response = client.get(url_prefix)
    assert b'Server online' in response.data

