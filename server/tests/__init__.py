"""This package  contains the server-side fairreckitapp test suite.

Modules:
    conftest: constants and fixtures that are shared among all files in the test suite.
    constants: constants that are shared among some files in the test suite.
    mock_experiment: mock run an experiment, recommendation or evaluation.
    test_events: test the event_handler events to see if the progress and status change.
    test_experiment: test various functionality related to the experiments.
    test_mail: test the email sending functionality.
    test_music_detail: test the music detail functionality and the spotify api.
    test_options_format: test the functionality of the options_formatter module.
    test_ping: test to see if the server is online.
    test_previous_results: test the functionality of various server-side functions that manipulate the previous results.
    test_result_loader: test result loader functionality.
    test_result_storage: test result storage functionality.
    test_result: test the functionality of various server-side retrival components.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
