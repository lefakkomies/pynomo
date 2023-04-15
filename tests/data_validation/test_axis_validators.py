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

from pynomo.data_validation.axis_validators import validate_type_1_axis_params, validate_type_9_axis_grid_params


@pytest.fixture
def fixture():
    def error(errors, message):
        print(message)

    return error


def test_validate_type_1_axis_params_a(fixture):
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_1_axis_params('params', params, fixture)
    print(errors)
    assert ok is False


def test_validate_type_1_axis_params_b(fixture):
    params = {'function': lambda x: x,
              'u_min': 0,
              'u_max': 10}
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_1_axis_params('params', params, fixture)
    print(errors)
    assert ok is True


def test_validate_type_9_axis_params_a(fixture):
    error = fixture
    params = {'scale_type': 'linear',
              'tick_distance_smart': 30,
              'base_stop': None}
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_9_axis_grid_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_9_axis_params_b(fixture):
    error = fixture
    params = {'function': lambda x: x,
              'grid': True,
              'u_min': 0,
              'u_max': 10}
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_9_axis_grid_params(True, params, error)
    print(errors)
    assert ok is False
