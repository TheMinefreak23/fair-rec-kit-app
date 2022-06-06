"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import time
from dataclasses import dataclass
from datetime import datetime
import yaml
from fairreckitlib.experiment.experiment_config_parsing import Parser

from fairreckitlib.recommender_system import RecommenderSystem

from flask import (Blueprint, request)

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
    validating: bool = False


def formatted_queue():
    """Format the queue to a list of formatted experiments (dictionaries).

    Returns:
        (list(dict)) the list of formatted experiments

    """
    # Format queue to dict list
    # TODO refactor: shouldn't have to convert like this
    return [formatted_experiment(experiment) for experiment in experiment_queue]


def formatted_experiment(experiment):
    """Format the experiment to a dictionary.

    Args:
        experiment(QueueItem): the experiment from the queue

    Returns:
        (dict) the formatted experiment

    """
    # TODO refactor: shouldn't have to convert like this
    if not experiment:
        return {}
    experiment.job['status'] = experiment.status.value
    experiment.job['progress'] = experiment.progress.value
    return experiment.job


def run_first():
    """Take the oldest settings in the queue and perform an experiment with them."""

    # Do one experiment at a time
    if current_experiment and current_experiment.status == Status.ACTIVE:
        return

    # Get the oldest experiment from the queue.
    # experiment = experiment_queue.pop()

    # Get the oldest experiment from the queue that is marked to do.
    first = next(filter(lambda item: item.status == Status.TODO, experiment_queue), None)

    # If there is a queue item to do, run it.
    # Either start a validation of an existing result or run a new experiment.
    if first:
        if first.validating:
            validate_experiment(first)
        else:
            run_new_experiment(first)
        # mock_experiment(experiment)


def set_up_experiment(experiment):
    """Set up an experiment before running it.

    Args:
        experiment(QueueItem): the experiment we are about to run

    Returns:
        (dict) the experiment events
    """

    # print('run experiment:', experiment)

    # Update current experiment
    global current_experiment
    current_experiment = experiment

    # Make a new event handler and get experiment events
    return EventHandler(current_experiment, run_first).events


def run_new_experiment(experiment):
    """Run a new experiment (first run).

    Args:
        experiment(QueueItem): the experiment to run

    """
    events = set_up_experiment(experiment)
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

    recommender_system.run_experiment(config, events=events)

    # TODO USE THIS FUNCTION INSTEAD OF PARSING
    # recommender_system.run_experiment_from_yml(config_file_path, num_threads=4)


def validate_experiment(experiment):
    """Validate an experiment by running it multiple times, using the experiment file path.

    Args:
        experiment(QueueItem): the experiment to validate

    """
    events = set_up_experiment(experiment)
    recommender_system.validate_experiment(result_dir=experiment.job['file_path'],
                                           num_runs=experiment.job['amount'],
                                           events=events)


@compute_bp.route('/options', methods=['GET'])
def params():
    """Route: Provide selection options.

    Returns:
         (dict) options response
    """
    response = {'options': options}
    # print(response)
    return response


# TODO rename route
@compute_bp.route('/', methods=['GET', 'POST'])
def handle_experiment():
    """Route: Perform an experiment or give the current experiment.

    Returns:
        (str) the queue for POST requests, or the current experiment ID (int) for GET requests
    """

    response = {}
    if request.method == 'POST':
        # Get settings and metadata from request
        data = request.get_json()
        settings = data.get('settings')
        # print('==/calculation POST==', json.dumps(data,indent=4))
        append_queue(data.get('metadata'), settings)

        # Run first experiment from the queue
        run_first()

        # print('queue', experiment_queue)
        response = {'queue': formatted_queue()}
    else:
        # TODO catch error
        global current_experiment
        if not current_experiment:
            print('Current experiment should have started but is None')
            response['status'] = Status.NA.value

        if current_experiment:
            response['status'] = current_experiment.status.value
            if current_experiment.status == Status.DONE:
                experiment_id = current_experiment.job['timestamp']['stamp']
                response['experimentID'] = experiment_id
            if current_experiment.status in [Status.DONE, Status.ABORTED]:
                current_experiment = None
    # print('calculation response:', response)
    return response


@compute_bp.route('/queue', methods=['GET'])
def queue():
    """Route: Provide the current experiment queue and the current experiment.

    Returns:
        (dict) the queue and experiment

    """
    # print('queue', json.dumps(formatted_queue(),indent=4))
    return {'queue': formatted_queue(),
            'current': formatted_experiment(current_experiment) if current_experiment else None}


@compute_bp.route('/queue/abort', methods=['POST'])
def abort():
    """Cancel the item with the ID from the queue.

    Returns:
         (string) a removal message
    """
    data = request.get_json()
    item_id = data.get('id')
    print('trying to cancel', item_id)
    # Find the first experiment with the ID in the queue
    experiment = next(
        filter(
            lambda item:
            item.job['timestamp']['stamp'] == item_id,
            experiment_queue),
        None)
    # print(experiment)
    # Cancel queued experiment
    if experiment.status == Status.TODO:
        experiment.status = Status.CANCELLED
    # Abort active experiment
    if experiment.status == Status.ACTIVE:
        recommender_system.abort_computation(experiment.name)
        experiment.status = Status.ABORTED
    return "Removed index"


def append_queue(metadata, settings):
    """Add a regular/new experiment item (settings) to the queue.

    Args:
        metadata(dict): the experiment metadata
        settings(dict): the experiment settings
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

    # Create configuration dictionary.
    config_dict, config_id = config_dict_from_settings(job)

    # TODO refactor job and config_dict overlap
    current_job = QueueItem(job,
                            config_dict,
                            Status.TODO,
                            ProgressStatus.NA,
                            config_id)

    experiment_queue.append(current_job)


def add_validation(file_path, amount):
    """Add a validation experiment to the queue.

    Args:
        file_path: the path to the existing experiment result
        amount: the amount of runs for validation

    """
    experiment = QueueItem(job={'file_path': file_path, 'amount': amount},
                           config={},
                           name='',
                           status=Status.TODO,
                           progress=ProgressStatus.NA,
                           validating=True)
    experiment_queue.append(experiment)
    run_first()
