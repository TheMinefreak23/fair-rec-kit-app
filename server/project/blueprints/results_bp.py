"""The methods in this module call functions that are in the models folder to load and edit results.

blueprint routes:
    results
    edit
    delete

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from flask import (Blueprint, request)

from project.models.result_storage import edit_result, load_results_overview, delete_result

blueprint = Blueprint('results', __name__, url_prefix='/api/all-results')


@blueprint.route('/', methods=['GET'])
def results():
    """Load in the results overview.

    Returns:
        The requested results overview
    """
    return load_results_overview()


@blueprint.route('/edit', methods=['POST'])
def edit():
    """Change the metadata of a selected experiment.

    Returns:
        A message indicating the operation was succesful
    """
    data = request.get_json()
    data_id = data.get('id')
    new_name = data.get('new_name')
    new_tags = data.get('new_tags')
    new_email = data.get('new_email')
    edit_result(data_id, new_name, new_tags, new_email)
    return "Edited index"


@blueprint.route('/delete', methods=['POST'])
def delete():
    """Delete a selected result from the results.

    Returns:
        A message indicating the operation was succesful
    """
    data = request.get_json()
    result_id = data.get('id')
    name = data.get('name')
    delete_result(result_id, name)
    return "Removed index"
