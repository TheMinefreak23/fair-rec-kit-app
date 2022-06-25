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
import copy
from flask import (Blueprint, request)
import pandas as pd

from project.blueprints.constants import BAD_REQUEST_RESPONSE
from project.models import result_loader, \
    result_store, \
    recommender_system, queue
from project.models.options_formatter import make_filter_option
from project.models.result_loader import result_by_id, add_dataset_columns, \
    get_chunk, rename_headers, \
    id_to_index, ADDITIONAL_COLUMNS, sort_headers, filter_results
from project.models.result_storage import load_results_overview

blueprint = Blueprint('result', __name__, url_prefix='/api/result')


@blueprint.route('/set-recs', methods=['POST'])
def set_recs():
    """Set the recommendations for the current shown result.

    Returns:
        (JSON) A status message and the possible filters for this dataset
    """
    # Get POST request data
    try:
        result_id = request.json['id']  # Result timestamp
        run_id = request.json['runid']
        pair_id = request.json['pairid']
    except KeyError:
        return BAD_REQUEST_RESPONSE

    path = result_loader.get_overview(result_id, run_id)[
        pair_id]['ratings_path']
    # TODO REMOVE WHEN LIB IS UP TO DATE: TEMPORARY FIX
    path = path.replace('\\', '/')
    # Declare current_recs as a dictionary in a dictionary
    if not run_id in result_store.current_recs:
        result_store.current_recs[run_id] = {}
    # Load the correct ratings file
    result_store.current_recs[run_id][pair_id] = pd.read_csv(
        path, sep='\t', header=0)
    return {'status': 'success'}


@blueprint.route('/filters', methods=['POST'])
def available_filters():
    """Get the available filters based on the dataset and matrix.

    Returns:
        (dict) the available filters
    """
    json_data = request.json
    dataset_name = json_data.get("dataset", "")
    matrix_name = json_data.get("matrix", "")
    filters = recommender_system.get_available_data_filters()[dataset_name][matrix_name]
    formatted_filters = make_filter_option(filters)
    # print('== FILTERS == ', dataset_name, matrix_name, ': ', formatted_filters['options'])
    return {'filters': formatted_filters['options']}


@blueprint.route('/result-by-id', methods=['POST', 'GET'])
def set_result():
    """Retrieve a requested result by its ID.

    Returns:
        (JSON) The result that belongs to the requested ID
    """
    if request.method == 'POST':
        try:
            result_id = request.json['id']
        except KeyError:
            return BAD_REQUEST_RESPONSE

        result_by_id(int(result_id), result_store)
        if result_store.current_result:
            response = {'status': 'success'}
        else:
            response = {'status': 'result not found'}

    else:  # GET request
        response = {'result': result_store.current_result}

    return response


@blueprint.route('/', methods=['POST'])
def user_result():
    """Get recommender results per user for the shown result.

    Returns:
        (JSON) user item data

    """
    json_data = request.json
    # Get required request data
    try:
        pair_id = json_data['pairid']
        run_id = json_data['runid']
    except KeyError:
        return BAD_REQUEST_RESPONSE

    matrix_name = json_data.get('matrix', '')
    dataset_name = json_data.get('dataset', '')

    # Load the current recs from the storage (without changing the original)
    recs = copy.deepcopy(result_store.current_recs[run_id][pair_id])

    recs = filter_results(recs, dataset_name, matrix_name, json_data.get("filters", []))

    # Add optional columns to the dataframe (if any)
    chosen_headers = json_data.get("optionalHeaders", [])
    if len(chosen_headers) > 0:
        recs = add_dataset_columns(
            dataset_name, recs, chosen_headers, matrix_name)

    # Sort rows
    # Make sure not to sort on a column that does not exist anymore
    sort_index = json_data.get("sortindex", 0)
    if len(recs.columns) <= sort_index:
        sort_index = 0
    # Sort dataframe based on index and ascending or not
    df_sorted = recs.sort_values(
        by=recs.columns[sort_index], ascending=json_data.get("ascending"))

    chunk_size = int(json_data.get("amount", 20))
    df_subset = get_chunk(int(json_data.get("start", 0)),
                          chunk_size,
                          df_sorted)

    rename_headers(dataset_name, matrix_name, df_subset)

    sort_headers(df_subset)

    print(df_subset.head())

    return df_subset.to_json(orient='records')


@blueprint.route('/headers', methods=['POST'])
def headers():
    """Load the optional headers for the requested dataset.

    Returns:
       (JSON) A list of the available headers for this dataset
    """
    try:
        dataset_name = request.json['dataset']
        matrix_name = request.json['matrix']
    except KeyError:
        return BAD_REQUEST_RESPONSE

    columns = {}
    dataset = recommender_system.data_registry.get_set(dataset_name)
    if dataset:
        columns = dataset.get_available_columns(matrix_name)

    if matrix_name in ADDITIONAL_COLUMNS:
        columns.update(ADDITIONAL_COLUMNS[matrix_name])

    return columns


@blueprint.route('/validate', methods=['POST'])
def validate():
    """Give the server the task of running a requested experiment again.

    Returns:
        A message indicating the operation was succesful
    """
    json_data = request.json
    try:
        file_path = request.json['filepath']
        result_id = request.json['ID']
    except KeyError:
        return BAD_REQUEST_RESPONSE

    overview = load_results_overview()
    overview_index = id_to_index(overview, result_id)
    result = overview['all_results'][overview_index]
    amount = int(json_data.get('amount', 1))
    queue.add_validation(overview_index, file_path, amount, result)
    queue.run_first()
    return "Validated"
