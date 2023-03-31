import pytest

from pynomo.data_validation.axis_validators import validate_type_1_axis_params, validate_type_9_axis_params


@pytest.fixture
def fixture():
    def error(errors, message):
        print(message)

    return error


def test_validate_type_1_axis_params_a(fixture):
    error = fixture
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_1_axis_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_1_axis_params_b(fixture):
    error = fixture
    params = {'function': lambda x: x,
              'u_min': 0,
              'u_max': 10}
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_1_axis_params(True, params, error)
    print(errors)
    assert ok is True


def test_validate_type_9_axis_params_a(fixture):
    error = fixture
    params = {'scale_type': 'linear',
              'tick_distance_smart': 30,
              'base_stop': None}
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_9_axis_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_9_axis_params_b(fixture):
    error = fixture
    params = {'function': lambda x: x,
              'grid': True,
              'u_min': 0,
              'u_max': 10}
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_9_axis_params(True, params, error)
    print(errors)
    assert ok is False
