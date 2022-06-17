"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json
# from fairreckitlib.core.core_constants import ELLIOT_API
from fairreckitlib.core.core_constants import TYPE_PREDICTION, TYPE_RECOMMENDATION

# constants
DEFAULTS = {  # 'split': 80,
    'recCount': {'min': 1, 'max': 100, 'default': 10},
}  # default values
DEFAULT_SPLIT = {'name': 'Train/testsplit',
                 'default': '80', 'min': 0, 'max': 100}


class OptionsFormatter:
    """Formatter for the experiment options"""
    def __init__(self, recommender_system):
        self.model_api_dict = {}
        # TODO for now use this to get the dataset matrix
        self.dataset_matrices = {}
        self.options = self.create_available_options(recommender_system)

    def create_available_options(self, recommender_system):
        """Gets options from FairRecKitLib and formats them for usage on the client side

        Args:
            recommender_system(RecommenderSystem): the recommender system to get the options from

        Returns:
            (dict) the formatted options
        """

        # DEV
        #print(recommender_system.get_available_datasets())
        #print(recommender_system.get_available_data_filters())

        datasets = recommender_system.get_available_datasets()
        self.dataset_matrices = {dataset: list(matrices.keys()) for (
            dataset, matrices) in datasets.items()}
        # print(DATASET_MATRICES)
        predictors = recommender_system.get_available_algorithms(TYPE_PREDICTION)
        recommenders = recommender_system.get_available_algorithms(
            TYPE_RECOMMENDATION)
        # TODO different metrics for diff types
        pred_metrics = recommender_system.get_available_metrics(TYPE_PREDICTION)
        rec_metrics = recommender_system.get_available_metrics(TYPE_RECOMMENDATION)

        self.model_api_dict = create_model_api_dict(predictors, recommenders)

        # Format categorised settings (most settings are categorised once)
        # TODO refactor
        # print('before format categ.', json.dumps(list(datasets.items())[0], indent=4))
        datasets = format_categorised(datasets)
        # print('after format categ.', json.dumps(datasets[0], indent=4))
        recommenders = format_categorised(recommenders)
        predictors = format_categorised(predictors)
        pred_metrics = format_categorised(pred_metrics)
        rec_metrics = format_categorised(rec_metrics)

        self.set_dynamic_options(datasets, rec_metrics + pred_metrics, recommender_system)

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
        options = reformat_all(uncategorised, categorised)
        options['defaults'] = DEFAULTS

        # print('datasets tests', json.dumps(datasets[0], indent=4))
        # print('recommender tests', json.dumps(recommenders[0], indent=4))
        # print(options)

        return options

    def set_dynamic_options(self, datasets, metrics, recommender_system):
        """Set the nested (dynamic) list options

        Args:
            datasets: the available datasets
            metrics: the available metrics
            recommender_system: the recommender system for the experiment

        """
        filters = recommender_system.get_available_data_filters()

        # Filters for datasets
        for dataset in datasets:
            # TODO this is stupid because we just created the options key
            dataset['params'] = dataset['options']
            del dataset['options']
            self.set_dataset_params(dataset, filters, recommender_system)

        # Filters for metrics
        for metric in metrics:
            for option in metric['options']:
                metric_datasets = []
                for dataset in datasets:
                    metric_dataset_options = [
                        self.make_matrix_option(dataset, filters)
                    ]
                    metric_datasets.append({'name': dataset['name'], 'params': {
                        'dynamic': metric_dataset_options}})
                # Make dataset option
                # TOOD refactor
                dataset_option = {'name': 'dataset',
                                 'title': 'subgroups',
                                 'options': reformat(metric_datasets, False)
                                  }
                option['params']['dynamic'] = [dataset_option]

    def set_dataset_params(self, dataset, filters, recommender_system):
        """Set the dataset option parameters

        Args:
            dataset: the dataset to set the parameters for
            filter_option(dict): the filters available for the datasets
            recommender_system: the recommender system for the experiments

        """
        converters = recommender_system.get_available_rating_converters()
        splits = recommender_system.get_available_splitters()

        formatted_splits = reformat(splits, False)
        # Same split option for all datasets
        split_type_option = {'name': 'type of split',
                             'single': True,
                             'required': True,
                             'title': 'splitting',
                             # 'article': 'a',
                             'default': formatted_splits[0],
                             'options': formatted_splits}

        dataset['params']['values'] = [DEFAULT_SPLIT]
        # print('dataset', dataset)
        # TODO refactor
        dataset['params']['dynamic'] = [
            self.make_matrix_option(dataset, filters, converters), split_type_option]
            #print('==FILTERS==', formatted_filters)
        # print(dataset['params']['options'])

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


        return {'name': 'filter pass',# TODO rename to filter groups?
                 'title': 'subset',
                 'options': reformat(filter_pass_list, False)}

    def make_matrix_option(self, dataset, filters, converters=None):
        matrices = []
        dataset_name = dataset['name']
        for matrix_name in self.dataset_matrices[dataset_name]:
            dynamic_options = []
            if converters: # TODO refactor
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

        print('experiment settings from client:', json.dumps(settings, indent=4))

        name = experiment['metadata']['name']
        experiment_id = experiment['timestamp']['stamp'] + '_' + name

        form_to_data(settings)
        print('formatted from form', json.dumps(settings, indent=4))

        # Format datasets
        # Add generic split to all dataset
        for dataset in settings['datasets']:
            # print(dataset)
            # TODO refactor
            dataset['dataset'] = dataset['name']
            matrix = dataset['matrix'][0]
            dataset['matrix'] = matrix['name']
            # TODO refactor = dataset['name'] = reformat_list(dataset['matrix'])
            # TODO for now pick item matrix if available, else first matrix
            # print(DATASET_MATRICES)
            # print(dataset['dataset'])
            # available_matrices = DATASET_MATRICES[dataset['dataset']]
            # dataset['matrix'] = 'user-track-count'
            # if 'user-track-count' in available_matrices else available_matrices[0]
            if 'conversion' in matrix and matrix['conversion'] != []:
                dataset['rating_converter'] = matrix['conversion'][0]
            dataset['splitting'] = dataset['splitting'][0]
            # TODO rename split param
            dataset['splitting']['test_ratio'] = (
                100 - int(dataset['params']['Train/testsplit'])) / 100

        # Format models
        models = {}
        for approach in settings['approaches']:
            model_name = approach['name']
            if approach['params'] is None:  # handle params null
                # TODO handle params null in frontend?
                model_setting = {'name': model_name}
            else:
                model_setting = approach
            models.setdefault(self.model_api_dict[model_name], []).append(model_setting)
        # print(name)
        config_dict = {
            'data': settings['datasets'],
            'models': models,
            'evaluation': settings['metrics'],
            'name': experiment_id,
            'top_K': int(settings['recommendations']),
            'rated_items_filter': not settings['includeRatedItems']
            if 'includeRatedItems' in settings else False,
            'type': settings['experimentMethod']}

        # print(config_dict)
        # return config_dict, experiment_id


# TODO do this in another way
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
    # print(dict)
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
        # print(settings[header])
        # options['header'] = header TODO handle categories/APIs differently
        formatted_settings.append({'name': header, 'options': options})
    # print(formatted_settings)
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

            # Disable Elliot options
            # if option['name'] == ELLIOT_API:
            # for disable_option in option['options']:
            #disable_option['disabled'] = True
            # print(disable_option)

            #option['name'] = option['name'] + ' (unavailable)'
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
        # print(option_list)
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
        # print(option)
        option['params'] = {param['name']: parse_if_number(
            param['value']) for param in option['params']}
        # Format inner formgrouplists
        for inner_option_name, inner_option_list in option.items():
            # TODO use settings/lists key after all?
            if inner_option_name not in ['name', 'params']:
                # print(json.dumps(option, indent=4))
                reformat_list(option, inner_option_name, inner_option_list)
    settings[option_name] = option_list
