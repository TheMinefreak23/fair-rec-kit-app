# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from unittest.mock import patch

from project.result_storage import *
from tests.test_result_storage import test_experiment, test_id, save_mock_result, delete_test_results, \
    test_results_path

url_prefix = '/api/all-results'


# Test getting the results overview GET route
def test_results(client):
    save_mock_result()
    url = url_prefix + '/'
    response = client.get(url)
    assert len(response.json) == 1

    delete_test_results()


# Test getting a result by id POST and GET routes
def test_result_by_id(client):
    save_mock_result()
    url = url_prefix + '/result-by-id'
    response = client.post(url,
                           json={'id': test_id})  # Check if the result we just saved can be retrieved
    assert response.status_code == 200  # Assert success
    print(response.data)
    assert b'success' in response.data  # Result found
    get_response = client.get(url)  # Check if the result we just saved can be retrieved
    assert get_response.json.get('result', test_experiment)

    delete_test_results()


# Test editing a result POST route
@patch('project.result_storage.RESULTS_OVERVIEW_PATH', test_results_path)
def test_edit(client):
    save_mock_result()
    index = 0
    # New metadata (that we expect)
    metadata = {'name': 'foo', 'tags': 'bar', 'email': 'foo@bar.com'}
    # Use the metadata to create the edit settings
    edit_settings = \
        {'index': index, 'new_name': metadata['name'],
         'new_tags': metadata['tags'], 'new_email': metadata['email']}
    # POST edit request
    response = client.post(url_prefix + '/edit', json=edit_settings)
    edited_results = load_results_overview()

    # Check success response
    assert b'Edited index' in response.data

    # Check if the edited result in the stored results is as expected
    assert edited_results['all_results'][index]['metadata'] == metadata


# TODO: delete test



