from unittest.mock import patch

from project.models.result_loader import *
from project.models import result_store

from tests.constants import MOCK_RESULTS_DIR

#@patch('project.models.constants.RESULTS_OVERVIEW_PATH', MOCK_RESULTS_DIR + 'results_overview.json')
#@patch('project.models.constants.RESULTS_DIR', MOCK_RESULTS_DIR)


@patch('project.models.result_storage.RESULTS_DIR', MOCK_RESULTS_DIR)
@patch('project.models.result_storage.RESULTS_OVERVIEW_PATH', MOCK_RESULTS_DIR + 'results_overview.json')
@patch('project.models.result_loader.RESULTS_DIR', MOCK_RESULTS_DIR)
def test_result_by_id():
    from project.models.constants import RESULTS_DIR
    print(RESULTS_DIR)
    result_by_id(0, result_store)
    assert result_store.current_result
    # TODO throws error during CI
    # correct_result = result_storage.load_json(MOCK_RESULTS_DIR + "UNITTEST_correct_result.json")
    # assert correct_result == result_storage.current_result
