"""This module contains constants and fixtures that are shared among all files in the test suite.

fixture_test_app(): make the app for testing.
client(test_app): get the app client for testing.
runner(test_app): get the app CLI runner for testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import pytest

from project import create_app


@pytest.fixture(name='test_app')
def fixture_test_app():
    """Make the app for testing.

    Returns:
        yields the app
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(test_app):
    """Get the app client for testing.

    Args:
        test_app: the Flask app

    Returns:
        the client
    """
    return test_app.test_client()


@pytest.fixture()
def runner(test_app):
    """Get the app CLI runner for testing.

    Args:
        test_app: the Flask App

    Returns:
        the CLI runner
    """
    return test_app.test_cli_runner()
