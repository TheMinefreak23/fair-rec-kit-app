# simple
def test_greeting_example(client):
    response = client.get('/greeting')
    assert b"Greetings from the backend" in response.data

# JSON form data
def test_form_example(client):
    response = client.post("/computation/calculation", json={
        'timestamp': 0,
        'number': 0,
        'dataset': 'test',
    })
    assert response.status_code == 200
