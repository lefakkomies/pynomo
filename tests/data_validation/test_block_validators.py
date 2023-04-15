from pprint import pprint

import pytest
import logging
from pynomo.data_validation.axis_schemas import give_default_axis_values
from pynomo.data_validation.block_validators import validate_type_1_block_params, validate_type_2_block_params, \
    validate_type_3_block_params, validate_type_4_block_params, validate_type_5_block_params, \
    validate_type_6_block_params, validate_type_7_block_params, validate_type_8_block_params


@pytest.fixture
def fixture():
    def error(errors, message):
        print(message)

    return error


######################################################################################
# Block type 1
######################################################################################
def test_validate_type_1_block_params_a(fixture):
    # incorrect input
    error = fixture
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_1_block_params(True, params, error)
    logging.info(errors)
    assert ok is False


def test_validate_type_1_block_params_b(fixture):
    # incorrect input
    error = fixture
    params = {'f1_params': 1.0,
              'f2_params': {},
              'f3_params': {},
              'f4_params': {}
              }
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
    ok, errors = validate_type_1_block_params('para', params, error)
    print(errors)
    assert ok is True


######################################################################################
# Block type 2
######################################################################################
def test_validate_type_2_block_params_a(fixture):
    # incorrect input
    error = fixture
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_2_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_2_block_params_b(fixture):
    # incorrect input
    error = fixture
    params = {'f1_params': 1.0,
              'f2_params': {},
              'f3_params': {},
              'f4_params': {}
              }
    ok, errors = validate_type_2_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_2_block_params_c(fixture):
    # correct input
    error = fixture
    f_params = {**give_default_axis_values('type_1'), **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    params = {'f1_params': f_params,
              'f2_params': f_params,
              'f3_params': f_params
              }
    ok, errors = validate_type_2_block_params('para', params, error)
    print(errors)
    assert ok is True


######################################################################################
# Block type 3
######################################################################################
def test_validate_type_3_block_params_a(fixture):
    # incorrect input
    error = fixture
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_3_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_3_block_params_b(fixture):
    # incorrect input
    error = fixture
    params = {'f1_params': 1.0,
              'f2_params': {},
              'f3_params': {},
              'f4_params': {}
              }
    ok, errors = validate_type_3_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_3_block_params_c(fixture):
    # only one axis
    error = fixture
    f_params = {**give_default_axis_values('type_3'), **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    params = {'f_params': [f_params]}
    ok, errors = validate_type_3_block_params('para', params, error)
    print(errors)
    assert ok is False


def test_validate_type_3_block_params_d(fixture):
    # three axes
    error = fixture
    f_params = {**give_default_axis_values('type_3'), **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    params = {'f_params': [f_params, f_params, f_params]}
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_3_block_params('para', params, error)
    print(errors)
    assert ok is False


def test_validate_type_3_block_params_e(fixture):
    # four axes
    error = fixture
    f_params = {**give_default_axis_values('type_3'), **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    params = {'f_params': [f_params, f_params, f_params, f_params]}
    ok, errors = validate_type_3_block_params('para', params, error)
    print(errors)
    assert ok is True


######################################################################################
# Block 4 type
######################################################################################
def test_validate_type_4_block_params_a(fixture):
    # incorrect input
    error = fixture
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_4_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_4_block_params_b(fixture):
    # Incorrect input
    error = fixture
    params = {'f1_params': 1.0,
              'f2_params': {},
              'f3_params': {},
              'f4_params': {}
              }
    ok, errors = validate_type_4_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_4_block_params_c(fixture):
    # only one axis
    error = fixture
    f_params = {**give_default_axis_values('type_3'), **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    params = {'f_params': [f_params]}
    ok, errors = validate_type_4_block_params('para', params, error)
    print(errors)
    assert ok is False


def test_validate_type_4_block_params_d(fixture):
    # ok
    error = fixture
    f_params = {**give_default_axis_values('type_4'), **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    params = {'f1_params': f_params,
              'f2_params': f_params,
              'f3_params': f_params,
              'f4_params': f_params
              }
    ok, errors = validate_type_4_block_params('para', params, error)
    print(errors)
    assert ok is True


######################################################################################
# Block type 5
######################################################################################
def test_validate_type_5_block_params_a(fixture):
    # incorrect input
    error = fixture
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_5_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_5_block_params_b(fixture):
    # Incorrect input
    error = fixture
    params = {'f1_params': 1.0,
              'f2_params': {},
              'f3_params': {},
              'f4_params': {}
              }
    ok, errors = validate_type_5_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_5_block_params_c(fixture):
    # Wrong values
    error = fixture
    params = {'u_func': lambda x: x,
              'u_values': 1,
              'v_func': lambda x: x,
              'wd_func': lambda x, y: x + y,
              'wd_values': [1, 2, 3]
              }
    ok, errors = validate_type_5_block_params('para', params, error)
    print(errors)
    assert ok is False


def test_validate_type_5_block_params_d(fixture):
    # Correct values
    error = fixture
    params = {'u_func': lambda x: x,
              'u_values': [1, 2, 3],
              'v_func': lambda x: x,
              'wd_func': lambda x: x,
              'wd_values': [1, 2, 3]
              }
    ok, errors = validate_type_5_block_params('para', params, error)
    print(errors)
    assert ok is True


######################################################################################
# Block type 6
######################################################################################
def test_validate_type_6_block_params_a(fixture):
    # incorrect input
    error = fixture
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_6_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_6_block_params_b(fixture):
    # incorrect input
    error = fixture
    params = {'f1_params': 1.0,
              'f2_params': {},
              'f3_params': {},
              'f4_params': {}
              }
    ok, errors = validate_type_3_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_6_block_params_c(fixture):
    # incorrect input
    error = fixture
    f_params = {**give_default_axis_values('type_6'), **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    params = {'f_params': [f_params]}
    ok, errors = validate_type_3_block_params('para', params, error)
    print(errors)
    assert ok is False


def test_validate_type_6_block_params_d(fixture):
    # only one axis
    error = fixture
    f_params = {**give_default_axis_values('type_6'), **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    params = {'f1_params': f_params,
              'f2_params': f_params
              }
    ok, errors = validate_type_6_block_params('para', params, error)
    print(errors)
    assert ok is True


def test_validate_type_6_block_params_e(fixture):
    # incorrect three axes
    error = fixture
    f_params = {**give_default_axis_values('type_6'), **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    params = {'f1_params': f_params,
              'f2_params': f_params,
              'f3_params': f_params
              }
    ok, errors = validate_type_6_block_params('para', params, error)
    print(errors)
    assert ok is False


######################################################################################
# Block type 7
######################################################################################
def test_validate_type_7_block_params_a(fixture):
    # incorrect input
    error = fixture
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_7_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_7_block_params_b(fixture):
    # incorrect input
    error = fixture
    params = {'f1_params': 1.0,
              'f2_params': {},
              'f3_params': {},
              'f4_params': {}
              }
    ok, errors = validate_type_7_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_7_block_params_c(fixture):
    # correct input
    error = fixture
    f_params = {**give_default_axis_values('type_7'), **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    params = {'f1_params': f_params,
              'f2_params': f_params,
              'f3_params': f_params
              }
    ok, errors = validate_type_7_block_params('para', params, error)
    print(errors)
    assert ok is True


######################################################################################
# Block type 8
######################################################################################
def test_validate_type_8_block_params_a(fixture):
    # incorrect input
    error = fixture
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_8_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_8_block_params_b(fixture):
    # incorrect input
    error = fixture
    params = {'f1_params': 1.0,
              'f2_params': {},
              'f3_params': {},
              'f4_params': {}
              }
    ok, errors = validate_type_8_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_8_block_params_c(fixture):
    # only one axis
    error = fixture
    f_params = {**give_default_axis_values('type_8'), **{'function_x': lambda x: x,
                                                         'function_y': lambda x: x,
                                                         'u_min': 0.0,
                                                         'u_max': 1.0}}
    params = {'f_params': f_params}
    ok, errors = validate_type_8_block_params('para', params, error)
    print(errors)
    assert ok is True


def test_validate_type_8_block_params_d(fixture):
    # only one axis
    error = fixture
    f_params = {**give_default_axis_values('type_8'), **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    params = {'f_params': f_params}
    ok, errors = validate_type_8_block_params('para', params, error)
    print(errors)
    assert ok is True


def test_validate_type_8_block_params_e(fixture):
    # Too many fields present
    error = fixture
    f_params = {**give_default_axis_values('type_8'), **{'function_x': lambda x: x,
                                                         'function_y': lambda x: x,
                                                         'function': lambda x: x,
                                                         'u_min': 0.0,
                                                         'u_max': 1.0}}
    params = {'f_params': f_params}
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_8_block_params('para', params, error)
    print(errors)
    assert ok is False
