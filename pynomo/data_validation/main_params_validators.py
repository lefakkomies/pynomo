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

""" Validator for main params, the top level dictionary defining the nomograph

"""
import numbers
import numpy as np
from typing import Any, Callable, Dict, Union, List

from pynomo.data_validation.dictionary_validation_functions import validate_params_
from pynomo.data_validation.main_schemas import main_params_schema


######################################################################################
# Main param top level validator
######################################################################################
def validate_main_params(params: Dict[str, dict | list]) -> (bool, Dict[str, Union[str, List[str]]]):
    ok, errors = validate_params_(main_params_schema, params)
    return ok, errors


if __name__ == '__main__':
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    ok, errors = validate_main_params(params)
    print(ok, errors)
