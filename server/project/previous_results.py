"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from . import result_storage

from flask import (Blueprint, request)

results_bp = Blueprint('results', __name__, url_prefix='/api/all-results')


@results_bp.route('/', methods=['GET'])
def results():
    return result_storage.load_results_overview()


@results_bp.route('/edit', methods=['POST'])
def edit():
    data = request.get_json()
    id = data.get('id')
    new_name = data.get('new_name')
    new_tags = data.get('new_tags')
    new_email = data.get('new_email')
    result_storage.edit_result(id, new_name, new_tags, new_email)
    return "Edited index"


@results_bp.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    result_id = data.get('id')
    result_storage.delete_result(result_id)
    return "Removed index"

    


