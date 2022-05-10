"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json
from fairreckitlib.algorithms.elliot_alg.factory import ELLIOT_API

model_API_dict = {}

# constants
DEFAULTS = {'split': 80,
            'recCount': {'min': 0, 'max': 100, 'default': 10},
            }  # default values
DEFAULT_SPLIT = {'name': 'Train/testsplit', 'default': '80', 'min': 1, 'max': 99}
filters = json.load(open('parameters/filters.json'))


# TODO do this in another way
def create_model_api_dict(predictors, recommenders):
    approaches = list(predictors.items()) + list(recommenders.items())
    model_to_api = {}
    for (header, options) in approaches:
        for option in options:
            model_to_api[option['name']] = header
    # print(dict)
    return model_to_api


def create_available_options(recommender_system):
    """Gets options from FairRecKitLib and formats them for usage on the client side

    Args:
        recommender_system(RecommenderSystem): the recommender system to get the options from

    Returns:
        (dict) the formatted options
    """
    options = {}

    frk_datasets = recommender_system.get_available_datasets()
    frk_predictors = recommender_system.get_available_predictors()
    frk_recommenders = recommender_system.get_available_recommenders()
    frk_metrics = recommender_system.get_available_metrics()
    # print('DATASETS:\n', frk_datasets)
    # print(frk_predictors)
    # print(frk_recommenders)
    # print(frk_metrics)

    global model_API_dict
    model_API_dict = create_model_api_dict(frk_predictors, frk_recommenders)

    def format_categorised(settings):
        formatted_settings = []
        for (header, options) in settings.items():
            # print(settings[header])
            # options['header'] = header TODO handle categories/APIs differently
            formatted_settings.append({'name': header, 'options': options})
        # print(formatted_settings)
        return formatted_settings

    # Format categorised settings
    datasets = format_categorised(frk_datasets)
    recommenders = format_categorised(frk_recommenders)
    predictors = format_categorised(frk_predictors)
    metrics = format_categorised(frk_metrics)

    # Generate metrics parameter data
    # metric_categories = metrics['categories']
    for category in metrics:
        if category['name'] == 'Accuracy':
            metric_params = {'values': [{'name': 'k', 'default': 10, 'min': 1, 'max': 20}]}
        else:
            metric_params = {}
        category['options'] = list(map(lambda metric: {'name': metric, 'params': metric_params}, category['options']))

    # print(METRICS)
    options['defaults'] = DEFAULTS

    # Format datasets
    # TODO do this in backend
    for dataset in datasets:
        # TODO this is stupid because we just created the options key
        dataset['params'] = dataset['options']
        del dataset['options']

        # Reformat and add parameters
        params = dataset['params']
        params['values'] = [DEFAULT_SPLIT]
        splits = ['Random'] + (['Time'] if params['timestamp'] else [])
        params['options'] = [{'name': 'Type of split', 'default': "Random", 'options': splits}]

        dataset['params'] = params

    formatted_filters = reformat(filters, False)
    # Add dynamic (nested settings) settings
    # MOCK: for now use all filters/metrics per dataset
    filter_list = [{'name': 'filter',
                    'plural': 'filters', 'article': 'a', 'options': formatted_filters}]

    for dataset in datasets:
        dataset['params']['dynamic'] = filter_list

    for metric in metrics:
        for option in metric['options']:
            option['params']['dynamic'] = filter_list

    print(options)
    options = reformat_all(options, datasets, recommenders, predictors, metrics)
    options['filters'] = formatted_filters
    # print(options)

    return options


def reformat_all(options, datasets, recommenders, predictors, metrics):
    options['datasets'] = reformat(datasets, False)
    # options['approaches'] = APPROACHES
    options['predictors'] = reformat(predictors, True)
    options['recommenders'] = reformat(recommenders, True)
    options['metrics'] = reformat(metrics, True)
    return options


def config_dict_from_settings(experiment):
    """Create a configuration dictionary from client settings

    Args:
        experiment(dict): the experiment settings sent from the client
    Returns:
        (dict) the configuration
    """
    settings = experiment['settings']

    name = experiment['metadata']['name'] 
    experiment_id = experiment['timestamp']['stamp'] + '_' + name

    # Format datasets
    datasets = list(
        map(lambda dataset: {
            'name': dataset['name'],
            'splitting': {'test_ratio': (100 - settings['split']) / 100,
                          'type': settings['splitMethod']}},
            settings['datasets']))

    # Format models
    models = {}
    for approach in settings['approaches']:
        model_name = approach['name']
        if approach['params'] is None:  # handle params null
            model_setting = {'name': model_name}  # TODO handle params null in frontend?
        else:
            model_setting = approach
        models.setdefault(model_API_dict[model_name], []).append(model_setting)

    #evaluation = {'metrics': list(map(lambda metric: metric['name'], settings['metrics'])), 'filters': []}

    # TODO for now leave out the metrics
    evaluation = {'metrics': [], 'filters': []}

    # evaluation = list(map(lambda metric: {'name': metric['name']}, settings['metrics']))  # TODO filters

    """
    if settings['experimentMethod'] == 'recommendation':
        config = RecommenderExperimentConfig(datasets, models, evaluation, id,
                                             settings['experimentMethod'], settings['recommendations'])
    else:
        config = PredictorExperimentConfig(datasets, models, evaluation, id,
                                           settings['experimentMethod'])

    print(config)"""

    print(name)
    config_dict = {'datasets': datasets,
                   'models': models,
                   'evaluation': evaluation,
                   'name': experiment_id,
                   'top_K': settings['recommendations'],
                   'type': settings['experimentMethod']}

    print(config_dict)
    return config_dict, experiment_id


# Reformat an options list
def reformat_options(options):
    # Add text and value fields
    return list(map(lambda option: {'name': option['name'], 'value': option}, options))


# Reformat options for form usage
def reformat(options, nested):
    if nested:
        for option in options:
            option['options'] = reformat_options(option['options'])

            # Disable Elliot options
            if option['name'] == ELLIOT_API:
                for disable_option in option['options']:
                    disable_option['disabled'] = True
                    #print(disable_option)

                option['name'] = option['name'] + ' (unavailable)'
    else:
        options = reformat_options(options)

    return options
