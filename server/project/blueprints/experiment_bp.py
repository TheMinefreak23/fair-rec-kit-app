"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json

from flask import (Blueprint, request)
from fairreckitlib.recommender_system import RecommenderSystem
from ..options_formatter import create_available_options
from ..experiment_queue import ExperimentQueue, formatted_experiment
from ..experiment import Status

blueprint = Blueprint('experiment', __name__, url_prefix='/api/experiment')

# Constants
RESULTS_DIR = 'results'

# Initialise
recommender_system = RecommenderSystem('datasets', RESULTS_DIR)
options = create_available_options(recommender_system)
queue = ExperimentQueue(recommender_system)  # TODO refactor


@blueprint.route('/options', methods=['GET'])
def params():
    """Route: Provide selection options.

    Returns:
         (dict) the options response
    """
    response = {'options': options}
    # print(response)
    return response


# TODO rename route
@blueprint.route('/', methods=['GET', 'POST'])
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
        queue.append_queue(data.get('metadata'), settings)

        # Run first experiment from the queue
        queue.run_first()

        # print('queue', experiment_queue)
        response = {'queue': queue.formatted_queue()}
    else:
        # TODO catch error
        # TODO refactor
        if not queue.current_experiment:
            print('Current experiment should have started but is None')
            response['status'] = Status.NA.value

        if queue.current_experiment:
            response['status'] = queue.current_experiment.queue_item.status.value
            if queue.current_experiment.queue_item.status == Status.DONE:
                experiment_id = queue.current_experiment.queue_item.job['timestamp']['stamp']
                response['experimentID'] = experiment_id
            if queue.current_experiment.queue_item.status in [Status.DONE, Status.ABORTED]:
                queue.current_experiment = None
    # print('calculation response:', response)
    return response


@blueprint.route('/queue', methods=['GET'])
def get_queue():
    """Route: Provide the current experiment queue and the current experiment.

    Returns:
        (dict) the queue and experiment

    """
    # print('queue', queue)
    return {'queue': queue.formatted_queue(),
            'current': formatted_experiment(queue.current_experiment) if queue.current_experiment else None}


@blueprint.route('/queue/abort', methods=['POST'])
def abort():
    """Cancel the item with the ID from the queue.

    Returns:
         (string) a removal message
    """
    data = request.get_json()
    item_id = data.get('id')
    print('trying to cancel', item_id)
    # Find the first experiment with the ID in the queue (should be unique)
    experiment = next(
        filter(
            lambda item:
            item.queue_item.job['timestamp']['stamp'] == item_id,
            queue),
        None)
    # print(experiment)
    # Cancel queued experiment
    #TODO refactor
    status = experiment.queue_item.status
    if status == Status.TODO:
        experiment.queue_item.status = Status.CANCELLED
    # Abort active experiment
    if status == Status.ACTIVE:
        recommender_system.abort_computation(experiment.name)
        experiment.queue_item.status = Status.ABORTED
    return "Removed index"
    # TODO handle item not in queue
