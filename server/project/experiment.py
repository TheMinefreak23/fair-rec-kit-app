"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import json
import os
import threading
import time
from datetime import datetime
import yaml
from fairreckitlib.experiment.experiment_config_parsing import Parser
from fairreckitlib.experiment.experiment_event import ON_END_EXPERIMENT, ON_END_THREAD_EXPERIMENT, ON_BEGIN_THREAD_EXPERIMENT, ON_BEGIN_EXPERIMENT

from fairreckitlib.recommender_system import RecommenderSystem

from flask import (Blueprint, request)

from . import result_storage
from .options_formatter import create_available_options, config_dict_from_settings

compute_bp = Blueprint('experiment', __name__, url_prefix='/api/experiment')

# Constants
CONFIG_DIR = 'config_files'
RESULTS_DIR = 'results'

# Initialise
recommender_system = RecommenderSystem('datasets', RESULTS_DIR)
options = create_available_options(recommender_system)
experiment_queue = []
# TODO refactor
experiment_running = False
current_experiment_name = ''


def calculate_first():
    """Take the oldest settings in the queue and perform an experiment with them"""
    # TODO We need this delay for the queue to work fsr
    #time.sleep(0.1)
    # Get the oldest experiment from the queue.
    experiment = experiment_queue.pop()

    run_experiment(experiment)
    #mock_experiment(experiment)


#experiment_thread = threading.Thread(target=calculate_first)


def run_experiment(experiment):
    """Run an experiment and save the result."""
    global experiment_running
    experiment_running = True

    print(experiment)

    # Create configuration dictionary.
    config_dict, config_id = config_dict_from_settings(experiment)
    global current_experiment_name
    current_experiment_name = config_id

    # Create config files directory if it doesn't exist yet.
    if not os.path.isdir(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)
        
    # Save configuration to yaml file.
    config_file_path = CONFIG_DIR + '/' + config_id

    with open(config_file_path + '.yml', 'w+', encoding='utf-8') as config_file:
        yaml.dump(config_dict, config_file)

    parser = Parser(True)
    config = parser.parse_experiment_config_from_yml(config_file_path,
                                                     recommender_system.data_registry,
                                                     recommender_system.experiment_factory)

    def on_end_experiment(event_listener, **kwargs):
        # TODO get real recs&eval result
        result_storage.save_result(experiment, mock_result(experiment['settings']))
        global experiment_running
        experiment_running = False
        print('yay')
        # Calculate next item in queue
        if experiment_queue:
            calculate_first()


    events = {
        ON_BEGIN_EXPERIMENT: lambda x, **kwargs: print('uwu'),
        ON_END_EXPERIMENT: lambda x, **kwargs: print('owo'),
        ON_BEGIN_THREAD_EXPERIMENT: lambda x, **kwargs: print('letsgooo'),
        ON_END_THREAD_EXPERIMENT: on_end_experiment
    }

    recommender_system.run_experiment(events, config, num_threads=4)

    # TODO USE THIS FUNCTION INSTEAD OF PARSING
    #recommender_system.run_experiment_from_yml(config_file_path, num_threads=4)


def mock_experiment(experiment):
    """Mock running an experiment and save the mock result."""
    # Mock experiment duration.
    time.sleep(2.5)
    result_storage.save_result(experiment, mock_result(experiment['settings']))


def mock_result(settings):
    """Mock result experiment.

    Args:
        settings(dict): the experiment settings

    Returns: (list) the mock result
    """
    result = []
    datasets = settings['datasets']
    for dataset in datasets:
        recs = []
        for approach in settings['approaches']:
            recommendation = {'approach': approach['name'],
                              'recommendation': recommend(dataset, approach),
                              'evals': []}
            for metric in settings['metrics']:
                evaluation = evaluate_all(metric['settings'], approach, metric)
                recommendation['evals'].append(
                    {'name': metric['name'], 'evaluation': evaluation, 'params': metric['params']})
                print(metric)
            recs.append(recommendation)
        result.append({'dataset': dataset, 'recs': recs})
    return result


@compute_bp.route('/options', methods=['GET'])
def params():
    """Route: Send selection options.

    Returns:
         (dict) options response
    """
    response = {'options': options}
    # print(response)
    return response


# TODO rename route
@compute_bp.route('/calculation', methods=['GET', 'POST'])
def calculate():
    """Route: Perform a calculation (experiment).

    Returns:
        (str) the queue for POST requests, or the current (dict) result for GET requests
    """

    response = {}
    if request.method == 'POST':
        data = request.get_json()
        settings = data.get('settings')
        # print(data)
        append_queue(data.get('metadata'), settings)
        print('queue',experiment_queue)
        # response = {'status': 'success'}
        response = {'queue': experiment_queue }
    else:
        # Wait until the current experiment is done.
        #if experiment_thread.is_alive():
        #    experiment_thread.join()
        if not experiment_running:
            response['calculation'] = result_storage.current_result
        response['status'] = 'busy' if experiment_running else 'done'
    print('/calculation response:', response)
    return response


@compute_bp.route('/queue', methods=['GET', 'POST'])
def queue():
    """Route: Send the queue. Handle it using a thread.

    Returns:
         (string) the queue
    """
    """
    # Handle experiment thread.
    global experiment_thread
    # If the thread is running, wait until it's done.
    if experiment_thread.is_alive():
        experiment_thread.join()
    # Else, if the queue isn't empty, start a thread to compute the oldest entry.
    elif experiment_queue:
        print('Starting experiment thread')
        experiment_thread = threading.Thread(target=calculate_first)
        experiment_thread.start()
    else:
        print('error') 
    response = {}
    #response['updated'] = False

    if not experiment_running:
        calculate_first()
        #response['updated'] = True

    print('experiment running')

    print('queue:', experiment_queue)
    response['queue'] = experiment_queue
    return response
    """
    if experiment_queue and not experiment_running:
        calculate_first()
    return { 'queue': experiment_queue }


# Test cancel experiment
@compute_bp.route('/cancel', methods=['GET'])
def cancel_current():
    recommender_system.abort_computation(current_experiment_name)
    return "Canceled"


@compute_bp.route('/queue/delete', methods=['POST'])
def delete_item():
    """Pop the selected index from the queue.

    Returns:
         (string) a removal message
    """
    data = request.get_json()
    index = data.get('index')
    experiment_queue.pop(index)
    return "Removed index"


def recommend(dataset, approach):
    """Mock recommendation.

    Args:
        dataset(dict): a dataset with a name
        approach(dict): an approach with a name

    Returns:
        (string) a magic result
    """
    # Combine the names, flipping the approach name.
    return dataset['name'] + approach['name'][::-1]


def evaluate_all(settings, approach, metric):
    """
    Do a mock evaluation for all filters.

    :param settings: the experiment settings
    :param approach: the approach with a name
    :param metric: the metric
    :return: the evaluation dictionary containing all evaluations
    """
    base_eval = evaluate(approach, metric)
    evaluation = {'global': round(base_eval, 2), 'filtered': []}

    for setting in settings:
        if setting['filters']:
            # Evaluate per filter.
            for metric_filter in setting['filters']:
                evals = []
                for parameter in metric_filter['params']:
                    value = parameter['value']
                    # Just use the value if it's a number, otherwise use the length of the word.
                    filter_eval = value if isinstance(value, int) else len(value)
                    val = round((base_eval * len(metric_filter['name']) / filter_eval), 2)
                    evals.append({parameter['name'] + ' ' + str(value): val})
                evaluation['filtered'].append({metric_filter['name']: evals})

    return evaluation


def evaluate(approach, metric):
    """
    Mock evaluation: Give a magic number using an approach and metric.

    :param approach: an approach with a name
    :param metric: a metric with a name and value
    :return: the magic mock evaluation
    """
    # Mock evaluation
    value = len(approach['name']) * len(metric['name'])
    print('metric:', metric)
    # Do something with the metrics parameters.
    if metric['params']:
        print(metric['name'], 'has params', metric['params'])
        for parameter in metric['params']:
            value *= len(parameter['name']) * int(parameter['value'])

    return value / 100


def append_queue(metadata, settings):
    """
    Add a experiment item (settings) to the queue.

    :param metadata: the experiment metadata
    :param settings: the experiment settings
    """
    # Handle empty name
    if 'name' not in metadata:
        metadata['name'] = 'Untitled'

    # Set time
    timestamp = time.time()
    now = datetime.now()
    current_dt = now.strftime('%Y-%m-%d %H:%M:%S') #+ ('-%02d' % (now.microsecond / 10000))
    current_request = {'timestamp': {'stamp': str(int(timestamp)),
                                     'datetime': current_dt},
                       'metadata': metadata,
                       'settings': settings}
    experiment_queue.append(current_request)
