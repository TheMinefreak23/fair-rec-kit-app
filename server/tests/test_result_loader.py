from unittest.mock import patch

from project.result_loader import *
from project import result_storage

# test_results_path = "mock/" TODO doesn't work for some reason

# TODO refactor
@patch('project.result_storage.RESULTS_OVERVIEW_PATH', 'mock/results_overview.json')
@patch('project.result_storage.RESULTS_ROOT_FOLDER', 'mock/')
@patch('project.result_loader.RESULTS_ROOT_FOLDER', 'mock/')
def test_result_by_id():
    from project.result_storage import RESULTS_ROOT_FOLDER
    print(RESULTS_ROOT_FOLDER)
    result_by_id(0)
    correct_result = result_storage.load_json("mock/UNITTEST_correct_result.json")
    assert correct_result == result_storage.current_result
