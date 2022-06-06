# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import json
import time
from unittest.mock import patch

import polling as polling
import requests

from project import result_storage
from project.experiment import *
from tests.test_result_storage import test_results_path, test_experiment, delete_test_results

# TODO add more edge cases

url_prefix = '/api/experiment'
test_options = json.load(open('tests/options.json'))
TEST_RESULTS_PATH = 'test_results' # TODO patch doesn't work


def get_test_options():
    name = test_options['metadata']['name']
    experiment = QueueItem(test_options, {}, Status.TODO, ProgressStatus.NA, name)
    experiment.job['timestamp']['stamp'] = str(time.time())
    print(experiment)
    return experiment


# Delete all results by deleting the test result directory
def delete_test_results(results_dir):
    os.rmdir(results_dir)


# TODO
def test_queue_format():
    # Empty queue gives empty formatted queue
    queue_result = formatted_queue()
    assert queue_result == []


# Test if experiment route works on mock JSON form data
#@patch('project.experiment.RESULTS_DIR', TEST_RESULTS_PATH)
def test_form(client):
    from project.experiment import RESULTS_DIR
    print('RESULTS DIR', RESULTS_DIR)
    from project.experiment import experiment_queue
    old_queue_length = len(experiment_queue)
    post_response = client.post(url_prefix + '/calculation', json=test_options)

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

    #delete_test_results(RESULTS_DIR)

# TODO this test is kind of redundant, use fixtures?
"""
@patch('project.experiment.RESULTS_DIR', TEST_RESULTS_PATH)
def test_calculate():
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


def test_params(client):
    response = client.get(url_prefix + '/options')
    assert response.status_code == 200
    assert json.loads(response.data)['options'] == options


def test_calculate_route_post(client):
    # Test POST
    post_response = client.post(url_prefix + '/calculation', json=test_options)
    assert post_response.status_code == 200
    assert json.loads(post_response.data)['queue'] == formatted_queue()


def test_calculate_route_get(client):
    # Test GET
    get_response = client.get(url_prefix + '/calculation')
    assert get_response.status_code == 200

    data = json.loads(get_response.data)
    assert 'status' in data
    # TODO Status is not available if there is no experiment
    #assert data['status'] == Status.NA.value


def test_queue(client):
    get_response = client.get(url_prefix + '/queue', )
    # TODO fixture?
    assert get_response.status_code == 200
    assert json.loads(get_response.data)['queue'] == formatted_queue()

# TODO
"""
def test_cancel(client):
"""


def test_append():
    metadata = test_options['metadata']
    settings = test_options['settings']

    append_queue(metadata, settings)

    queue_item = experiment_queue.pop()
    assert queue_item.job['metadata'] == metadata
    assert queue_item.job['settings'] == settings
    assert float(queue_item.job['timestamp']['stamp']) > time.time() - 1000 * 3600


def mock_experiment():
    """Mock running an experiment and save the mock result."""
    # Mock experiment duration.
    time.sleep(2.5)
    result_storage.save_result(current_experiment.job, result_storage.format_result(current_experiment.config))


def mock_recommend(dataset, approach):
    """Mock recommendation.

    Args:
        dataset(dict): a dataset with a name
        approach(dict): an approach with a name

    Returns:
        (string) a magic result
    """
    # Combine the names, flipping the approach name.
    return dataset['name'] + approach['name'][::-1]


def mock_evaluate_all(approach, metric):
    """
    Do a mock evaluation for all filters.

    Args:
        approach: the approach with a name
        metric: the metric
    Returns:
        the evaluation dictionary containing all evaluations
    """
    base_eval = mock_evaluate(approach, metric)
    evaluation = {'global': round(base_eval, 2), 'filtered': []}

    for metric_filter in metric['filters']:
        # Evaluate per filter.
        evals = []
        for (name, value) in metric_filter['params'].items():
            # Just use the value if it's a number, otherwise use the length of the word.
            filter_eval = value if isinstance(value, int) else len(value)
            val = round((base_eval * len(metric_filter['name']) / filter_eval), 2)
            evals.append({name + ' ' + str(value): val})
        evaluation['filtered'].append({metric_filter['name']: evals})

    return evaluation


def mock_evaluate(approach, metric):
    """
    Mock evaluation: Give a magic number using an approach and metric.

    Args:
        approach: an approach with a name
        metric: a metric with a name and value
    Returns:
        the magic mock evaluation
    """
    # Mock evaluation

    result = len(approach['name']) * len(metric['name'])
    # print('metric:', metric)
    # Do something with the metrics parameters.
    if metric['params']:
        # print(metric['name'], 'has params', metric['params'])
        for (name, value) in metric['params'].items():
            val = int(value) if value else 0
            result *= len(name) * val

    return result / 100

