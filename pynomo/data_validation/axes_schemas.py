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
import pyx
from pyx import color

from pynomo.data_validation.dictionary_validation_functions import scale_type_strings, tick_level_integers, \
    check_manual_axis_data, is_1_param_function, check_text_format_string, check_extra_params, check_pyx_text_size_type, \
    check_pyx_color_param, check_extra_titles

# Schemas for axes

# common axis params
axis_schema_common = {
    'scale_type': {
        'rules': {
            'required': True,
            'type': 'string',
            'allowed': scale_type_strings
        },
        'info': "Axis type, what kind of axis to make.",
        'default': 'linear'
    },
    'ID': {
        'rules': {'required': False, 'type': 'string'},
        'info': 'To identify the axis..',
        'default': False
    },
    'tag': {
        'rules': {'required': False, 'type': 'string'},
        'info': 'For aligning two axes. "none" means no alignment. ',
        'default': 'none'
    },
    'dtag': {
        'rules': {'required': False, 'type': 'string'},
        'info': 'For aligning second two axes in addition to "tag" axes. "none" means no alignment. ',
        'default': 'none'
    },
    'title': {
        'rules': {'required': False, 'type': 'string'},
        'info': 'Title of axis',
        'default': ''
    },
    'title_x_shift': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': 'Title shift in x-direction',
        'default': 0.0
    },
    'title_y_shift': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': 'Title shift in y-direction',
        'default': 0.0
    },
    'tick_levels': {
        'rules': {'required': False, 'type': 'integer', 'allowed': tick_level_integers},
        'info': 'How many levels (minor, minor-minor, etc.) of ticks are drawn. '
                'Largest effect to "linear" scale.',
        'default': 4
    },
    'tick_text_levels': {
        'rules': {'required': False, 'type': 'integer', 'allowed': tick_level_integers},
        'info': 'How many levels (minor, minor-minor, etc.) of texts are drawn.',
        'default': 3
    },
    'tick_side': {
        'rules': {'required': False, 'type': 'string', 'allowed': ['right', 'left']},
        'info': 'Tick and text side in final paper.',
        'default': 3
    },
    'reference': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': ' If axis is treated as reference line that is a turning point.',
        'default': 3
    },
    'reference_padding': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': 'Fraction of reference line over other lines.',
        'default': 0.2
    },
    'manual_axis_data': {
        'rules': {'required': False, 'check_with': check_manual_axis_data},
        'info': 'Manually set tick/point positions and text positions.',
        'default': {}
    },
    'title_draw_center': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': 'Title is drawn to center of line.',
        'default': False
    },
    'title_distance_center': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': "When 'u_title_draw_center' is 'True' sets distance of title from axis.",
        'default': 0.5
    },
    'title_opposite_tick': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': ' Title in opposite direction w.r.t ticks.',
        'default': True
    },
    'align_func': {
        'rules': {'required': False, 'check_with': is_1_param_function},
        'info': 'Function to align different scales.',
        'default': lambda u: u
    },
    'align_x_offset': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': "If axis is aligned with other axis, this value x offsets final scale.",
        'default': 0.0
    },
    'align_y_offset': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': "If axis is aligned with other axis, this value y offsets final scale.",
        'default': 0.0
    },
    'text_format': {
        'rules': {'required': False, 'check_with': check_text_format_string},
        'info': "If axis is aligned with other axis, this value y offsets final scale.",
        'default': 0.0
    },
    'extra_params': {
        'rules': {'required': False, 'check_with': check_extra_params},
        'info': "List of dictionary of params to be drawn additionally.",
        'default': 0.0
    },
    'text_distance_0': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': "Distance of text from scale line.",
        'default': 1.0
    },
    'text_distance_1': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': "Distance of text from scale line.",
        'default': 1.0 / 4
    },
    'text_distance_2': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': "Distance of text from scale line.",
        'default': 1.0 / 4
    },
    'text_distance_3': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': "Distance of text from scale line.",
        'default': 1.0 / 4
    },
    'text_distance_4': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': "Distance of text from scale line.",
        'default': 1.0 / 4
    },
    'text_distances': {
        'rules': {'required': False,
                  'type': 'list',
                  'schema': {'type': {'allowed': ['float', 'integer']}}
                  },
        'info': "Distance of text from scale line.",
        'default': [1.0, 1.0 / 4.0, 1.0 / 4, 1.0 / 4]
    },
    'grid_length_0': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': "Length of the tick..",
        'default': 3.0 / 4
    },
    'grid_length_1': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': "Length of the tick..",
        'default': 0.9 / 4
    },
    'grid_length_2': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': "Length of the tick..",
        'default': 0.5 / 4
    },
    'grid_length_3': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': "Length of the tick..",
        'default': 0.3 / 4
    },
    'grid_length_4': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': "Length of the tick..",
        'default': 0.2 / 4
    },
    'text_size_0': {
        'rules': {'required': False, 'check_with': check_pyx_text_size_type},
        'info': "Length of the tick..",
        'default': pyx.text.size.small
    },
    'text_size_1': {
        'rules': {'required': False, 'check_with': check_pyx_text_size_type},
        'info': "Length of the tick..",
        'default': pyx.text.size.scriptsize
    },
    'text_size_2': {
        'rules': {'required': False, 'check_with': check_pyx_text_size_type},
        'info': "Length of the tick..",
        'default': pyx.text.size.tiny
    },
    'text_size_3': {
        'rules': {'required': False, 'check_with': check_pyx_text_size_type},
        'info': "Length of the tick..",
        'default': pyx.text.size.tiny
    },
    'text_size_4': {
        'rules': {'required': False, 'check_with': check_pyx_text_size_type},
        'info': "Length of the tick..",
        'default': pyx.text.size.tiny
    },
    'text_size_log_0': {
        'rules': {'required': False, 'check_with': check_pyx_text_size_type},
        'info': "Length of the tick..",
        'default': pyx.text.size.small
    },
    'text_size_log_1': {
        'rules': {'required': False, 'check_with': check_pyx_text_size_type},
        'info': "Length of the tick..",
        'default': pyx.text.size.tiny
    },
    'text_size_log_2': {
        'rules': {'required': False, 'check_with': check_pyx_text_size_type},
        'info': "Length of the tick..",
        'default': pyx.text.size.tiny
    },
    'text_size_manual': {
        'rules': {'required': False, 'check_with': check_pyx_text_size_type},
        'info': "Length of the tick..",
        'default': pyx.text.size.small
    },
    'full_angle': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': ' If true, text can be upside down, otherwise +- 90 degrees from horizontal.'
                ' Good for example for full circle scales.',
        'default': True
    },
    'extra_angle': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': 'Angle to rotate tick text from horizontal along tick.',
        'default': 0.0
    },
    'text_horizontal_align_center': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': 'Aligns tick text horizontally to center. Good when text rotated 90 degrees.',
        'default': False
    },
    'turn_relative': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': ' Side left or right is relative according to traveling of scale from min to max.',
        'default': True
    },
    'arrow_size': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': 'Used with arrow scale.',
        'default': 0.2
    },
    'arrow_length': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': 'Used with arrow scale.',
        'default': 0.2
    },
    'arrow_color': {
        'rules': {'required': False, 'check_with': check_pyx_color_param},
        'info': 'Arrow color.',
        'default': color.rgb.black
    },
    'axis_color': {
        'rules': {'required': False, 'check_with': check_pyx_color_param},
        'info': 'Axis color.',
        'default': color.rgb.black
    },
    'text_color': {
        'rules': {'required': False, 'check_with': check_pyx_color_param},
        'info': 'Text color.',
        'default': color.rgb.black
    },
    'extra_titles': {
        'rules': {'required': False, 'check_with': check_extra_titles},
        'info': 'Text color.',
        'default': []
    },
    'base_start': {
        'rules': {'required': False,
                  'type': {'allowed': ['float', 'integer']},
                  'nullable': True
                  },
        'info': "Defines number with 'base_stop' (instead of 'u_min' or 'u_max') "
                "to find major tick decades.",
        'default': None
    },
    'base_stop': {
        'rules': {'required': False,
                  'type': {'allowed': ['float', 'integer']},
                  'nullable': True
                  },
        'info': "Defines number with 'base_start' (instead of 'u_min' or 'u_max') "
                "to find major tick decades.",
        'default': None
    },
    'tick_distance_smart': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': 'Used with arrow scale.',
        'default': 0.05
    },
    'text_distance_smart': {
        'rules': {'required': False, 'type': {'allowed': ['float', 'integer']}},
        'info': 'Used with arrow scale.',
        'default': 0.25
    },
}


# type 1 specific axis params
# type 2 specific axis params
# type 3 specific axis params
# type 4 specific axis params
# type 5 specific axis params
# type 6 specific axis params
# type 7 specific axis params
# type 8 specific axis params
# type 9 specific axis params
