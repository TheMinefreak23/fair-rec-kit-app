"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from unittest.mock import patch

from project.models import result_store
from project.models.result_loader import result_by_id
from project.models.result_storage import load_json

from tests.constants import MOCK_RESULTS_DIR


@patch('project.models.result_storage.RESULTS_DIR', MOCK_RESULTS_DIR)
@patch('project.models.result_storage.RESULTS_OVERVIEW_PATH',
       MOCK_RESULTS_DIR +
       'results_overview.json')
@patch('project.models.result_loader.RESULTS_DIR', MOCK_RESULTS_DIR)
def test_result_by_id():
    """Test setting the full result by its ID"""
    result_by_id(0, result_store)
    # TODO throws error during CI
    correct_result = load_json(MOCK_RESULTS_DIR + "UNITTEST_correct_result.json")
    assert correct_result == result_store.current_result
