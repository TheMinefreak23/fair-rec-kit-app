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
results_overview_path = 'results.json'
mock_results_overview_path = 'mock/results_overview.json'
mock_results_path = 'mock/results.json'
results_root_folder = 'mock/'
recommendations_path = 'recs.json'
evaluations_path = 'evals.json'


def save_result(metadata, settings, result):
    timestamp = time.time()
    now = datetime.datetime.now()
    currentDt = now.strftime('%Y-%m-%dT%H:%M:%S') + ('-%02d' % (now.microsecond / 10000))

    global current_result  # TODO use class instead of global?
    # current_result = {'timestamp': {'stamp': timestamp, 'datetime': currentDt}, 'metadata': metadata,
    #                  'settings': settings, 'result': result}
    current_result = {'id': 0, 'value': 0}
    update_results_overview(current_result)


def result_by_id(id):

    results_overview = load_json(results_overview_path)
    current_result_overview = {}
    # Filter: Loop through all results and find the one with the matching ID.
    for result in results_overview['all-results']:
        if result['timestamp']['datetime'] == id:
            current_result_overview = result

    resultList = []
    current_name = current_result_overview['metadata']['name']
    relative_path = results_root_folder + id + "_" + current_name
    #loops through all the subdirectories, and thus - runs, of a certain calculation
    for subdir in [f.path for f in os.scandir(relative_path) if f.is_dir()]:
        run_overview_name = os.path.basename(os.path.normpath(subdir) + "_overview.json"
        run_overview = load_json(subdir + "/" + run_overview_name)
        for run_result in run_overview["results"]:
            resultList.append(run_result)

    print(resultList)
    #Currently, this function only returns a list of runs, their subresults (splitted on different datasets, algorithms and filters)
    #and finally for each of these results a path to the evaluation and ratings file
    #TODO instead of returning a path, this function should convert the tsv files at each path to JSON, then return the JSON instead

    # current_result = results_df.filter(like='')


def newest_result():
    return current_result


def load_json(path):
    with open(path, 'r') as file:
        return json.load(file)  # Load existing data into a dict.


def load_results_overview():
    return load_json(mock_results_overview_path)


def update_results_overview(new_result):
    create_results_overview()
    file_data = load_json(results_overview_path)
    file_data['all_results'].append(new_result)
    with open(results_path, 'w') as file:  # Open the file in write mode.
        # Rewind file pointer's position.
        file.seek(0)
        # Store it as json data.
        json.dump(file_data, file, indent=4)


# Create results file if it doesn't exist yet or is empty
def create_results_overview():
    if not os.path.exists(results_overview_path) or os.stat(results_overview_path).st_size == 0:
        with open(results_overview_path, 'w') as file:  # Open the file in write mode.
            json.dump({'all_results': []}, file, indent=4)
