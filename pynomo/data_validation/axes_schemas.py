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
from cerberus import Validator
from pyx import color

from pynomo.data_validation.dictionary_validation_functions import scale_type_strings, tick_level_integers, \
    check_manual_axis_data, is_1_param_function, check_text_format_string, check_extra_params, check_pyx_text_size_type, \
    check_pyx_color_param, check_extra_titles, is_2_param_function, check_pyx_linewidth_param

# Schemas for axes

# common axis params
axis_info_common = {
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
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'Title shift in x-direction',
        'default': 0.0
    },
    'title_y_shift': {
        'rules': {'required': False, 'type': ['float', 'integer']},
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
        'rules': {'required': False, 'type': ['float', 'integer']},
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
        'rules': {'required': False, 'type': ['float', 'integer']},
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
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "If axis is aligned with other axis, this value x offsets final scale.",
        'default': 0.0
    },
    'align_y_offset': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "If axis is aligned with other axis, this value y offsets final scale.",
        'default': 0.0
    },
    'text_format': {
        'rules': {'required': False, 'check_with': check_text_format_string},
        'info': "Text format.",
        'default': "$%4.4g$"
    },
    'extra_params': {
        'rules': {'required': False, 'check_with': check_extra_params},
        'info': "List of dictionary of params to be drawn additionally.",
        'default': 0.0
    },
    'text_distance_0': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "Distance of text from scale line.",
        'default': 1.0
    },
    'text_distance_1': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "Distance of text from scale line.",
        'default': 1.0 / 4
    },
    'text_distance_2': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "Distance of text from scale line.",
        'default': 1.0 / 4
    },
    'text_distance_3': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "Distance of text from scale line.",
        'default': 1.0 / 4
    },
    'text_distance_4': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "Distance of text from scale line.",
        'default': 1.0 / 4
    },
    'text_distances': {
        'rules': {'required': False,
                  'type': 'list',
                  'schema': {'type': ['float', 'integer']}
                  },
        'info': "Distance of text from scale line.",
        'default': [1.0, 1.0 / 4.0, 1.0 / 4, 1.0 / 4]
    },
    'grid_length_0': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "Length of the tick..",
        'default': 3.0 / 4
    },
    'grid_length_1': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "Length of the tick..",
        'default': 0.9 / 4
    },
    'grid_length_2': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "Length of the tick..",
        'default': 0.5 / 4
    },
    'grid_length_3': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "Length of the tick..",
        'default': 0.3 / 4
    },
    'grid_length_4': {
        'rules': {'required': False, 'type': ['float', 'integer']},
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
        'rules': {'required': False, 'type': ['float', 'integer']},
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
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'Used with arrow scale.',
        'default': 0.2
    },
    'arrow_length': {
        'rules': {'required': False, 'type': ['float', 'integer']},
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
                  'type': ['float', 'integer'],
                  'nullable': True
                  },
        'info': "Defines number with 'base_stop' (instead of 'u_min' or 'u_max') "
                "to find major tick decades.",
        'default': None
    },
    'base_stop': {
        'rules': {'required': False,
                  'type': ['float', 'integer'],
                  'nullable': True
                  },
        'info': "Defines number with 'base_start' (instead of 'u_min' or 'u_max') "
                "to find major tick decades.",
        'default': None
    },
    'tick_distance_smart': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'Used with arrow scale.',
        'default': 0.05
    },
    'text_distance_smart': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'Used with arrow scale.',
        'default': 0.25
    },
}

# typical for many
axis_info_generic_a = {
    'function': {
        'rules': {'required': True, 'check_with': is_1_param_function},
        'info': 'Function in equation.',
        'default': None
    },
    'u_min': {
        'rules': {'required': True, 'type': ['float', 'integer']},
        'info': "Minimum value of function variable.",
        'default': None
    },
    'u_max': {
        'rules': {'required': True, 'type': ['float', 'integer']},
        'info': "Maximum value of function variable.",
        'default': None
    }
}
# type 1 specific axis params
axis_info_type_1 = axis_info_generic_a
# type 2 specific axis params
axis_info_type_2 = axis_info_generic_a
# type 3 specific axis params
axis_info_type_3 = axis_info_generic_a
# type 4 specific axis params
axis_info_type_4 = axis_info_generic_a
# type 5 specific axis params
axis_info_type_5 = {}  # no axes separately
# type 6 specific axis params
axis_info_type_6 = axis_info_generic_a
# type 7 specific axis params
axis_info_type_7 = axis_info_generic_a
# type 8 specific axis params
axis_info_type_8 = {
    'function': {
        'rules': {'required': True, 'check_with': is_1_param_function},
        'info': 'Function in equation.',
        'default': None
    },
    'u_min': {
        'rules': {'required': True, 'type': ['float', 'integer']},
        'info': "Minimum value of function variable.",
        'default': None
    },
    'u_max': {
        'rules': {'required': True, 'type': ['float', 'integer']},
        'info': "Maximum value of function variable.",
        'default': None
    },
    'function_x': {
        'rules': {'required': True,
                  'check_with': is_1_param_function,
                  'dependencies': ['function_y']},
        'info': 'Function in equation.',
        'default': None
    },
    'function_y': {
        'rules': {'required': True,
                  'check_with': is_1_param_function,
                  'dependencies': ['function_x']},
        'info': 'Function in equation.',
        'default': None
    }
}
# type 9 specific axis params
axis_info_type_9 = {
    'grid': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': 'Sets axis as grid if true.',
        'default': False
    },
    'f': {
        'rules': {'required': False,
                  'check_with': is_1_param_function,
                  'exclude': {
                      'grid': {'allowed': [False]}}
                  },
        'info': 'Function f in determinant row.',
        'default': None
    },
    'g': {
        'rules': {'required': False,
                  'check_with': is_1_param_function,
                  'exclude': {
                      'grid': {'allowed': [False]}}
                  },
        'info': 'Function g in determinant row.',
        'default': None
    },
    'h': {
        'rules': {'required': False,
                  'check_with': is_1_param_function,
                  'exclude': {
                      'grid': {'allowed': [False]}}
                  },
        'info': 'Function h in determinant row.',
        'default': None
    },
    'f_grid': {
        'rules': {'required': True,
                  'check_with': is_2_param_function,
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': 'Function f_grid in determinant row.',
        'default': None
    },
    'g_grid': {
        'rules': {'required': False,
                  'check_with': is_2_param_function,
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': 'Function g_grid in determinant row.',
        'default': None
    },
    'h_grid': {
        'rules': {'required': False,
                  'check_with': is_2_param_function,
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': 'Function h_grid in determinant row.',
        'default': None
    },
    'u_start': {
        'rules': {'required': False,
                  'type': ['float', 'integer'],
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "Minimum value of function variable.",
        'default': None
    },
    'u_stop': {
        'rules': {'required': True,
                  'type': ['float', 'integer'],
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "Maximum value of function variable.",
        'default': None
    },
    'v_start': {
        'rules': {'required': True,
                  'type': ['float', 'integer'],
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "Minimum value of function variable.",
        'default': None
    },
    'v_stop': {
        'rules': {'required': True,
                  'type': ['float', 'integer'],
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "Maximum value of function variable.",
        'default': None
    },
    'text_prefix_u': {
        'rules': {'required': False,
                  'type': 'string',
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "Text prefix for u before value.",
        'default': ''
    },
    'text_prefix_v': {
        'rules': {'required': False,
                  'type': 'string',
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "Text prefix for v before value.",
        'default': ''
    },
    'v_texts_u_start': {
        'rules': {'required': False,
                  'type': 'boolean',
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "If v-texts are in u start side.",
        'default': False
    },
    'v_texts_u_stop': {
        'rules': {'required': False,
                  'type': 'boolean',
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "If v-texts are in u stop side.",
        'default': True
    },
    'u_texts_v_start': {
        'rules': {'required': False,
                  'type': 'boolean',
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "If u-texts are in v start side.",
        'default': False
    },
    'u_texts_v_stop': {
        'rules': {'required': False,
                  'type': 'boolean',
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "If u-texts are in v stop side.",
        'default': True
    },
    'u_line_color': {
        'rules': {'required': False,
                  'check_with': check_pyx_color_param,
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "u-line color.",
        'default': color.rgb.black
    },
    'v_line_color': {
        'rules': {'required': False,
                  'check_with': check_pyx_color_param,
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "v-line color.",
        'default': color.rgb.black
    },
    'u_text_color': {
        'rules': {'required': False,
                  'check_with': check_pyx_color_param,
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "u-line color.",
        'default': color.rgb.black
    },
    'v_text_color': {
        'rules': {'required': False,
                  'check_with': check_pyx_color_param,
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "v-line color.",
        'default': color.rgb.black
    },
    'text_distance': {
        'rules': {'required': True,
                  'type': ['float', 'integer'],
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "Text distance.",
        'default': 0.25
    },
    'circles': {
        'rules': {'required': False,
                  'type': 'boolean',
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "Circles.",
        'default': True
    },
    'text_format_u': {
        'rules': {'required': False,
                  'type': 'boolean',
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "Text format u. For example '$%4.4g$'",
        'default': "$%4.4g$"
    },
    'text_format_v': {
        'rules': {'required': False,
                  'type': 'boolean',
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "Text format v. For example '$%4.4g$'",
        'default': "$%4.4g$"
    },
    'u_line_width': {
        'rules': {'required': False,
                  'check_with': check_pyx_linewidth_param,
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "u linewidth",
        'default': pyx.style.linewidth.normal
    },
    'v_line_width': {
        'rules': {'required': False,
                  'check_with': check_pyx_linewidth_param,
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': "u linewidth",
        'default': pyx.style.linewidth.normal
    },
    'u_values': {
        'rules': {'required': False,
                  'type': 'list',  # list of strings
                  'schema': {'type': ['float', 'integer']},
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': 'List of grid u values.',
        'default': []
    },
    'v_values': {
        'rules': {'required': False,
                  'type': 'list',  # list of strings
                  'schema': {'type': ['float', 'integer']},
                  'depends_on': {
                      'grid': {'allowed': [True]}}
                  },
        'info': 'List of grid v values.',
        'default': []
    },
}
# type 10 specific axis params
axis_info_type_10 = {
    'function': {
        'rules': {'required': True, 'check_with': is_1_param_function},
        'info': 'Function in equation.',
        'default': None
    },
    'u_min': {
        'rules': {'required': True, 'type': ['float', 'integer']},
        'info': "Minimum value of function variable.",
        'default': None
    },
    'u_max': {
        'rules': {'required': True, 'type': ['float', 'integer']},
        'info': "Maximum value of function variable.",
        'default': None
    }
}

# Axis definition for w-scale of type 10 with two functions
axis_info_type_10_w = {
    'u_min': {
            'rules': {'required': True, 'type': ['float', 'integer']},
        'info': "Minimum value of function variable.",
        'default': None
    },
    'u_max': {
        'rules': {'required': True, 'type': ['float', 'integer']},
        'info': "Maximum value of function variable.",
        'default': None
    },
    'function_3': {
        'rules': {'required': True,
                  'check_with': is_1_param_function,
                  'dependencies': ['function_y']},
        'info': 'Function in equation.',
        'default': None
    },
    'function_4': {
        'rules': {'required': True,
                  'check_with': is_1_param_function,
                  'dependencies': ['function_x']},
        'info': 'Function in equation.',
        'default': None
    }
}


def give_dictionary_dropping_rules(dict_in):
    result = {}
    # this is easier to read than dict comprehensions...
    for key in dict_in.keys():
        result[key] = dict_in[key]['rules']
    return result



def give_rules_from_dictionaries(dict1, dict2):
    return {
        **give_dictionary_dropping_rules(dict1),
        **give_dictionary_dropping_rules(dict2)
    }


axis_schema_type_1 = give_rules_from_dictionaries(axis_info_common, axis_info_type_1)


"""
axis_schema_type_1 = 
    {
    **{key: axis_info_common[key]['rules'] for key in axis_info_common if 'rules' in axis_info_common[key]},
    **{key: axis_info_type_1[key]['rules'] for key in axis_info_type_1 if 'rules' in axis_info_type_1[key]}
}

new_dict = {key: {k:v for k,v in value.items() if k!='rules'} for key, value in axis_info_type_10_w.items() if 'rules' in value}

"""

print(axis_schema_type_1)


