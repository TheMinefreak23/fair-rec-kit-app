# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from flask import (Blueprint, request)

from . import result_storage

compute_bp = Blueprint('computation', __name__, url_prefix='/computation')

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
    response = {'options': options}
    return response


# Route: Do a calculation.
@compute_bp.route('/calculation', methods=['GET', 'POST'])
def calculate():
    response = {}
    if request.method == 'POST':
        response = {'status': 'success'}
        data = request.get_json()
        print(data)
        settings = data.get('settings')

        result = []
        # Mocks result computation. TODO compute result with libs here
        for dataset in settings['datasets']:
            recs = []
            for approach in settings['approaches']:
                recommendation = {'recommendation': approach[::-1], 'evals': []}
                for metric in settings['metrics']:
                    evaluation = len(approach) * len(metric['name']) * metric['k']
                    recommendation['evals'].append(evaluation)
                recs.append(recommendation)
            result.append({'dataset': dataset, 'recs': recs})

        result_storage.save_result(data.get('metadata'), settings, result)
    else:
        response['calculation'] = result_storage.newest_result()
    return response
