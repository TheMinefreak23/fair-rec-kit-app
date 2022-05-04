"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json

from flask import (Blueprint, request)
import pandas as pd

from . import result_storage

result_bp = Blueprint('result', __name__, url_prefix='/api/result')


@result_bp.route('/set-recs', methods=['POST'])
def set_recs():
    """
    Set current shown recommendations

    :return:
    """
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
@result_bp.route('/result', methods=['POST'])
def user_result():
    json = request.json
    chunk_size = json.get("amount", 20)
    chunk_size = int(chunk_size)

    chosen_headers = json.get("headers", []) + json.get("itemheaders", []) + json.get("userheaders", [])

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
        df_sorted[chosen_header] = 5

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
    mock_json = {
        "headers" : [
            { "name" : "general option 1"},
            { "name" : "general option 2"}

        ],

        "itemHeaders" : [
            { "name" : "item option 1"},
            { "name" : "item option 2"}
        ],

        "userHeaders" : [
            {"name": "user option 1"},
            {"name": "user option 2"}
        ]

    }

    result = json.dumps(mock_json)
    print(result)
    return result

