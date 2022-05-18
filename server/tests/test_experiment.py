# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import json
import time
from unittest.mock import patch

from project.experiment import *
from tests.test_result_storage import test_results_path, test_experiment, delete_test_results

url_prefix = '/api/experiment'
test_options = json.load(open('tests/options.json'))
TEST_RESULTS_PATH = 'test/test_results'


def get_test_options():
    test_options['timestamp']['stamp'] = str(time.time())
    print(test_options)
    return test_options


# Delete all results by emptying the file
#def delete_test_results():
#    os.rmdir(TEST_RESULTS_PATH)


# Test if experiment route works on mock JSON form data
@patch('project.experiment.RESULTS_DIR', TEST_RESULTS_PATH)
def test_form(client):
    from project.experiment import experiment_queue
    old_queue_length = len(experiment_queue)
    response = client.post(url_prefix + '/calculation', json=get_test_options())
    assert response.status_code == 200  # Assert success
    from project.experiment import experiment_queue
    assert len(experiment_queue) == old_queue_length + 1  # Check if the queue has a new result

    # Start the queue
    #queue_response = client.get(url_prefix + '/queue')
    time.sleep(0.1)

    # Check the result
    get_response = client.get(url_prefix + '/calculation')
    from project.result_storage import current_result
    assert json.loads(get_response.data)['calculation'] == current_result
    assert get_response.status_code == 200

    #delete_test_results()


@patch('project.experiment.RESULTS_DIR', TEST_RESULTS_PATH)
def test_calculate():
    from project.experiment import experiment_queue
    experiment_queue.append(get_test_options())
    old_queue_length = len(experiment_queue)

    from project.experiment import experiment_queue
    calculate_first()
    assert len(experiment_queue) == old_queue_length - 1

    #delete_test_results()


@patch('project.result_storage.RESULTS_OVERVIEW_PATH', test_results_path)
def test_experiment():
    print(get_test_options())
    run_experiment(get_test_options())
    from project.result_storage import current_result
    assert current_result['metadata']['name'] == test_options['metadata']['name']
    #delete_test_results()


def test_params(client):
    response = client.get(url_prefix + '/options')
    assert response.status_code == 200
    assert json.loads(response.data)['options'] == options


def test_calculate_route_post(client):
    # Test POST
    post_response = client.post(url_prefix + '/calculation', json=test_experiment)
    assert post_response.status_code == 200
    assert json.loads(post_response.data) == experiment_queue


def test_calculate_route_get(client):
    # Test GET
    get_response = client.get(url_prefix + '/calculation')
    assert get_response.status_code == 200
    from project.result_storage import current_result
    assert json.loads(get_response.data)['calculation'] == current_result


def test_queue(client):
    thread_alive = not experiment_thread.is_alive()

    get_response = client.get(url_prefix + '/queue',)
    assert get_response.status_code == 200
    assert json.loads(get_response.data) == experiment_queue

    # Assert that the thread has started running if the queue wasn't empty
    if not thread_alive and experiment_queue:
        assert experiment_thread.is_alive()


def test_delete(client):
    index = 0

    # Copy the test experiment but change the name
    test_experiment2 = test_experiment
    test_experiment2['metadata']['name'] = 'bar'

    # Add the test experiments to the queue
    from project.experiment import experiment_queue
    experiment_queue.append(test_experiment)
    experiment_queue.append(test_experiment2)

    old_queue_length = len(experiment_queue)

    response = client.post(url_prefix + '/queue/delete', json={'index': index})
    from project.experiment import experiment_queue
    neighbour = experiment_queue[index+1]

    # Test that the correct experiment has been deleted
    assert experiment_queue[index] == neighbour

    assert b'Removed index' in response.data
    assert len(experiment_queue) == old_queue_length -1


def test_append():
    metadata = test_experiment['metadata']
    settings = 'test'

    append_queue(metadata, settings)

    queue_item = experiment_queue.pop()
    assert queue_item['metadata'] == metadata
    assert queue_item['settings'] == settings
    assert float(queue_item['timestamp']['stamp']) > time.time() - 1000*3600

    # test no name
    metadata.pop('name', None)
    append_queue(metadata, settings)
    # No error



