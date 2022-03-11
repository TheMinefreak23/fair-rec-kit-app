import time

from flask import (Blueprint,request)

bp = Blueprint('auth', __name__, url_prefix='/auth')

# constants
DATASETS = ['LFM2B', 'LFM1B', 'LFM360K']
APPROACHES = ['ALS']
METRICS = ['P@K', 'R@K', 'NDCG']

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
