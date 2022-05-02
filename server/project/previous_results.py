"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from flask import (Blueprint, request)
import pandas as pd

from . import result_storage

results_bp = Blueprint('results', __name__, url_prefix='/api/all-results')


@results_bp.route('/', methods=['GET'])
def results():
    return result_storage.load_results_overview()


@results_bp.route('/result-by-id', methods=['POST', 'GET'])
def result_by_id():
    if request.method == 'POST':
        data = request.get_json()
        result_storage.result_by_id(data['id'])
        print(data)
        if result_storage.current_result:
            response = {'status': 'success'}
        else:
            response = {'status': 'result not found'}

    else:  # GET request
        response = {'result': result_storage.current_result}

    return response


@results_bp.route('/edit', methods=['POST'])
def edit():
    data = request.get_json()
    index = data.get('index')
    new_name = data.get('new_name')
    new_tags = data.get('new_tags')
    new_email = data.get('new_email')
    result_storage.edit_result(index, new_name, new_tags, new_email)
    return "Edited index"


@results_bp.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    index = data.get('index')
    result_storage.delete_result(index)
    return "Removed index"


