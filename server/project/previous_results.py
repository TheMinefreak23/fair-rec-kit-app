"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json

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


# Set current shown recommendations
@results_bp.route('/set-recs', methods=['POST'])
def set_recs():
    json = request.json
    result_id = json.get("id")  # Result timestamp TODO use to get result
    print(result_id)

    # Get random mockdata for now TODO
    filepaths = ['mock/1647818279_HelloWorld/1647818279_run_0/LFM-360K_0/Foo_ALS_0/ratings.tsv',
                 'mock/1649162862_HelloFRK/run_0/LFM-1B_0/Implicit_AlternatingLeastSquares_0/ratings.tsv',
                 'mock/1649162862_HelloFRK/run_0/LFM-1B_0/LensKit_PopScore_0/ratings.tsv',
                 'mock/1649162862_HelloFRK/run_0/LFM-360K_0/Implicit_AlternatingLeastSquares_0/ratings.tsv',
                 'mock/1649162862_HelloFRK/run_0/LFM-360K_0/LensKit_PopScore_0/ratings.tsv']
    import random
    random_file = random.choice(filepaths)
    print(random_file)
    result_storage.current_recs = pd.read_csv(random_file, sep='\t', header=None)
    return {'status': 'success'}


## get recommender results per user
@results_bp.route('/result', methods=['POST'])
def user_result():
    json = request.json
    chunk_size = json.get("amount", 20)
    chunk_size = int(chunk_size)
    print(json.get("generalHeaders", []))
    chosen_headers = json.get("generalHeaders", []) + json.get("userheaders", []) + json.get("itemheaders", [])
    chosen_headers2 = []

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

    # return {'results': dfSubset.to_json(orient='records'), 'caption': 'hellofriend'}
    return df_subset.to_json(orient='records')

@results_bp.route('/headers', methods=['GET'])
def headers():
    with open('project/headers.json') as j:
        jsonfile = json.load(j)

    result = jsonfile['LFM-1B']
    j.close()

    print(result)

    return result


