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
import pytest

from pynomo.data_validation.axis_schemas import give_default_axis_values
from pynomo.data_validation.axis_validators import validate_type_1_axis_params, validate_type_9_axis_grid_params, \
    validate_type_2_axis_params, validate_type_3_axis_params, validate_type_4_axis_params, validate_type_6_axis_params, \
    validate_type_7_axis_params, validate_type_8_axis_params, validate_type_10_axis_params, \
    validate_type_10_w_axis_params


@pytest.fixture
def fixture():
    def error(errors, message):
        print(message)

    return error


######################################################################################
# Type 1
######################################################################################
def test_validate_type_1_axis_params_a(fixture):
    # not enough fields
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_1_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_1_axis_params_b(fixture):
    # needed minimum axis params
    params = {'function': lambda x: x,
              'u_min': 0,
              'u_max': 10}
    ok, errors = validate_type_1_axis_params('params', params, fixture)
    print(errors)
    assert ok is True


def test_validate_type_1_axis_params_c(fixture):
    # incorrect params
    params = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    ok, errors = validate_type_1_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_1_axis_params_d(fixture):
    # wrong types
    params = {'function': 1.0,
              'u_min': None,
              'u_max': 'ten'}
    ok, errors = validate_type_1_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_1_axis_params_e(fixture):
    # needed minimum axis params, with extra params
    params = {'function': lambda x: x,
              'u_min': 0,
              'u_max': 10,
              'extra_params': [
                  {'u_min': 0,
                   'u_max': 10, }
              ]}
    ok, errors = validate_type_1_axis_params('params', params, fixture)
    print(errors)
    assert ok is True

def test_validate_type_1_axis_params_f(fixture):
    # needed minimum axis params, with extra params, incorrect
    params = {'function': lambda x: x,
              'u_min': 0,
              'u_max': 10,
              'extra_params': [
                  {'u_minnnn': 0,
                   'u_maxxxx': 10, }
              ]}
    ok, errors = validate_type_1_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


######################################################################################
# Type 2
######################################################################################
def test_validate_type_2_axis_params_a(fixture):
    # not enough fields
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_2_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_2_axis_params_b(fixture):
    # needed minimum axis params
    params = {'function': lambda x: x,
              'u_min': 0,
              'u_max': 10}
    ok, errors = validate_type_2_axis_params('params', params, fixture)
    print(errors)
    assert ok is True


def test_validate_type_2_axis_params_c(fixture):
    # incorrect params
    params = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    ok, errors = validate_type_2_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_2_axis_params_d(fixture):
    # wrong types
    params = {'function': 1.0,
              'u_min': None,
              'u_max': 'ten'}
    ok, errors = validate_type_2_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


######################################################################################
# Type 3
######################################################################################
def test_validate_type_3_axis_params_a(fixture):
    # not enough fields
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_3_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_3_axis_params_b(fixture):
    # needed minimum axis params
    params = {'function': lambda x: x,
              'u_min': 0,
              'u_max': 10}
    ok, errors = validate_type_3_axis_params('params', params, fixture)
    print(errors)
    assert ok is True


def test_validate_type_3_axis_params_c(fixture):
    # incorrect params
    params = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    ok, errors = validate_type_3_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


######################################################################################
# Type 4
######################################################################################
def test_validate_type_4_axis_params_a(fixture):
    # not enough fields
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_4_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_4_axis_params_b(fixture):
    # needed minimum axis params
    params = {'function': lambda x: x,
              'u_min': 0,
              'u_max': 10}
    ok, errors = validate_type_4_axis_params('params', params, fixture)
    print(errors)
    assert ok is True


def test_validate_type_4_axis_params_c(fixture):
    # incorrect params
    params = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    ok, errors = validate_type_4_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_4_axis_params_d(fixture):
    # wrong types
    params = {'function': 1.0,
              'u_min': None,
              'u_max': 'ten'}
    ok, errors = validate_type_4_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


######################################################################################
# Type 6
######################################################################################
def test_validate_type_6_axis_params_a(fixture):
    # not enough fields
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_6_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_6_axis_params_b(fixture):
    # needed minimum axis params
    params = {'function': lambda x: x,
              'u_min': 0,
              'u_max': 10}
    ok, errors = validate_type_6_axis_params('params', params, fixture)
    print(errors)
    assert ok is True


def test_validate_type_6_axis_params_c(fixture):
    # incorrect params
    params = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    ok, errors = validate_type_6_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_6_axis_params_d(fixture):
    # wrong types
    params = {'function': 1.0,
              'u_min': None,
              'u_max': 'ten'}
    ok, errors = validate_type_6_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


######################################################################################
# Type 7
######################################################################################
def test_validate_type_7_axis_params_a(fixture):
    # not enough fields
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_7_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_7_axis_params_b(fixture):
    # needed minimum axis params
    params = {'function': lambda x: x,
              'u_min': 0,
              'u_max': 10}
    ok, errors = validate_type_7_axis_params('params', params, fixture)
    print(errors)
    assert ok is True


def test_validate_type_7_axis_params_c(fixture):
    # incorrect params
    params = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    ok, errors = validate_type_7_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_7_axis_params_d(fixture):
    # wrong types
    params = {'function': 1.0,
              'u_min': None,
              'u_max': 'ten'}
    ok, errors = validate_type_7_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


######################################################################################
# Type 8
######################################################################################
def test_validate_type_8_axis_params_a(fixture):
    # not enough fields
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_8_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_8_axis_params_b(fixture):
    # needed minimum axis params
    params = {'function': lambda x: x,
              'u_min': 0,
              'u_max': 10}
    ok, errors = validate_type_8_axis_params('params', params, fixture)
    print(errors)
    assert ok is True


def test_validate_type_8_axis_params_c(fixture):
    # incorrect params
    params = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    ok, errors = validate_type_8_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_8_axis_params_d(fixture):
    # wrong types
    params = {'function': 1.0,
              'u_min': None,
              'u_max': 'ten'}
    ok, errors = validate_type_8_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_8_axis_params_e(fixture):
    # too many definitions for function
    params = {'function': lambda x: x,
              'function_x': lambda x: x,
              'function_y': lambda x: x,
              'u_min': 0,
              'u_max': 10}
    ok, errors = validate_type_8_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_8_axis_params_f(fixture):
    # ok, defined via function_x and function_y
    params = {
        'function_x': lambda x: x,
        'function_y': lambda x: x,
        'u_min': 0,
        'u_max': 10}
    ok, errors = validate_type_8_axis_params('params', params, fixture)
    print(errors)
    assert ok is True


def test_validate_type_8_axis_params_g(fixture):
    # not ok, defined only via function_x
    params = {
        'function_y': lambda x: x,
        'u_min': 0,
        'u_max': 10}
    ok, errors = validate_type_8_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


######################################################################################
# type 9
######################################################################################
def test_validate_type_9_axis_params_a(fixture):
    # incorrect parameters
    error = fixture
    params = {'scale_type': 'linear',
              'tick_distance_smart': 30,
              'base_stop': None}
    ok, errors = validate_type_9_axis_grid_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_9_axis_params_b(fixture):
    # incorrect parameters
    error = fixture
    params = {'function': lambda x: x,
              'grid': True,
              'u_min': 0,
              'u_max': 10}
    ok, errors = validate_type_9_axis_grid_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_9_axis_params_c(fixture):
    # correct axis parameters
    error = fixture
    params = {
        **give_default_axis_values('type_9_axis'),
        **{'f': lambda x: x,
           'g': lambda x: x,
           'h': lambda x: x,
           'grid': False,
           'u_min': 0,
           'u_max': 10},
    }
    ok, errors = validate_type_9_axis_grid_params(True, params, error)
    print(errors)
    assert ok is True


def test_validate_type_9_axis_params_d(fixture):
    # correct grid parameters
    error = fixture
    params = {
        **give_default_axis_values('type_9_grid'),
        **{'f_grid': lambda x, y: x + y,
           'g_grid': lambda x, y: x + y,
           'h_grid': lambda x, y: x + y,
           'grid': True,
           'u_start': 0,
           'u_stop': 10,
           'v_start': 0,
           'v_stop': 10
           },
    }
    ok, errors = validate_type_9_axis_grid_params(True, params, error)
    print(errors)
    assert ok is True


def test_validate_type_9_axis_params_e(fixture):
    # correct grid minimum parameters
    error = fixture
    params = {
        **{'f_grid': lambda x, y: x + y,
           'g_grid': lambda x, y: x + y,
           'h_grid': lambda x, y: x + y,
           'grid': True,
           'u_start': 0,
           'u_stop': 10,
           'v_start': 0,
           'v_stop': 10
           },
    }
    ok, errors = validate_type_9_axis_grid_params(True, params, error)
    print(errors)
    assert ok is True


def test_validate_type_9_axis_params_f(fixture):
    # correct minimum axis parameters
    error = fixture
    params = {
        **{'f': lambda x: x,
           'g': lambda x: x,
           'h': lambda x: x,
           'grid': False,
           'u_min': 0,
           'u_max': 10},
    }
    ok, errors = validate_type_9_axis_grid_params(True, params, error)
    print(errors)
    assert ok is True


######################################################################################
# Type 10
######################################################################################
def test_validate_type_10_axis_params_a(fixture):
    # not enough fields
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_type_10_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_10_axis_params_b(fixture):
    # needed minimum axis params
    params = {'function': lambda x: x,
              'u_min': 0,
              'u_max': 10}
    ok, errors = validate_type_10_axis_params('params', params, fixture)
    print(errors)
    assert ok is True


def test_validate_type_10_axis_params_c(fixture):
    # incorrect params
    params = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    ok, errors = validate_type_10_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_10_axis_params_d(fixture):
    # wrong types
    params = {'function': 1.0,
              'u_min': None,
              'u_max': 'ten'}
    ok, errors = validate_type_10_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_10_axis_params_e(fixture):
    # incorrect for w
    params = {'function': lambda x: x,
              'u_min': 0,
              'u_max': 10}
    ok, errors = validate_type_10_w_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_10_axis_params_f(fixture):
    # ok for w
    params = {'function_3': lambda x: x,
              'function_4': lambda x: x,
              'u_min': 0,
              'u_max': 10}
    ok, errors = validate_type_10_w_axis_params('params', params, fixture)
    print(errors)
    assert ok is True
