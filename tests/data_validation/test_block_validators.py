import pytest

from pynomo.data_validation.axis_schemas import give_default_axis_values
from pynomo.data_validation.block_validators import validate_type_1_block_params


@pytest.fixture
def fixture():
    def error(errors, message):
        print(message)

    return error


def test_validate_type_1_block_params_a(fixture):
    # incorrect input
    error = fixture
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_1_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_1_block_params_b(fixture):
    # correct input
    error = fixture
    params = {'f1_params': 1.0,
              'f2_params': {},
              'f3_params': {},
              'f4_params': {}
              }
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_1_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_1_block_params_c(fixture):
    # correct input
    error = fixture
    f_params = {**give_default_axis_values('type_1'), **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    params = {'f1_params': f_params,
              'f2_params': f_params,
              'f3_params': f_params
              }
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_1_block_params('para', params, error)
    print(errors)
    assert ok is True
