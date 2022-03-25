# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from flask import (Blueprint, request)

from . import result_storage

results_bp = Blueprint('results', __name__, url_prefix='/all-results')

@results_bp.route('/', methods=['GET'])
def results():
    #result_storage.create_results()
    #return result_storage.load_results()
    return {}

@results_bp.route('/edit', methods=['POST'])
def edit():
    data = request.get_json()
    print(data)
    #data.get('email')
    #data.get('name')
    #data.get('tag')
