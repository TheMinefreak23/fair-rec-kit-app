# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import json
import random
from unittest.mock import patch

import pytest

from project.result_storage import *


test_id = -1
test_computation = {'result': None, 'timestamp': {'stamp': test_id}, 'metadata': {'name': 'foo'}}
test_results_path = 'test_results.json'


@patch('project.result_storage.results_overview_path', test_results_path)
def save_mock_result():
    save_result(test_computation, 'foo')  # Save a result with the id


# Delete all results by emptying the file
def delete_test_results():
    open(test_results_path, 'w').close()


# Test saving a result to the result overview
def test_save_result():
    test_computation['result'] = 'foo'
    save_mock_result()
    expected = test_computation
    # The current result gets updated
    from project.result_storage import current_result
    assert current_result is expected

    result_by_id(test_id)
    # The result is saved to a JSON on the path
    from project.result_storage import current_result
    assert current_result is expected

    delete_test_results()


# TODO test result_by_id and make a fixture for reuse in previous results testing


# Test that loading a JSON on an invalid path throws an exception
def test_no_path_json():
    with pytest.raises(Exception):
        load_json('')


# Test updating of results overview
@patch('project.result_storage.results_overview_path', test_results_path)
def test_update_results():
    print(load_results_overview())
    old_results_length = len(load_results_overview()['all_results'])
    add_result(test_computation)
    new_results_length = len(load_results_overview()['all_results'])
    print(load_results_overview())
    assert new_results_length == old_results_length+1

    delete_test_results()

# TODO test edit_result and use fixture for reuse in previous_results


# Test that the overview exists on the path after being created
def test_overview_created():
    create_results_overview()
    assert os.path.exists(RESULTS_OVERVIEW_PATH)


# Test that the overview gets created when it is loaded
def test_load_overview_exists():
    assert load_results_overview() is not None