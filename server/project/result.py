"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from .computation import options
from flask import (Blueprint, request)
import pandas as pd
import json as Jason

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


    filters = options['filters']


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
    response = {'status': 'success', 'availableFilters' : filters}
    print(response)
    return response


## get recommender results per user
@result_bp.route('/result', methods=['POST'])
def user_result():
    json = request.json
    chunksize = json.get("amount", 20)
    chunksize = int(chunksize)

    ##read mock dataframe
    recs = result_storage.current_recs

    ##sort dataframe based on index and ascending or not
    df_sorted = recs.sort_values(by=recs.columns[json.get("sortindex", 0)], ascending=json.get("ascending"))

    # getting only chunk of data
    startrows = json.get("start", 0)
    startrows = int(startrows)
    endrows = startrows + chunksize
    endrows = int(endrows)

    # determine if at the end of the dataset
    columns_number = len(df_sorted)
    if endrows > columns_number:
        endrows = columns_number

    # return part of table that should be shown
    df_subset = df_sorted[startrows:endrows]

    # return {'results': dfSubset.to_json(orient='records'), 'caption': 'hellofriend'}
    return df_subset.to_json(orient='records')

