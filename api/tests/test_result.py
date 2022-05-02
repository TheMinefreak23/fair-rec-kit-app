"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from tests.test_result_storage import test_id

url_prefix = '/api/result'

# Test setting of current shown recommendations POST route
# TODO this is kind of a stub because of the randomness
def test_set_recs(client):
    response = client.post(url_prefix + '/set-recs', json={'id': test_id})

    # current_recs = TODO check result

    assert b'success' in response.data