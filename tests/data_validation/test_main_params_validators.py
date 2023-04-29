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

from pynomo.data_validation.main_params_validators import validate_main_params


@pytest.fixture
def fixture():
    def error(errors, message):
        print(message)

    return error

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

def test_validate_main_params_b(fixture):
    # incorrect input
    error = fixture
    params = {'filename': 'filename'}
    ok, errors = validate_main_params(params)
    logging.info(errors)
    assert ok is True