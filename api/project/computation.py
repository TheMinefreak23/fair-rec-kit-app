# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import json
import threading
import time
import datetime

from flask import (Blueprint, request)

from . import result_storage

compute_bp = Blueprint('computation', __name__, url_prefix='/computation')

# constants
DATASETS = [
    {'text': 'LFM2B', 'timestamp': True, 'params': {}},
    {'text': 'LFM1B', 'timestamp': True, 'params': {}},
    {'text': 'LFM360K', 'timestamp': False, 'params': {}},
    {'text': 'ML25M', 'timestamp': True, 'params': {}},
    {'text': 'ML100K', 'timestamp': True, 'params': {}},
]

JSONapproach = open('project/approaches.json')
APPROACHES = json.load(JSONapproach)

K_METRICS = ['P@K', 'R@K', 'HR@K', 'RR@K', 'NDCG@K']
OTHER_METRICS = ['DCG', 'RMSE', 'MAE', 'MRR', 'Item Coverage', 'Gini index']
DEFAULTS = {'split': 80,
            'recCount': {'min': 0, 'max': 100, 'default': 10},
            }  # default values
FILTERS = [{'text': 'Artist Gender', 'params': {'options': [{'text': 'Gender', 'options': ['Male', 'Female']}]}},
           {'text': 'User Gender', 'params': {'options': [{'text': 'Gender', 'options': ['Male', 'Female']}]}},
           {'text': 'Country user threshold',
            'params': {'values': [{'text': 'threshold', 'min': 1, 'max': 1000, 'default': 10}]}},
           {'text': 'Minimum age', 'params': {'values': [{'text': 'threshold', 'min': 1, 'max': 1000, 'default': 18}]}},
           {'text': 'Maximum age', 'params': {'values': [{'text': 'threshold', 'min': 1, 'max': 1000, 'default': 18}]}}]

computation_queue = []


# Route: Send selection options.
@compute_bp.route('/options', methods=['GET'])
def params():
    options = {}
    options['datasets'] = DATASETS
    options['approaches'] = APPROACHES

    # Generate parameter data
    metrics = []
    for metric in K_METRICS:
        metric_params = {'values': [{'text': 'k', 'default': 10, 'min': 1, 'max': 20}]}
        metrics.append({'text': metric, 'params': metric_params})
    for metric in OTHER_METRICS:
        metrics.append({'text': metric, 'params': []})

    options['metrics'] = metrics
    options['defaults'] = DEFAULTS
    options['filters'] = FILTERS
    response = {'options': options}
    return response


# Route: Do a calculation.
@compute_bp.route('/calculation', methods=['GET', 'POST'])
def calculate():
    computation_thread = threading.Thread(target=calculate_first)
    response = {}
    if request.method == 'POST':
        data = request.get_json()
        settings = data.get('settings')
        print(data)
        append_queue(data.get('metadata'), settings)

        # Handle computation thread.
        computation_thread.start()

    #   response = {'status': 'success'}
    #else:
        computation_thread.join()
        response['calculation'] = result_storage.newest_result()
        print(response)
    return response


@compute_bp.route('/queue', methods=['GET', 'POST'])
def queue():
    return json.dumps(computation_queue)


@compute_bp.route('/queue/delete', methods=['POST'])
#Pop the selected index from the queue
def deleteItem():
    data = request.get_json()
    index = data.get('index')
    computation_queue.pop(index)
    return "Removed index"


def recommend(dataset, approach):
    return dataset['text'] + approach['text'][::-1]  # Mock


def evaluate(approach, metric):
    value = len(approach['text']) * len(metric['text'])
    parameter = metric['parameter']
    if parameter:
        value *= parameter['text']  # Mock


# add a computation request to the queue
def append_queue(metadata, settings):
    timestamp = time.time()
    now = datetime.datetime.now()
    current_dt = now.strftime('%Y-%m-%dT%H:%M:%S') + ('-%02d' % (now.microsecond / 10000))
    current_request = {'timestamp': {'stamp': timestamp, 'datetime': current_dt}, 'metadata': metadata,
                       'settings': settings}
    computation_queue.append(current_request)


def calculate_first():
    time.sleep(5) # Mock computation duration.

    computation = computation_queue.pop() # Get the oldest computation from the queue.

    settings = computation['settings']
    # Mocks result computation. TODO compute result with libs here
    result = []
    datasets = settings['datasets']
    for dataset in datasets:
        recs = []
        for approach in settings['approaches']:
            recommendation = {'recommendation': recommend(dataset, approach), 'evals': []}
            for metric in settings['metrics']:
                evaluation = evaluate(approach, metric)
                recommendation['evals'].append({'text': metric['text'], 'evaluation': evaluation})
            recs.append(recommendation)
        result.append({'dataset': dataset, 'recs': recs})

    result_storage.save_result(computation,result)
