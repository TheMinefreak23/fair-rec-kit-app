from unittest.mock import patch

import pytest

from project.result_loader import *
from project.result_storage import *

test_results_path = "mock/"

@patch('project.result_storage.RESULTS_ROOT_FOLDER', test_results_path)
def test_result_by_id():
    result_by_id(0)
    correct_result = result_storage.load_json("mock/UNITTEST_correct_result.json")
    assert correct_result == result_storage.current_result
