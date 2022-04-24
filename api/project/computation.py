# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import json
import threading
import time
from datetime import datetime

from fairreckitlib.experiment.parsing.run import parse_experiment_config_from_yml
from fairreckitlib.recommender_system import RecommenderSystem

from flask import (Blueprint, request)

from . import result_storage

compute_bp = Blueprint('computation', __name__, url_prefix='/api/computation')

recommender_system = RecommenderSystem('../../../datasets', 'results')
frk_datasets = recommender_system.get_available_datasets()
frk_predictors = recommender_system.get_available_predictors()
frk_recommenders = recommender_system.get_available_recommenders()
frk_metrics = recommender_system.get_available_metrics()
#print(frk_datasets)
#print(frk_predictors)
#print(frk_recommenders)
print(frk_metrics)

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

"""
def name_to_text(settings):
    return {'text': settings[key] for key in settings if key == 'name'}


# TODO lower-case now it's not a constant
#DATASETS = name_to_text(frk_datasets)
approaches = name_to_text(frk_recommenders)
metrics = name_to_text(frk_metrics)"""


# TODO: DO THIS IN BACKEND?
def settings_from_api(settings):
    formatted_settings = []
    for (header,options) in settings.items():
        formatted_settings.append({'name': header, 'options': options})
    print(formatted_settings)
    return formatted_settings


APPROACHES = settings_from_api(frk_recommenders)
METRICS = settings_from_api(frk_metrics)

# Generate metrics parameter data
#metric_categories = METRICS['categories']
for category in METRICS:
    if category['name'] == 'Accuracy':
        metric_params = {'values': [{'name': 'k', 'default': 10, 'min': 1, 'max': 20}]}
    else:
        metric_params = {}
    category['options'] = list(map(lambda metric: {'name': metric, 'params': metric_params}, category['options']))

print(METRICS)

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


def run_experiment(settings):
    file_name = 'test'
    config_file_path = 'config_files/' + file_name
    # recommender_system.run_experiment_from_yml(config_file_path, num_threads=4)

    config_name = 'test'
    config = parse_experiment_config_from_yml(config_file_path, recommender_system)

    stamp = str(int(datetime.timestamp(datetime.now())))
    config.name = stamp + '_' + config_name
    # config.datasets = [{'name': 'ML-100K', 'splitting': {'test_ratio': 0.2}, 'type': 'random'}]
    # config.models = [{'Implicit': [{'name': 'AlternatingLeastSquares'}]}]
    config.evaluation = {'metrics': ['P@K', 'R@K'], 'filters': []}
    recommender_system.run_experiment(config, num_threads=4)


def mock_computation(settings):
    # Mocks result computation. TODO compute result with libs here
    result = []
    datasets = settings['datasets']
    for dataset in datasets:
        recs = []
        for approach in settings['approaches']:
            recommendation = {'approach': approach['name'], 'recommendation': recommend(dataset, approach), 'evals': []}
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

    #print(METRICS)
    options['defaults'] = DEFAULTS
    # options['filters'] = FILTERS

    # MOCK: for now use all filters/metrics per dataset
    for dataset in DATASETS:
        dataset['params']['dynamic']= [{'name': 'filter', 'nested': False,
                                   'plural': 'filters', 'article': 'a', 'options': FILTERS}]

    for metric in METRICS['categories']:
        #print(metric)
        metric['options'][0]['params']['dynamic']= [{'name': 'result filter', 'nested': False,
                                  'plural': 'Result filters', 'article': 'a', 'options': FILTERS}]
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
                    evals.append({parameter['name']+' '+ str(value):val})
                evaluation['filtered'].append({filter['name']: evals})

    return evaluation


def evaluate(approach, metric):
    # Mock evaluation
    value = len(approach['name']) * len(metric['name'])

    # Do something with the metrics parameters.
    if hasattr(metric, 'parameter') and metric['parameter']:
        for parameter in metric['parameter']:
            value *= len(parameter['name'])

    return value


# add a computation request to the queue
def append_queue(metadata, settings):
    timestamp = time.time()
    now = datetime.now()
    current_dt = now.strftime('%Y-%m-%dT%H:%M:%S') + ('-%02d' % (now.microsecond / 10000))
    current_request = {'timestamp': {'stamp': timestamp, 'datetime': current_dt}, 'metadata': metadata,
                       'settings': settings}
    computation_queue.append(current_request)
