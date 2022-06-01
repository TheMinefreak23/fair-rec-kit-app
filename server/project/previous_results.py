"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json
from logging import root

from flask import (Blueprint, request)
import pandas as pd
from fairreckitlib.data.set.dataset import add_dataset_columns as add_data_columns

from . import result_storage
from .experiment import add_validation, options, recommender_system

#from fairreckitlib.data.filter.filter_factory import create_filter_factory
#from fairreckitlib.data.filter.filter_constants import *


results_bp = Blueprint('results', __name__, url_prefix='/api/all-results')


def filter_results(dataframe, filters):
    """Filter a dataframe with results using specified filters

    Args:
        dataframe: a dataframe containing results that need to be filtered
        filters: an array that contains filters

    Returns:
        results after filtering
    """
    #filter = fairreckitlib.data.filter
    #filter(dataframe, filters)

    return dataframe



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
    path = result_storage.get_overview(result_id, run_id)[
        pair_id]['ratings_path']
    result_storage.current_recs[pair_id] = pd.read_csv(
        path, sep='\t', header=0)
    return {'status': 'success', 'availableFilters': options['filters']}


# get recommender results per user
@results_bp.route('/result', methods=['POST'])
def user_result():
    """"Get recommender results per user

    Returns:
        (JSON) user item data

    """
    json = request.json
    pair_id = json.get("pairid")
    filters = json.get("filters")

    chunk_size = json.get("amount", 20)
    chunk_size = int(chunk_size)
    chosen_headers = json.get("optionalHeaders", [])
    matrix_name = json.get("matrix")
    dataset_name = json.get("dataset", "")
    sortIndex = json.get("sortindex", 0)

    # read mock dataframe
    recs = result_storage.current_recs[pair_id]
    dataset = recommender_system.data_registry.get_set(dataset_name)

    #TODO refactor/do dynamically
    spotify_datasets = ['LFM-2B']
    if dataset_name in spotify_datasets:
        recs=add_spotify_columns(dataset_name, recs)

    recs = filter_results(recs, filters)

    #Add optional columns to the dataframe (if any)
    if (len(chosen_headers) > 0):
      recs=add_dataset_columns(dataset_name, recs, chosen_headers, matrix_name)

    #Make sure not to sort on a column that does not exist anymore
    if (len(recs.columns) <= sortIndex):
        sortIndex = 0
    # sort dataframe based on index and ascending or not
    df_sorted = recs.sort_values(
        by=recs.columns[sortIndex], ascending=json.get("ascending"))

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

    # rename the user and item headers so they reflect their respective content
    item = dataset.get_matrix_config(matrix_name).item.key
    user = dataset.get_matrix_config(matrix_name).user.key
    df_subset.rename(columns = {'user': user, 'item': item}, inplace = True)
    return df_subset.to_json(orient='records')

def add_dataset_columns(dataset_name, dataframe, columns, matrix_name):
    #print(dataset_name)
    dataset = recommender_system.data_registry.get_set(dataset_name)
    if dataset is None:
        return dataframe

    result = list(map(lambda column: column.lower(), columns))
    dataframe = add_data_columns(dataset, matrix_name, dataframe, result)
    #dataframe = add_user_columns(dataset, dataframe, result)
    #print(dataframe.head())
    return dataframe


@results_bp.route('/headers', methods=['POST'])
def headers():
    json = request.json
    dataset_name = json.get("name")
    dataset = recommender_system.data_registry.get_set(dataset_name)
    for matrix_name in dataset.get_available_matrices():
        columns = dataset.get_available_columns(matrix_name)
    #return result_storage.load_json('project/headers.json')[dataset_name]
    return columns

# test
def add_spotify_columns(dataset_name, dataframe):
    dataset = recommender_system.data_registry.get_set(dataset_name)
    matrix_name = 'user-track-count'
    columns = ['track_id', 'track_spotify-uri']
    dataframe = add_data_columns(dataset, matrix_name, dataframe, columns)
    print(dataframe.head())
    return dataframe

@results_bp.route('/export', methods=['POST'])
def export(): 
    #Load results from json
    json = request.json
    results = json.get('results', '{}')
    
    #Load the file selector
    import tkinter as tk
    from tkinter.filedialog import asksaveasfilename
    root = tk.Tk()

    #Focus on the file selector and hide the overlay
    root.overrideredirect(True)
    root.geometry('0x0+0+0')
    root.deiconify()
    root.lift()
    root.focus_force()
    tk.Tk().withdraw()

    data = [('tsv', '*.tsv')]
    try:
        fn = asksaveasfilename(initialdir='/', title='Export Table', filetypes=data, defaultextension='.tsv', initialfile="experiment", parent=root)
        df = pd.DataFrame(results)
        df.to_csv(fn, index=False)
        return {'message' : 'Exported succesfully'}
    except:
        return {'message' : 'Export cancelled'}
    

@results_bp.route('/validate', methods=['POST'])
def validate(): 
    json = request.json
    filepath = json.get('filepath')
    amount = json.get('amount', 1)
    add_validation(filepath, amount)
    return "Validated"
