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

""" Testing of main params validators

    Testing of main params defined in main_param_validators.py

"""
import sys
from pprint import pprint

import pytest
import logging

from pyx import text, path
from numpy import pi
from pyx import color
import os

from pynomo.data_validation.axis_schemas import give_default_axis_values
from pynomo.data_validation.main_params_validators import validate_main_params

# add logging to console
logging.basicConfig(level=logging.INFO)


# This is used to run example codes as tests
def _run_external_file(filename):
    module_dir = os.path.dirname(__file__)
    filename_full_path = module_dir + "/../../examples/" + filename

    lines = ""
    with open(filename_full_path, "r") as file:
        for line in file:
            if "Nomographer" not in line:
                lines += line
    exec(lines, globals())  # globals() to have same context and allow imports

    # main_params defined (and assumed to be defined) in executed source
    ok, errors = validate_main_params(main_params)
    print(f"Testing: {filename}")
    pprint(errors)
    assert ok is True


@pytest.fixture
def fixture():
    def error(errors, message):
        print(message)

    return error


@pytest.fixture
def working_block_dict():
    f_params = {**give_default_axis_values('type_1'),
                **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    working_block = {'f1_params': f_params,
                     'f2_params': f_params,
                     'f3_params': f_params,
                     'block_type': 'type_1'
                     }
    return working_block


@pytest.fixture
def non_working_block_dict():
    f_params = {**give_default_axis_values('type_1'),
                **{'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}}
    non_working_block = {'f1_paramsi': f_params,
                         'f2_paramsi': f_params,
                         'f3_params': f_params,
                         'block_type': 'type_AA'
                         }
    return non_working_block


######################################################################################
# Top level main param validation
######################################################################################
def test_validate_main_params_a(fixture):
    # incorrect input
    error = fixture
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is False


def test_validate_main_params_b(fixture, working_block_dict):
    # correct input
    error = fixture
    params = {'filename': 'filename',
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is True


def test_validate_main_params_c(fixture, non_working_block_dict):
    # incorrect input
    error = fixture
    params = {'filename': 'filename',
              'block_params': [non_working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is False


def test_validate_main_params_d(fixture, working_block_dict):
    # correct input
    error = fixture
    params = {'filename': 'filename',
              'title_color': color.rgb.black,
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is True


def test_validate_main_params_e(fixture, working_block_dict):
    # incorrect input
    error = fixture
    params = {'filename': 'filename',
              'title_color': 'Redd',
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is False


######################################################################################
# Transformations
######################################################################################
def test_validate_main_params_f(fixture, working_block_dict):
    # correct input transformation
    error = fixture
    params = {'filename': 'filename',
              'title_color': color.rgb.black,
              'transformations': [('scale paper',)],
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is True


def test_validate_main_params_g(fixture, working_block_dict):
    # correct input transformation
    error = fixture
    params = {'filename': 'filename',
              'transformations': [('scale paper',), ('rotate', pi / 2)],
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is True


def test_validate_main_params_g(fixture, working_block_dict):
    # correct input transformation
    error = fixture
    params = {'filename': 'filename',
              'transformations': [('matrix', [[1, 2, 3], [4, 5, 6], [7, 8, 9]]), ('rotate', pi / 2)],
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is True


def test_validate_main_params_g(fixture, working_block_dict):
    # incorrect input transformation
    error = fixture
    params = {'filename': 'filename',
              'transformations': [('matrix', [[1, 2, 3], [4, 5, 6]])],
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is False


######################################################################################
# Extra texts
######################################################################################
def test_validate_main_params_h(fixture, working_block_dict):
    # correct extra texts
    error = fixture
    working_extra_texts = [{
        'x': 1,
        'y': 2,
        'text': 'testing',
        'width': 5,
        'pyx_extra_defs': [color.rgb.red, text.size.Huge]
    }]
    params = {'filename': 'filename',
              'extra_texts': working_extra_texts,
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is True


def test_validate_main_params_i(fixture, working_block_dict):
    # incorrect extra texts
    error = fixture
    non_working_extra_texts = [{
        'a': 'a',
        'x': 1,
        'y': 2,
        'text': 'testing',
        'width': 5,
    }]
    params = {'filename': 'filename',
              'extra_texts': non_working_extra_texts,
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is False


def test_validate_main_params_j(fixture, working_block_dict):
    # incorrect extra texts
    error = fixture
    non_working_extra_texts = [{
        'x': 'x',
        'y': 2,
        'text': 'testing',
        'width': 5,
    }]
    params = {'filename': 'filename',
              'extra_texts': non_working_extra_texts,
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is False


######################################################################################
# Isopleth params
######################################################################################
def test_validate_main_params_k(fixture, working_block_dict):
    # correct isopleth params
    error = fixture
    isopleth_params = [{'color': 'MidnightBlue',
                        'linewidth': 'THICK',
                        'linestyle': 'dashdotted',
                        'transparency': 0.2},
                       {'color': 'Orange',
                        'linewidth': 'THIN',
                        'linestyle': 'dashdotted',
                        'transparency': 0.9}]
    params = {'filename': 'filename',
              'isopleth_params': isopleth_params,
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is True


def test_validate_main_params_k(fixture, working_block_dict):
    # incorrect isopleth params
    error = fixture
    isopleth_params = [{'color': 'MidnightBlue',
                        'linewidth': 'THICKKKK',
                        'linestyle': 'dashdotted',
                        'transparency': 0.2},
                       {'color': 'Orange',
                        'linewidth': 'THIN',
                        'linestyle': 'dashdotted',
                        'transparency': 0.9}]
    params = {'filename': 'filename',
              'isopleth_params': isopleth_params,
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is False


def test_validate_main_params_l(fixture, working_block_dict):
    # incorrect isopleth params
    error = fixture
    isopleth_params = [{'color': 'MidnightBluesssss',
                        'linewidth': 'THICK',
                        'linestyle': 'dashdotted',
                        'transparency': 0.2},
                       {'color': 'Orange',
                        'linewidth': 'THIN',
                        'linestyle': 'dashdotted',
                        'transparency': 0.9}]
    params = {'filename': 'filename',
              'isopleth_params': isopleth_params,
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is False


def test_validate_main_params_l(fixture, working_block_dict):
    # incorrect isopleth params
    error = fixture
    isopleth_params = [{'color': 'MidnightBlue',
                        'linewidth': 'THICK',
                        'linestyle': 'dashdotted',
                        'transparency': 0.2},
                       {'color': 'Orange',
                        'linewidth': 'THIN',
                        'linestyle': 'dashdotted',
                        'transparency': 'x'}]
    params = {'filename': 'filename',
              'isopleth_params': isopleth_params,
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is False


######################################################################################
# pre_func, post_func
######################################################################################

def test_validate_main_params_m(fixture, working_block_dict):
    # correct isopleth params
    error = fixture

    def post(c):
        c.stroke(path.line(2, 2, 15, 2) +
                 path.line(15, 2, 10, 15) +
                 path.line(15, 15, 2, 15) +
                 path.line(2, 15, 2, 2))

    params = {'filename': 'filename',
              'pre_func': post,
              'post_func': post,
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is True


def test_validate_main_params_n(fixture, working_block_dict):
    # incorrect isopleth params
    error = fixture

    def post(c):
        c.add(2)

    params = {'filename': 'filename',
              'pre_func': post,
              'post_func': post,
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    print(errors)
    assert ok is False


######################################################################################
# Tests based on example-files
# (assuming file will generate dict with name 'main_params' that is checked)
######################################################################################


def test_validate_LC_filter():
    _run_external_file("LC_filter.py")


def test_validate_ex_star_navi():
    _run_external_file("ex_star_navi.py")


def test_validate_ex_dubois():
    _run_external_file("ex_dubois.py")


def test_validate_ex_amortized_loan():
    _run_external_file("ex_amortized_loan.py")


def test_validate_ex_BMI():
    _run_external_file("ex_BMI.py")


def test_validate_ex_rfset():
    _run_external_file("ex_rfset.py")


def test_ex_second_order_eq():
    _run_external_file("ex_second_order_eq.py")


def test_genus1():
    _run_external_file("genus1.py")


# Axes
def test_validate_ex_axes_1():
    _run_external_file("ex_axes_1.py")


def test_validate_ex_axes_2():
    _run_external_file("ex_axes_2.py")


def test_validate_ex_axes_3():
    _run_external_file("ex_axes_3.py")


def test_validate_ex_axes_4():
    _run_external_file("ex_axes_4.py")


def test_validate_ex_axes_5():
    _run_external_file("ex_axes_5.py")


def test_validate_ex_axes_6():
    _run_external_file("ex_axes_6.py")


def test_validate_ex_axes_7():
    _run_external_file("ex_axes_7.py")


def test_validate_ex_axes_7_1():
    _run_external_file("ex_axes_7_1.py")


def test_validate_ex_axes_8():
    _run_external_file("ex_axes_8.py")


def test_validate_ex_axes_9():
    _run_external_file("ex_axes_9.py")


# nomo types
def test_validate_ex_type1_nomo_1():
    _run_external_file("ex_type1_nomo_1.py")


def test_validate_ex_type2_nomo_1():
    _run_external_file("ex_type2_nomo_1.py")


def test_validate_ex_type3_nomo_1():
    _run_external_file("ex_type3_nomo_1.py")


def test_validate_ex_type4_nomo_1():
    _run_external_file("ex_type4_nomo_1.py")


def test_validate_ex_type5_nomo_1():
    _run_external_file("ex_type5_nomo_1.py")


def test_validate_ex_type6_nomo_1():
    _run_external_file("ex_type6_nomo_1.py")


def test_validate_ex_type7_nomo_1():
    _run_external_file("ex_type7_nomo_1.py")


def test_validate_ex_type8_nomo_1():
    _run_external_file("ex_type8_nomo_1.py")


def test_validate_ex_type9_nomo_1():
    _run_external_file("ex_type9_nomo_1.py")


def test_validate_ex_type10_nomo_1():
    _run_external_file("ex_type10_nomo_1.py")
