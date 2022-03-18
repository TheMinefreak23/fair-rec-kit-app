# simple
def test_greeting_example(client):
    response = client.get('/greeting')
    assert b"Greetings from the backend" in response.data


# JSON form data
def test_form_example(client):
    response = client.post("/computation/calculation", json={
        'metadata': {'name': 'Jon Snow', 'tag': 'I dun wan it'},
        'settings': {'dataset': 'test_set', 'approach': 'test_approach', 'metrics': 'test_metrics'},
        'result': {'ranking': 'foo_ranks', 'metrics': 'bar_metrics'},
    })
    assert response.status_code == 200
