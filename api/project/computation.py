# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import json
import threading
import time
import datetime

from flask import (Blueprint, request)

from . import result_storage

compute_bp = Blueprint('computation', __name__, url_prefix='/api/computation')

# constants
DATASETS = [
    {'text': 'LFM2B', 'timestamp': True, 'params': {'values' : [{'text' : 'Train/testsplit', 'default' : '80', 'min':0, 'max':100}], 'options': [{'text' : 'Type of split', 'default' : "Random", 'options' : ["Random", "Time"]}]}},
    {'text': 'LFM1B', 'timestamp': True, 'params': {'values' : [{'text' : 'Train/testsplit', 'default' : '80', 'min':0, 'max':100}], 'options': [{'text' : 'Type of split', 'default' : "Random", 'options' : ["Random", "Time"]}]}},
    {'text': 'LFM360K', 'timestamp': False, 'params': {'values' : [{'text' : 'Train/testsplit', 'default' : '80', 'min':0, 'max':100}]}},
    {'text': 'ML25M', 'timestamp': True, 'params': {'values' : [{'text' : 'Train/testsplit', 'default' : '80', 'min':0, 'max':100}], 'options': [{'text' : 'Type of split', 'default' : "Random", 'options' : ["Random", "Time"]}]}},
    {'text': 'ML100K', 'timestamp': True, 'params': {'values' : [{'text' : 'Train/testsplit', 'default' : '80', 'min':0, 'max':100}], 'options': [{'text' : 'Type of split', 'default' : "Random", 'options' : ["Random", "Time"]}]}}
]

APPROACHES = json.load(open('project/approaches.json'))
METRICS = json.load(open('project/metrics.json'))

# Generate parameter data
metric_categories = METRICS['categories']
for category in metric_categories:
    if category['text'] == 'Accuracy':
        metric_params = {'values': [{'text': 'k', 'default': 10, 'min': 1, 'max': 20}]}
    else:
        metric_params = {}
    category['options'] = list(map(lambda metric: {'text': metric, 'params': metric_params}, category['options']))

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


def calculate_first():
    time.sleep(2.5)  # Mock computation duration.

    computation = computation_queue.pop()  # Get the oldest computation from the queue.

    settings = computation['settings']
    # Mocks result computation. TODO compute result with libs here
    result = []
    datasets = settings['datasets']
    for dataset in datasets:
        recs = []
        for approach in settings['approaches']:
            recommendation = {'approach': approach['name'],'recommendation': recommend(dataset, approach), 'evals': []}
            for metric in settings['metrics']:
                evaluation = evaluate_all(dataset['settings'], approach, metric)

                recommendation['evals'].append({'name': metric['name'], 'evaluation': evaluation})
            recs.append(recommendation)
        result.append({'dataset': dataset, 'recs': recs})

    result_storage.save_result(computation, result)


computation_thread = threading.Thread(target=calculate_first)


# Route: Send selection options.
@compute_bp.route('/options', methods=['GET'])
def params():
    options = {}

    print(METRICS)
    options['defaults'] = DEFAULTS
    # options['filters'] = FILTERS

    # MOCK: for now use all filters/metrics per dataset
    for dataset in DATASETS:
        dataset['params']['dynamic']= [{'name': 'filter', 'nested': False,
                                   'plural': 'filters', 'article': 'a', 'options': FILTERS}]

    #for metric in METRICS['categories']:
        #print(metric)
        #metric['options']['params']['dynamic']= [{'name': 'filter', 'nested': False,
        #                          'plural': 'filters', 'article': 'a', 'options': FILTERS}]
    options['datasets'] = DATASETS
    options['approaches'] = APPROACHES
    options['metrics'] = METRICS


    response = {'options': options}
    print(response)
    return response


# Route: Do a calculation.
@compute_bp.route('/calculation', methods=['GET', 'POST'])
def calculate():
    response = {}
    if request.method == 'POST':
        data = request.get_json()
        settings = data.get('settings')
        print(data)
        append_queue(data.get('metadata'), settings)

        # response = {'status': 'success'}
        response = json.dumps(computation_queue)
    else:
        if computation_thread.is_alive():
            computation_thread.join()
        response['calculation'] = result_storage.newest_result()
        print(response)
    return response


@compute_bp.route('/queue', methods=['GET', 'POST'])
def queue():
    # Handle computation thread.
    global computation_thread
    if computation_thread.is_alive():
        computation_thread.join()
    elif computation_queue:
        print('Starting computation thread')
        computation_thread = threading.Thread(target=calculate_first)
        computation_thread.start()
    return json.dumps(computation_queue)


@compute_bp.route('/queue/delete', methods=['POST'])
# Pop the selected index from the queue
def deleteItem():
    data = request.get_json()
    index = data.get('index')
    computation_queue.pop(index)
    return "Removed index"


def recommend(dataset, approach):
    return dataset['name'] + approach['name'][::-1]  # Mock recommendation


def evaluate_all(settings, approach, metric):
    base_eval = evaluate(approach, metric)
    evaluation = {'global': base_eval, 'filtered': []}

    print(settings)
    for setting in settings:
        print(setting)
        # Evaluate per filter
        if setting['filters']:
            print(setting['filters'])
            for filter in setting['filters']:
                evals = []
                for parameter in filter['parameter']:
                    value = parameter['value']
                    # Just use the value if it's a number, otherwise use the length of the word.
                    filter_eval = value if type(value) == int else len(value)
                    val = "%.2f" % (base_eval * len(filter['name']) / filter_eval)
                    evals.append({parameter['name']+' '+str(value):val})
                evaluation['filtered'].append({filter['name']: evals})

    return evaluation


def evaluate(approach, metric):
    # Mock evaluation
    value = len(approach['name']) * len(metric['name'])

    # Do something with the metrics parameters.
    if metric['parameter']:
        for parameter in metric['parameter']:
            value *= len(parameter['name'])

    return value


# add a computation request to the queue
def append_queue(metadata, settings):
    timestamp = time.time()
    now = datetime.datetime.now()
    current_dt = now.strftime('%Y-%m-%dT%H:%M:%S') + ('-%02d' % (now.microsecond / 10000))
    current_request = {'timestamp': {'stamp': timestamp, 'datetime': current_dt}, 'metadata': metadata,
                       'settings': settings}
    computation_queue.append(current_request)
