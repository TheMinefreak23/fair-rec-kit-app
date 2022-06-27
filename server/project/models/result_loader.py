"""This module contains functions to load & modify data from evaluation results.

methods:
    result_by_id
    get_overview
    id_to_name
    id_to_index
    name_to_index

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
from fairreckitlib.data.set.dataset import add_dataset_columns as add_data_columns

from fairreckitlib.data.filter.filter_config import FilterConfig
from fairreckitlib.data.filter.filter_config import FilterPassConfig
from fairreckitlib.data.filter.filter_config import DataSubsetConfig

from fairreckitlib.data.pipeline.data_pipeline import DataPipeline
from fairreckitlib.core.config.config_factories import GroupFactory
from fairreckitlib.data.filter.filter_factory import create_filter_factory
from fairreckitlib.core.events.event_dispatcher import EventDispatcher

from project.models.options_formatter import reformat_list
from . import recommender_system
from .constants import RESULTS_DIR
from .result_storage import load_results_overview, load_json

ADDITIONAL_COLUMNS = {
    'user-track-count': {'spotify': ['audio_snippet']}
}


def result_by_id(result_id, result_storage):
    """Set the current result to a result in the results overview by its id.

    Args:
    result_id(int): the result id
    result_store(ResultStorage): the result storage with the current result
    """
    results_overview = load_results_overview()
    relative_path = RESULTS_DIR + str(result_id) + "_" + \
                    id_to_name(results_overview, result_id)

    data = results_overview['all_results'][id_to_index(
        results_overview, result_id)]
    data['metadata']['runs'] = 0  # Store runs
    # loops through all the subdirectories, and thus - runs, of a certain calculation

    for subdir in [f.path for f in os.scandir(relative_path) if f.is_dir()]:
        run_overview = load_json(subdir + "/overview.json")
        # loops through individual results by looping through each entry in the overview.json
        for pair_id, pair_data in enumerate(run_overview['overview']):
            evaluation_path_full = os.getcwd() + "/" + \
                                   pair_data['evaluation_path']

            # TODO REMOVE WHEN LIB IS UP TO DATE: TEMPORARY FIX
            # evaluation_path_full = evaluation_path_full.replace('\\', '/')

            # ratings_settings_path_full = os.getcwd() + "/" + \
            #    pair_data['ratings_settings_path']

            if os.path.exists(evaluation_path_full):
                evaluation_data = load_json(evaluation_path_full)
                dataset_index = name_to_index(data['result'],
                                              run_overview['overview'][pair_id]['dataset'],
                                              'dataset', by_name=True)
                approach_index = name_to_index(
                    data['result'][dataset_index]['recs'],
                    run_overview['overview'][pair_id]['recommender_system'], 'approach')
                data['result'][dataset_index]['recs'][approach_index]['evals'] = add_evaluation(
                    data['result'][dataset_index]['recs'][approach_index]['evals'],
                    evaluation_data['evaluations'])
        data['metadata']['runs'] += 1

    result_storage.current_result = data


def get_overview(evaluation_id, runid):
    """Return a specific entry from a specific overview.json.

    Args:
    evaluation_id(int): the calculation id of the evaluation
    runid(int): the id of the specific dataset-recommender approach pair
    """
    results_overview = load_results_overview()

    name = id_to_name(results_overview, evaluation_id)

    relative_path = RESULTS_DIR + str(evaluation_id) + \
                    "_" + name + "/" + "run_" + str(runid)
    overview_path = relative_path + "/overview.json"
    run_overview = load_json(overview_path)
    return run_overview['overview']


def add_evaluation(data, evaluation):
    """Add an evaluation to the data."""
    if not evaluation:
        return data
    if not data:
        return format_evaluation(evaluation)
    for index, value in enumerate(evaluation):
        data[index]['evaluations'].append(value['evaluation'])
    return data


def format_evaluation(evaluation):
    """Format an evaluation to be used in the current_result."""
    for eval_item in evaluation:
        evaluation_list = [eval_item['evaluation']]
        eval_item.pop('evaluation')
        eval_item['evaluations'] = evaluation_list
    return evaluation


def id_to_name(json_data, result_id):
    """Return the name of a specific evaluation.

    args:
    json_data(dict): loaded json data from results_overview
    result_id(int): the id of the evaluation
    """
    return json_data['all_results'][id_to_index(json_data, result_id)]['metadata']['name']


def id_to_index(json_data, result_id):
    """Return the index of the entry in results_overview of a specific evaluation.

    args:
    json_data(dict): loaded json data from results_overview
    result_id(int): the id of the evaluation
    """
    current_result_overview_id = -1
    # Filter: Loop through all results and find the one with the matching ID.
    for iteration_id, data in enumerate(json_data['all_results']):
        if int(data['timestamp']['stamp']) == int(result_id):
            current_result_overview_id = iteration_id
    return current_result_overview_id


def name_to_index(json_data, name, key, by_name=False):
    """Return the index of the entry in results_overview of a dataset-recommender approach pair.

    Args:
    json_data(list): the loaded json data from results_overview
    name(str): the name of the dataset or the name of the approach
    key(str): the object that the function
                should match on (either 'dataset' or 'recommender_system')
    """
    current_index = -1
    for i, data in enumerate(json_data):
        result_value = data[key]
        if by_name and result_value['name'] == name or result_value == name:
            current_index = i
    return current_index


def get_chunk(start_rows, chunk_size, df_sorted):
    """Get a chunk of a dataframe.

    Args:
        start_rows: rows to start at
        chunk_size: size of the rows chunk
        df_sorted: the sorted dataframe to get the chunk from

    Returns:
        The part of the dataframe
    """
    # getting only chunk of data
    end_rows = start_rows + chunk_size
    end_rows = int(end_rows)

    # determine if at the end of the dataset
    rows_number = len(df_sorted)
    end_rows = min(end_rows, rows_number)

    # return part of table that should be shown
    return df_sorted[start_rows:end_rows]


def rename_headers(dataset_name, matrix_name, df_subset):
    """Rename the user and item headers, so they reflect their respective content.

    Args:
        dataset_name: the name of the dataset of the matrix
        matrix_name: the matrix name of the matrix with the headers
        df_subset: the dataframe with the headers

    """
    dataset = recommender_system.data_registry.get_set(dataset_name)
    if dataset is not None and not dataset.get_matrix_config(matrix_name) is None:
        item = dataset.get_matrix_config(matrix_name).item.key
        user = dataset.get_matrix_config(matrix_name).user.key
        df_subset.rename(columns={'user': user, 'item': item}, inplace=True)


def sort_headers(df_subset):
    """Sort the ratings headers.

    Args:
        df_subset: the ratings dataframe
    """
    for header_prefix in ['artist', 'track', 'movie']:
        name_headers = [header for header in df_subset.columns.values
                        if header in (header_prefix + '_name',
                                      header_prefix + '_title')]
        # print(name_headers)

        # Copy
        old_df = df_subset.copy()

        # Remove old headers
        for name_header in name_headers:
            df_subset.pop(name_header)

        # Get index of the first ID column
        score_index = list(df_subset.columns.values).index('score')
        id_index = next((i for i, e in enumerate(df_subset.columns.values)
                         if header_prefix + '_id' == e),
                        score_index - 1)
        # print(id_index)

        # Put identifying columns after ID columns
        for (index, name_header) in enumerate(name_headers):
            df_subset.insert(id_index + index + 1, name_header, old_df[name_header])


def show_info_columns(matrix_name, columns, recs):
    """Show additional info columns for the ratings.

    Args:
        matrix_name: the matrix of the experiment result
        columns(list): the columns selected for viewing
        recs: the recommendations/ratings result

    Returns:
        (dataframe) the ratings with the added info columns
    """
    if matrix_name == 'user-track-count':
        if 'audio_snippet' in columns:
            recs['audio_snippet'] = recs['track_spotify-uri']
    return recs


def add_dataset_columns(dataset_name, dataframe, columns, matrix_name):
    """Add columns to the requested result based on its dataset.

    Args:
        dataset_name: the name of dataset belonging to the dataframe
        dataframe: a pandas dataframe of the requested user results
        columns: the current list of columns
        matrix_name: the name of the matrix belonging to the dataframe

    Returns:
        The updated dataframe
    """
    dataset = recommender_system.data_registry.get_set(dataset_name)
    if dataset is None:
        return dataframe

    result = list(map(lambda column: column.lower(), columns))
    dataframe = add_data_columns(dataset, matrix_name, dataframe, result)

    show_info_columns(matrix_name, result, dataframe)
    return dataframe


def filter_results(dataframe, dataset_name, matrix_name, filters):
    """Filter a dataframe with results using specified filters.

    Args:
        dataframe: a dataframe containing results that need to be filtered
        dataset_name: the name of the dataframe dataset
        matrix_name: the name of the dataframe matrix
        filters(list): filter settings

    Returns:
        results after filtering
    """
    if not filters:
        return dataframe

    # Convert filters
    settings = {}  # TODO refactor?
    reformat_list(settings, 'subset', filters)  # TODO use reformat option instead?
    # print('after reformat list', settings)

    # Make a data subset config from the filters
    filter_pass_configs = []
    for filter_pass in settings['subset']:
        print(filter_pass)
        filter_configs = [FilterConfig(name=f['name'],
                                       params=f['params'])
                          for f in filter_pass['filter']]
        filter_pass_configs.append(FilterPassConfig(filters=filter_configs))

    subset_config = DataSubsetConfig(dataset=dataset_name,
                                     matrix=matrix_name,
                                     filter_passes=filter_pass_configs)

    data_factory = GroupFactory('subset')
    data_factory.add_factory(create_filter_factory(recommender_system.data_registry))

    # TODO: could also use parsing
    # TODO refactor (duplicate code in options formatter)
    # subset = []
    # for filter_pass in settings['subset']:
    #    subset.append({'filter_pass': filter_pass['filter']})
    #
    # import json
    # print('filters data format', json.dumps(subset, indent=4))
    # from fairreckitlib.data.filter.filter_config_parsing import parse_data_subset_config
    # subset_config = parse_data_subset_config({'subset': subset},
    #                                         recommender_system.data_registry,
    #                                         data_factory,
    #                                         EventDispatcher())

    # print('subset config', subset_config)

    temp_filter_dir = 'filtered'
    os.mkdir(temp_filter_dir)

    data_pipeline = DataPipeline(data_factory, EventDispatcher())
    dataframe = data_pipeline.filter_rows(temp_filter_dir,
                                          dataframe,
                                          subset_config)
    # from fairreckitlib.data.filter.filter_passes import filter_from_filter_passes
    # filter_from_filter_passes('filtered',dataframe,subset_config,)

    os.rmdir(temp_filter_dir)

    return dataframe
