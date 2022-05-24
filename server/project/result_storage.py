"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import csv  # TODO fix this import
import json
import os
from os import walk
from csv import writer
import time
import datetime
import pandas as pd

# Global current result variables
current_result = {}
current_recs = {}

# Storage paths
RESULTS_ROOT_FOLDER = 'results/'
RESULTS_OVERVIEW_PATH = RESULTS_ROOT_FOLDER + 'results_overview.json'


def save_result(experiment, result):
    """Save result to overview.

    Args:
        experiment(dict): the experiment settings
        result(dict): the computed result
    """
    global current_result
    experiment['result'] = result

    current_result = experiment
    add_result(current_result)
    print(current_result)


def old_result_by_id(result_id):
    results = load_results_overview()
    global current_result

    # Filter: Loop through all results and find the one with the matching ID.
    for result in results['all_results']:
        if 'timestamp' in result:
            if result['timestamp']['stamp'] == result_id:
                print('result', result)
                current_result = result
        else:
            current_result = None  # If there is an incorrectly formatted result, return nothing


def old_result_by_id2(result_id):
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

    #calculation_id = results_overview['all_results'][result_id]['timestamp']['stamp']
    calculation_id = result_id # TODO replace calculation_id with result_id?
    current_name = id_to_name(results_overview, calculation_id)
    relative_path = results_root_folder + str(calculation_id) + "_" + current_name
    data = {'id': result_id, 'name': current_name, 'runs': []}
    # loops through all the subdirectories, and thus - runs, of a certain calculation
    for subdir in [f.path for f in os.scandir(relative_path) if f.is_dir()]:
        run_overview_name = os.path.basename(os.path.normpath(subdir))
        run_overview = load_json(subdir + "/overview.json")
        run_data = {'index': run_overview_name, 'results': []}
        # loops through individual results
        for run_result in run_overview['overview']:
            evaluation_path_full = os.getcwd() + "\\" + run_result['evaluation_path']
            ratings_settings_path_full = os.getcwd() + "\\" + run_result['ratings_settings_path']
            print(evaluation_path_full)
            evaluation_data = {}
            if os.path.exists(evaluation_path_full):
                evaluation_data = load_json(evaluation_path_full)
            ratings_settings_data = pd.read_csv(
                ratings_settings_path_full,
                sep='\t',
                header=None).to_dict(orient='records')
            result_data = {
                'name': run_result['name'],
                'dataset': run_result['dataset'],
                'recommender_system': run_result['recommender_system'],
                'evaluations': evaluation_data,
                'ratings_settings': ratings_settings_data}
            run_data['results'].append(result_data)

        data['runs'].append(run_data)

    global current_result
    current_result = data

    # print('current result',current_result)

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

    #calculation_id = results_overview['all_results'][result_id]['timestamp']['stamp']
    calculation_id = result_id # TODO replace calculation_id with result_id?
    current_name = id_to_name(results_overview, calculation_id)
    current_index = id_to_index(results_overview, calculation_id)
    relative_path = results_root_folder + str(calculation_id) + "_" + current_name
    data = results_overview['all_results'][current_index]
    print(data)
    # loops through all the subdirectories, and thus - runs, of a certain calculation
    for subdir in [f.path for f in os.scandir(relative_path) if f.is_dir()]:
        run_overview_name = os.path.basename(os.path.normpath(subdir))
        run_index = int(run_overview_name[-1])
        run_overview = load_json(subdir + "/overview.json")
        # loops through individual results
        for pair_id in range(len(run_overview['overview'])):
            evaluation_path_full = os.getcwd() + "\\" + run_overview['overview'][pair_id]['evaluation_path']
            ratings_settings_path_full = os.getcwd() + "\\" + run_overview['overview'][pair_id]['ratings_settings_path']
            print(evaluation_path_full)
            evaluation_data = {}
            if os.path.exists(evaluation_path_full):
                evaluation_data = load_json(evaluation_path_full)
            print('evaluation data', evaluation_data)
            ratings_settings_data = pd.read_csv(
                ratings_settings_path_full,
                sep='\t',
                header=None).to_dict(orient='records') # TODO ratings_settings still needs to go somewhere
            dataset_index = name_to_index(data['result'], run_overview['overview'][pair_id]['dataset'], 'dataset', True)
            print('name from overview', run_overview['overview'][pair_id]['dataset'])
            print('dataset index', dataset_index)
            approach_index = name_to_index(
                data['result'][dataset_index]['recs'],
                run_overview['overview'][pair_id]['recommender_system'], 'approach')
            print('name from overview', run_overview['overview'][pair_id]['recommender_system'])
            print('approach index', approach_index)
            data['result'][dataset_index]['recs'][approach_index]['evals'] = evaluation_data['evaluations'] if evaluation_data else []


    global current_result
    current_result = data
    #print('current result', json.dumps(current_result, indent=4))


def get_overview(evaluation_id, runid):
    results_overview = load_results_overview()
    # TODO DEV: Mock
    if evaluation_id == 0:
        results_overview = load_json('mock/results_overview.json')

    name = id_to_name(results_overview, evaluation_id)

    # TODO DEV: Mock
    results_root_folder = RESULTS_ROOT_FOLDER
    if evaluation_id == 0:
        results_root_folder = 'mock/'

    relative_path = results_root_folder + str(evaluation_id) + "_" + name + "/" + "run_" + str(runid)
    overview_path = relative_path + "/overview.json"
    run_overview = load_json(overview_path)
    return run_overview['overview']
    #rec_paths = []
    #for index in range(0, len(run_overview['overview'])):
    #    rec_paths[index] = run_overview['overview'][pairid]['ratings_path']
    #return rec_paths
        


def id_to_name(json_data, result_id):
    return json_data['all_results'][id_to_index(json_data, result_id)]['metadata']['name']

def id_to_index(json_data, result_id):
    current_result_overview_id = -1
    # Filter: Loop through all results and find the one with the matching ID.
    for iteration_id in range(len(json_data['all_results'])):
        if int(json_data['all_results'][iteration_id]['timestamp']['stamp']) == int(result_id):
            current_result_overview_id = iteration_id
    return current_result_overview_id

def name_to_index(json_data, name, key, by_name = False):
    current_index = -1
    print('json_data',json_data)
    for i in range(len(json_data)):
        print(json_data[i][key],'==',name,'?',json_data[i][key] == name)
        result_value = json_data[i][key]
        if by_name and result_value['name'] == name or result_value == name:
            current_index = i
    return current_index

def load_json(path):
    """Load a JSON file to a dictionary using its path.

    Args:
        path(string): the path to the JSON file
    Returns:
        (dict) the JSON as a dictionary
    """
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)  # Load existing data into a dict.


def load_results_overview():
    """Load the results overview.

    Returns:
        (dict) the loaded results
    """
    # Ensure the results overview exists.
    create_results_overview()
    return load_json(RESULTS_OVERVIEW_PATH)


def write_results_overview(results):
    """Write (store) results to the overview.

    Args:
        results(dict): the results to store
    """
    # Open the file in write mode.
    with open(RESULTS_OVERVIEW_PATH, 'w', encoding='utf-8') as file:
        # Store it as json data.
        json.dump(results, file, indent=4)


def add_result(result):
    """Add a result at the end of the results overview.

    Args:
        result(dict): the (new) result
    """
    file_results = load_results_overview()
    file_results['all_results'].append(result)
    write_results_overview(file_results)


def delete_result(result_id):
    """Delete a result by its id.

    Args:
        index(int): the index of the result
    """
    file_results = load_results_overview()
    # Remove from list
    file_results['all_results'] = [
        result for result in file_results['all_results']
        if result['timestamp']['stamp'] != result_id
    ]
    # TODO delete actual result
    write_results_overview(file_results)


def edit_result(index, new_name, new_tags, new_email):
    """Edit a result.

    Args:
        index(int): the result index
        new_name(string): the new metadata name of the result
        new_tags(string): the new metadata tags of the result
        new_email(string): the new metadata email of the result
    """
    file_results = load_results_overview()
    to_edit_result = file_results['all_results'][index]
    print(new_tags)

    def edit_metadata(attr, new_val):
        # Don't change the attribute if the input field has been left empty
        if new_val != '':
            to_edit_result['metadata'][attr] = new_val
            print('changed '+attr, to_edit_result['metadata'][attr])

    for (data_name, new_data) in [('name', new_name), ('tags', new_tags), ('email', new_email)]:
        edit_metadata(data_name, new_data)

    # TODO Add more editable values
    file_results['all_results'][index] = to_edit_result

    write_results_overview(file_results)


def create_results_overview():
    """Create a results file if it doesn't exist yet or is empty."""
    if not os.path.exists(RESULTS_ROOT_FOLDER):
        os.mkdir(RESULTS_ROOT_FOLDER)
    if not os.path.exists(RESULTS_OVERVIEW_PATH) or os.stat(RESULTS_OVERVIEW_PATH).st_size == 0:
        with open(RESULTS_OVERVIEW_PATH, 'w', encoding='utf-8') as file:  # Open the file in write mode.
            json.dump({'all_results': []}, file, indent=4)


def parse_tags(tags_string):
    """Parse result tags (given by user as metadata)

    Args:
        tags_string(string): the tags as raw string input (comma-separated)

    Returns:
        the split list of tags
    """
    # Split tags by comma and get the unique tags
    unique = list(set(tags_string.split(',')))
    # Remove empty tags
    return [tag for tag in unique if tag]
