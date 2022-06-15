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
# import pandas as pd
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

            # TODO REMOVE WHEN LIB IS UP TO DATE: TEMPORARY FIX
            evaluation_path_full = evaluation_path_full.replace('\\', '/')

            # ratings_settings_path_full = os.getcwd() + "/" + \
            #    pair_data['ratings_settings_path']

            if os.path.exists(evaluation_path_full):
                evaluation_data = load_json(evaluation_path_full)
                # TODO ratings_settings still needs to go somewhere
                # ratings_settings_data = pd.read_csv(
                #    ratings_settings_path_full,
                #    sep='\t',
                #    header=None).to_dict(orient='records')
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
    # print('current result', json.dumps(current_result, indent=4))


# TODO: refactor: use in result_by_id?
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
    # rec_paths = []
    # for index in range(0, len(run_overview['overview'])):
    #    rec_paths[index] = run_overview['overview'][pairid]['ratings_path']
    # return rec_paths


def add_evaluation(data, evaluation):
    """
    Add an evaluation to the data.
    """
    # todo: refactor docstring
    if not evaluation:
        return data
    if not data:
        return format_evaluation(evaluation)
    for index, value in enumerate(evaluation):
        data[index]['evaluations'].append(value['evaluation'])
    return data


def format_evaluation(evaluation):
    """Format an evaluation to be used in the current_result."""
    # todo: refactor docstring
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
            # print('==ID TO INDEX',
            # 'ID',result_id,'INDEX',
            # iteration_id,
            # 'NAME',
            # data['metadata']['name'])
    return current_result_overview_id


def name_to_index(json_data, name, key, by_name=False):
    """Returns the index of the entry in results_overview
    of a specific dataset-recommender approach pair.

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
