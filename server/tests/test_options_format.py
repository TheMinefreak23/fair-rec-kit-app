"""This module tests the functionality of the options_formatter module.
test_model_api_dict(): test model-to-API dictionary generation.
test_format_categorised(): test data to form reformatting fpr categorised options.
test_reformat_all(): test data to form reformatting for multiple options.
test_reformat(): test data to form reformatting.
test_reformat_options(): test reformatting of options.
test_form_to_data(): test form to data formatting.
test_parse_if_number(): test parsing of string to int or float.
test_reformat_list(): test reformatting of form list to data list.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from project.models.options_formatter \
    import create_model_api_dict, format_categorised,\
    reformat_all, reformat, \
    reformat_options, form_to_data, \
    parse_if_number, reformat_list

form_options = {}

data_options = {}
nested_data_options = {}


def test_model_api_dict():
    """Test model-to-API dictionary generation."""
    # Empty case
    model_to_api = create_model_api_dict({}, {})
    assert not model_to_api

    # Simple case
    #model_to_api = create_model_api_dict({}, {})
    #assert model_to_api == {}


def test_format_categorised():
    """Test data to form reformatting fpr categorised options."""
    # Empty case
    formatted = format_categorised({})
    assert not formatted


# def test_available_options():


def test_reformat_all():
    """Test data to form reformatting for multiple options."""
    # Empty case
    formatted = reformat_all({}, {})
    assert not formatted


def test_reformat():
    """Test data to form reformatting."""
    # Empty case
    assert reformat([], False) == []
    # TODO same as test_reformat_options:
    assert reformat([], True) == []


def test_reformat_options():
    """Test reformatting of options."""
    # Empty case
    assert reformat_options([]) == []


#def test_config_from_settings():
    # TODO assumption: no Empty case
    #config_dict_from_settings()


def test_form_to_data():
    """Test form to data formatting."""
    # Empty case
    settings = {'lists': {}}
    form_to_data(settings)
    assert not settings

    # Lists key deleted
    # assert 'lists' not in settings


def test_parse_if_number():
    """Test parsing of string to int or float."""
    # Already float case
    float_number = 0.1
    assert isinstance(parse_if_number(float_number), float)

    # Already int (and thus float) case
    number = 0
    #assert isinstance(parse_if_number(number), float)
    assert isinstance(parse_if_number(number), int)

    # Parseable to int (numeric) case
    assert isinstance(parse_if_number(str(number)), int)

    # Parseable to float case
    assert isinstance(parse_if_number(str(float_number)), float)

    # Neither parseable to int nor float
    word = 'foobar'
    assert parse_if_number(word) == word


def test_reformat_list():
    """Test reformatting of form list to data list."""
    # Empty dict case
    settings = {}
    reformat_list(settings, 'foo', [])
    assert settings == {'foo': []}

    # Basic case
    settings = {}
    option = {'params': [{'name': 'the beast', 'value': '666'}]}
    reformat_list(settings, 'foo', [option])
    assert settings['foo'] == [{'params': {'the beast': 666}}]

    # List value case
    settings = {}
    # TODO refactor?
    option = {'params': [{'name': 'the beast', 'value': ['1', '2']}]}
    reformat_list(settings, 'foo', [option])
    assert settings['foo'] == [{'params': {'the beast': [1, 2]}}]
    # TODO test nested inner recursive formatting
