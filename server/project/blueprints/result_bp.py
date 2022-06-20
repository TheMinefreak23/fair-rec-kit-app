"""This module has functions for retrieval of a specific result.

Methods:
    filter_results
    get_chunk
    rename_headers
    add_dataset_columns
    add_spotify_columns

blueprint routes:
    set_recs
    set_result
    user_result
    headers
    export
    validate

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json
import copy
from flask import (Blueprint, request)
import pandas as pd
from fairreckitlib.data.set.dataset import add_dataset_columns as add_data_columns

from project.models import result_loader, \
    result_store, options_formatter, \
    recommender_system, queue
from project.models.result_loader import result_by_id

blueprint = Blueprint('result', __name__, url_prefix='/api/result')


def filter_results(dataframe, filters):
    """Filter a dataframe with results using specified filters.

    Args:
        dataframe: a dataframe containing results that need to be filtered
        filters: an array that contains filters

    Returns:
        results after filtering
    """
    # filter = fairreckitlib.data.filter
    # filter(dataframe, filters)
    # todo: filter
    print('TODO do something with the filters: ', filters)
    return dataframe


# Set current shown recommendations
@blueprint.route('/set-recs', methods=['POST'])
def set_recs():
    """Set the recommendations for the current shown result.

    Returns:
        (JSON) A status message and the possible filters for this dataset
    """
    json_data = request.json
    result_id = json_data.get("id")  # Result timestamp TODO use to get result
    run_id = json_data.get("runid")
    pair_id = json_data.get("pairid")
    path = result_loader.get_overview(result_id, run_id)[
        pair_id]['ratings_path']
    # Declare current_recs as a dictionary in a dictionary
    if not run_id in result_store.current_recs:
        result_store.current_recs[run_id] = {}
    # Load the correct ratings file
    result_store.current_recs[run_id][pair_id] = pd.read_csv(
        path, sep='\t', header=0)
    return {'status': 'success', 'availableFilters': options_formatter.options['filters']}


@blueprint.route('/result-by-id', methods=['POST', 'GET'])
def set_result():
    """Retrieve a requested result by its ID.

    Returns:
        (JSON) The result that belongs to the requested ID
    """
    if request.method == 'POST':
        data = request.get_json()
        print('result_by_id data', data)
        result_by_id(int(data['id']), result_store)
        if result_store.current_result:
            response = {'status': 'success'}
        else:
            response = {'status': 'result not found'}

    else:  # GET request
        print('current result', json.dumps(
            result_store.current_result, indent=4))
        response = {'result': result_store.current_result}

    return response


@blueprint.route('/', methods=['POST'])
def user_result():
    """Get recommender results per user for the shown result.

    Returns:
        (JSON) user item data

    """
    json_data = request.json
    pair_id = json_data.get("pairid")
    run_id = json_data.get("runid")

    chunk_size = int(json_data.get("amount", 20))
    chosen_headers = json_data.get("optionalHeaders", [])
    matrix_name = json_data.get("matrix" "")
    dataset_name = json_data.get("dataset", "")
    sort_index = json_data.get("sortindex", 0)

    #Load the current recs from the storage (without changing the original)
    recs = copy.deepcopy(result_store.current_recs[run_id][pair_id])

    #TODO refactor/do dynamically
    spotify_datasets = ['LFM-2B']
    if dataset_name in spotify_datasets:
        recs = add_spotify_columns(dataset_name, recs)

    #recs = filter_results(recs, filters)
    #Add optional columns to the dataframe (if any)
    if len(chosen_headers) > 0:
        recs=add_dataset_columns(dataset_name, recs, chosen_headers, matrix_name)
    #Make sure not to sort on a column that does not exist anymore
    if len(recs.columns) <= sort_index:
        sort_index = 0
    # sort dataframe based on index and ascending or not
    df_sorted = recs.sort_values(
        by=recs.columns[sort_index], ascending=json_data.get("ascending"))

    df_subset = get_chunk(int(json_data.get("start", 0)),
                          chunk_size,
                          df_sorted)

    rename_headers(dataset_name, matrix_name, df_subset)

    return df_subset.to_json(orient='records')


def get_chunk(start_rows, chunk_size, df_sorted):
    """Get a chunk of a dataframe.

    Args:
        start_rows: rows to start at
        chunk_size: size of the rows chunk
        df_sorted: the sorted dataframe to get the chunk from

    Returns:
        The part of the dataframe
    """
    # getting only chunk of data
    end_rows = start_rows + chunk_size
    end_rows = int(end_rows)

    # determine if at the end of the dataset
    rows_number = len(df_sorted)
    end_rows = min(end_rows, rows_number)

    # return part of table that should be shown
    return df_sorted[start_rows:end_rows]


def rename_headers(dataset_name, matrix_name, df_subset):
    """Rename the user and item headers, so they reflect their respective content.

    Args:
        dataset_name: the name of the dataset of the matrix
        matrix_name: the matrix name of the matrix with the headers
        df_subset: the dataframe with the headers

    """
    dataset = recommender_system.data_registry.get_set(dataset_name)
    if not dataset is None and not dataset.get_matrix_config(matrix_name) is None:
        item = dataset.get_matrix_config(matrix_name).item.key
        user = dataset.get_matrix_config(matrix_name).user.key
        df_subset.rename(columns={'user': user, 'item': item}, inplace=True)


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


@blueprint.route('/headers', methods=['POST'])
def headers():
    """Load the optional headers for the requested dataset.

    Returns:
       (JSON) A list of the available headers for this dataset
    """
    json_data = request.json
    dataset_name = json_data.get("name")
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
    columns = []
    dataframe = add_data_columns(dataset, matrix_name, dataframe, columns)
    print(dataframe.head())
    return dataframe

@blueprint.route('/validate', methods=['POST'])
def validate():
    """Give the server the task of running a requested experiment again.

    Returns:
        A message indicating the operation was succesful
    """
    json_data = request.json
    filepath = json_data.get('filepath')
    amount = int(json_data.get('amount', 1))
    queue.add_validation(filepath, amount)
    return "Validated"
