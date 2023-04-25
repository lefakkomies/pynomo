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

""" Validators to be used in main params schema

"""
import numbers
import numpy as np
from typing import Any, Callable, Dict, Union, List

from pynomo.data_validation.dictionary_validation_functions import is_3x3_list_of_numbers_, is_number, validate_params_

######################################################################################
# Transformation validation
######################################################################################
allowed_transformation_strings_ = ['scale paper', 'optimize', 'rotate', 'matrix']


def validate_transformations(field: Any, value: Any, error: Callable):
    ok: bool = True
    errors: Dict[str, Union[str, List[str]]] = {}
    if not isinstance(value, list):
        error_str = f"Transformations should be list"
        error(field, error_str)
        return False, {value: error_str}
    for item in value:
        if not isinstance(item, tuple):
            error_str = f"Transformations should be list of tuples, {item}"
            error(field, error_str)
            return False, {value: error_str}
        if len(item) == 0:
            error_str = f"Transformation should not be empty"
            error(field, error_str)
            return False, {value: error_str}
        if not item[0] in allowed_transformation_strings_:
            error_str = f"Unknown transformation {item[0]}"
            error(field, error_str)
            return False, {value: error_str}
        if item[0] == 'scale paper':
            if len(item) != 1:
                error_str = f"Transformation scale paper with unknown parameter: {item}"
                error(field, error_str)
                return False, {value: error_str}
        if item[0] == 'optimize':
            if len(item) != 1:
                error_str = f"Transformation optimize with unknown parameter: {item}"
                error(field, error_str)
                return False, {value: error_str}
        if item[0] == 'polygon':
            if len(item) != 1:
                error_str = f"Transformation polygon with unknown parameter: {item}"
                error(field, error_str)
                return False, {value: error_str}
        if item[0] == 'rotate':
            if len(item) != 2:
                error_str = f"Transformation rotate with unknown number of parameters: {item}"
                error(field, error_str)
                return False, {value: error_str}
            if not isinstance(item[1], (int, float, complex, np.generic, numbers.Number)):
                error_str = f"Transformation rotate with non-number parameter: {item}"
                error(field, error_str)
                return False, {value: error_str}
        if item[0] == 'matrix':
            if len(item) != 2:
                error_str = f"Transformation matrix with unknown number of parameters: {item}"
                error(field, error_str)
                return False, {value: error_str}
            if not is_3x3_list_of_numbers_(item[1]):
                error_str = f"Transformation matrix without 3x3 matrix as parameter: {item}"
                error(field, error_str)
                return False, {value: error_str}
    return ok, errors


def validate_transformations_(field: Any, value: Any, error: Callable):
    validate_transformations(field, value, error)


######################################################################################
# Extra texts
######################################################################################

extra_text_item_schema = {
    'x': {
        'required': True,
        'check_with': is_number
    },
    'y': {
        'required': True,
        'check_with': is_number
    },
    'text': {
        'required': True,
        'type': 'string'
    },
    'width': {
        'required': True,
        'check_with': is_number
    },
    'pyx_extra_defs': {
        'required': False,
        'type': 'list'
    }
}


def validate_main_extra_texts(field: Any, value: Any, error: Callable):
    ok: bool = True
    errors: Dict[str, Union[str, List[str]]] = {}
    ok, errors = validate_params_(extra_text_item_schema, value)
    return ok, errors


def validate_main_extra_texts_(field: Any, value: Any, error: Callable):
    validate_main_extra_texts(field, value, error)


######################################################################################
# Isopleth params
######################################################################################


isopleth_param_schema = {
    'color': {
        'required': False,
        'type': 'string'
    },
    'linewidth': {
        'required': True,
        'type': 'string'
    },
    'linestyle': {
        'required': True,
        'type': 'string'
    },
    'transparency': {
        'required': True,
        'check_with': is_number
    }
}

allowed_linewidth_strings_ = ['THIN', 'THIn', 'THin', 'Thin', 'thin',
                              'thick', 'Thick', 'THick', 'THIck', 'THICk', 'THICK',
                              'normal', 'NORMAL']
allowed_linestyle_strings_ = ['solid', 'dashed', 'dotted', 'dashdotted']
allowed_color_strings_ = ['GreenYellow',
                          'Yellow',
                          'Goldenrod',
                          'Dandelion',
                          'Apricot',
                          'Peach',
                          'Melon',
                          'YellowOrange',
                          'Orange',
                          'BurnOrange',
                          'BitterSweet',
                          'RedOrange',
                          'Mahogany',
                          'Maroon',
                          'BrickRed',
                          'Red',
                          'OrangeRed',
                          'RubineRed',
                          'WildStrawberry',
                          'Salmon',
                          'CarnationPink',
                          'Magenta',
                          'VioletRed',
                          'Rhodamine',
                          'Mulberry',
                          'RedViolet',
                          'Fuchsia',
                          'Lavender',
                          'Thistle',
                          'Orchid',
                          'DarkOrchid',
                          'Purple',
                          'Plum',
                          'Violet',
                          'RoyalPurple',
                          'BlueViolet',
                          'Periwinkle',
                          'CadetBlue',
                          'CornFlowerBlue',
                          'MidnightBlue',
                          'NavyBlue',
                          'RoyalBlue',
                          'Blue',
                          'Cerulean',
                          'Cyan',
                          'ProcessBlue',
                          'SkyBlue',
                          'Turquoise',
                          'TealBlue',
                          'AquaMarine',
                          'BlueGreen',
                          'Emerald',
                          'JungleGreen',
                          'SeaGreen',
                          'Green',
                          'ForestGreen',
                          'PineGreen',
                          'LimeGreen',
                          'YellowGreen',
                          'SpringGreen',
                          'OliveGreen',
                          'RawSienna',
                          'Sepia',
                          'Brown',
                          'Tan',
                          'Gray',
                          'Black',
                          'White'
                          ]


def validate_isopleth_params(field: Any, value: Any, error: Callable):
    ok: bool = True
    errors: Dict[str, Union[str, List[str]]] = {}
    if not isinstance(value, list):
        error_str = f"Isopleth params should be list"
        error(field, error_str)
        return False, {value: error_str}
    for item in value:
        if not isinstance(item, dict):
            error_str = f"Isopleth params should be list of dicts, {item}"
            error(field, error_str)
            return False, {value: error_str}
        ok, errors = validate_params_(isopleth_param_schema, item)
        if not ok:
            return ok, errors
        if 'color' in item:
            if not item['color'] in allowed_color_strings_:
                error_str = f"Unknown color {item['color']}"
                error(field, error_str)
                return False, {value: error_str}
        if 'linewidth' in item:
            if not item['linewidth'] in allowed_linewidth_strings_:
                error_str = f"Unknown linewidth {item['linewidth']}"
                error(field, error_str)
                return False, {value: error_str}
        if 'linestyle' in item:
            if not item['linestyle'] in allowed_linestyle_strings_:
                error_str = f"Unknown linestyle {item['linestyle']}"
                error(field, error_str)
                return False, {value: error_str}
    return ok, errors


def validate_isopleth_params_(field: Any, value: Any, error: Callable):
    validate_isopleth_params(field, value, error)


