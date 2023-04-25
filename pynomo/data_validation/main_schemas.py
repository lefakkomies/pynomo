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

""" Schemas for main params., the top level dictionary defining the nomograph

"""

from typing import Dict, Union, List, Any, Callable
import numbers
import numpy as np

from pyx import color

from pynomo.data_validation.dictionary_validation_functions import check_pyx_color_param, is_1_param_function

main_params_info: Dict[str, dict] = {
    'filename': {
        'rules': {
            'required': True,
            'type': 'string'
        },
        'info': "Filename of generated nomograph file. pdf and eps formats are supported.",
        'default': 'pynomo_output.pdf'
    },
    'paper_height': {
        'rules': {
            'required': False,
            'type': ['float', 'integer']
        },
        'info': "Height of paper (roughly, ticks and texts extend this).",
        'default': 20.0
    },
    'paper_width': {
        'rules': {
            'required': False,
            'type': ['float', 'integer']
        },
        'info': "Width of paper (roughly, ticks and texts extend this).",
        'default': 20.0
    },
    'title_str': {
        'rules': {
            'required': False,
            'type': 'string'
        },
        'info': "Title string of nomograph.",
        'default': ''
    },

    'title_x': {
        'rules': {
            'required': False,
            'type': ['float', 'integer']
        },
        'info': "Title x-position.",
        'default': None
    },
    'title_y': {
        'rules': {
            'required': False,
            'type': ['float', 'integer']
        },
        'info': "Title y-position.",
        'default': None
    },
    'title_box_width': {
        'rules': {
            'required': False,
            'type': ['float', 'integer']
        },
        'info': "Title box width.",
        'default': None
    },
    'title_color': {
        'rules': {
            'required': False,
            'check_with': check_pyx_color_param
        },
        'info': "Title color.",
        'default': color.rgb.black
    },
    'make_grid': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': 'If true, draws grid to help position texts, etc.',
        'default': False
    },
    'debug': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': 'If true, prints dicts of definitions.',
        'default': False
    },
    'transformations': {
        'rules': {'required': False,
                  'check_with': validate_transformations_},
        'info': "Array of tuples defining transformations",
        'default': [('rotate', 0.01), ('scale paper',)]
    },
    'pre_func': {
        'rules': {'required': False,
                  'check_with': is_1_param_function},
        'info': "PyX function(canvas) to draw under nomograph. Function takes canvas context as a parameter.",
        'default': None
    },
    'post_func': {
        'rules': {'required': False,
                  'check_with': is_1_param_function},
        'info': "PyX function(canvas) to draw over nomograph. Function takes canvas context as a parameter.",
        'default': None
    }
}
