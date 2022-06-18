"""This module tests the functionality of various server-side functions that manipulate the previous results.

test_results(client): test if the server-side result loading component is functional.
test_edit(client): test if the server-side result editing component is functional.
test_delete(client): test if the server-side result deletion component is functional.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json
import os
from unittest.mock import patch

from project.models.result_storage import load_results_overview
from tests.test_result_storage import save_mock_result, delete_test_results, \
    TEST_RESULTS_PATH, TEST_RESULTS_ROOT, TEST_ID

URL_PREFIX = '/api/all-results'


# Test getting the results overview GET route
@patch('project.models.result_storage.RESULTS_OVERVIEW_PATH', TEST_RESULTS_PATH)
@patch('project.models.result_storage.RESULTS_DIR', TEST_RESULTS_ROOT)
def test_results(client):
    """Test if the server-side result loading component is functional.

    Args:
        client: The client component used to send requests to the server
    """
    save_mock_result()
    url = URL_PREFIX + '/'
    response = client.get(url)
    # Check if a result has been loaded
    assert len(json.loads(response.data)) == 1

    delete_test_results()

# Test editing a result POST route
@patch('project.models.result_storage.RESULTS_OVERVIEW_PATH', TEST_RESULTS_PATH)
@patch('project.models.result_storage.RESULTS_DIR', TEST_RESULTS_ROOT)
def test_edit(client):
    """Test if the server-side result editing component is functional.

    Args:
        client: The client component used to send requests to the server
    """
    save_mock_result()
    # New metadata (that we expect)
    metadata = {'name': 'bar', 'tags': 'bar', 'email': 'foo@bar.com'}
    # Use the metadata to create the edit settings
    edit_settings = \
        {'id': TEST_ID, 'new_name': metadata['name'],
         'new_tags': metadata['tags'], 'new_email': metadata['email']}
    # POST edit request
    response = client.post(URL_PREFIX + '/edit', json=edit_settings)
    edited_results = load_results_overview()

    # Check success response
    assert response.data == b'Edited index'

    # Check if the edited result in the stored results is as expected
    assert edited_results['all_results'][0]['metadata'] == metadata

    delete_test_results()

    # Delete new test result directory
    os.removedirs(TEST_RESULTS_ROOT + '-1_bar')


@patch('project.models.result_storage.RESULTS_OVERVIEW_PATH', TEST_RESULTS_PATH)
def test_delete(client):
    """Test if the server-side result deletion component is functional.

    Args:
        client: The client component used to send requests to the server
    """
    initial_results = load_results_overview()
    save_mock_result()
    index = 0
    #Create the settings required to remove an entry
    delete_settings = { 'name': 'foo', 'id': index}
    response = client.post(URL_PREFIX + '/delete', json=delete_settings)
    edited_results = load_results_overview()

     # Check success response
    assert response.data == b'Removed index'

     # Check if the removed result is no longer in the results overview
    assert len(edited_results) == len(initial_results)
