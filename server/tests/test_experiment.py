"""
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

from tests.constants import MOCK_RESULTS_DIR
# MOCK_RESULTS_PATH = 'mock/'

# TODO add more edge cases

URL_PREFIX = '/api/experiment'

with open('tests/options.json', encoding='utf-8') as test_options_file:
    mock_options = json.load(test_options_file)

TEST_RESULTS_PATH = 'test_results'
# recommender_system = RecommenderSystem('datasets', MOCK_RESULTS_DIR)


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


#@patch('project.models.queue.queue', [])
def test_queue_format():
    """Test whether the queue gets formatted correctly."""
    # Empty queue gives empty formatted queue
    queue.queue = []
    queue_result = queue.formatted_queue()
    assert queue_result == []

    # TODO


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


#@patch('project.experiment.RESULTS_DIR', TEST_RESULTS_PATH)
#def test_run_first():
    #"""Test the handling of the first queue experiment item"""

    #queue.queue.append(get_mock_options())
    #old_queue_length = len(queue.queue)

    # TODO
    #run_first()
    #assert len(queue.queue) == old_queue_length - 1

    #delete_test_results()


# TODO this test is kind of redundant, use fixtures?
#@patch('project.result_storage.RESULTS_OVERVIEW_PATH', test_results_path)
#def test_run_experiment():
#    print(get_test_options())
#    run_experiment(get_test_options())
#    from project.result_storage import current_result
#    assert current_result['metadata']['name'] == test_options['metadata']['name']
#    delete_test_results()


#@patch
#def test_validate():


def test_params(client):
    """Test params route."""
    response = client.get(URL_PREFIX + '/options')
    assert response.status_code == 200
    assert json.loads(response.data)['options'] == options_formatter.options


def test_experiment_route_post(client):
    """Test POST request on experiment route."""
    post_response = client.post(URL_PREFIX + '/', json=mock_options)
    assert post_response.status_code == 200
    assert json.loads(post_response.data)['queue'] == queue.formatted_queue()


def test_experiment_route_get(client):
    """Test GET request on experiment route."""
    get_response = client.get(URL_PREFIX + '/')
    assert get_response.status_code == 200

    data = json.loads(get_response.data)
    assert 'status' in data
    # TODO Status is not available if there is no experiment
    #assert data['status'] == Status.NA.value

#TODO
#@patch('project.experiment.RESULTS_DIR', TEST_RESULTS_PATH)
#@patch('project.models.recommender_system', RecommenderSystem('datasets', TEST_RESULTS_PATH))
#def test_form(client):
    #"""Test if experiment route works on mock JSON form data."""

    #old_queue_length = len(queue.queue)
    #post_response = client.post(URL_PREFIX + '/', json=mock_options)

    #assert post_response.status_code == 200  # Assert success

    #data = json.loads(post_response.data)
    #assert data['queue'] == queue.formatted_queue()
    # Check that the queue has a new item or no new item (item handled immediately)
    #assert len(queue.queue) == old_queue_length + 1 \
    #       or len(queue.queue) == old_queue_length

    # Start the queue
    # queue_response = client.get(url_prefix + '/queue')
    # time.sleep(0.1)

    #def finished():
    #    get_response = client.get(URL_PREFIX + '/calculation')
    #    status = json.loads(get_response.data)['status']
        # The experiment is queued, so it should be either on to do, active or done
    #    assert status in [Status.TODO.value, Status.ACTIVE.value, Status.DONE.value]
    #    return status == Status.DONE.value

    # Poll for a result
    #polling.poll(
    #    finished,
    #    step=5,
    #    poll_forever=True
    #)

    # Check the result
    # TODO refactor
    #get_response = client.get(url_prefix + '/calculation')

    #data = json.loads(get_response.data)
    #assert data['calculation'] == current_result
    #assert get_response.status_code == 200

    #delete_test_results()


def test_queue(client):
    """Test GET request on queue route."""
    get_response = client.get(URL_PREFIX + '/queue', )
    # TODO fixture?
    assert get_response.status_code == 200
    assert json.loads(get_response.data)['queue'] == queue.formatted_queue()


#@patch('project.experiment.experiment_queue', [])
def test_abort(client):
    """Test whether an experiment gets appended to the queue correctly."""
    queue.queue = []

    url = URL_PREFIX + '/queue/abort'
    experiment = get_mock_options()
    experiment_id = experiment.queue_item.job['timestamp']['stamp']

    # Test empty queue (item not present) TODO assume item present?
    # client.post(url, json={'id': experiment_id})

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
    # TODO refactor? global not working
    with open('tests/options.json', encoding='utf-8') as file:
        mock = json.load(file)
    metadata = mock['metadata']
    settings = mock['settings']

    queue.append_queue(metadata, settings)

    queue_item = queue.queue.pop().queue_item
    assert queue_item.job['metadata'] == metadata
    assert queue_item.job['settings'] == settings
    assert float(queue_item.job['timestamp']['stamp']) > time.time() - 1

    # TODO refactor
    assert queue_item.status == Status.TODO
    assert queue_item.progress == ProgressStatus.NA

    # Test empty input dicts TODO assumption not empty (keyerror)
    #append_queue({}, {})
    #append_queue({}, {'lists': {'datasets': [], 'approaches': [], 'metrics': []}})

    # Test empty metadata
    # TODO refactor? global not working
    with open('tests/options.json', encoding='utf-8') as file:
        mock = json.load(file)
    queue.append_queue({}, mock['settings'])
    queue_item = queue.queue.pop().queue_item
    assert queue_item.job['metadata'] == { 'name': 'Untitled' }


#@patch('project.experiment.RESULTS_DIR', MOCK_RESULTS_PATH)
#@patch('project.experiment.recommender_system', RecommenderSystem('datasets', MOCK_RESULTS_PATH))
@patch('project.models.recommender_system', RecommenderSystem('datasets', MOCK_RESULTS_DIR))
def test_add_validation():
    """Test whether a valudation experiment gets appended to the queue correctly."""

    # TODO Test invalid file path?
    # add_validation('',)

    test_path = '1654518468_Test938_perturbance'
    test_amount = 0
    queue.add_validation(test_path, test_amount)
    queue_item = queue.queue.pop().queue_item
    assert queue_item.job['file_path'] == test_path
    assert queue_item.job['amount'] == test_amount
    assert queue_item.name == ''
    assert queue_item.validating

    # TODO refactor
    assert queue_item.status == Status.TODO
    assert queue_item.progress == ProgressStatus.NA
