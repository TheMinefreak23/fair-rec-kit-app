#This program has been developed by students from the bachelor Computer Science at
#Utrecht University within the Software Project course.
#© Copyright Utrecht University (Department of Information and Computing Sciences)

import time

from flask import (Blueprint,request)

bp = Blueprint('computation', __name__, url_prefix='/computation')

# constants
DATASETS = ['LFM2B', 'LFM1B', 'LFM360K']
APPROACHES = ['ALS', 'POP', 'RAND']
METRICS = ['P@K', 'R@K', 'HR@K','RR@K', 'NDCG@K', 'DCG']

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
    options['metrics'] = METRICS
    options['numbers'] = [1, 2, 3]
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
