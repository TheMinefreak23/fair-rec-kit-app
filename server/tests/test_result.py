"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from unittest.mock import patch
from project.result_storage import *
from project.experiment import RecommenderSystem
from tests.test_result_storage import test_experiment, test_id, save_mock_result, delete_test_results, \
    test_results_path
from tests.test_result_loader import MOCK_RESULTS_DIR

url_prefix = '/api/result'

# Test setting of current shown recommendations POST route
@patch('project.result_storage.RESULTS_OVERVIEW_PATH', MOCK_RESULTS_DIR + 'results_overview.json')
@patch("project.result_storage.RESULTS_ROOT_FOLDER", MOCK_RESULTS_DIR)
@patch('project.result_loader.RESULTS_ROOT_FOLDER', MOCK_RESULTS_DIR)
def test_set_recs(client):
    """Test if the server-side loading of user recommendations is functional.
    
    Args:
        client: The client component used to send requests to the server
    """
    url = url_prefix + '/set-recs'
    settings = {'id' : 0, 'runid' : 0, 'pairid' : 0}
    response = client.post(url, json=settings)
    # Check succes response
    assert json.loads(response.data)['status'] == 'success'
    # Check that something has been stored in current current_recs at the given runid
    assert current_recs[0]

# TODO refactor
@patch('project.result_storage.RESULTS_OVERVIEW_PATH', MOCK_RESULTS_DIR + 'results_overview.json')
@patch('project.result_storage.RESULTS_ROOT_FOLDER', MOCK_RESULTS_DIR)
@patch('project.result_loader.RESULTS_ROOT_FOLDER', MOCK_RESULTS_DIR)
def test_result_by_id(client):
    """Test if the server-side retrieval of a result by its ID is functional.
    
    Args:
        client: The client component used to send requests to the server
    """
    url = url_prefix + '/result-by-id'
    #Check the post response
    settings = {'id' : 0}
    response1 = client.post(url, json=settings)
    assert json.loads(response1.data)['status'] == 'success'
    
    # Check the get response
    response2 = client.get(url)
    assert json.loads(response2.data)

def test_get_recs(client):
    """Test if the server-side retrieval of user recommendations is functional.
    
    Args:
        client: The client component used to send requests to the server
    """
    url = url_prefix + '/'
    amount = 10
    settings = {
        'pairid' : 0,
        'runid' : 0,
        'amount' : amount
        }
    response = client.post(url, json=settings)
    result = json.loads(response.data)

    # Check that the post is loaded in correctly
    assert result
    # Check that the amount of loaded entries is correct
    assert len(result) == amount

    # Check that ascending/descending influences the order of entries
    settings = {
        'pairid' : 0,
        'runid' : 0,
        'amount' : amount,
        'ascending' : True,
        'dataset': 'LFM-2B'
        }
    response = client.post(url, json=settings)
    result2 = json.loads(response.data)    
    assert result[0] != result2[0]

    # Check that spotify columns are added
    settings = {
        'pairid' : 0,
        'runid' : 0,
        'amount' : amount,
        'dataset': 'LFM-2B'
        }
    response = client.post(url, json=settings)
    result3 = json.loads(response.data)    
    assert len(result[0]) < len(result3[0])

def test_headers(client):
    """Test if the server-side header retrieval component is functional.
    
    Args:
        client: The client component used to send requests to the server
    """
    url = url_prefix + '/headers'
    response = client.post(url, json={'name' : 'foo'})
    result1 = json.loads(response.data)
    # Check that an invalid name does not return anything
    assert result1 == {}
    response = client.post(url, json={'name' : 'ML-100K'})
    result2 = json.loads(response.data)
    # Check that a valid name does return something 
    assert result2

@patch("project.experiment.recommender_system", RecommenderSystem('datasets', MOCK_RESULTS_DIR))
def test_validate(client):
    """Test if the server-side validation component is functional.

    Args:
        client: The client component used to send requests to the server
    """
    url = url_prefix + '/validate'
    response = client.post(url, json={'filepath' : '1654518468_Test938_perturbance', 'amount' : 0})
    assert b'Validated' == response.data
