"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import enum
import json
import os
import threading
import time
from dataclasses import dataclass
from datetime import datetime
import yaml
from fairreckitlib.experiment.experiment_config_parsing import Parser

from fairreckitlib.recommender_system import RecommenderSystem

from flask import (Blueprint, request)

from . import result_storage
from .events import ProgressStatus, Status, EventHandler
from .options_formatter import create_available_options, config_dict_from_settings

compute_bp = Blueprint('experiment', __name__, url_prefix='/api/experiment')

# Constants
CONFIG_DIR = 'config_files'
RESULTS_DIR = 'results'

# Initialise
recommender_system = RecommenderSystem('datasets', RESULTS_DIR)
options = create_available_options(recommender_system)
experiment_queue = []
current_experiment = None



# TODO refactor job and config_dict overlap
@dataclass
class QueueItem:
    """Dataclass for experiment setting items in the queue"""
    job: dict
    config: dict
    status: Status
    progress: ProgressStatus
    name: str


def formatted_queue():
    # Format queue to dict list
    # TODO refactor: shouldn't have to convert like this
    # dict_queue = [{'job': experiment.job, 'status': experiment.status.value} for experiment in experiment_queue]
    return [formatted_experiment(experiment) for experiment in experiment_queue]


def formatted_experiment(experiment):
    # TODO refactor: shouldn't have to convert like this
    if not experiment: return {}
    experiment.job['status'] = experiment.status.value
    experiment.job['progress'] = experiment.progress.value
    return experiment.job


def calculate_first():
    """Take the oldest settings in the queue and perform an experiment with them"""

    # Do one experiment at a time
    if current_experiment and current_experiment.status == Status.ACTIVE:
        return

    # Get the oldest experiment from the queue.
    # experiment = experiment_queue.pop()

    # Get the oldest experiment from the queue that is marked to do.
    first = next(filter(lambda item: item.status == Status.TODO, experiment_queue), None)

    # If there is a queue item to do, run it.
    if first:
        run_experiment(first)
        # mock_experiment(experiment)


# experiment_thread = threading.Thread(target=calculate_first)

def end_experiment():
    if current_experiment.status is not Status.ABORTED:
        # result_storage.save_result(current_experiment.job, {})
        result_storage.save_result(current_experiment.job, format_result(current_experiment.config))

    # Calculate next item in queue
    calculate_first()


def run_experiment(experiment):
    """Run an experiment and save the result."""

    #print('run experiment:', experiment)

    # Set current experiment
    global current_experiment
    current_experiment = experiment

    # Create config files directory if it doesn't exist yet.
    if not os.path.isdir(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)

    # Save configuration to yaml file.
    config_file_path = CONFIG_DIR + '/' + current_experiment.name

    with open(config_file_path + '.yml', 'w+', encoding='utf-8') as config_file:
        yaml.dump(current_experiment.config, config_file)

    parser = Parser(True)
    config = parser.parse_experiment_config_from_yml(config_file_path,
                                                     recommender_system.data_registry,
                                                     recommender_system.experiment_factory)

    event_handler = EventHandler(current_experiment, end_experiment)
    recommender_system.run_experiment(config, events=event_handler.events)

    # TODO USE THIS FUNCTION INSTEAD OF PARSING
    # recommender_system.run_experiment_from_yml(config_file_path, num_threads=4)

def send_email(metadata, timestamp):
    print("llanfairpwlchfairgwyngychgogerychchwryrndrwbwchllantisiligogogoch")
    print(metadata["name"])
    print(metadata["email"])
    print(timestamp)


def mock_experiment():
    """Mock running an experiment and save the mock result."""
    # Mock experiment duration.
    time.sleep(2.5)
    result_storage.save_result(current_experiment.job, format_result(current_experiment.config))


def format_result(settings):
    """Mock result experiment.

    Args:
        settings(dict): the experiment settings

    Returns: (list) the mock result
    """
    #print('== settings ==', settings)
    result = []
    datasets = settings['data']
    for (dataset_index, dataset) in enumerate(datasets):
        # Add dataset identifier to name
        dataset['name'] = dataset['dataset'] + '_' + dataset['matrix'] + '_' + str(dataset_index)
        recs = []
        for (api, approaches) in settings['models'].items():
            for (approach_index, approach) in enumerate(approaches):
                # Add approach, with index as identifier in the name
                recommendation = {'approach': api + '_' + approach['name'] + '_' + str(approach_index),
                                  #'recommendation': mock_recommend(dataset, approach),
                                  'evals': []}
                """
                for metric in settings['metrics']:
                    evaluation = mock_evaluate_all(approach, metric)
                    recommendation['evals'].append(
                        {'name': metric['name'], 'evaluation': evaluation, 'params': metric['params']})
                    print(metric)"""
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
        #print('==/calculation POST==', json.dumps(data,indent=4))
        append_queue(data.get('metadata'), settings)

        calculate_first()

        #print('queue', experiment_queue)
        # response = {'status': 'success'}

        response = {'queue': formatted_queue()}
    else:
        # TODO catch error
        global current_experiment
        if not current_experiment: 
            print('Current experiment should have started but is None')
        response['status'] = current_experiment.status.value if current_experiment else Status.NA.value
        if current_experiment:
            if current_experiment.status == Status.DONE:
                # Set current result, TODO hacky
                result_storage.result_by_id(current_experiment.job['timestamp']['stamp'])
                response['calculation'] = result_storage.current_result
            if current_experiment.status == Status.DONE or current_experiment.status == Status.ABORTED:
                current_experiment = None
    # print('calculation response:', response)
    return response


@compute_bp.route('/queue', methods=['GET'])
def queue():
    #print('queue', json.dumps(formatted_queue(),indent=4))
    return {'queue': formatted_queue(), 'current': formatted_experiment(current_experiment) if current_experiment else None}


@compute_bp.route('/queue/abort', methods=['POST'])
def abort():
    """Cancel the item with the ID from the queue.

    Returns:
         (string) a removal message
    """
    data = request.get_json()
    item_id = data.get('id')
    print('trying to cancel',item_id)
    # Find the first experiment with the ID in the queue
    experiment = next(filter(lambda item: item.job['timestamp']['stamp'] == item_id, experiment_queue), None)
    #print(experiment)
    # Cancel queued experiment
    if experiment.status == Status.TODO:
        experiment.status = Status.CANCELLED
    # Abort active experiment
    if experiment.status == Status.ACTIVE:
        recommender_system.abort_computation(experiment.name)
        experiment.status = Status.ABORTED
    return "Removed index"


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
    #print('metric:', metric)
    # Do something with the metrics parameters.
    if metric['params']:
        #print(metric['name'], 'has params', metric['params'])
        for (name, value) in metric['params'].items():
            val = int(value) if value else 0
            result *= len(name) * val

    return result / 100


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
    current_dt = now.strftime('%Y-%m-%d %H:%M:%S')  # + ('-%02d' % (now.microsecond / 10000))
    job = {'timestamp': {'stamp': str(int(timestamp)),
                         'datetime': current_dt},
           'metadata': metadata,
           'settings': settings}

    """
    # Parse tags
    if 'tags' in metadata:
        job['metadata']['tags'] = result_storage.parse_tags(metadata['tags'])
    """

    # Create configuration dictionary.
    config_dict, config_id = config_dict_from_settings(job)

    # TODO refactor job and config_dict overlap
    current_job = QueueItem(job, config_dict, Status.TODO, ProgressStatus.NA, config_id)

    experiment_queue.append(current_job)
