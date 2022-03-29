# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from flask import (Blueprint, request)
import pandas as pd

from . import result_storage

results_bp = Blueprint('results', __name__, url_prefix='/all-results')

@results_bp.route('/', methods=['GET'])
def results():
    #result_storage.create_results()
    return result_storage.load_results_overview()


@results_bp.route('/result-by-id', methods=['POST','GET'])
def result_by_id():
    if request.method == 'POST':
        data = request.get_json()
        result_storage.result_by_id(data['id'])
        print(data)
        response = {'status': 'success'}

    else: # GET request
        response = result_storage.current_result

    return response


@results_bp.route('/edit', methods=['POST'])
def edit():
    data = request.get_json()
    print(data)
    #data.get('email')
    #data.get('name')
    #data.get('tag')

@results_bp.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    index = data.get('index')
    result_storage.delete_result(index)
    return "Removed index"
  
## only get one results
@results_bp.route('/result', methods=['GET'])
def user_result():
    data = pd.read_csv('mock/1647818279_HelloWorld/1647818279_run_0/LFM-360K_0/Foo_ALS_0/ratings.tsv', sep='\t', header=None)
    return data.to_json(orient='records')
    
