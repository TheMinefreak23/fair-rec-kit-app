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
        response = {'result' : result_storage.current_result}

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
  
## get recommender results per user
@results_bp.route('/result', methods=['POST'])
def user_result():
    json = request.json
    chunksize = json.get("amount", 20)
    chunksize = int(chunksize)

    ##read mock dataframe
    df = pd.read_csv('mock/1647818279_HelloWorld/1647818279_run_0/LFM-360K_0/Foo_ALS_0/ratings.tsv', sep='\t',
                            header=None)

    ##sort dataframe based on index and ascending or not
    dfSorted = df.sort_values(by=df.columns[json.get("sortindex",0)], ascending=json.get("ascending"))

    #getting only chunk of data
    startrows = json.get("start", 0)
    startrows = int(startrows)
    endrows= startrows + chunksize
    endrows = int(endrows)

    #determine if at the end of the dataset
    columns_number = len(dfSorted)
    if(endrows > columns_number):
        endrows = columns_number

    #return part of table that should be shown
    dfSubset = dfSorted[startrows:endrows]
    return dfSubset.to_json(orient='records')
