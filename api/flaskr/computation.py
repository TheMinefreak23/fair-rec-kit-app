# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from flask import (Blueprint, request)

from previous_results import save_result, newest_result

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
        reverse = data.get('dataset')[::-1]
        magic = data.get('number') ** 2 + len(reverse)
        save_result(magic, reverse)
    else:
        response['calculation'] = newest_result()
    return response
