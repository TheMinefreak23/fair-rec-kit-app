"""This module contains functions to load & modify data from evaluation results.

methods:
    result_by_id
    get_overview
    id_to_name
    id_to_index
    name_to_index

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
from fairreckitlib.data.set.dataset import add_dataset_columns as add_data_columns

from . import recommender_system
from .constants import RESULTS_DIR
from .result_storage import load_results_overview, load_json


def result_by_id(result_id, result_storage):
    """Set the current result to a result in the results overview by its id.

    Args:
    result_id(int): the result id
    result_store(ResultStorage): the result storage with the current result
    """
    results_overview = load_results_overview()
    relative_path = RESULTS_DIR + str(result_id) + "_" + \
                    id_to_name(results_overview, result_id)
    data = results_overview['all_results'][id_to_index(
        results_overview, result_id)]
    data['metadata']['runs'] = 0  # Store runs
    # loops through all the subdirectories, and thus - runs, of a certain calculation
    for subdir in [f.path for f in os.scandir(relative_path) if f.is_dir()]:
        run_overview = load_json(subdir + "/overview.json")
        # loops through individual results by looping through each entry in the overview.json
        for pair_id, pair_data in enumerate(run_overview['overview']):
            evaluation_path_full = os.getcwd() + "/" + \
                                   pair_data['evaluation_path']

            if os.path.exists(evaluation_path_full):
                evaluation_data = load_json(evaluation_path_full)
                dataset_index = name_to_index(data['result'],
                                              run_overview['overview'][pair_id]['dataset'],
                                              'dataset', by_name=True)
                approach_index = name_to_index(
                    data['result'][dataset_index]['recs'],
                    run_overview['overview'][pair_id]['recommender_system'], 'approach')
                data['result'][dataset_index]['recs'][approach_index]['evals'] = add_evaluation(
                    data['result'][dataset_index]['recs'][approach_index]['evals'],
                    evaluation_data['evaluations'])
        data['metadata']['runs'] += 1

    result_storage.current_result = data

def get_overview(evaluation_id, runid):
    """Return a specific entry from a specific overview.json.

    Args:
    evaluation_id(int): the calculation id of the evaluation
    runid(int): the id of the specific dataset-recommender approach pair
    """
    results_overview = load_results_overview()

    name = id_to_name(results_overview, evaluation_id)

    relative_path = RESULTS_DIR + str(evaluation_id) + \
                    "_" + name + "/" + "run_" + str(runid)
    overview_path = relative_path + "/overview.json"
    run_overview = load_json(overview_path)
    return run_overview['overview']


def add_evaluation(data, evaluation):
    """Add an evaluation to the data."""
    if not evaluation:
        return data
    if not data:
        return format_evaluation(evaluation)
    for index, value in enumerate(evaluation):
        data[index]['evaluations'].append(value['evaluation'])
    return data


def format_evaluation(evaluation):
    """Format an evaluation to be used in the current_result."""
    for eval_item in evaluation:
        evaluation_list = [eval_item['evaluation']]
        eval_item.pop('evaluation')
        eval_item['evaluations'] = evaluation_list
    return evaluation


def id_to_name(json_data, result_id):
    """Return the name of a specific evaluation.

    args:
    json_data(dict): loaded json data from results_overview
    result_id(int): the id of the evaluation
    """
    return json_data['all_results'][id_to_index(json_data, result_id)]['metadata']['name']


def id_to_index(json_data, result_id):
    """Return the index of the entry in results_overview of a specific evaluation.

    args:
    json_data(dict): loaded json data from results_overview
    result_id(int): the id of the evaluation
    """
    current_result_overview_id = -1
    # Filter: Loop through all results and find the one with the matching ID.
    for iteration_id, data in enumerate(json_data['all_results']):
        if int(data['timestamp']['stamp']) == int(result_id):
            current_result_overview_id = iteration_id
    return current_result_overview_id


def name_to_index(json_data, name, key, by_name=False):
    """Return the index of the entry in results_overview of a dataset-recommender approach pair.

    Args:
    json_data(list): the loaded json data from results_overview
    name(str): the name of the dataset or the name of the approach
    key(str): the object that the function
                should match on (either 'dataset' or 'recommender_system')
    """
    current_index = -1
    for i, data in enumerate(json_data):
        result_value = data[key]
        if by_name and result_value['name'] == name or result_value == name:
            current_index = i
    return current_index


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
    return dataframe


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
