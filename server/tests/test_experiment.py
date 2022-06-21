"""This module tests various functionality related to the experiments.

get_mock_options(): generate experiment from test options JSON.
delete_test_results(): delete all results by deleting the test result directory.
test_queue_format(): test whether the queue gets formatted correctly.
test_experiment_format(): test whether an experiment gets formatted correctly.
test_params(client): test params route.
test_experiment_route_post(client): test POST request on experiment route.
test_experiment_route_get(client): test GET request on experiment route.
test_queue(client): test GET request on queue route.
test_abort(client): test whether an experiment gets appended to the queue correctly.
test_append(): test whether an experiment gets appended to the queue correctly.
test_add_validation(): test whether a valudation experiment gets appended to the queue correctly.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json
import os
import time
from unittest.mock import patch

# import polling
from fairreckitlib.recommender_system import RecommenderSystem

from project.models.experiment import QueueItem, Status, ProgressStatus, Experiment
from project.models import queue, options_formatter
from project.models.experiment_queue import formatted_experiment
from tests.common import check_bad_request

from tests.constants import MOCK_RESULTS_DIR

URL_PREFIX = '/api/experiment'

with open('tests/options.json', encoding='utf-8') as test_options_file:
    mock_options = json.load(test_options_file)

TEST_RESULTS_PATH = 'test_results'


def get_mock_options():
    """Generate experiment from test options JSON.

    Returns:
         (QueueItem) experiment
    """
    name = mock_options['metadata']['name']
    mock_options['timestamp'] = {'stamp': str(time.time())}
    queue_item = QueueItem(mock_options, {}, Status.TODO, ProgressStatus.NA, name)
    experiment = Experiment(queue_item, RecommenderSystem('datasets', TEST_RESULTS_PATH))
    # Make new timestamp
    print(experiment)
    return experiment


def delete_test_results():
    """Delete all results by deleting the test result directory."""
    os.rmdir(TEST_RESULTS_PATH)


def test_queue_format():
    """Test whether the queue gets formatted correctly."""
    # Empty queue gives empty formatted queue
    queue.queue = []
    queue_result = queue.formatted_queue()
    assert queue_result == []



def test_experiment_format():
    """Test whether an experiment gets formatted correctly."""
    # NoneType experiment gives empty dictionary
    experiment_result = formatted_experiment(None)
    assert experiment_result == {}

    # Mock experiment
    experiment = get_mock_options()
    queue_item = experiment.queue_item
    experiment_result = formatted_experiment(experiment)
    assert experiment_result['status'] == queue_item.status.value
    assert experiment_result['progress'] == queue_item.progress.value



def test_params(client):
    """Test params route.

    Args:
        client: The client component used to send requests to the server
    """
    response = client.get(URL_PREFIX + '/options')
    assert response.status_code == 200
    assert json.loads(response.data)['options'] == options_formatter.options


def test_experiment_route_post(client):
    """Test POST request on experiment route.

    Args:
        client: The client component used to send requests to the server
    """
    url = URL_PREFIX + '/'

    assert check_bad_request(client, url)

    # Test mock
    post_response = client.post(url, json=mock_options)
    assert post_response.status_code == 200
    assert json.loads(post_response.data)['queue'] == queue.formatted_queue()


def test_experiment_route_get(client):
    """Test GET request on experiment route.

    Args:
        client: The client component used to send requests to the server
    """
    get_response = client.get(URL_PREFIX + '/')
    assert get_response.status_code == 200

    data = json.loads(get_response.data)
    assert 'status' in data

def test_queue(client):
    """Test GET request on queue route.

    Args:
        client: The client component used to send requests to the server
    """
    get_response = client.get(URL_PREFIX + '/queue', )
    assert get_response.status_code == 200
    assert json.loads(get_response.data)['queue'] == queue.formatted_queue()


def test_abort(client):
    """Test whether an experiment gets appended to the queue correctly.

    Args:
        client: The client component used to send requests to the server
    """
    queue.queue = []

    url = URL_PREFIX + '/queue/abort'
    experiment = get_mock_options()
    experiment_id = experiment.queue_item.job['timestamp']['stamp']

    # Test different status experiments
    experiment.queue_item.status = Status.TODO
    queue.queue.append(experiment)
    client.post(url, json={'id': experiment_id})
    queue.queue.pop() # Empty queue
    assert experiment.queue_item.status == Status.CANCELLED

    experiment.queue_item.status = Status.ACTIVE
    queue.queue.append(experiment)
    client.post(url, json={'id': experiment_id})
    queue.queue.pop() # Empty queue
    assert experiment.queue_item.status == Status.ABORTED


def test_append():
    """Test whether an experiment gets appended to the queue correctly."""
    # Use mock options from JSON
    with open('tests/options.json', encoding='utf-8') as file:
        mock = json.load(file)
    metadata = mock['metadata']
    settings = mock['settings']

    queue.append_queue(metadata, settings)

    queue_item = queue.queue.pop().queue_item
    assert queue_item.job['metadata'] == metadata
    assert queue_item.job['settings'] == settings
    assert float(queue_item.job['timestamp']['stamp']) > time.time() - 1

    assert queue_item.status == Status.TODO
    assert queue_item.progress == ProgressStatus.NA

    # Test empty metadata
    with open('tests/options.json', encoding='utf-8') as file:
        mock = json.load(file)
    queue.append_queue({}, mock['settings'])
    queue_item = queue.queue.pop().queue_item
    assert queue_item.job['metadata'] == { 'name': 'Untitled' }


@patch('project.models.recommender_system', RecommenderSystem('datasets', MOCK_RESULTS_DIR))
def test_add_validation():
    """Test whether a validation experiment gets appended to the queue correctly."""
    test_path = '1654518468_Test938_perturbance'
    test_amount = 0
    queue.add_validation(test_path, test_amount)
    queue_item = queue.queue.pop().queue_item
    assert queue_item.job['file_path'] == test_path
    assert queue_item.job['amount'] == test_amount
    assert queue_item.name == ''
    assert queue_item.validating

    assert queue_item.status == Status.TODO
    assert queue_item.progress == ProgressStatus.NA
