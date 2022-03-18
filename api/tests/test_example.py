# simple
def test_greeting_example(client):
    response = client.get('/greeting')
    assert b"Greetings from the backend" in response.data


# JSON form data
def test_form_example(client):
    response = client.post("/computation/calculation", json={
        'metadata': {'name': 'Jon Snow', 'tag': 'I dun wan it'},
        'settings': {'datasets': ['test_set1','test_set2'],
                     'approaches': ['foo','bar_approach'],
                     'metrics': [{'name': 'foo', 'k': 0},{'name': 'bar_metric','k':2}]
                     },
    })
    assert response.status_code == 200
