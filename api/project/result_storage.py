  # This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import csv  # TODO fix this import
import json
import os
from os import walk
from csv import writer
import time
import datetime
import pandas as pd

# Results overview format
# timestamp (ID)
# metadata: name, tag
# settings: datasets, approaches, metrics, per metric: name, k value

# Result detail format
# timestamp (ID), per dataset: recommendations result, per recs result: metrics evaluations

current_result = {}
current_recs = {}
results_overview_path = 'results.json'
mock_results_overview_path = 'mock/results_overview.json'
mock_results_path = 'mock/results.json'
results_root_folder = 'mock/'
recommendations_path = 'recs.json'
evaluations_path = 'evals.json'


def save_result(computation, result):
    global current_result
    computation['result'] = result
    current_result = computation
    update_results_overview(current_result)
    print(current_result)


def result_by_id(resultid):

    results_overview = load_json(results_overview_path)
    current_result_overview = {}
    # Filter: Loop through all results and find the one with the matching ID.
    for result in results_overview['all-results']:
        if result['timestamp']['datetime'] == resultid:
            current_result_overview = result

    current_name = current_result_overview['metadata']['name']
    relative_path = results_root_folder + resultid + "_" + current_name
    data = {'id': resultid, 'name': current_name, 'runs': []}
    # loops through all the subdirectories, and thus - runs, of a certain calculation
    for subdir in [f.path for f in os.scandir(relative_path) if f.is_dir()]:
        run_overview_name = os.path.basename(os.path.normpath(subdir))
        run_overview = load_json(subdir + "/" + run_overview_name + "_overview.json")
        run_data = {'name': run_overview_name, 'results': []}
        # loops through individual results
        for run_result in run_overview["results"]:
            evaluation_path_full = subdir + "/" + run_overview_name + "/" + result_data['evaluation_path']
            ratings_path_full = subdir + "/" + run_overview_name + "/" + result_data['ratings_path']
            evaluation_data = pd.read_csv(evaluation_path_full, sep='\t', header=None).to_dict(orient='records')
            ratings_data = pd.read_csv(ratings_path_full, sep='\t', header=None).to_dict(orient='records')
            result_data = {'name': run_result['name'], 'evaluation': evaluation_data, 'ratings': ratings_data}
            run_data['results'].append(result_data)

        data['runs'].append(run_data)

    global current_result
    current_result = json.dumps(data)


def newest_result():
    return current_result


def load_json(path):
    with open(path, 'r') as file:
        return json.load(file)  # Load existing data into a dict.


def load_results_overview():
    create_results_overview()
    return load_json(results_overview_path)


def update_results_overview(new_result):
    create_results_overview()
    file_data = load_json(results_overview_path)
    file_data['all_results'].append(new_result)
    with open(results_overview_path, 'w') as file:  # Open the file in write mode.
        # Rewind file pointer's position.
        file.seek(0)
        # Store it as json data.
        json.dump(file_data, file, indent=4)


def delete_result(index):
    create_results_overview()
    file_data = load_results_overview()
    file_data['all_results'].pop(index)
    with open(results_overview_path, 'w') as file:  # Open the file in write mode.
        # Rewind file pointer's position.
        file.seek(0)
        # Store it as json data.
        json.dump(file_data, file)


def edit_result(index, new_name, new_tags, new_email):
    create_results_overview()
    file_data = load_results_overview()
    to_edit_result = file_data['all_results'].pop(index)

    if new_name != '':  # Don't change the name if the input field has been left empty
        to_edit_result['metadata']['name'] = new_name
        print(to_edit_result['metadata']['name'])
    if new_tags != '':  # Don't change the tags if the input field has been left empty
        to_edit_result['metadata']['tags'] = new_tags
        print(to_edit_result['metadata']['tags'])
    if new_email != '':  # Don't change the e-mail if the input field has been left empty
        to_edit_result['metadata']['email'] = new_email
        print(to_edit_result['metadata']['email'])

    # TODO Add more editable values
    file_data['all_results'].insert(index, to_edit_result)

    with open(results_overview_path, 'w') as file:  # Open the file in write mode.
        # Rewind file pointer's position.
        file.seek(0)
        # Store it as json data.
        json.dump(file_data, file)


# Create results file if it doesn't exist yet or is empty
def create_results_overview():
    if not os.path.exists(results_overview_path) or os.stat(results_overview_path).st_size == 0:
        with open(results_overview_path, 'w') as file:  # Open the file in write mode.
            json.dump({'all_results': []}, file, indent=4)
