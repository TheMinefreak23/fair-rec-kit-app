# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from unittest.mock import patch

from project.result_storage import *
from tests.test_result_storage import save_mock_result, delete_test_results, \
    test_results_path

url_prefix = '/api/all-results'


# Test getting the results overview GET route
@patch('project.result_storage.RESULTS_OVERVIEW_PATH', test_results_path)
def test_results(client):
    """Test if the server-side result loading component is functional
    
    Args:
        client: The client component used to send requests to the server
    """
    save_mock_result()
    url = url_prefix + '/'
    response = client.get(url)
    # Check if a result has been loaded
    assert len(json.loads(response.data)) == 1

    delete_test_results()

# Test editing a result POST route
@patch('project.result_storage.RESULTS_OVERVIEW_PATH', test_results_path)
def test_edit(client):
    """Test if the server-side result editing component is functional
    
    Args:
        client: The client component used to send requests to the server
    """
    save_mock_result()
    index = -1
    # New metadata (that we expect)
    metadata = {'name': 'bar', 'tags': 'bar', 'email': 'foo@bar.com'}
    # Use the metadata to create the edit settings
    edit_settings = \
        {'id': index, 'new_name': metadata['name'],
         'new_tags': metadata['tags'], 'new_email': metadata['email']}
    # POST edit request
    response = client.post(url_prefix + '/edit', json=edit_settings)
    edited_results = load_results_overview()

    # Check success response
    assert b'Edited index' == response.data

    # Check if the edited result in the stored results is as expected
    assert edited_results['all_results'][0]['metadata'] == metadata


@patch('project.result_storage.RESULTS_OVERVIEW_PATH', test_results_path)
def test_delete(client):
    """Test if the server-side result deletion component is functional
    
    Args:
        client: The client component used to send requests to the server
    """
    initial_results = load_results_overview()
    save_mock_result()
    index = 0
    #Create the settings required to remove an entry
    delete_settings = { 'name': 'foo', 'id': index}
    response = client.post(url_prefix + '/delete', json=delete_settings)
    edited_results = load_results_overview()

     # Check success response
    assert b'Removed index' == response.data

     # Check if the removed result is no longer in the results overview
    assert len(edited_results) == len(initial_results)
