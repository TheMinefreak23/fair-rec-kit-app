"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json

from flask import (Blueprint, request)
import pandas as pd
from fairreckitlib.data.set.dataset import add_dataset_columns as add_data_columns

from . import result_loader
from . import result_storage
from .experiment import options, recommender_system, add_validation

result_bp = Blueprint('result', __name__, url_prefix='/api/result')


def filter_results(dataframe, filters):
    """Filter a dataframe with results using specified filters.

    Args:
        dataframe: a dataframe containing results that need to be filtered
        filters: an array that contains filters

    Returns:
        results after filtering
    """
    #filter = fairreckitlib.data.filter
    #filter(dataframe, filters)

    return dataframe


# Set current shown recommendations
@result_bp.route('/set-recs', methods=['POST'])
def set_recs():
    """Set the recommendations for the current shown result.
    
    Returns:
        (JSON) A status message and the possible filters for this dataset
    """
    json = request.json
    result_id = json.get("id")  # Result timestamp TODO use to get result
    run_id = json.get("runid")
    pair_id = json.get("pairid")
    path = result_loader.get_overview(result_id, run_id)[
        pair_id]['ratings_path']
    # Declare current_recs as a dictionary in a dictionary
    if not run_id in result_storage.current_recs:
        result_storage.current_recs[run_id] = {}
    # Load the correct ratings file
    result_storage.current_recs[run_id][pair_id] = pd.read_csv(
        path, sep='\t', header=0)
    return {'status': 'success', 'availableFilters': options['filters']}


@result_bp.route('/result-by-id', methods=['POST', 'GET'])
def result_by_id():
    """Retrieve a requested result by its ID.
    
    Returns:
        (JSON) The result that belongs to the requested ID
    """
    if request.method == 'POST':
        data = request.get_json()
        print('result_by_id data', data)
        result_loader.result_by_id(int(data['id']))
        if result_storage.current_result:
            response = {'status': 'success'}
        else:
            response = {'status': 'result not found'}

    else:  # GET request
        print('current result', json.dumps(result_storage.current_result, indent=4))
        response = {'result': result_storage.current_result}

    return response


# get recommender results per user
@result_bp.route('/', methods=['POST'])
def user_result():
    """"Get recommender results per user for the shown result.

    Returns:
        (JSON) user item data

    """
    json = request.json
    pair_id = json.get("pairid")
    run_id = json.get("runid")
    filters = json.get("filters", [])

    chunk_size = int(json.get("amount", 20))
    chosen_headers = json.get("optionalHeaders", [])
    matrix_name = json.get("matrix" "")
    dataset_name = json.get("dataset", "")
    sortIndex = json.get("sortindex", 0)

    # read mock dataframe
    recs = result_storage.current_recs[run_id][pair_id]
    dataset = recommender_system.data_registry.get_set(dataset_name)
    #TODO refactor/do dynamically
    spotify_datasets = ['LFM-2B']
    if dataset_name in spotify_datasets:
        recs = add_spotify_columns(dataset_name, recs)

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
    start_rows = int(json.get("start", 0))
    end_rows = start_rows + chunk_size
    end_rows = int(end_rows)

    # determine if at the end of the dataset
    rows_number = len(df_sorted)
    if end_rows > rows_number:
        end_rows = rows_number

    # return part of table that should be shown
    df_subset = df_sorted[start_rows:end_rows]

    # rename the user and item headers so they reflect their respective content
    if not dataset is None and not dataset.get_matrix_config(matrix_name) is None:
        item = dataset.get_matrix_config(matrix_name).item.key
        user = dataset.get_matrix_config(matrix_name).user.key
        df_subset.rename(columns = {'user': user, 'item': item}, inplace = True)
    return df_subset.to_json(orient='records')


def add_dataset_columns(dataset_name, dataframe, columns, matrix_name):
    """Add columns to the requested result based on its dataset.

    Args:
        dataset_name: the name of dataset belonging to the dataframe
        dataframe: a pandas dataframe of the requested user results
        columns: the current list of columns
        matrix_name: the name of the matrix belonging to the dataframe

    Returns:
        The updated dataframe
    """
    dataset = recommender_system.data_registry.get_set(dataset_name)
    if dataset is None:
        return dataframe

    result = list(map(lambda column: column.lower(), columns))
    dataframe = add_data_columns(dataset, matrix_name, dataframe, result)
    # dataframe = add_user_columns(dataset, dataframe, result)
    # print(dataframe.head())
    return dataframe


@result_bp.route('/headers', methods=['POST'])
def headers():
    """Load the optional headers for the requested dataset.
    
    Returns:
       (JSON) A list of the available headers for this dataset
    """
    json = request.json
    dataset_name = json.get("name")
    columns = {}
    dataset = recommender_system.data_registry.get_set(dataset_name)
    if dataset:
        for matrix_name in dataset.get_available_matrices():
            columns = dataset.get_available_columns(matrix_name)
    return columns



def add_spotify_columns(dataset_name, dataframe):
    """Add columns from the Spotify integration to the dataframe.

    Args:
        dataset_name: the name of dataset belonging to the dataframe
        dataframe: a pandas dataframe of the requested user results
        

    Returns:
        The updated dataframe
    """
    dataset = recommender_system.data_registry.get_set(dataset_name)
    matrix_name = 'user-track-count'
    columns = ['track_id', 'track_spotify-uri']
    dataframe = add_data_columns(dataset, matrix_name, dataframe, columns)
    print(dataframe.head())
    return dataframe


@result_bp.route('/export', methods=['POST'])
def export():
    """Give the user the option to export the current shown results to a .tsv file.

    Returns:
        A message indicating if the export was succesful
    """
    #TODO rework this
    # Load results from json
    json = request.json
    results = json.get('results', '{}')

    # Load the file selector
    import tkinter as tk
    from tkinter.filedialog import asksaveasfilename
    root = tk.Tk()

    # Focus on the file selector and hide the overlay
    root.overrideredirect(True)
    root.geometry('0x0+0+0')
    root.deiconify()
    root.lift()
    root.focus_force()
    tk.Tk().withdraw()

    data = [('tsv', '*.tsv')]
    try:
        fn = asksaveasfilename(initialdir='/', title='Export Table', filetypes=data, defaultextension='.tsv',
                               initialfile="experiment", parent=root)
        df = pd.DataFrame(results)
        df.to_csv(fn, index=False)
        return {'message': 'Exported succesfully'}
    except:
        return {'message': 'Export cancelled'}


@result_bp.route('/validate', methods=['POST'])

def validate():
    """Give the server the task of running a requested experiment again.

    Returns:
        A message indicating the operation was succesful
    """
    json = request.json
    filepath = json.get('filepath') 
    amount = int(json.get('amount', 1))
    add_validation(filepath, amount)
    return "Validated"
