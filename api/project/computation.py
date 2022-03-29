# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import json
import time
import datetime

from flask import (Blueprint, request)

from . import result_storage

compute_bp = Blueprint('computation', __name__, url_prefix='/computation')

# constants
DATASETS = [
    {'name' : 'LFM2B', 'timestamp' : True, 'params' : {'filters' : ['age', 'gender', 'country']}}, 
    {'name' : 'LFM1B', 'timestamp' : True, 'params' : {'filters' : ['age', 'gender', 'occupation']}},
    {'name' : 'LFM360K', 'timestamp' : False, 'params' : {'filters' : ['age', 'gender', 'occupation']}},
    {'name' : 'ML25M', 'timestamp' : True, 'params' : []},
    {'name' : 'ML100K', 'timestamp' : True, 'params' : {'filters' : ['age', 'gender', 'occupation']}},
    ]
APPROACHES = [
    {'name': 'ALS', 'params': {'values': [{'name': 'features', 'min': 1, 'max': 1000, 'default': 10}]}},
    {'name': 'POP',
     'params': {'options': [{'name': 'method', 'options': ['quantile', 'rank', 'count'], 'default': 'quantile'}]}},
    {'name': 'RAND', 'params': []}]
K_METRICS = ['P@K', 'R@K', 'HR@K', 'RR@K', 'NDCG@K']
OTHER_METRICS = ['DCG', 'RMSE', 'MAE', 'MRR', 'Item Coverage', 'Gini index']
DEFAULTS = {'split': 80,
            'recCount': {'min': 0, 'max': 100, 'default': 10},
            }  # default values
FILTERS = [{'name' : 'Artist Gender', 'params' : {'options' : [{'name':'Gender', 'options' : ['Male', 'Female']}]}},
           {'name' : 'User Gender', 'params' : {'options' : [{'name':'Gender', 'options' : ['Male', 'Female']}]}},
           {'name' : 'Country user threshold', 'params' : {'values' : [{'name' : 'threshold', 'min' : 1, 'max':1000, 'default':10}]}},
           {'name' : 'Minimum age', 'params' : {'values' : [{'name' : 'threshold', 'min' : 1, 'max':1000, 'default':18}]}},
           {'name' : 'Maximum age', 'params' : {'values' : [{'name' : 'threshold', 'min' : 1, 'max':1000, 'default':18}]}}]

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
        metric_params = {'values': [{'name': 'k', 'default': 10, 'min': 1, 'max': 20}]}
        metrics.append({'name': metric, 'params': metric_params})
    for metric in OTHER_METRICS:
        metrics.append({'name': metric, 'params': []})

    options['metrics'] = metrics
    options['defaults'] = DEFAULTS
    options['filters'] = FILTERS
    response = {'options': options}
    return response


# Route: Do a calculation.
@compute_bp.route('/calculation', methods=['GET', 'POST'])
def calculate():
    response = {}
    if request.method == 'POST':
        response = {'status': 'success'}
        data = request.get_json()
        settings = data.get('settings')
        print(data)
        append_queue(data.get('metadata'), settings)

        result = []
        # Mocks result computation. TODO compute result with libs here
        datasets = settings['datasets']
        for dataset in datasets:
            recs = []
            for approach in settings['approaches']:
                recommendation = {'recommendation': recommend(dataset, approach), 'evals': []}
                for metric in settings['metrics']:
                    evaluation = evaluate(approach, metric)
                    recommendation['evals'].append({'name': metric['name'], 'evaluation': evaluation})
                recs.append(recommendation)
            result.append({'dataset': dataset, 'recs': recs})

        result_storage.save_result(data.get('metadata'), settings, result)
        
    else:
        response['calculation'] = result_storage.newest_result()
        print(response)
    return response

@compute_bp.route('/queue', methods=['GET','POST'])
def queue():
    return json.dumps(computation_queue)

@compute_bp.route('/queue/delete', methods=['POST'])
def deleteItem():
    data = request.get_json()
    index = data.get('index')
    computation_queue.pop(index)
    return "Removed index"

def recommend(dataset, approach):
    return dataset + approach['name'][::-1]  # Mock


def evaluate(approach, metric):
    return len(approach['name']) * len(metric['name']) * len(metric['parameter']['name'])  # Mock

#add a computation request to the queue
def append_queue(metadata, settings):
    timestamp = time.time()
    now = datetime.datetime.now()
    currentDt = now.strftime('%Y-%m-%dT%H:%M:%S') + ('-%02d' % (now.microsecond / 10000))
    current_request = {'timestamp': {'stamp': timestamp, 'datetime' : currentDt}, 'metadata': metadata, 'settings': settings}
    computation_queue.append(current_request)