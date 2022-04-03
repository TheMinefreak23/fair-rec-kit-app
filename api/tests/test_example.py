# simple
def test_greeting_example(client):
    response = client.get('/greeting')
    assert b"Greetings from the backend" in response.data


# JSON form data
def test_form_example(client):
    response = client.post("/computation/calculation", json={
        'settings': {
            'metadata': {'name': 'Jon Snow', 'tag': 'I dont want it'},
            'datasets': ['test_set1', 'test_set2'],
            'approaches': [{'name': 'foo', 'parameter': {'name': 'method', 'value': 'quantile'}},
                           {'name': 'bar_approach'}],
            'metrics': [{'name': 'foo', 'parameter': {'name': 'bar', 'value': ''}},
                        {'name': 'bar_metric', 'parameter': {'name': 'foob'}}]
        },
    })
    assert response.status_code == 200
