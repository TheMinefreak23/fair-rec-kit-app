"""This module is used to convert user experiment options to a configuration format and vice-versa.

classes:
    OptionsFormatter

methods:
    create_model_api_dict
    format_categorised
    reformat_all
    reformat
    reformat_options
    form_to_data
    parse_if_number
    reformat_list
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json
from fairreckitlib.core.core_constants import TYPE_PREDICTION, TYPE_RECOMMENDATION

# constants
DEFAULTS = {
    'recCount': {'min': 1, 'max': 100, 'default': 10},
}  # default values
DEFAULT_SPLIT = {'name': 'Train/testsplit',
                 'default': '80', 'min': 0, 'max': 100}
with open('parameters/resultFilter.json', encoding='utf-8') as filter_file:
    filters = json.load(filter_file)  # TODO LOAD from dataset


class OptionsFormatter:
    """Formatter for the experiment options.

    methods:
        __init__
        create_available_options
        set_dataset_params
        config_dict_from_settings
    """

    def __init__(self, recommender_system):
        """Initialize OptionsFormatter.

        args:
            recommender_system(obj): the recommender system to be used
        """
        self.model_api_dict = {}
        self.dataset_matrices = {}
        self.options = self.create_available_options(recommender_system)

    def create_available_options(self, recommender_system):
        """Get options from FairRecKitLib and formats them for usage on the client side.

        Args:
            recommender_system(RecommenderSystem): the recommender system to get the options from

        Returns:
            (dict) the formatted options
        """
        datasets = recommender_system.get_available_datasets()
        self.dataset_matrices = {dataset: list(matrices.keys()) for (
            dataset, matrices) in datasets.items()}
        predictors = recommender_system.get_available_algorithms(TYPE_PREDICTION)
        recommenders = recommender_system.get_available_algorithms(
            TYPE_RECOMMENDATION)
        pred_metrics = recommender_system.get_available_metrics(TYPE_PREDICTION)
        rec_metrics = recommender_system.get_available_metrics(TYPE_RECOMMENDATION)

        self.model_api_dict = create_model_api_dict(predictors, recommenders)

        # Format categorised settings (most settings are categorised once)
        datasets = format_categorised(datasets)
        recommenders = format_categorised(recommenders)
        predictors = format_categorised(predictors)
        pred_metrics = format_categorised(pred_metrics)
        rec_metrics = format_categorised(rec_metrics)

        # Add dynamic (nested settings) settings
        formatted_filters = reformat(filters, False)

        # MOCK: for now use all filters/metrics per dataset
        filter_option = {'name': 'filter',
                         'title': 'filters',
                         'options': formatted_filters}

        for dataset in datasets:
            dataset['params'] = dataset['options']
            del dataset['options']
            self.set_dataset_params(dataset, filter_option, recommender_system)

        for metric in rec_metrics + pred_metrics:
            for option in metric['options']:
                option['params']['dynamic'] = [filter_option]

        uncategorised = [
            ('datasets', datasets),
        ]
        categorised = [
            ('predictors', predictors),
            ('recommenders', recommenders),
            ('recMetrics', rec_metrics),
            ('predMetrics', pred_metrics)
        ]
        options = reformat_all(uncategorised, categorised)
        options['defaults'] = DEFAULTS
        options['filters'] = formatted_filters

        return options

    def set_dataset_params(self, dataset, filter_option, recommender_system):
        """Set the dataset option parameters.

        Args:
            dataset: the dataset to set the parameters for
            filter_option: the filter option available for the dataset
            recommender_system: the recommender system for the experiments

        """
        converters = recommender_system.get_available_rating_converters()
        splits = recommender_system.get_available_splitters()

        formatted_splits = reformat(splits, False)
        split_type_option = {'name': 'type of split',
                             'single': True,
                             'required': True,
                             'title': 'splitting',
                             'default': formatted_splits[0],
                             'options': formatted_splits}

        dataset['params']['values'] = [DEFAULT_SPLIT]
        matrices = []
        for matrix_name in self.dataset_matrices[dataset['name']]:
            dataset_matrix_converters = converters[dataset['name']][matrix_name]
            converter_option = {'name': 'rating converter',
                                'single': True,
                                'title': 'conversion',
                                'options': reformat(dataset_matrix_converters, False)}
            matrices.append({'name': matrix_name, 'params': {
                'dynamic': [converter_option]}})
        matrix_option = {
            'name': 'matrix',
            'single': True,
            'required': True,
            'title': 'matrix',
            'options': reformat(matrices, False),
        }
        # converter_option
        dataset['params']['dynamic'] = [
            matrix_option, filter_option, split_type_option]

    def config_dict_from_settings(self, experiment):
        """Create a configuration dictionary from client settings.

        Args:
            experiment(dict): the experiment settings sent from the client
        Returns:
            (dict) the configuration
        """
        settings = experiment['settings']

        print('experiment settings from client:', json.dumps(settings, indent=4))

        name = experiment['metadata']['name']
        experiment_id = experiment['timestamp']['stamp'] + '_' + name

        form_to_data(settings)
        print('formatted from form', json.dumps(settings, indent=4))

        # Format datasets
        # Add generic split to all dataset
        for dataset in settings['datasets']:
            dataset['dataset'] = dataset['name']
            matrix = dataset['matrix'][0]
            dataset['matrix'] = matrix['name']
            if 'conversion' in matrix and matrix['conversion'] != []:
                dataset['rating_converter'] = matrix['conversion'][0]
            dataset['splitting'] = dataset['splitting'][0]
            # TODO rename split param
            dataset['splitting']['Train/testsplit'] = str(dataset['params']['Train/testsplit']) \
            + '/' + str(100 - dataset['params']['Train/testsplit'])

            del dataset['params']['Train/testsplit']

        # Format models
        models = {}
        for approach in settings['approaches']:
            model_name = approach['name']
            if approach['params'] is None:  # handle params null
                model_setting = {'name': model_name}
            else:
                model_setting = approach
            models.setdefault(self.model_api_dict[model_name], []).append(model_setting)
        config_dict = {
            'data': settings['datasets'],
            'models': models,
            'evaluation': settings['metrics'],
            'name': experiment_id,
            'top_K': int(settings['recommendations']),
            'rated_items_filter': not settings['includeRatedItems']
            if 'includeRatedItems' in settings else False,
            'type': settings['experimentMethod']}

        return config_dict, experiment_id


def create_model_api_dict(predictors, recommenders):
    """Generate a dictionary that maps approaches (models) to an API.

    Args:
        predictors(dict): the predictor approaches
        recommenders(dict): the recommender approaches

    Returns:
        (dict) the model-to-API dictionary
    """
    approaches = list(predictors.items()) + list(recommenders.items())
    model_to_api = {}
    for (header, options) in approaches:
        for option in options:
            model_to_api[option['name']] = header
    return model_to_api


def format_categorised(settings):
    """Format categorised (has a 'parent' key) settings.

    Args:
        settings(dict): the categorised settings

    Returns:
        (dict) the formatted settings

    """
    formatted_settings = []
    for (header, options) in settings.items():
        formatted_settings.append({'name': header, 'options': options})
    return formatted_settings


def reformat_all(uncategorised, categorised):
    """Reformat all (uncategorised and categorised) options.

    Args:
        uncategorised(list(tuple(str, list)): uncategorised (option type, options) tuples
        categorised(list(tuple(str, list)): categorised (option type, options) tuples

    Returns:
        (dict) the formatted options
    """
    options = {}
    for (option_type, inner_options) in uncategorised:
        options[option_type] = reformat(inner_options, False)
    for (option_type, inner_options) in categorised:
        options[option_type] = reformat(inner_options, True)
    return options


def reformat(options, nested):
    """Reformat options for form usage.

    Args:
        options(list(dict)): the options
        nested(bool): whether the options are nested or not

    Returns:
        (dict) the formatted options
    """
    if nested:
        for option in options:
            option['options'] = reformat_options(option['options'])
    else:
        options = reformat_options(options)

    return options


def reformat_options(options):
    """Reformat an options list from data to form.

    Args:
        options: the data options to format

    Returns:
        (list(dict)) the formatted 'name, value' options
    """
    # Add text and value fields
    return [{'name': option['name'], 'value': option} for option in options]


def form_to_data(settings):
    """Format from group list form format to data format.

    Args:
        settings(dict(dict)): the settings from which to reformat the lists

    """
    for option_name, option_list in settings['lists'].items():
        reformat_list(settings, option_name, option_list)
    del settings['lists']


def parse_if_number(string):
    """Cast a string to an int/float if it is one, or don't.

    Args:
        string: the string to parse

    Returns:
        the parsed string
    """
    if string:
        if isinstance(string, list):
            return [parse_if_number(s) for s in string]
        if isinstance(string, (float,int)):
            return string
        if string.isnumeric():
            return int(string)
        try:
            number = float(string)
            return number
        except ValueError:
            return string
    return string


def reformat_list(settings, option_name, option_list):
    """Reformat option list in settings from form to data.

    Args:
        settings(dict): the settings in which to store the option
        option_name(str): the name of the option list to format
        option_list(list): the option list

    """
    for option in option_list:
        option['params'] = {param['name']: parse_if_number(
            param['value']) for param in option['params']}
        # Format inner formgrouplists
        for inner_option_name, inner_option_list in option.items():
            if inner_option_name not in ['name', 'params']:
                reformat_list(option, inner_option_name, inner_option_list)
    settings[option_name] = option_list
