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

import pytest
import logging

from pyx import text

logging.basicConfig(level=logging.INFO)

from numpy import pi
from pyx import color

from pynomo.data_validation.axis_schemas import give_default_axis_values
from pynomo.data_validation.main_params_validators import validate_main_params


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
    logging.info(errors)
    assert ok is False


def test_validate_main_params_b(fixture, working_block_dict):
    # correct input
    error = fixture
    params = {'filename': 'filename',
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    logging.info(errors)
    assert ok is True


def test_validate_main_params_c(fixture, non_working_block_dict):
    # incorrect input
    error = fixture
    params = {'filename': 'filename',
              'block_params': [non_working_block_dict]}
    ok, errors = validate_main_params(params)
    logging.info(errors)
    assert ok is False


def test_validate_main_params_d(fixture, working_block_dict):
    # correct input
    error = fixture
    params = {'filename': 'filename',
              'title_color': color.rgb.black,
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    logging.info(errors)
    assert ok is True


def test_validate_main_params_e(fixture, working_block_dict):
    # incorrect input
    error = fixture
    params = {'filename': 'filename',
              'title_color': 'Redd',
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    logging.info(errors)
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
    logging.info(errors)
    assert ok is True


def test_validate_main_params_g(fixture, working_block_dict):
    # correct input transformation
    error = fixture
    params = {'filename': 'filename',
              'transformations': [('scale paper',), ('rotate', pi / 2)],
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    logging.info(errors)
    assert ok is True


def test_validate_main_params_g(fixture, working_block_dict):
    # correct input transformation
    error = fixture
    params = {'filename': 'filename',
              'transformations': [('matrix', [[1, 2, 3], [4, 5, 6], [7, 8, 9]]), ('rotate', pi / 2)],
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    logging.info(errors)
    assert ok is True


def test_validate_main_params_g(fixture, working_block_dict):
    # incorrect input transformation
    error = fixture
    params = {'filename': 'filename',
              'transformations': [('matrix', [[1, 2, 3], [4, 5, 6]])],
              'block_params': [working_block_dict]}
    ok, errors = validate_main_params(params)
    logging.info(errors)
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
    logging.info(errors)
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
    logging.info(errors)
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
    logging.info(errors)
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
    logging.info(errors)
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
    logging.info(errors)
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
    logging.info(errors)
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
    logging.info(errors)
    assert ok is False


