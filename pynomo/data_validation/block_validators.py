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

""" Block validators

    Block validators validate that dictionaries defining blocks have required keys and no unknown keys or
    wrong data-types

    Example:
        # Validates dictionary defining block type 1

        # define error function that is required
        def error(errors, message):
            print(message)

        # ok:       True if validation ok
        # errors:   dictionary of keys and error messages related to that key
        ok, errors = validate_type_1_block_params("block 1", params, error)


"""

from pprint import pprint
from typing import Dict, Union, List, Any, Callable

from pynomo.data_validation.axis_schemas import give_default_axis_values
from pynomo.data_validation.block_schemas import block_schema_type_1, block_schema_type_2, block_schema_type_3, \
    block_schema_type_4, block_schema_type_5, block_schema_type_6, block_schema_type_7, block_schema_type_8, \
    block_schema_type_9, block_schema_type_10
from pynomo.data_validation.dictionary_validation_functions import validate_params_


######################################################################################
# Top level validator for block params
######################################################################################
def validate_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok: bool = True
    errors: Dict[str, Union[str, List[str]]] = {}
    if not isinstance(value, dict):
        error_str = f"Block params should be dict"
        error(field, error_str)
        return False, {field: error_str}
    if 'block_type' not in value:
        error_str = f"Block should have type defined with key 'block_type'"
        error(field, error_str)
        return False, {field: error_str}
    if not isinstance(value['block_type'], str):
        error_str = f"'block_type' should be string"
        error(field, error_str)
        return False, {field: error_str}
    result, errors = validate_block_params_with_type(value['block_type'], value)
    if not result:
        error(field, str(errors))
        return False, {field: str(errors)}
    return result, errors


def validate_block_params_with_type(block_type: str, params: Dict[str, dict]) -> (
        bool, Dict[str, Union[str, List[str]]]):
    switcher = {
        'type_1': lambda: validate_params_(block_schema_type_1, params),
        'type_2': lambda: validate_params_(block_schema_type_2, params),
        'type_3': lambda: validate_params_(block_schema_type_3, params),
        'type_4': lambda: validate_params_(block_schema_type_4, params),
        'type_5': lambda: validate_params_(block_schema_type_5, params),
        'type_6': lambda: validate_params_(block_schema_type_6, params),
        'type_7': lambda: validate_params_(block_schema_type_7, params),
        'type_8': lambda: validate_params_(block_schema_type_8, params),
        'type_9': lambda: validate_params_(block_schema_type_9, params),
        'type_10': lambda: validate_params_(block_schema_type_10, params)
    }
    result, errors = switcher.get(block_type, lambda: (False, "Incorrect key"))()
    if not result:
        if isinstance(errors, str):
            if errors == "Incorrect key":
                print(f"Internal error: incorrect block_type '{block_type}' when validating values")
                return False, {'block_type': f'Incorrect type "{block_type}"'}
    return result, errors


def validate_type_1_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok_: bool
    errors_: Dict[str, Union[str, List[str]]]
    ok_, errors_ = validate_block_params_with_type('type_1', value)
    if not ok_:
        error(errors_, str(errors_))
    return ok_, errors_


def validate_type_2_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok_: bool
    errors_: Dict[str, Union[str, List[str]]]
    ok_, errors_ = validate_block_params_with_type('type_2', value)
    if not ok_:
        error(errors_, errors_)
    return ok_, errors_


def validate_type_3_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok_: bool
    errors_: Dict[str, Union[str, List[str]]]
    ok_, errors_ = validate_block_params_with_type('type_3', value)
    if not ok_:
        error(errors_, errors_)
    return ok_, errors_


def validate_type_4_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok_: bool
    errors_: Dict[str, Union[str, List[str]]]
    ok_, errors_ = validate_block_params_with_type('type_4', value)
    if not ok_:
        error(errors_, errors_)
    return ok_, errors_


def validate_type_5_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok_: bool
    errors_: Dict[str, Union[str, List[str]]]
    ok_, errors_ = validate_block_params_with_type('type_5', value)
    if not ok_:
        error(errors_, errors_)
    return ok_, errors_


def validate_type_6_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok_: bool
    errors_: Dict[str, Union[str, List[str]]]
    ok_, errors_ = validate_block_params_with_type('type_6', value)
    if not ok_:
        error(errors_, errors_)
    return ok_, errors_


def validate_type_7_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok_: bool
    errors_: Dict[str, Union[str, List[str]]]
    ok_, errors_ = validate_block_params_with_type('type_7', value)
    if not ok_:
        error(errors_, errors_)
    return ok_, errors_


def validate_type_8_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok_: bool
    errors_: Dict[str, Union[str, List[str]]]
    ok_, errors_ = validate_block_params_with_type('type_8', value)
    if not ok_:
        error(errors_, str(errors_))
    return ok_, errors_


def validate_type_9_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok_: bool
    errors_: Dict[str, Union[str, List[str]]]
    ok_, errors_ = validate_block_params_with_type('type_9', value)
    if not ok_:
        error(errors_, errors_)
    return ok_, errors_


def validate_type_10_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok_: bool
    errors_: Dict[str, Union[str, List[str]]]
    ok_, errors_ = validate_block_params_with_type('type_10', value)
    if not ok_:
        error(errors_, errors_)
    return ok_, errors_


if __name__ == "__main__":
    default_values = give_default_axis_values('type_1')
    required_values = {'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}
    params = {'f1_params': {**default_values, **required_values},
              'f2_params': {**default_values, **required_values},
              'f3_params': {**default_values, **required_values}
              }
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_1_block_params('para', params, lambda a, b: print(a, b))
    print(errors)
    # pprint(give_default_axis_values('type_1'))
