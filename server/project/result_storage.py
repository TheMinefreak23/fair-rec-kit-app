"""This module contains functions to load, save and modify data from the result overview.

methods:
    format_result
    save_result
    load_json
    load_results_overview
    write_results_overview
    add_result
    delete_result
    edit_result
    create_results_overview
    parse_tags

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from copy import deepcopy
import json
import os
import shutil

# Global current result variables
current_result = {}
current_recs = {}

# Storage paths
RESULTS_ROOT_FOLDER = 'results/'
RESULTS_OVERVIEW_PATH = RESULTS_ROOT_FOLDER + 'results_overview.json'


def format_result(settings):
    """Mock result experiment.

    Args:
        settings(dict): the experiment settings

    Returns: (list) the mock result
    """
    #print('== settings ==', settings)
    result = []
    datasets = settings['data']
    for (dataset_index, dataset) in enumerate(datasets):
        # Add dataset identifier to name
        dataset['name'] = dataset['dataset'] + '_' + dataset['matrix'] + '_' + str(dataset_index)
        recs = []
        for (api, approaches) in settings['models'].items():
            for (approach_index, approach) in enumerate(approaches):
                # Add approach, with index as identifier in the name
                recommendation = {'approach': api + '_' + approach['name'] + '_' + str(approach_index),
                                  #'recommendation': mock_recommend(dataset, approach),
                                  'evals': []}
                """
                for metric in settings['metrics']:
                    evaluation = mock_evaluate_all(approach, metric)
                    recommendation['evals'].append(
                        {'name': metric['name'], 'evaluation': evaluation, 'params': metric['params']})
                    print(metric)"""
                recs.append(recommendation)
        result.append({'dataset': dataset, 'recs': recs})
    return result


def save_result(experiment, config):
    """Save result to overview.

    Args:
    experiment(dict): the experiment input settings
    config(dict): the final experiment configuration
    """
    experiment['result'] = format_result(config)

    global current_result
    current_result = experiment
    add_result(current_result)
    #print('current result', current_result)


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


def delete_result(result_id, result_name):
    """Delete a result by its id.

    Args:
        result_id(int): the id of the specified result
        result_name(string): the name of the specified result
    """
    file_results = load_results_overview()
    # Remove from list
    file_results['all_results'] = [
        result for result in file_results['all_results']
        if result['timestamp']['stamp'] != result_id
    ]
    write_results_overview(file_results)
    # Remove from results folder
    path = RESULTS_ROOT_FOLDER + str(result_id) + '_' + result_name
    if (os.path.isdir(path)):
        shutil.rmtree(path)
    


def edit_result(result_id, new_name, new_tags, new_email):
    """Edit a result.

    Args:
        result_id(int): the result ID
        new_name(string): the new metadata name of the result
        new_tags(string): the new metadata tags of the result
        new_email(string): the new metadata email of the result
    """
    file_results = load_results_overview()['all_results']
    # Get index of the first item with the ID
    index = next((i for i in range(len(file_results)) if file_results[i]['timestamp']['stamp'] == result_id), None)
    to_edit_result = file_results[index]

    def makepath(result_id, to_edit_result):
        return RESULTS_ROOT_FOLDER + str(result_id) + '_' + to_edit_result['metadata']['name']

    old_name = to_edit_result['metadata']['name']
    old_path = makepath(result_id, to_edit_result)
    
    def edit_metadata(attr, new_val):
        # Don't change the attribute if the input field has been left empty
        if new_val != '':
            to_edit_result['metadata'][attr] = new_val
            print('changed ' + attr, to_edit_result['metadata'][attr])

    for (data_name, new_data) in [('name', new_name), ('tags', new_tags), ('email', new_email)]:
        edit_metadata(data_name, new_data)

    # TODO Add more editable values
    file_results[index] = to_edit_result

    write_results_overview({'all_results': file_results})
    
    #Update the folder name to match the new name
    new_path = makepath(result_id, to_edit_result)
    if (os.path.isdir(old_path)):
        os.rename(old_path, new_path)
    
    #Update the name in all overview.json files
    for subdir in [f.path for f in os.scandir(new_path) if f.is_dir()]:
        run_overview = load_json(subdir + '/overview.json')
        for pair in run_overview['overview']:
            pair['evaluation_path'] = pair['evaluation_path'].replace(old_name, new_name)
            pair['ratings_path'] = pair['ratings_path'].replace(old_name, new_name)
            pair['ratings_settings_path'] = pair['ratings_settings_path'].replace(old_name, new_name)
        file = open(subdir + '/overview.json','w')
        file.write(json.dumps(run_overview))

        
def create_results_overview():
    """Create a results file if it doesn't exist yet or is empty."""
    if not os.path.exists(RESULTS_ROOT_FOLDER):
        os.mkdir(RESULTS_ROOT_FOLDER)
    if not os.path.exists(RESULTS_OVERVIEW_PATH) \
            or os.stat(RESULTS_OVERVIEW_PATH).st_size == 0:
        # Open the file in write mode.
        with open(RESULTS_OVERVIEW_PATH, 'w', encoding='utf-8') as file:
            json.dump({'all_results': []}, file, indent=4)

# TODO UNUSED
def parse_tags(tags_string):
    """Parse result tags (given by user as metadata).

    Args:
        tags_string(string): the tags as raw string input (comma-separated)

    Returns:
        the split list of tags
    """
    # Split tags by comma and get the unique tags
    unique = list(set(tags_string.split(',')))
    print('parsed tags unique list', unique)
    # Remove empty tags
    return [tag for tag in unique if tag]
