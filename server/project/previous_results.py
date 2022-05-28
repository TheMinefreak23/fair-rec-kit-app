"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json

from flask import (Blueprint, request)
import pandas as pd
from fairreckitlib.data.set.dataset import add_dataset_columns

from . import result_storage
from .experiment import options, recommender_system

results_bp = Blueprint('results', __name__, url_prefix='/api/all-results')


@results_bp.route('/', methods=['GET'])
def results():
    return result_storage.load_results_overview()


# TODO DEV we shouldn't need this, just for development
@results_bp.route('/old-result-by-id', methods=['POST', 'GET'])
def old_result_by_id():
    if request.method == 'POST':
        data = request.get_json()
        result_storage.old_result_by_id(data['id'])
        if result_storage.current_result:
            response = {'status': 'success'}
        else:
            response = {'status': 'result not found'}
        print(result_storage.current_result)
    else:  # GET request
        response = {'result': result_storage.current_result}
    return response


@results_bp.route('/result-by-id', methods=['POST', 'GET'])
def result_by_id():
    if request.method == 'POST':
        data = request.get_json()
        print('result_by_id data', data)
        result_storage.result_by_id(int(data['id']))
        if result_storage.current_result:
            response = {'status': 'success'}
        else:
            response = {'status': 'result not found'}

    else:  # GET request
        print('current result', json.dumps(result_storage.current_result, indent=4))
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
    result_id = data.get('id')
    result_storage.delete_result(result_id)
    return "Removed index"


# Set current shown recommendations
@results_bp.route('/set-recs', methods=['POST'])
def set_recs():
    json = request.json
    result_id = json.get("id")  # Result timestamp TODO use to get result
    run_id = json.get("runid")
    pair_id = json.get("pairid")
    path = result_storage.get_overview(result_id, run_id)[pair_id]['ratings_path']
    result_storage.current_recs[pair_id] = pd.read_csv(path, sep='\t', header=0)
    return {'status': 'success', 'availableFilters': options['filters']}


@results_bp.route('/result', methods=['POST'])
def user_result():
    """"Get recommender results per user

    Returns:
        (JSON) user item data

    """
    json = request.json
    pair_id = json.get("pairid")
    filters = json.get("filters")
    # TODO implement backend filtering

    chunk_size = json.get("amount", 20)
    chunk_size = int(chunk_size)
    chosen_headers = json.get("optionalHeaders", [])
    dataset = json.get("dataset", "")
    sortIndex = json.get("sortindex", 0)

    # read mock dataframe
    recs = result_storage.current_recs[pair_id]

    #Add optional columns to the dataframe (if any)
    if (len(chosen_headers) > 0):
      recs=add_dataset_columns(dataset, recs, chosen_headers)

    
    #Make sure not to sort on a column that does not exist anymore
    if (len(recs.columns) <= sortIndex):
        sortIndex = 0
    ##sort dataframe based on index and ascending or not
    df_sorted = recs.sort_values(by=recs.columns[sortIndex], ascending=json.get("ascending"))

    
    # getting only chunk of data
    start_rows = json.get("start", 0)
    start_rows = int(start_rows)
    end_rows = start_rows + chunk_size
    end_rows = int(end_rows)

    # determine if at the end of the dataset
    rows_number = len(df_sorted)
    if end_rows > rows_number:
        end_rows = rows_number

    # return part of table that should be shown
    df_subset = df_sorted[start_rows:end_rows]
    return df_subset.to_json(orient='records')

def add_dataset_columns(dataset_name, dataframe, columns):
    dataset = recommender_system.data_registry.get_set(dataset_name)
    if dataset is None:
        return dataframe

    result = list(map(lambda column: column.lower(), columns))
    matrix_name = 'movies' # TODO
    dataframe = add_dataset_columns(dataset, matrix_name, dataframe, result)
    #dataframe = add_item_columns(dataset, dataframe, result)
    #dataframe = add_user_columns(dataset, dataframe, result)
    return dataframe

@results_bp.route('/headers', methods=['GET'])
def headers():
    """Get available dataset headers

    Returns:
        (JSON) all available header options

    """
    return result_storage.load_json('project/headers.json')
