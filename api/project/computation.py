# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

import time

from flask import (Blueprint, request)

bp = Blueprint('computation', __name__, url_prefix='/computation')

# constants
DATASETS = ['LFM2B', 'LFM1B', 'LFM360K']
APPROACHES = [
    {'name': 'ALS', 'params': {'values': [{'name': 'features', 'min': 1, 'max': 1000, 'default': 10}]}},
    {'name': 'POP',
     'params': {'options': [{'name': 'method', 'options': ['quantile', 'rank', 'count'], 'default': 'quantile'}]}},
    {'name': 'RAND', 'params': []}]
K_METRICS = ['P@K', 'R@K', 'HR@K', 'RR@K', 'NDCG@K']
OTHER_METRICS = ['DCG']
DEFAULTS = {'split': 80,
            'recCount': {'min': 0, 'max': 100, 'default': 10},
            }  # default values

# list with results of calculations
calculations = [
    {
        'timestamp': '0',
        'number': '0',
        'reverse': ''
    }
]


# Route: Send selection options.
@bp.route('/options', methods=['GET'])
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
    response = {'options': options}
    return response


# Route: Do a calculation.
@bp.route('/calculation', methods=['GET', 'POST'])
def calculate():
    response = {}
    if request.method == 'POST':
        response = {'status': 'success'}
        data = request.get_json()
        print(data)
        reverse = data.get('dataset')[::-1]
        magic = data.get('number') ** 2 + len(reverse)
        calculations.insert(0, {'timestamp': time.time(), 'number': magic, 'reverse': reverse})
    else:
        response['calculation'] = calculations[0]
    return response
