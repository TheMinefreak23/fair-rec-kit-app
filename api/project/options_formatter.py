"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

model_API_dict = {}

# constants
DEFAULTS = {'split': 80,
            'recCount': {'min': 0, 'max': 100, 'default': 10},
            }  # default values
FILTERS = [{'name': 'Artist Gender', 'params': {'options': [{'name': 'Gender', 'options': ['Male', 'Female']}]}},
           {'name': 'User Gender', 'params': {'options': [{'name': 'Gender', 'options': ['Male', 'Female']}]}},
           {'name': 'Country user threshold',
            'params': {'values': [{'name': 'threshold', 'min': 1, 'max': 1000, 'default': 10}]}},
           {'name': 'Minimum age', 'params': {'values': [{'name': 'threshold', 'min': 1, 'max': 1000, 'default': 18}]}},
           {'name': 'Maximum age', 'params': {'values': [{'name': 'threshold', 'min': 1, 'max': 1000, 'default': 18}]}}]


# TODO do this in another way
def create_model_API_dict(predictors, recommenders):
    approaches = list(predictors.items()) + list(recommenders.items())
    dict = {}
    for (header, options) in approaches:
        for option in options:
            dict[option['name']] = header
    #print(dict)
    return dict


def create_available_options(recommender_system):
    """
    Gets options from FairRecKitLib and formats them for usage on the client side

    :param recommender_system: the recomender system to get the options from
    :return: the formatted options
    """
    options = {}

    frk_datasets = recommender_system.get_available_datasets()
    frk_predictors = recommender_system.get_available_predictors()
    frk_recommenders = recommender_system.get_available_recommenders()
    frk_metrics = recommender_system.get_available_metrics()
    #print('DATASETS:\n', frk_datasets)
    # print(frk_predictors)
    # print(frk_recommenders)
    # print(frk_metrics)

    global model_API_dict
    model_API_dict = create_model_API_dict(frk_predictors, frk_recommenders)

    # TODO: DO THIS IN BACKEND?
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
    # options['filters'] = FILTERS

    # Format datasets
    # TODO do this in backend
    for dataset in datasets:
        # TODO this is stupid because we just created the options key
        dataset['params'] = dataset['options']
        del dataset['options']

        # Reformat and add parameters
        params = dataset['params']
        params['values'] = [{'name': 'Train/testsplit', 'default': '80', 'min': 0, 'max': 100}]
        splits = ['Random'] + (['Time'] if params['timestamp'] else [])
        params['options'] = [{'name': 'Type of split', 'default': "Random", 'options': splits}]

        dataset['params'] = params


    # Add dynamic (nested settings) settings
    # MOCK: for now use all filters/metrics per dataset
    filter_list = [{'name': 'filter', 'nested': False,
                    'plural': 'filters', 'article': 'a', 'options': FILTERS}]

    for dataset in datasets:
        dataset['params']['dynamic'] = filter_list

    for metric in metrics:
        for option in metric['options']:
            option['params']['dynamic'] = filter_list

    options['datasets'] = datasets
    options['recommenders'] = recommenders
    options['predictors'] = predictors
    options['metrics'] = metrics

    # print(options)

    return options


def config_dict_from_settings(computation):
    """
    Create a configuration dictionary from client settings

    :param computation: the computation settings sent from the client
    :return: the configuration dictionary
    """
    settings = computation['settings']

    name = computation['metadata']['name']
    id = computation['timestamp']['stamp'] + '_' + name

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

    evaluation = {'metrics': list(map(lambda metric: metric['name'], settings['metrics'])), 'filters': []}
    # evaluation = list(map(lambda metric: {'name': metric['name']}, settings['metrics']))  # TODO filters

    """
    if settings['computationMethod'] == 'recommendation':
        config = RecommenderExperimentConfig(datasets, models, evaluation, id,
                                             settings['computationMethod'], settings['recommendations'])
    else:
        config = PredictorExperimentConfig(datasets, models, evaluation, id,
                                           settings['computationMethod'])

    print(config)"""

    print(name)
    config_dict = {'datasets': datasets,
                   'models': models,
                   'evaluation': evaluation,
                   'name': id,
                   'top_K': settings['recommendations'],
                   'type': settings['computationMethod']}

    print(config_dict)
    return config_dict, id
