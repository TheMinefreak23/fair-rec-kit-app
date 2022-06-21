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
import copy
import json
from fairreckitlib.core.core_constants import TYPE_PREDICTION, TYPE_RECOMMENDATION

# constants
DEFAULTS = {
    'recCount': {'min': 1, 'max': 100, 'default': 10},
}  # default values
DEFAULT_SPLIT = {'name': 'Train/testsplit',
                 'default': '80', 'min': 0, 'max': 100}


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
        self.recommender_system = recommender_system
        self.options_without_filters = {}  # Store options without filters for updating later
        self.options = {}
        self.create_available_options()

    def create_available_options(self, chosen_datasets=[]):
        """Get options from FairRecKitLib and formats them for usage on the client side.

        Args:
            chosen_datasets(list): existing chosen datasets with which the subgroup should be updated

        Returns:
            (dict) the formatted options
        """

        filters = self.recommender_system.get_available_data_filters()

        if not chosen_datasets:
            datasets = self.recommender_system.get_available_datasets()
            self.dataset_matrices = {dataset: list(matrices.keys()) for (
                dataset, matrices) in datasets.items()}
            predictors = self.recommender_system.get_available_algorithms(TYPE_PREDICTION)
            recommenders = self.recommender_system.get_available_algorithms(
                TYPE_RECOMMENDATION)
            pred_metrics = self.recommender_system.get_available_metrics(TYPE_PREDICTION)
            rec_metrics = self.recommender_system.get_available_metrics(TYPE_RECOMMENDATION)

            self.model_api_dict = create_model_api_dict(predictors, recommenders)

            # Format categorised settings (most settings are categorised once)
            datasets = format_categorised(datasets)
            recommenders = format_categorised(recommenders)
            predictors = format_categorised(predictors)
            pred_metrics = format_categorised(pred_metrics)
            rec_metrics = format_categorised(rec_metrics)

            # Filters for datasets
            for dataset in datasets:
                # TODO this is stupid because we just created the options key
                dataset['params'] = dataset['options']
                del dataset['options']
                self.set_dataset_params(dataset, filters)

            uncategorised = {
                'datasets': datasets,
            }
            categorised = {
                'predictors': predictors,
                'recommenders': recommenders,
                'recMetrics': rec_metrics,
                'predMetrics': pred_metrics
            }

            # Store options before final reformat for faster update
            self.options_without_filters = {'uncategorised': copy.deepcopy(uncategorised),
                                            'categorised': copy.deepcopy(categorised)}

            # Use stored dictionary for dataset-matrix pairs (all available options)
            self.set_metric_filters(rec_metrics + pred_metrics, self.dataset_matrices, filters)
        else:
            # Get the stored options without filters
            options = copy.deepcopy(self.options_without_filters)
            uncategorised = options['uncategorised']
            categorised = options['categorised']

            # Get dataset options from chosen datasets
            datasets_matrices = {}
            for dataset in chosen_datasets:
                if 'matrix' in dataset:
                    print('CHOSEN DATASETS MATRIX', dataset['matrix'])
                    matrix_name = dataset['matrix']['name']
                    datasets_matrices.setdefault(dataset['name'], []).append(matrix_name)

            self.set_metric_filters(categorised['recMetrics'] +
                                    categorised['predMetrics'],
                                    datasets_matrices,
                                    filters)

        options = reformat_all(uncategorised, categorised)
        options['defaults'] = DEFAULTS

        self.options = options

    def set_metric_filters(self, metrics, dataset_matrices, filters):
        """Create the subgroup options for the metrics using the available datasets.

        Args:
            metrics: the available metrics to filter
            dataset_matrices(dict): the datasets with matrices to choose from
            filters: the available filters
        """
        # Filters for metrics
        for metric in metrics:
            for option in metric['options']:
                metric_datasets = []
                for (dataset_name, matrix_names) in dataset_matrices.items():
                    metric_dataset_options = [
                        self.make_matrix_option(dataset_name, matrix_names, filters)
                    ]
                    metric_datasets.append({'name': dataset_name, 'params': {
                        'dynamic': metric_dataset_options}})
                # Make dataset option
                dataset_option = {'name': 'dataset',
                                  'title': 'subgroups',
                                  'options': reformat(metric_datasets, False)
                                  }
                option['params']['dynamic'] = [dataset_option]
                print('DATASET OPTION', dataset_option)

    def set_dataset_params(self, dataset, filters):
        """Set the dataset option parameters.

        Args:
            dataset: the dataset to set the parameters for
            filters: the filters available for the datasets

        """
        converters = self.recommender_system.get_available_rating_converters()
        splits = self.recommender_system.get_available_splitters()

        formatted_splits = reformat(splits, False)
        # Same split option for all datasets
        split_type_option = {'name': 'type of split',
                             'single': True,
                             'required': True,
                             'title': 'splitting',
                             'default': formatted_splits[0],
                             'options': formatted_splits}

        dataset['params']['values'] = [DEFAULT_SPLIT]
        # print('dataset', dataset)
        dataset_name = dataset['name']
        dataset['params']['dynamic'] = [
            self.make_matrix_option(dataset_name,
                                    self.dataset_matrices[dataset_name],
                                    filters, converters),
            split_type_option]

    def make_filter_option(self, matrix_filters):
        """Make a filter list option

        Args:
            matrix_filters: the filters available for the matrix

        Returns:
            the filter option for the form
        """
        # TODO refactor

        filter_pass_option = {'name': 'filter',
                              'title': 'filter',
                              'options': reformat(matrix_filters, False)
                              }
        filter_pass_list = [{'name': 'filter pass', 'params': {'dynamic': [filter_pass_option]}}]

        return {'name': 'filter pass',  # TODO rename to filter groups?
                'title': 'subset',
                'options': reformat(filter_pass_list, False)}

    def make_matrix_option(self, dataset_name, matrix_names, filters, converters=None):
        matrices = []
        for matrix_name in matrix_names:
            dynamic_options = []
            if converters:  # TODO refactor
                dataset_matrix_converters = converters[dataset_name][matrix_name]
                # Converter per matrix
                converter_option = {'name': 'rating converter',
                                    'single': True,
                                    'title': 'conversion',
                                    'options': reformat(dataset_matrix_converters, False)}
                dynamic_options.append(converter_option)
            # Filter per matrix
            matrix_filters = filters[dataset_name][matrix_name]
            dynamic_options.append(self.make_filter_option(matrix_filters))

            matrices.append({'name': matrix_name, 'params': {
                'dynamic': dynamic_options}})
        return self.make_single_dynamic_option('matrix', matrices)

    def make_single_dynamic_option(self, name, list):
        """Make option for a single form group list

        Args:
            option_name(str): the name of the option
            option_list(list): the list of options available for the option

        Returns:
            the option for the form
        """
        return {
            'name': name,
            'single': True,
            'required': True,
            'title': name,
            'options': reformat(list, False),
        }

    def config_dict_from_settings(self, experiment):
        """Create a configuration dictionary from client settings.

        Args:
            experiment(dict): the experiment settings sent from the client
        Returns:
            (dict) the configuration
        """
        settings = experiment['settings']

        # settings_without_raw = {key: settings[key] for key in settings if key != 'rawSettings'}
        # print('experiment settings from client:', json.dumps(settings_without_raw, indent=4))

        name = experiment['metadata']['name']
        experiment_id = experiment['timestamp']['stamp'] + '_' + name

        form_to_data(settings)
        settings_without_raw = {key: settings[key] for key in settings if key != 'rawSettings'}
        print('formatted from form', json.dumps(settings_without_raw, indent=4))

        def format_data_matrix(data):
            # TODO refactor
            data['dataset'] = data['name']
            del data['name']
            data_matrix = data['matrix']
            data['matrix'] = data_matrix['name']
            # print(data)
            subset = data_matrix['subset']
            # print(data)
            data['subset'] = []
            for filter_pass in subset:
                data['subset'].append({'filter_pass': filter_pass['filter']})
            # print(data)

        # Format datasets
        for dataset in settings['datasets']:
            # print(dataset)
            matrix = dataset['matrix']
            format_data_matrix(dataset)
            if 'conversion' in matrix:
                dataset['rating_converter'] = matrix['conversion']
            # TODO rename split param
            dataset['splitting']['test_ratio'] = (100 -
                                                  int(dataset['params']['Train/testsplit'])
                                                  ) / 100

        # Format models
        models = {}
        for approach in settings['approaches']:
            model_name = approach['name']
            if approach['params'] is None:  # handle params null
                model_setting = {'name': model_name}
            else:
                model_setting = approach
            models.setdefault(self.model_api_dict[model_name], []).append(model_setting)
        # print(name)

        # Format metrics (filters)
        metrics = []
        print(settings['metrics'])
        for metric in settings['metrics']:
            # Format subgroups
            if metric['subgroups']:
                for subgroup in metric['subgroups']:
                    format_data_matrix(subgroup)
                    # TODO clone?
                    subgroup_metric = {'name': metric['name'],
                                       'params': metric['params'],
                                       'subgroup': subgroup}
                    metrics.append(subgroup_metric)
            else:
                metrics.append(metric)
            del metric['subgroups']

        config_dict = {
            'data': settings['datasets'],
            'models': models,
            'evaluation': metrics,
            'name': experiment_id,
            'top_K': int(settings['recommendations']),
            'rated_items_filter': not settings['includeRatedItems']
            if 'includeRatedItems' in settings else False,
            'type': settings['experimentMethod']}

        # print('config dict from settings:', json.dumps(config_dict, indent=4))
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
        uncategorised(dict): uncategorised (option type, options) key-value pairs
        categorised(dict): categorised (option type, options) key-value pairs

    Returns:
        (dict) the formatted options
    """
    options = {}
    for (option_type, inner_options) in uncategorised.items():
        options[option_type] = reformat(inner_options, False)
    for (option_type, inner_options) in categorised.items():
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
    # TODO refactor
    if string:
        if string == 'null':
            return None
        if isinstance(string, dict):
            return {k: parse_if_number(v) for k, v in string.items()}
        if isinstance(string, list):
            return [parse_if_number(s) for s in string]
        if isinstance(string, (float, int)):
            return string
        if string.isnumeric():
            return int(string)
        try:
            number = float(string)
            return number
        except ValueError:
            return string
    return string


def reformat_list(settings, option_name, option_group):
    """Reformat option form group list in settings from form to data.

    Args:
        settings(dict): the settings in which to store the option
        option_name(str): the name of the option list to format
        option_group(list|dict): the option list or single option

    """

    def reformat_option(option):
        option['params'] = {param['name']: parse_if_number(
            param['value']) for param in option['params']}
        # Format inner formgrouplists
        for inner_option_name, inner_option_list in option.items():
            if inner_option_name not in ['name', 'params']:
                reformat_list(option, inner_option_name, inner_option_list)

    if isinstance(option_group, list):
        for option_item in option_group:
            reformat_option(option_item)
    else:  # Single option group
        reformat_option(option_group)

    settings[option_name] = option_group
