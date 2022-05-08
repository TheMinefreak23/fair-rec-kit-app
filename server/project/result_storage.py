"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json
import os

# Global current result variables
current_result = {}
current_recs = None

# Storage paths
RESULTS_OVERVIEW_PATH = 'results.json'


def save_result(experiment, result):
    """Save result to overview.

    Args:
        experiment(dict): the experiment settings
        result(dict): the computed result
    """
    global current_result
    experiment['result'] = result

    # Parse tags
    if 'tags' in experiment['metadata']:
        experiment['metadata']['tags'] = parse_tags(experiment['metadata']['tags'])

    current_result = experiment
    add_result(current_result)
    print(current_result)


def result_by_id(result_id):
    """
    Get a result from the results overview by its id.

    :param result_id: the result id
    :return: the corresponding result (settings, recs, evaluation)
    """
    results = load_json(RESULTS_OVERVIEW_PATH)

    # Filter: Loop through all results and find the one with the matching ID.
    for result in results['all_results']:
        global current_result
        if 'timestamp' in result:
            if result['timestamp']['stamp'] == result_id:
                # print('result', result)
                current_result = result
        else:
            # If there is an incorrectly formatted result, return nothing.
            current_result = None

    # print('current result',current_result)


def load_json(path):
    """
    Load a JSON file to a dictionary using its path.

    :param path: the path to the JSON file
    :return: the JSON as a dictionary
    """
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)  # Load existing data into a dict.


def load_results_overview():
    """
    Load the results overview.

    :return: the loaded results
    """
    # Ensure the results overview exists.
    create_results_overview()
    return load_json(RESULTS_OVERVIEW_PATH)


def write_results_overview(results):
    """
    Write (store) results to the overview.

    :param results: the results to store
    """
    # Open the file in write mode.
    with open(RESULTS_OVERVIEW_PATH, 'w', encoding='utf-8') as file:
        # Store it as json data.
        json.dump(results, file, indent=4)


def add_result(result):
    """
    Add a result at the end of the results overview.

    :param result: the (new) result
    """
    file_results = load_results_overview()
    file_results['all_results'].append(result)
    write_results_overview(file_results)


def delete_result(index):
    """
    Delete a result by its index.

    :param index: the index of the result
    """
    file_results = load_results_overview()
    file_results['all_results'].pop(index)
    write_results_overview(file_results)


def edit_result(index, new_name, new_tags, new_email):
    """
    Edit a result.

    :param index: the result index
    :param new_name: the new metadata name of the result
    :param new_tags: the new metadata tags of the result
    :param new_email: the new metadata email of the result
    """
    file_results = load_results_overview()
    to_edit_result = file_results['all_results'][index]
    print(new_tags)

    def edit_metadata(attr, new_val):
        # Don't change the attribute if the input field has been left empty
        if new_val != '':  #
            to_edit_result['metadata'][attr] = new_val
            print('changed '+attr, to_edit_result['metadata'][attr])

    for (data_name, new_data) in [('name', new_name), ('tags', new_tags), ('email', new_email)]:
        edit_metadata(data_name, new_data)

    # TODO Add more editable values
    file_results['all_results'][index] = to_edit_result

    write_results_overview(file_results)


def create_results_overview():
    """Create a results file if it doesn't exist yet or is empty."""
    if not os.path.exists(RESULTS_OVERVIEW_PATH) or os.stat(RESULTS_OVERVIEW_PATH).st_size == 0:
        with open(RESULTS_OVERVIEW_PATH, 'w', encoding='utf-8') as file:  # Open the file in write mode.
            json.dump({'all_results': []}, file, indent=4)


def parse_tags(tags_string):
    """
    Parse result tags (given by user as metadata)

    :param tags_string: the tags as raw string input (comma-separated)
    :return: the split list of tags
    """
    # Split tags by comma and get the unique tags
    unique = list(set(tags_string.split(',')))
    # Remove empty tags
    return [tag for tag in unique if tag]
