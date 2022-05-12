"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from flask import (Blueprint, request)
import pandas as pd

from . import result_storage
from .experiment import options

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
        print('data', data)
        result_storage.result_by_id(int(data['id']))
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


# Set current shown recommendations
@results_bp.route('/set-recs', methods=['POST'])
def set_recs():
    json = request.json
    result_id = json.get("id")  # Result timestamp TODO use to get result
    run_id = json.get("runid")
    pair_id = json.get("pairid")
    path = result_storage.get_rec_path(result_id, run_id, pair_id)
    #result_storage.current_recs = pd.read_csv(path, sep='\t', header=None)
    result_storage.current_recs = pd.read_csv('D:/GitHub/fair-rec-kit-app/server/mock/0_Foobar/run_0/ML-100K_0/LensKit_BiasedMF_0/ratings.tsv', sep='\t', header=0)
    result_storage.current_headers = result_storage.current_recs.columns
    for bruh in result_storage.current_recs.columns:
        print(bruh)
    print(result_storage.current_headers)
    return {'status': 'success', 'availableFilters' : options['filters']}


## get recommender results per user
@results_bp.route('/result', methods=['POST'])
def user_result():
    json = request.json

    filters = json.get("filters")
    #TODO implement backend filtering

    chunk_size = json.get("amount", 20)
    chunk_size = int(chunk_size)
    chosen_headers = json.get("generalHeaders", []) + json.get("userheaders", []) + json.get("itemheaders", [])

    #read mock dataframe
    recs = result_storage.current_recs
    if recs is None:
        set_recs()
        recs = result_storage.current_recs


    #TODO what if sorted on column that is removed?
    #TODO saving sorted dataframe inbetween
    ##sort dataframe based on index and ascending or not
    df_sorted = recs.sort_values(by=recs.columns[json.get("sortindex", 0)], ascending=json.get("ascending"))

    # adding extra columns to dataframe
    for chosen_header in chosen_headers:
        df_sorted[chosen_header['name']] = chosen_header['name']

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
    #return ({'headers': list(result_storage.current_headers),'table': df_subset.to_json(orient='records')})

@results_bp.route('/headers', methods=['POST'])
def headers():
    info = request.json
    index = info.get("index", 0)
    file = info.get("location", "")
    headers = result_storage.load_json('project/headers.json')
    overview = result_storage.load_json('../server/mock/' + file)    
    dataset = overview['overview'][index]['name'].split('_')[0]
    result = headers[dataset]
    return result
    # result = result_storage.current_recs.columns
    # return {'headers': list(result)}


