"""This module contains constants and fixtures that are shared among all files in the test suite.

test_bad_request(): test a malformed request

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from tests.constants import BAD_JSON_REQUEST


def check_bad_request(client, url):
    """Test whether a malformed request gives a bad request code in response."""
    post_response = client.post(url, json=BAD_JSON_REQUEST)
    return post_response.status_code == 400