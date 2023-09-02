import os
import kavw_cli_jinja.__main__ as app
import kavw_cli_jinja.errors as errors
import pytest
from unittest.mock import patch


def get_script_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_valid_json():
    return '{"username": "world"}'


@patch('builtins.print')
def test_success(mock_print):
    app.main(['app', get_script_dir() + '/data/example.jinja2', get_valid_json()])
    assert "Hello, world!" == str(mock_print.call_args[0][0])


def get_few_arguments_data():
    for row in [[], [1], [1, 2]]:
        yield row


@pytest.mark.parametrize("test_input", get_few_arguments_data())
def test_too_few_arguments(test_input):
    with pytest.raises(errors.TooFewArguments):
        app.main(test_input)


def test_too_much_arguments():
    with pytest.raises(errors.TooMuchArguments):
        app.main([1, 2, 3, 4])


@pytest.mark.parametrize("test_input", [
    '[1]', '"some string"', '1', '1.1', 'true', 'false', 'null'
])
def test_invalid_json(test_input):
    with pytest.raises(errors.InvalidJson):
        app.main(['app', get_script_dir() + '/data/example.jinja2', test_input])


def test_invalid_path():
    with pytest.raises(errors.InvalidPath):
        app.main(['app', get_script_dir() + '/data/foo.jinja2', get_valid_json()])


def test_invalid_dir():
    with pytest.raises(errors.InvalidDir):
        app.main(['app', get_script_dir() + '/foo/example.jinja2', get_valid_json()])
