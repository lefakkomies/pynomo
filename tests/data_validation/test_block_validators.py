# -*- coding: utf-8 -*-
#
#    This file is part of PyNomo -
#    a program to create nomographs with Python (https://github.com/lefakkomies/pynomo)
#
#    Copyright (C) 2007-2023  Leif Roschier  <leif.roschier@iki.fi>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Testing of block validators

    Testing of block validators defined in block_validators.py

"""

import pytest
import logging

from pynomo.data_validation.axis_schemas import give_default_axis_values
from pynomo.data_validation.block_validators import validate_type_1_block_params, validate_type_2_block_params, \
    validate_type_3_block_params, validate_type_4_block_params, validate_type_5_block_params, \
    validate_type_6_block_params, validate_type_7_block_params, validate_type_8_block_params, \
    validate_type_9_block_params, validate_type_10_block_params, validate_block_params


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
    ok, errors = validate_type_8_block_params('para', params, error)
    print(errors)
    assert ok is False


######################################################################################
# Block type 9 (determinant)
######################################################################################
def test_validate_type_9_block_params_a(fixture):
    # incorrect input
    error = fixture
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_9_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_9_block_params_b(fixture):
    # incorrect input
    error = fixture
    params = {'f1_params': 1.0,
              'f2_params': {},
              'f3_params': {},
              }
    ok, errors = validate_type_9_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_9_block_params_c(fixture):
    # correct input for all axis
    error = fixture
    f_params = {
        **give_default_axis_values('type_9_axis'),
        **{'f': lambda x: x, 'g': lambda x: x, 'h': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}
    }
    params = {'f1_params': f_params,
              'f2_params': f_params,
              'f3_params': f_params,
              }
    # pprint(params)
    ok, errors = validate_type_9_block_params(True, params, error)
    # print(errors)
    assert ok is True


def test_validate_type_9_block_params_d(fixture):
    # incorrect input for all grid
    error = fixture
    f_params = {
        **give_default_axis_values('type_9_axis'),
        **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0, 'grid': True}
    }
    params = {'f1_params': f_params,
              'f2_params': f_params,
              'f3_params': f_params,
              }
    # pprint(params)
    ok, errors = validate_type_9_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_9_block_params_e(fixture):
    # correct input for all grid
    error = fixture
    f_params = {
        **give_default_axis_values('type_9_grid'),
        **{'f_grid': lambda x, y: x + y,
           'g_grid': lambda x, y: x + y,
           'h_grid': lambda x, y: x + y,
           'u_start': 0.0,
           'u_stop': 1.0,
           'v_start': 0.0,
           'v_stop': 1.0,
           'grid': True}
    }
    params = {'f1_params': f_params,
              'f2_params': f_params,
              'f3_params': f_params,
              }
    # pprint(params)
    ok, errors = validate_type_9_block_params(True, params, error)
    print(errors)
    assert ok is True


def test_validate_type_9_block_params_f(fixture):
    # correct input for all grid + axis
    error = fixture
    f_params_grid = {
        **give_default_axis_values('type_9_grid'),
        **{'f_grid': lambda x, y: x + y,
           'g_grid': lambda x, y: x + y,
           'h_grid': lambda x, y: x + y,
           'u_start': 0.0,
           'u_stop': 1.0,
           'v_start': 0.0,
           'v_stop': 1.0,
           'grid': True}
    }
    f_params_axis = {
        **give_default_axis_values('type_9_axis'),
        **{'f': lambda x: x, 'g': lambda x: x, 'h': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}
    }
    params = {'f1_params': f_params_axis,
              'f2_params': f_params_grid,
              'f3_params': f_params_axis,
              }
    # pprint(params)
    ok, errors = validate_type_9_block_params(True, params, error)
    print(errors)
    assert ok is True


def test_validate_type_9_block_params_g(fixture):
    # correct input for all grid + axis
    error = fixture
    N_params_1 = {
        'u_min': 3.0,
        'u_max': 10.0,
        'f': lambda u: 0,
        'g': lambda u: u,
        'h': lambda u: 1.0,
        'title': r'$u_1$',
        'scale_type': 'linear',
        'tick_levels': 3,
        'tick_text_levels': 2,
        'grid': False}
    N_params_2 = {
        'u_min': 0.0,  # for alignment
        'u_max': 1.0,  # for alignment
        'f_grid': lambda u, v: u + 2.0,
        'g_grid': lambda u, v: 2 * v + 5.0,
        'h_grid': lambda u, v: 1.0,
        'u_start': 0.0,
        'u_stop': 1.0,
        'v_start': 0.0,
        'v_stop': 1.0,
        'u_values': [0.0, 0.25, 0.5, 0.75, 1.0],
        'v_values': [0.0, 0.25, 0.5, 0.75, 1.0],
        'grid': True,
        'text_prefix_u': r'$u_2$=',
        'text_prefix_v': r'$v_2$=',
    }
    params = {'f1_params': N_params_1,
              'f2_params': N_params_1,
              'f3_params': N_params_2,
              }
    # pprint(params)
    ok, errors = validate_type_9_block_params(True, params, error)
    print(errors)
    assert ok is True


######################################################################################
# Block type 10
######################################################################################
def test_validate_type_10_block_params_a(fixture):
    # incorrect input
    error = fixture
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_10_block_params(True, params, error)
    logging.info(errors)
    assert ok is False


def test_validate_type_10_block_params_b(fixture):
    # incorrect input
    error = fixture
    params = {'f1_params': 1.0,
              'f2_params': {},
              'f3_params': {},
              'f4_params': {}
              }
    ok, errors = validate_type_10_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_10_block_params_c(fixture):
    # correct input
    error = fixture
    f_params = {**give_default_axis_values('type_10'), **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    f_params_w = {
        **give_default_axis_values('type_10_w'),
        **{'function_3': lambda x: x,
           'function_4': lambda x: x,
           'u_min': 0.0,
           'u_max': 1.0}
    }
    params = {'f1_params': f_params,
              'f2_params': f_params,
              'f3_params': f_params_w
              }
    ok, errors = validate_type_10_block_params(True, params, error)
    print(errors)
    assert ok is True


######################################################################################
# General block validators
######################################################################################
def test_validate_block_params_a(fixture):
    # correct input
    error = fixture
    f_params = {**give_default_axis_values('type_10'), **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    f_params_w = {
        **give_default_axis_values('type_10_w'),
        **{'function_3': lambda x: x,
           'function_4': lambda x: x,
           'u_min': 0.0,
           'u_max': 1.0}
    }
    params = {'f1_params': f_params,
              'f2_params': f_params,
              'f3_params': f_params_w,
              'block_type': 'type_10'
              }
    ok, errors = validate_block_params(True, params, error)
    print(errors)
    assert ok is True


def test_validate_block_params_b(fixture):
    # incorrect input
    error = fixture
    f_params = {**give_default_axis_values('type_10'), **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    f_params_w = {
        **give_default_axis_values('type_10_w'),
        **{'function_3': lambda x: x,
           'function_4': lambda x: x,
           'u_min': 0.0,
           'u_max': 1.0}
    }
    params = {'f1_params': f_params,
              'f2_params': f_params,
              'f3_params': f_params_w,
              'block_type': 'type_1'
              }
    ok, errors = validate_block_params(True, params, error)
    print(errors)
    assert ok is False
