"""This module tests the functionality of various server-side retrival components.

test_set_recs(client): test if the server-side loading of user recommendations is functional.
test_result_by_id(client): test if the server-side retrieval of a result by its ID is functional.
test_get_recs(client): test if the server-side retrieval of user recommendations is functional.
test_headers(client): test if the server-side header retrieval component is functional.
test_validate(client): test if the server-side validation component is functional.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json
from unittest.mock import patch

from fairreckitlib.recommender_system import RecommenderSystem

from project.models import result_store, queue
from tests.common import check_bad_request
from tests.constants import MOCK_RESULTS_DIR

URL_PREFIX = '/api/result'


# Test setting of current shown recommendations POST route
@patch('project.models.result_storage.RESULTS_DIR', MOCK_RESULTS_DIR)
@patch('project.models.result_storage.RESULTS_OVERVIEW_PATH',
       MOCK_RESULTS_DIR +
       'results_overview.json')
@patch('project.models.result_loader.RESULTS_DIR', MOCK_RESULTS_DIR)
def test_set_recs(client):
    """Test if the server-side loading of user recommendations is functional.

    Args:
        client: The client component used to send requests to the server
    """
    url = URL_PREFIX + '/set-recs'
    settings = {'id': 0, 'runid': 0, 'pairid': 0}
    check_bad_request(client, url)
    response = client.post(url, json=settings)
    # Check succes response
    assert json.loads(response.data)['status'] == 'success'
    # Check that something has been stored in current current_recs at the given runid
    assert result_store.current_recs[0]


@patch('project.models.result_storage.RESULTS_DIR', MOCK_RESULTS_DIR)
@patch('project.models.result_storage.RESULTS_OVERVIEW_PATH',
       MOCK_RESULTS_DIR +
       'results_overview.json')
@patch('project.models.result_loader.RESULTS_DIR', MOCK_RESULTS_DIR)
def test_result_by_id(client):
    """Test if the server-side retrieval of a result by its ID is functional.

    Args:
        client: The client component used to send requests to the server
    """
    url = URL_PREFIX + '/result-by-id'
    # Check the post response
    assert check_bad_request(client, url)

    settings = {'id': 0}
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
    url = URL_PREFIX + '/'

    assert check_bad_request(client, url)

    amount = 10
    settings = {
        'pairid': 0,
        'runid': 0,
        'amount': amount
    }
    response = client.post(url, json=settings)
    result = json.loads(response.data)

    # Check that the post is loaded in correctly
    assert result
    # Check that the amount of loaded entries is correct
    assert len(result) == amount

    # Check that ascending/descending influences the order of entries
    settings = {
        'pairid': 0,
        'runid': 0,
        'amount': amount,
        'ascending': True,
        'dataset': 'LFM-2B-Sample'
    }
    response = client.post(url, json=settings)
    result2 = json.loads(response.data)
    assert result[0] != result2[0]

    # Check that optional columns are added
    settings = {
        'pairid': 0,
        'runid': 0,
        'amount': amount,
        'dataset': 'LFM-2B-Sample',
        'matrix': 'user-track-count',
        'optionalHeaders': ['user_age']
    }
    response = client.post(url, json=settings)
    result3 = json.loads(response.data)
    assert len(result[0]) < len(result3[0])


def test_headers(client):
    """Test if the server-side header retrieval component is functional.

    Args:
        client: The client component used to send requests to the server
    """
    url = URL_PREFIX + '/headers'

    assert check_bad_request(client, url)

    # Check that an invalid name does not return anything
    response = client.post(url, json={'dataset': 'foo', 'matrix': 'bar'})
    result1 = json.loads(response.data)
    assert result1 == {}

    # Check that a valid name does return something
    response = client.post(url, json={'dataset': 'ML-100K', 'matrix': 'user-movie-rating'})
    result2 = json.loads(response.data)

    assert result2


@patch('project.models.recommender_system', RecommenderSystem('datasets', MOCK_RESULTS_DIR))
def test_validate(client):
    """Test if the server-side validation component is functional.

    Args:
        client: The client component used to send requests to the server
    """
    queue.recommender_system = RecommenderSystem('datasets', MOCK_RESULTS_DIR)
    url = URL_PREFIX + '/validate'
    assert check_bad_request(client, url)
    response = client.post(url, json={'filepath': '1654518468_Test938_perturbance', \
        'amount': 0, 'ID': 0})
    assert response.data == b'Validated'
