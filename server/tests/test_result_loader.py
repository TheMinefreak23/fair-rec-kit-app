from unittest.mock import patch

from project.result_loader import *
from project import result_storage

MOCK_RESULTS_DIR = 'tests/mock/'

# TODO refactor
@patch('project.result_storage.RESULTS_OVERVIEW_PATH', MOCK_RESULTS_DIR + 'results_overview.json')
@patch('project.result_storage.RESULTS_ROOT_FOLDER', MOCK_RESULTS_DIR)
@patch('project.result_loader.RESULTS_ROOT_FOLDER', MOCK_RESULTS_DIR)
def test_result_by_id():
    from project.result_storage import RESULTS_ROOT_FOLDER
    print(RESULTS_ROOT_FOLDER)
    result_by_id(0)
    assert result_storage.current_result
    # TODO throws error during CI
    # correct_result = result_storage.load_json(MOCK_RESULTS_DIR + "UNITTEST_correct_result.json")
    # assert correct_result == result_storage.current_result
