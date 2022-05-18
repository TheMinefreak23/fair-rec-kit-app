"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json
from fairreckitlib.core.apis import ELLIOT_API
from fairreckitlib.core.config_constants import TYPE_PREDICTION, TYPE_RECOMMENDATION

model_API_dict = {}

# constants
DEFAULTS = {#'split': 80,
            'recCount': {'min': 0, 'max': 100, 'default': 10},
            }  # default values
DEFAULT_SPLIT = {'name': 'Train/testsplit', 'default': 80, 'min': 1, 'max': 99}
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

    datasets = recommender_system.get_available_datasets()
    print (datasets)
    predictors = recommender_system.get_available_algorithms(TYPE_PREDICTION)
    recommenders = recommender_system.get_available_algorithms(TYPE_RECOMMENDATION)
    # TODO different metrics for diff types
    pred_metrics = recommender_system.get_available_metrics(TYPE_PREDICTION)
    rec_metrics = recommender_system.get_available_metrics(TYPE_RECOMMENDATION)
    converters = recommender_system.get_available_rating_converters()
    # print('recommenders', recommenders)
    # print('rating converters', converters)
    splits = recommender_system.get_available_splitters()
    # print('splits', splits)

    global model_API_dict
    model_API_dict = create_model_api_dict(predictors, recommenders)

    def format_categorised(settings):
        formatted_settings = []
        for (header, options) in settings.items():
            # print(settings[header])
            # options['header'] = header TODO handle categories/APIs differently
            formatted_settings.append({'name': header, 'options': options})
        # print(formatted_settings)
        return formatted_settings

    # Format categorised settings (most settings are categorised once)
    # TODO refactor
    datasets = format_categorised(datasets)
    recommenders = format_categorised(recommenders)
    predictors = format_categorised(predictors)
    pred_metrics = format_categorised(pred_metrics)
    rec_metrics = format_categorised(rec_metrics)

    # Add dynamic (nested settings) settings
    formatted_filters = reformat(filters, False)
    formatted_converters = reformat(converters, False)
    formatted_splits = reformat(splits, False)

    # MOCK: for now use all filters/metrics per dataset
    filter_option = {'name': 'filter',
                     'title': 'filters',
                     'article': 'a',
                     'options': formatted_filters}
    converter_option = {'name': 'rating converter',
                        'single': True,
                        'title': 'conversion',
                        'article': 'a',
                        'options': formatted_converters}
    # split_types = ['Random'] + (['Time'] if params['timestamp'] else [])
    split_type_option = {'name': 'type of split',
                         'single': True,
                         'required': True,
                         'title': 'splitting',
                         'article': 'a',
                         'default': 'Random',  # TODO use this
                         'options': formatted_splits}

    for dataset in datasets:
        # TODO this is stupid because we just created the options key
        dataset['params'] = dataset['options']
        del dataset['options']
        dataset['params']['values'] = [DEFAULT_SPLIT]
        dataset['params']['dynamic'] = [filter_option, converter_option, split_type_option]
        # print(dataset['params']['options'])

    for metric in rec_metrics + pred_metrics:
        for option in metric['options']:
            option['params']['dynamic'] = [filter_option]

    # TODO refactor
    uncategorised = [
        ('datasets', datasets),
    ]
    categorised = [
        ('predictors', predictors),
        ('recommenders', recommenders),
        ('recMetrics', rec_metrics),
        ('predMetrics', pred_metrics)
    ]
    options = reformat_all(options, uncategorised, categorised)
    options['defaults'] = DEFAULTS
    options['filters'] = formatted_filters

    # print('datasets tests', json.dumps(datasets[0], indent=4))
    # print('recommender tests', json.dumps(recommenders[0], indent=4))
    # print(options)

    return options


def reformat_all(options, uncategorised, categorised):
    for (option_type, inner_options) in uncategorised:
        options[option_type] = reformat(inner_options, False)
    for (option_type, inner_options) in categorised:
        options[option_type] = reformat(inner_options, True)
    return options


def config_dict_from_settings(experiment):
    """Create a configuration dictionary from client settings

    Args:
        experiment(dict): the experiment settings sent from the client
    Returns:
        (dict) the configuration
    """
    settings = experiment['settings']

    #print('raw experiment settings:', json.dumps(settings, indent=4))

    name = experiment['metadata']['name']
    experiment_id = experiment['timestamp']['stamp'] + '_' + name

    form_to_data(settings)
    #print('formatted from form', json.dumps(settings, indent=4))

    # Format datasets
    # Add generic split to all dataset
    for dataset in settings['datasets']:
        #print(dataset)
        # TODO refactor
        if dataset['conversion'] != [] and 'conversion' in dataset:
            dataset['conversion'] = dataset['conversion'][0]
        dataset['splitting'] = dataset['splitting'][0]
        # TODO rename split param
        dataset['splitting']['test_ratio'] = (100 - dataset['params']['Train/testsplit']) / 100


    # Format models
    models = {}
    for approach in settings['approaches']:
        model_name = approach['name']
        if approach['params'] is None:  # handle params null
            model_setting = {'name': model_name}  # TODO handle params null in frontend?
        else:
            model_setting = approach
        models.setdefault(model_API_dict[model_name], []).append(model_setting)

    # evaluation = {'metrics': list(map(lambda metric: metric['name'], settings['metrics'])), 'filters': []}

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

    #print(name)
    config_dict = {'datasets': settings['datasets'],
                   'models': models,
                   'evaluation': evaluation,
                   'name': experiment_id,
                   'top_K': settings['recommendations'],
                   'type': settings['experimentMethod']}

    #print(config_dict)
    return config_dict, experiment_id


def form_to_data(settings):
    # Format from group list form data
    for option_name, option_list in settings['lists'].items():
        #print(option_list)
        reformat_list(settings, option_name, option_list)
    del settings['lists']


# Reformat settings list from form to data
def reformat_list(settings, option_name, option_list):
    for option in option_list:
        #print(option)
        option['params'] = {param['name']: param['value'] for param in option['params']}
        # Format inner formgrouplists
        for inner_option_name, inner_option_list in option.items():
            if inner_option_name not in ['name', 'params']: # TODO use settings/lists key after all?
                #print(json.dumps(option, indent=4))
                reformat_list(option, inner_option_name, inner_option_list)
    settings[option_name] = option_list


# Reformat an options list from data to form
def reformat_options(options):
    # Add text and value fields
    return [{'name': option['name'], 'value': option} for option in options]


# Reformat options for form usage
def reformat(options, nested):
    if nested:
        for option in options:
            option['options'] = reformat_options(option['options'])

            # Disable Elliot options
            if option['name'] == ELLIOT_API:
                for disable_option in option['options']:
                    disable_option['disabled'] = True
                    # print(disable_option)

                option['name'] = option['name'] + ' (unavailable)'
    else:
        options = reformat_options(options)

    return options
