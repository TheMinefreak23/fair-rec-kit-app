
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
import pandas as pd
from .result_storage import RESULTS_ROOT_FOLDER, load_results_overview, load_json
from . import result_storage 


def result_by_id(result_id):
    """Set the current result to a result in the results overview by its id.

    Args:
    result_id(int): the result id
    """
    # TODO DEV
    results_overview = load_results_overview()
    results_root_folder = RESULTS_ROOT_FOLDER
    if result_id == 0:
        results_root_folder = 'mock/'
        results_overview = load_json(results_root_folder + "results_overview.json")
    relative_path = results_root_folder + str(result_id) + "_" + \
                    id_to_name(results_overview, result_id)
    data = results_overview['all_results'][id_to_index(results_overview, result_id)]
    # loops through all the subdirectories, and thus - runs, of a certain calculation
    for subdir in [f.path for f in os.scandir(relative_path) if f.is_dir()]:
        run_overview = load_json(subdir + "/overview.json")
        # loops through individual results by looping through each entry in the overview.json
        for pair_id, pair_data in enumerate(run_overview['overview']):
            evaluation_path_full = os.getcwd() + "\\" + \
                                   pair_data['evaluation_path']
            ratings_settings_path_full = os.getcwd() + "\\" + \
                                         pair_data['ratings_settings_path']

            if os.path.exists(evaluation_path_full):
                evaluation_data = load_json(evaluation_path_full)
                # TODO ratings_settings still needs to go somewhere
                ratings_settings_data = pd.read_csv(
                    ratings_settings_path_full,
                    sep='\t',
                    header=None).to_dict(orient='records')
                dataset_index = name_to_index(data['result'],
                                              run_overview['overview'][pair_id]['dataset'],
                                              'dataset', True)
                approach_index = name_to_index(
                    data['result'][dataset_index]['recs'],
                    run_overview['overview'][pair_id]['recommender_system'], 'approach')
                data['result'][dataset_index]['recs'][approach_index]['evals'] = evaluation_data[
                    'evaluations'] if evaluation_data else []

    result_storage.current_result = data


def get_overview(evaluation_id, runid):
    """Return a specific entry from a specific overview.json.

    Args:
    evaluation_id(int): the calculation id of the evaluation
    runid(int): the id of the specific dataset-recommender approach pair
    """
    results_overview = load_results_overview()
    # TODO DEV: Mock
    if evaluation_id == 0:
        results_overview = load_json('mock/results_overview.json')

    name = id_to_name(results_overview, evaluation_id)

    # TODO DEV: Mock
    results_root_folder = RESULTS_ROOT_FOLDER
    if evaluation_id == 0:
        results_root_folder = 'mock/'

    relative_path = results_root_folder + str(evaluation_id) + \
                    "_" + name + "/" + "run_" + str(runid)
    overview_path = relative_path + "/overview.json"
    run_overview = load_json(overview_path)
    return run_overview['overview']
    # rec_paths = []
    # for index in range(0, len(run_overview['overview'])):
    #    rec_paths[index] = run_overview['overview'][pairid]['ratings_path']
    # return rec_paths


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
            #print('==ID TO INDEX','ID',result_id,'INDEX',iteration_id,'NAME',data['metadata']['name'])
    return current_result_overview_id


def name_to_index(json_data, name, key, by_name=False):
    """Returns the index of the entry in results_overview
    of a specific dataset-recommender approach pair.

    Args:
    json_data(dict): the loaded json data from results_overview
    name(str): the name of the dataset or the name of the approach
    key(str): the object that the function should match on (either 'dataset' or 'recommender_system')
    """
    current_index = -1
    for i, data in enumerate(json_data):
        result_value = json_data[i][key]
        if by_name and result_value['name'] == name or result_value == name:
            current_index = i
    return current_index

