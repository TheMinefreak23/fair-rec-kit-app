# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from flask import (Blueprint, request)

from . import result_storage

results_bp = Blueprint('results', __name__, url_prefix='/all-results')

@results_bp.route('/results', methods=['GET'])
def results():
    return result_storage.load_results()


@results_bp.route('/edit', methods=['POST'])
def edit():
    data = request.get_json()
    print(data)
    #data.get('email')
    #data.get('name')
    #data.get('tag')
