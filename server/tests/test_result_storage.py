"""This module tests result storage functionality.

save_mock_result(): save a mock result.
delete_test_results(): delete all results in overview by emptying the file.
test_save_result(): test saving a result to the result overview.
test_no_path_json(): test that loading a JSON on an invalid path throws an exception.
test_update_results(): test updating of results overview.
test_overview_created(): test that the overview exists on the path after being created.
test_load_overview_exists(): test that the overview gets created when it is loaded.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
from unittest.mock import patch
import pytest

from project.models import result_store
from project.models.constants import RESULTS_OVERVIEW_PATH
from project.models.result_storage\
    import load_json, load_results_overview,\
    add_result, create_results_overview

TEST_ID = -1
TEST_EXPERIMENT = {'result': None, 'timestamp': {'stamp': TEST_ID}, 'metadata': {'name': 'foo'}}
TEST_RESULTS_ROOT = 'tests/'
TEST_RESULTS_PATH = TEST_RESULTS_ROOT + 'test_results.json'

# TODO refactor get from result_storage?
TEST_RESULT_DIRECTORY = TEST_RESULTS_ROOT + str(TEST_ID) + '_' + TEST_EXPERIMENT['metadata']['name']


@patch('project.models.result_storage.RESULTS_OVERVIEW_PATH', TEST_RESULTS_PATH)
def save_mock_result():
    """Save a mock result."""
    # Make directory.
    if not os.path.exists(TEST_RESULT_DIRECTORY):
        os.makedirs(TEST_RESULT_DIRECTORY)

    # Save a result with the id.
    result_store.save_result(TEST_EXPERIMENT, {'data': []})


def delete_test_results():
    """Delete all results in overview by emptying the file."""
    with open(TEST_RESULTS_PATH, 'w', encoding='utf-8') as test_results_file:
        test_results_file.close()


def test_save_result():
    """Test saving a result to the result overview."""
    TEST_EXPERIMENT['result'] = 'foo'
    save_mock_result()
    expected = TEST_EXPERIMENT
    # The current result gets updated
    assert result_store.current_result is expected

    # use mock result
    #result_by_id(test_id)
    # The result is saved to a JSON on the path
    #from project.result_storage import current_result
    #assert current_result is expected

    delete_test_results()


# TODO test result_by_id and make a fixture for reuse in previous results testing


def test_no_path_json():
    """Test that loading a JSON on an invalid path throws an exception."""
    with pytest.raises(Exception):
        load_json('')


@patch('project.models.result_storage.RESULTS_OVERVIEW_PATH', TEST_RESULTS_PATH)
def test_update_results():
    """Test updating of results overview."""
    # print(load_results_overview())
    old_results_length = len(load_results_overview()['all_results'])
    add_result(TEST_EXPERIMENT)
    new_results_length = len(load_results_overview()['all_results'])
    # print(load_results_overview())
    assert new_results_length == old_results_length+1

    delete_test_results()

# TODO test edit_result and use fixture for reuse in previous_results


def test_overview_created():
    """Test that the overview exists on the path after being created."""
    create_results_overview()
    assert os.path.exists(RESULTS_OVERVIEW_PATH)


def test_load_overview_exists():
    """Test that the overview gets created when it is loaded."""
    assert load_results_overview() is not None
