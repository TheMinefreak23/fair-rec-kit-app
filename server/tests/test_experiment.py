"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json
from unittest.mock import patch

import polling as polling
import requests

from project.experiment import *
from tests.test_result_storage import test_results_path, test_experiment, delete_test_results
MOCK_RESULTS_PATH = 'mock/'

# TODO add more edge cases

url_prefix = '/api/experiment'
mock_options = json.load(open('tests/options.json'))
TEST_RESULTS_PATH = 'test_results' # TODO patch doesn't work


def get_mock_options():
    """Generate experiment from test options JSON.

    Returns:
         (QueueItem) experiment

    """
    name = mock_options['metadata']['name']
    mock_options['timestamp'] = {'stamp': str(time.time())}
    experiment = QueueItem(mock_options, {}, Status.TODO, ProgressStatus.NA, name)
    # Make new timestamp
    print(experiment)
    return experiment


def delete_test_results():
    """Delete all results by deleting the test result directory."""
    os.rmdir(TEST_RESULTS_PATH)


@patch('project.experiment.experiment_queue', [])
def test_queue_format():
    """Test whether the queue gets formatted correctly."""
    # Empty queue gives empty formatted queue
    queue_result = formatted_queue()
    assert queue_result == []

    # TODO


def test_experiment_format():
    """Test whether an experiment gets formatted correctly."""
    # NoneType experiment gives empty dictionary
    experiment_result = formatted_experiment(None)
    assert experiment_result == {}

    # Mock experiment
    experiment = get_mock_options()
    experiment_result = formatted_experiment(experiment)
    assert experiment_result['status'] == experiment.status.value
    assert experiment_result['progress'] == experiment.progress.value


"""Test the handling of the first queue experiment item"""
"""    
@patch('project.experiment.RESULTS_DIR', TEST_RESULTS_PATH)
def test_run_first():
    from project.experiment import experiment_queue
    experiment_queue.append(get_test_options())
    old_queue_length = len(experiment_queue)

    from project.experiment import experiment_queue
    calculate_first()
    assert len(experiment_queue) == old_queue_length - 1

    delete_test_results()
"""

# TODO this test is kind of redundant, use fixtures?
"""
@patch('project.result_storage.RESULTS_OVERVIEW_PATH', test_results_path)
def test_run_experiment():
    print(get_test_options())
    run_experiment(get_test_options())
    from project.result_storage import current_result
    assert current_result['metadata']['name'] == test_options['metadata']['name']
    delete_test_results()
"""

"""
@patch
def test_validate():
"""


def test_params(client):
    """Test params route."""
    response = client.get(url_prefix + '/options')
    assert response.status_code == 200
    assert json.loads(response.data)['options'] == options


def test_experiment_route_post(client):
    """Test POST request on experiment route."""
    post_response = client.post(url_prefix + '/', json=mock_options)
    assert post_response.status_code == 200
    assert json.loads(post_response.data)['queue'] == formatted_queue()


def test_experiment_route_get(client):
    """Test GET request on experiment route."""
    get_response = client.get(url_prefix + '/')
    assert get_response.status_code == 200

    data = json.loads(get_response.data)
    assert 'status' in data
    # TODO Status is not available if there is no experiment
    #assert data['status'] == Status.NA.value


#@patch('project.experiment.RESULTS_DIR', TEST_RESULTS_PATH)
#@patch('project.experiment.recommender_system', RecommenderSystem('datasets', TEST_RESULTS_PATH))
#def test_form(client):
    """Test if experiment route works on mock JSON form data."""
    """
    from project.experiment import experiment_queue
    old_queue_length = len(experiment_queue)
    post_response = client.post(url_prefix + '/', json=mock_options)

    assert post_response.status_code == 200  # Assert success

    from project.experiment import experiment_queue
    data = json.loads(post_response.data)
    assert data['queue'] == formatted_queue()
    # Check that the queue has a new item or no new item (item handled immediately)
    assert len(experiment_queue) == old_queue_length + 1 or len(experiment_queue) == old_queue_length

    # Start the queue
    # queue_response = client.get(url_prefix + '/queue')
    # time.sleep(0.1)

    def finished():
        get_response = client.get(url_prefix + '/calculation')
        status = json.loads(get_response.data)['status']
        # The experiment is queued, so it should be either on to do, active or done
        assert status in [Status.TODO.value, Status.ACTIVE.value, Status.DONE.value]
        return status == Status.DONE.value

    # Poll for a result
    polling.poll(
        finished,
        step=5,
        poll_forever=True
    )

    # Check the result
    # TODO refactor
    get_response = client.get(url_prefix + '/calculation')
    from project.result_storage import current_result
    data = json.loads(get_response.data)
    assert data['calculation'] == current_result
    assert get_response.status_code == 200

    delete_test_results()
    """


def test_queue(client):
    """Test GET request on queue route."""
    get_response = client.get(url_prefix + '/queue', )
    # TODO fixture?
    assert get_response.status_code == 200
    assert json.loads(get_response.data)['queue'] == formatted_queue()


@patch('project.experiment.experiment_queue', [])
def test_abort(client):
    """Test whether an experiment gets appended to the queue correctly."""
    url = url_prefix + '/queue/abort'
    experiment = get_mock_options()
    experiment_id = experiment.job['timestamp']['stamp']

    # Test empty queue (item not present) TODO assume item present?
    # client.post(url, json={'id': experiment_id})

    # Test different status experiments
    experiment.status = Status.TODO
    from project.experiment import experiment_queue
    experiment_queue.append(experiment)
    client.post(url, json={'id': experiment_id})
    experiment_queue.pop() # Empty queue
    assert experiment.status == Status.CANCELLED

    experiment.status = Status.ACTIVE
    from project.experiment import experiment_queue
    experiment_queue.append(experiment)
    client.post(url, json={'id': experiment_id})
    experiment_queue.pop() # Empty queue
    assert experiment.status == Status.ABORTED


def test_append():
    """Test whether an experiment gets appended to the queue correctly."""

    # Use mock options from JSON
    # TODO refactor? global not working
    mock = json.load(open('tests/options.json'))
    metadata = mock['metadata']
    settings = mock['settings']

    append_queue(metadata, settings)

    queue_item = experiment_queue.pop()
    assert queue_item.job['metadata'] == metadata
    assert queue_item.job['settings'] == settings
    assert float(queue_item.job['timestamp']['stamp']) > time.time() - 1000 * 3600

    # TODO refactor
    assert queue_item.status == Status.TODO
    assert queue_item.progress == ProgressStatus.NA

    # Test empty input dicts TODO assumption not empty (keyerror)
    #append_queue({}, {})
    #append_queue({}, {'lists': {'datasets': [], 'approaches': [], 'metrics': []}})

    # Test empty metadata
    # TODO refactor? global not working
    mock = json.load(open('tests/options.json'))
    append_queue({}, mock['settings'])
    queue_item = experiment_queue.pop()
    assert queue_item.job['metadata'] == { 'name': 'Untitled' }


#@patch('project.experiment.RESULTS_DIR', MOCK_RESULTS_PATH)
@patch('project.experiment.recommender_system', RecommenderSystem('datasets', MOCK_RESULTS_PATH))
def test_add_validation():
    """Test whether a valudation experiment gets appended to the queue correctly."""

    # TODO Test invalid file path?
    # add_validation('',)

    test_path = '1654518468_Test938_perturbance'
    test_amount = 0
    add_validation(test_path, test_amount)
    queue_item = experiment_queue.pop()
    assert queue_item.job['file_path'] == test_path
    assert queue_item.job['amount'] == test_amount
    assert queue_item.name == ''
    assert queue_item.validating

    # TODO refactor
    assert queue_item.status == Status.TODO
    assert queue_item.progress == ProgressStatus.NA