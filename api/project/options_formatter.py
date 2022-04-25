# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

import json


def create_options():
    # Generate parameter data
    metric_categories = METRICS['categories']
    for category in metric_categories:
        if category['text'] == 'Accuracy':
            metric_params = {'values': [{'text': 'k', 'default': 10, 'min': 1, 'max': 20}]}
        else:
            metric_params = {}
        category['options'] = list(map(lambda metric: {'text': metric, 'params': metric_params}, category['options']))
        print(category)

    options = {'defaults': DEFAULTS}

    # print(METRICS)
    # options['filters'] = FILTERS
    filters = reformat(FILTERS, False)

    create_list_params(filters)

    options['datasets'] = reformat(DATASETS, False)
    # options['approaches'] = APPROACHES
    options['predictors'] = reformat(APPROACHES['libraries']['prediction'], True)
    options['recommenders'] = reformat(APPROACHES['libraries']['recommendation'], True)
    options['metrics'] = reformat(METRICS['categories'], True)
    return options


def create_list_params(filters):
    # Set nested-list parameters (filters)

    filter_list = [{'name': 'filter', 'nested': False,
                                         'plural': 'filters', 'article': 'a', 'options': filters}]

    # MOCK: for now use all filters/metrics per dataset
    for dataset in DATASETS:
        dataset['params']['dynamic'] = filter_list

    for metric in METRICS['categories']:
        for option in metric['options']:
            option['params']['dynamic'] = filter_list


# Reformat an options list
def reformat_options(options):
    # Add text and value fields
    return list(map(lambda option: {'text': option['text'], 'value': option}, options))


# Reformat options for form usage
def reformat(options, nested):
    if nested:
        for option in options:
            option['options'] = reformat_options(option['options'])
    else:
        options = reformat_options(options)

    return options


# constants
DATASETS = [
    {'text': 'LFM2B', 'timestamp': True,
     'params': {'values': [{'text': 'Train/testsplit', 'default': '80', 'min': 0, 'max': 100}],
                'options': [{'text': 'Type of split', 'default': "Random", 'options': ["Random", "Time"]}]}},
    {'text': 'LFM1B', 'timestamp': True,
     'params': {'values': [{'text': 'Train/testsplit', 'default': '80', 'min': 0, 'max': 100}],
                'options': [{'text': 'Type of split', 'default': "Random", 'options': ["Random", "Time"]}]}},
    {'text': 'LFM360K', 'timestamp': False,
     'params': {'values': [{'text': 'Train/testsplit', 'default': '80', 'min': 0, 'max': 100}]}},
    {'text': 'ML25M', 'timestamp': True,
     'params': {'values': [{'text': 'Train/testsplit', 'default': '80', 'min': 0, 'max': 100}],
                'options': [{'text': 'Type of split', 'default': "Random", 'options': ["Random", "Time"]}]}},
    {'text': 'ML100K', 'timestamp': True,
     'params': {'values': [{'text': 'Train/testsplit', 'default': '80', 'min': 0, 'max': 100}],
                'options': [{'text': 'Type of split', 'default': "Random", 'options': ["Random", "Time"]}]}}
]

# TODO not constant
APPROACHES = json.load(open('project/approaches.json'))
METRICS = json.load(open('project/metrics.json'))

DEFAULTS = {'split': 80,
            'recCount': {'min': 0, 'max': 100, 'default': 10},
            }  # default values
FILTERS = [{'text': 'Artist Gender', 'params': {'options': [{'text': 'Gender', 'options': ['Male', 'Female']}]}},
           {'text': 'User Gender', 'params': {'options': [{'text': 'Gender', 'options': ['Male', 'Female']}]}},
           {'text': 'Country user threshold',
            'params': {'values': [{'text': 'threshold', 'min': 1, 'max': 1000, 'default': 10}]}},
           {'text': 'Minimum age', 'params': {'values': [{'text': 'threshold', 'min': 1, 'max': 1000, 'default': 18}]}},
           {'text': 'Maximum age', 'params': {'values': [{'text': 'threshold', 'min': 1, 'max': 1000, 'default': 18}]}}]






