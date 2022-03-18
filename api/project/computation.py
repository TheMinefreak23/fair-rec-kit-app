# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from flask import (Blueprint, request)

from . import result_storage

compute_bp = Blueprint('computation', __name__, url_prefix='/computation')

# constants
DATASETS = ['LFM2B', 'LFM1B', 'LFM360K']
APPROACHES = ['ALS']
METRICS = ['P@K', 'R@K', 'NDCG']


# Route: Send selection options.
@compute_bp.route('/options', methods=['GET'])
def params():
    options = {}
    options['datasets'] = DATASETS
    options['approaches'] = APPROACHES
    options['metrics'] = METRICS
    options['numbers'] = [1, 2, 3]
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
