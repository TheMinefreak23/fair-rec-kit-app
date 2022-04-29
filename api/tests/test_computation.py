# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import json
from project.computation import *

url_prefix = '/api/computation'


# Test if computation route works on mock JSON form data
def test_form(client):
    file = open('tests/options.json')
    old_queue_length = len(computation_queue)
    response = client.post(url_prefix + '/calculation', json=json.load(file))
    assert response.status_code == 200  # Assert success
    assert len(computation_queue) == old_queue_length + 1  # Check if the queue has a new result