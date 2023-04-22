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

""" Axis validators

    Axis validators validate that dictionaries defining axes or grids have required keys and no unknown keys or
    wrong data-types

    Example:
        # Validates dictionary defining axis type 1 params

        # define error function that is required
        def error(errors, message):
            print(message)

        # ok:       True if validation ok
        # errors:   dictionary of keys and error messages related to that key
        ok, errors = validate_type_1_axis_params("axis 1", params, error)


    Note:

        actual validators are testable because they can return error bit and errors like in

        validate_type_1_axis_params()

        However, these can not be used inside nested schemas because returned value mixes the
        logic and error should be communicated via error() function. Thus, functions like

        _validate_type_1_axis_params()

        are used instead that return nothing

"""

from typing import Dict, Union, List, Any, Callable

from pynomo.data_validation.axis_schemas import axis_schema_type_9_axis, axis_schema_type_9_grid, axis_schema_type_1, \
    axis_schema_type_2, axis_schema_type_3, axis_schema_type_4, axis_schema_type_6, \
    axis_schema_type_7, axis_schema_type_10, axis_schema_type_10_w, axis_schema_type_8_function, \
    axis_schema_type_8_function_xy, axis_schema_type_1_extra_params, axis_schema_type_2_extra_params, \
    axis_schema_type_3_extra_params, axis_schema_type_4_extra_params, axis_schema_type_7_extra_params, \
    axis_schema_type_6_extra_params, axis_schema_type_8_function_extra_params, \
    axis_schema_type_8_function_xy_extra_params, axis_schema_type_9_axis_extra_params, \
    axis_schema_type_9_grid_extra_params, axis_schema_type_10_extra_params, axis_schema_type_10_w_extra_params
from pynomo.data_validation.dictionary_validation_functions import validate_params_


def validate_axis_params(axis_type: str, params: Dict[str, dict]) -> (bool, Dict[str, Union[str, List[str]]]):
    switcher = {
        'type_1': lambda: validate_params_(axis_schema_type_1, params),
        'type_1_extra_params': lambda: validate_params_(axis_schema_type_1_extra_params, params),
        'type_2': lambda: validate_params_(axis_schema_type_2, params),
        'type_2_extra_params': lambda: validate_params_(axis_schema_type_2_extra_params, params),
        'type_3': lambda: validate_params_(axis_schema_type_3, params),
        'type_3_extra_params': lambda: validate_params_(axis_schema_type_3_extra_params, params),
        'type_4': lambda: validate_params_(axis_schema_type_4, params),
        'type_4_extra_params': lambda: validate_params_(axis_schema_type_4_extra_params, params),
        # no type 5 axis params
        'type_6': lambda: validate_params_(axis_schema_type_6, params),
        'type_6_extra_params': lambda: validate_params_(axis_schema_type_6_extra_params, params),
        'type_7': lambda: validate_params_(axis_schema_type_7, params),
        'type_7_extra_params': lambda: validate_params_(axis_schema_type_7_extra_params, params),
        'type_8_function': lambda: validate_params_(axis_schema_type_8_function, params),
        'type_8_function_extra_params': lambda: validate_params_(axis_schema_type_8_function_extra_params, params),
        'type_8_function_xy': lambda: validate_params_(axis_schema_type_8_function_xy, params),
        'type_8_function_xy_extra_params': lambda: validate_params_(axis_schema_type_8_function_xy_extra_params, params),
        'type_9_axis': lambda: validate_params_(axis_schema_type_9_axis, params),
        'type_9_axis_extra_params': lambda: validate_params_(axis_schema_type_9_axis_extra_params, params),
        'type_9_grid': lambda: validate_params_(axis_schema_type_9_grid, params),
        'type_9_grid_extra_params': lambda: validate_params_(axis_schema_type_9_grid_extra_params, params),
        'type_10': lambda: validate_params_(axis_schema_type_10, params),
        'type_10_extra_params': lambda: validate_params_(axis_schema_type_10_extra_params, params),
        'type_10_w': lambda: validate_params_(axis_schema_type_10_w, params),
        'type_10_w_extra_params': lambda: validate_params_(axis_schema_type_10_w_extra_params, params),
    }
    result, errors = switcher.get(axis_type, "Incorrect key")()
    if result == "Incorrect key":
        print(f"Internal error: incorrect axis_type '{axis_type}' when getting default values")
        return False, {'error': f'Internal error checking "{axis_type}"'}
    return result, errors


# schema_string: string defining schema to be used
def _validate_axis_extra_params(field: Any, value: Any, error: Callable, schema_string: str) -> (bool, dict):
    ok: bool = True
    errors: Dict[str, Union[str, List[str]]] = {}
    if isinstance(value, dict):
        # validate extra params
        if 'extra_params' in value:
            extra_params_list = value['extra_params']
            if not isinstance(extra_params_list, list):
                error_str = f"Extra params should be list"
                error(field, error_str)
                return False, {value: error_str}
            for extra_params in extra_params_list:
                if not isinstance(extra_params, dict):
                    error_str = f"Extra params items should be dictionaries"
                    error(field, error_str)
                    return False, {value: error_str}
                ok, errors = validate_axis_params(schema_string, extra_params)
                return ok, errors
    return ok, errors


######################################################################################
# Type 1
######################################################################################
def validate_type_1_axis_params(field: Any, value: Any, error: Callable) -> (bool, dict):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_axis_params('type_1', value)
    if not ok:
        error(field, str(errors))
        return ok, errors
    # extra_params handling
    """
    if isinstance(value, dict):
        # validate extra params
        if 'extra_params' in value:
            extra_params_list = value['extra_params']
            if not isinstance(extra_params_list, list):
                error_str = f"Extra params should be list"
                error(field, error_str)
                return False, {value: error_str}
            for extra_params in extra_params_list:
                if not isinstance(extra_params, dict):
                    error_str = f"Extra params items should be dictionaries"
                    error(field, error_str)
                    return False, {value: error_str}
                ok, errors = validate_axis_params('type_1_extra_params', extra_params)
                return ok, errors
    """
    ok, errors = _validate_axis_extra_params(field, value, error, 'type_1_extra_params')
    return ok, errors


def validate_type_1_axis_params_(field: Any, value: Any, error: Callable):
    validate_type_1_axis_params(field, value, error)


######################################################################################
# Type 2
######################################################################################
def validate_type_2_axis_params(field: Any, value: Any, error: Callable):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_axis_params('type_2', value)
    if not ok:
        error(field, str(errors))
        return ok, errors
    ok, errors = _validate_axis_extra_params(field, value, error, 'type_2_extra_params')
    return ok, errors


def validate_type_2_axis_params_(field: Any, value: Any, error: Callable):
    validate_type_2_axis_params(field, value, error)


######################################################################################
# Type 3
######################################################################################
def validate_type_3_axis_params(field: Any, value: Any, error: Callable):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_axis_params('type_3', value)
    if not ok:
        error(field, str(errors))
        return ok, errors
    ok, errors = _validate_axis_extra_params(field, value, error, 'type_3_extra_params')
    return ok, errors


def validate_type_3_axis_params_(field: Any, value: Any, error: Callable):
    validate_type_3_axis_params(field, value, error)


######################################################################################
# Type 4
######################################################################################
def validate_type_4_axis_params(field: Any, value: Any, error: Callable):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_axis_params('type_4', value)
    if not ok:
        error(field, str(errors))
        return ok, errors
    ok, errors = _validate_axis_extra_params(field, value, error, 'type_4_extra_params')
    return ok, errors


def validate_type_4_axis_params_(field: Any, value: Any, error: Callable):
    validate_type_4_axis_params(field, value, error)


"""
# type 5
def validate_type_5_axis_params(field: Any, value: Any, error: Callable):
    # TODO run checker for type 5 axis params
    pass


def validate_type_5_axis_params_(field: Any, value: Any, error: Callable):
    validate_type_5_axis_params(field, value, error)
"""


######################################################################################
# Type 6
######################################################################################
def validate_type_6_axis_params(field: Any, value: Any, error: Callable):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_axis_params('type_6', value)
    if not ok:
        error(field, str(errors))
        return ok, errors
    ok, errors = _validate_axis_extra_params(field, value, error, 'type_6_extra_params')
    return ok, errors


def validate_type_6_axis_params_(field: Any, value: Any, error: Callable):
    validate_type_6_axis_params(field, value, error)


######################################################################################
# Type 7
######################################################################################
def validate_type_7_axis_params(field: Any, value: Any, error: Callable):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_axis_params('type_7', value)
    if not ok:
        error(field, str(errors))
        return ok, errors
    ok, errors = _validate_axis_extra_params(field, value, error, 'type_7_extra_params')
    return ok, errors


def validate_type_7_axis_params_(field: Any, value: Any, error: Callable):
    validate_type_7_axis_params(field, value, error)


######################################################################################
# Type 8
######################################################################################
def validate_type_8_axis_params(field: Any, value: Any, error: Callable):
    if not isinstance(value, dict):
        error_str = f"Axis definitions should be a dictionary in {field}"
        error(field, error_str)
        return False, error_str
    if all(key in value for key in ['function', 'function_x', 'function_y']):
        error_str = "Function can not be defined with both 'function' and " \
                    "function_x','function_y' keys in block type 8 axis parameters."
        error(field, error_str)
        return False, error_str
    if 'function' in value:
        ok: bool
        errors: Dict[str, Union[str, List[str]]]
        ok, errors = validate_axis_params('type_8_function', value)
        if not ok:
            error(field, str(errors))
            return ok, errors
        ok, errors = _validate_axis_extra_params(field, value, error, 'type_8_function_extra_params')
        return ok, errors
    if any(key in value for key in ['function_x', 'function_y']):
        ok: bool
        errors: Dict[str, Union[str, List[str]]]
        ok, errors = validate_axis_params('type_8_function_xy', value)
        if not ok:
            error(field, str(errors))
            return ok, errors
        ok, errors = _validate_axis_extra_params(field, value, error, 'type_8_function_xy_extra_params')
        return ok, errors
    return False, "Missing either key 'function' or keys 'function_x','function_y' in block type 8 axis parameters."


def validate_type_8_axis_params_(field: Any, value: Any, error: Callable):
    validate_type_8_axis_params(field, value, error)


######################################################################################
# Type 9
######################################################################################
def validate_type_9_axis_grid_params(field: Any, value: Any, error: Callable) -> (
        bool, Dict[str, Union[str, List[str]]]):
    if not isinstance(value, dict):
        error_str = f"Axis definitions should be a dictionary in {field}"
        error(field, error_str)
        return False, error_str
    if 'grid' in value.keys():
        if value['grid'] is False:
            ok, errors = validate_axis_params('type_9_axis', value)
            if not ok:
                error(field, str(errors))
                return ok, errors
            ok, errors = _validate_axis_extra_params(field, value, error, 'type_9_axis_extra_params')
            return ok, errors
        if value['grid'] is True:
            ok, errors = validate_axis_params('type_9_grid', value)
            if not ok:
                error(field, str(errors))
                return ok, errors
            ok, errors = _validate_axis_extra_params(field, value, error, 'type_9_grid_extra_params')
            return ok, errors
    else:  # grid not defined assume 'grid' = False
        ok, errors = validate_axis_params('type_9_axis', value)
        if not ok:
            error(field, str(errors))
            return ok, errors
        ok, errors = _validate_axis_extra_params(field, value, error, 'type_9_axis_extra_params')
        return ok, errors


def validate_type_9_axis_grid_params_(field: Any, value: Any, error: Callable):
    validate_type_9_axis_grid_params(field, value, error)


######################################################################################
# Type 10
######################################################################################
def validate_type_10_axis_params(field: Any, value: Any, error: Callable):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_axis_params('type_10', value)
    if not ok:
        error(field, str(errors))
        return ok, errors
    ok, errors = _validate_axis_extra_params(field, value, error, 'type_10_extra_params')
    return ok, errors


def validate_type_10_axis_params_(field: Any, value: Any, error: Callable):
    validate_type_10_axis_params(field, value, error)


######################################################################################
# Type 10 w axis
######################################################################################
def validate_type_10_w_axis_params(field: Any, value: Any, error: Callable):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_axis_params('type_10_w', value)
    if not ok:
        error(field, str(errors))
        return ok, errors
    ok, errors = _validate_axis_extra_params(field, value, error, 'type_10_w_extra_params')
    return ok, errors


def validate_type_10_w_axis_params_(field: Any, value: Any, error: Callable):
    validate_type_10_w_axis_params(field, value, error)


if __name__ == '__main__':
    from pprint import pprint
    from pynomo.data_validation.axis_schemas import give_default_axis_values

    pprint(give_default_axis_values('type_9_axis'))
