"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import time
from project.experiment import current_experiment
from project import result_storage


def mock_experiment():
    """Mock running an experiment and save the mock result."""
    # Mock experiment duration.
    time.sleep(2.5)
    result_storage.save_result(current_experiment.job, result_storage.format_result(current_experiment.config))


def mock_recommend(dataset, approach):
    """Mock recommendation.

    Args:
        dataset(dict): a dataset with a name
        approach(dict): an approach with a name

    Returns:
        (string) a magic result
    """
    # Combine the names, flipping the approach name.
    return dataset['name'] + approach['name'][::-1]


def mock_evaluate_all(approach, metric):
    """
    Do a mock evaluation for all filters.

    Args:
        approach(dict): the approach with a name
        metric(dict): the metric
    Returns:
        (dict) all evaluations
    """
    base_eval = mock_evaluate(approach, metric)
    evaluation = {'global': round(base_eval, 2), 'filtered': []}

    for metric_filter in metric['filters']:
        # Evaluate per filter.
        evals = []
        for (name, value) in metric_filter['params'].items():
            # Just use the value if it's a number, otherwise use the length of the word.
            filter_eval = value if isinstance(value, int) else len(value)
            val = round((base_eval * len(metric_filter['name']) / filter_eval), 2)
            evals.append({name + ' ' + str(value): val})
        evaluation['filtered'].append({metric_filter['name']: evals})

    return evaluation


def mock_evaluate(approach, metric):
    """
    Mock evaluation: Give a magic number using an approach and metric.

    Args:
        approach(dict): an approach with a name
        metric(dict): a metric with a name and value
    Returns:
        (float) the magic mock evaluation
    """
    # Mock evaluation

    result = len(approach['name']) * len(metric['name'])
    # print('metric:', metric)
    # Do something with the metrics parameters.
    if metric['params']:
        # print(metric['name'], 'has params', metric['params'])
        for (name, value) in metric['params'].items():
            val = int(value) if value else 0
            result *= len(name) * val

    return result / 100

