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
from pyx import color

from pynomo.data_validation.dictionary_validation_functions import check_general_axis_params, check_pyx_color_param, \
    check_type_8_axis_params, check_type_9_axis_params, check_type_10_w_axis_params, is_1_param_function, \
    check_manual_axis_data, scale_type_strings, check_text_format_string, check_type_4_axis_params, \
    check_type_3_axis_params, check_type_2_axis_params, check_type_1_axis_params

#
# Block parameter definitions.
#


# common block params
block_schema_common = {
    'block_type': {
        'rules': {
            'type': 'string',
            'allowed': ['type_1', 'type_2', 'type_3', 'type_4', 'type_5',
                        'type_6', 'type_7', 'type_8', 'type_9', 'type_10']
        },
        'info': "Block type, what kind of block to make."},
    'width': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'Width of the block during setup. To be scaled in main params finally.',
        'default': 10.0
    },
    'height': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'Height of the block during setup. To be scaled in main params finally.',
        'default': 10.0
    },
    'mirror_x': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': 'Mirror block w.r.t x-axis when drawn originally.',
        'default': False,
    },
    'mirror_y': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': 'Mirror block w.r.t y-axis when drawn originally.',
        'default': False
    },
    'debug': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': 'Prints block dictionary to console.',
        'default': False
    },
    'isopleth_values': {
        'rules': {'required': False, 'type': 'list'},
        'info': "List of isopleth values. Unknown is marked with "
                "string 'x'. For example [[1.0, 2.0, 'x']].",
        'default': []
    },
}
# type 1 specific block params
block_schema_type_1 = {
    'f1_params': {
        'rules': {'required': True, 'check_with': check_type_1_axis_params},
        'info': 'Axis parameters defining first scale.',
        'default': None
    },
    'f2_params': {
        'rules': {'required': True, 'check_with': check_type_1_axis_params},
        'info': 'Axis parameters defining second scale.',
        'default': None
    },
    'f3_params': {
        'rules': {'required': True, 'check_with': check_type_1_axis_params},
        'info': 'Axis parameters defining third scale.',
        'default': None
    },
    'proportion': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'Factor for spacings between lines.',
        'default': 1.0
    }
}
# type 2 specific block params
block_schema_type_2 = {
    'f1_params': {
        'rules': {'required': True, 'check_with': check_type_2_axis_params},
        'info': 'Axis parameters defining first scale.',
        'default': None
    },
    'f2_params': {
        'rules': {'required': True, 'check_with': check_type_2_axis_params},
        'info': 'Axis parameters defining second scale.',
        'default': None
    },
    'f3_params': {
        'rules': {'required': True, 'check_with': check_type_2_axis_params},
        'info': 'Axis parameters defining third scale.',
        'default': None
    }
}
# type 3 specific block params
block_schema_type_3 = {
    'f_params': {
        'rules': {'required': True, 'check_with': check_type_3_axis_params},
        'info': 'Axis parameters defining first scale.',
        'default': None
    },
    'reference_padding': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'Additional length to reference axes (turning-point lines).',
        'default': 0.2
    },
    'reference_titles': {
        'rules': {'required': False,
                  'type': 'list',  # list of strings
                  'schema': {'type': 'string'}},
        'info': 'List of reference line titles. For example ["$R_1$","$R_2$","$R_3$"].',
        'default': []
    },
    'reference_color': {
        'rules': {'required': False, 'check_with': check_pyx_color_param},
        'info': 'Color of reference lines).',
        'default': color.rgb.black
    }
}
# type 4 specific block params
block_schema_type_4 = {
    'f1_params': {
        'rules': {'required': True, 'check_with': check_type_4_axis_params},
        'info': 'Axis parameters defining first scale.',
        'default': None
    },
    'f2_params': {
        'rules': {'required': True, 'check_with': check_type_4_axis_params},
        'info': 'Axis parameters defining second scale.',
        'default': None
    },
    'f3_params': {
        'rules': {'required': True, 'check_with': check_type_4_axis_params},
        'info': 'Axis parameters defining third scale.',
        'default': None
    },
    'f4_params': {
        'rules': {'required': True, 'check_with': check_type_4_axis_params},
        'info': 'Axis parameters defining fourth scale.',
        'default': None
    },
    'padding': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'How much axis extend w.r.t. width/height.',
        'default': 0.9
    },
    'reference_color': {
        'rules': {'required': False, 'check_with': check_pyx_color_param},
        'info': 'Color of reference lines.',
        'default': color.rgb.black
    },
    'float_axis': {
        'rules': {'required': False, type: "string"},
        'info': 'If given "F1 or F2", then scaling is according to them, '
                'otherwise (any other string) according to F3 and F4.',
        'default': 'F1 or F2'
    }
}
# type 5 specific block params
block_schema_type_5 = {
    'u_func': {
        'rules': {'required': True, 'check_with': is_1_param_function},
        'info': 'u-function',
        'default': None
    },
    'v_func': {
        'rules': {'required': True, 'check_with': is_1_param_function},
        'info': 'v-function',
        'default': None
    },
    'wd_func': {
        'rules': {'required': True, 'check_with': is_1_param_function},
        'info': 'wd-function',
        'default': None
    },
    'wd_func_inv': {
        'rules': {'required': False, 'check_with': is_1_param_function},
        'info': 'wd-function',
        'default': lambda x: x,
    },
    'u_tag': {
        'rules': {'required': False, 'type': 'string'},
        'info': 'Aligning tag for u-scale',
        'default': 'none',
    },
    'u_title': {
        'rules': {'required': False, 'type': 'string'},
        'info': 'Title for u-scale',
        'default': '',
    },
    """
    'u_title_x_shift': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'u-title shift in x-direction',
        'default': 0.0
    },
    'u_title_y_shift': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'u-title shift in y-direction',
        'default': 0.25
    },
    """
    'scale_type_u': {
        'rules': {'required': False, 'type': 'string', 'allowed': scale_type_strings},
        'info': 'Scale-type for u-axis.',
        'default': 'linear'
    },
    """
    'u_tick_levels': {
        'rules': {'required': False, 'type': 'integer', 'allowed': tick_level_integers},
        'info': 'How many levels (minor, minor-minor, etc.) of ticks are drawn. '
                'Largest effect to "linear" scale.',
        'default': 4
    },
    'u_tick_text_levels': {
        'rules': {'required': False, 'type': 'integer', 'allowed': tick_level_integers},
        'info': 'How many levels (minor, minor-minor, etc.) of texts are drawn.',
        'default': 3
    },
    """
    'u_tick_side': {
        'rules': {'required': False, 'type': 'string', 'allowed': ['right', 'left']},
        'info': 'Tick and text side in final paper.',
        'default': 3
    },
    'u_reference': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': ' If axis is treated as reference line that is a turning point..',
        'default': 3
    },
    """
    'u_reference_padding': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'Fraction of reference line over other lines.',
        'default': 0.2
    },"""
    'u_manual_axis_data': {
        'rules': {'required': False, 'check_with': check_manual_axis_data},
        'info': ' If axis is treated as reference line that is a turning point..',
        'default': 3
    },
    'u_title_draw_center': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': 'Title is drawn to center of line.',
        'default': False
    },
    'u_title_distance_center': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "When 'u_title_draw_center' is 'True' sets distance of title from axis.",
        'default': 0.5
    },
    'u_title_opposite_tick': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': ' Title in opposite direction w.r.t ticks.',
        'default': True
    },
    'u_align_func': {
        'rules': {'required': False, 'check_with': is_1_param_function},
        'info': 'Function to align different scales.',
        'default': lambda u: u
    },
    'u_align_x_offset': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "If axis is aligned with other axis, this value x offsets final scale.",
        'default': 0.0
    },
    'u_align_y_offset': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "If axis is aligned with other axis, this value y offsets final scale.",
        'default': 0.0
    },
    'u_text_format': {
        'rules': {'required': False, 'check_with': check_text_format_string},
        'info': "If axis is aligned with other axis, this value y offsets final scale.",
        'default': 0.0
    },
    """
    # These are in documentation but not really in use...??

        'u_extra_params': {
            'rules': {'required': False, 'check_with': check_extra_params},
            'info': "List of dictionary of params to be drawn additionally.",
            'default': 0.0
        },

        'u_text_distance_0': {
            'rules': {'required': False, 'type': ['float', 'integer']},
            'info': "Distance of text from scale line.",
            'default': 1.0  # TODO: update correct value
        },
        'u_text_distance_1': {
            'rules': {'required': False, 'type': ['float', 'integer']},
            'info': "Distance of text from scale line.",
            'default': 1.0  # TODO: update correct value
        },
        'u_text_distance_2': {
            'rules': {'required': False, 'type': ['float', 'integer']},
            'info': "Distance of text from scale line.",
            'default': 1.0  # TODO: update correct value
        },
        'u_text_distance_3': {
            'rules': {'required': False, 'type': ['float', 'integer']},
            'info': "Distance of text from scale line.",
            'default': 1.0  # TODO: update correct value
        },
        'u_text_distance_4': {
            'rules': {'required': False, 'type': ['float', 'integer']},
            'info': "Distance of text from scale line.",
            'default': 1.0  # TODO: update correct value
        },
        'u_grid_length_0': {
            'rules': {'required': False, 'type': ['float', 'integer']},
            'info': "Length of the tick..",
            'default': 1.0  # TODO: update correct value
        },
        'u_grid_length_1': {
            'rules': {'required': False, 'type': ['float', 'integer']},
            'info': "Length of the tick..",
            'default': 1.0  # TODO: update correct value
        },
        'u_grid_length_2': {
            'rules': {'required': False, 'type': ['float', 'integer']},
            'info': "Length of the tick..",
            'default': 1.0  # TODO: update correct value
        },
        'u_grid_length_3': {
            'rules': {'required': False, 'type': ['float', 'integer']},
            'info': "Length of the tick..",
            'default': 1.0  # TODO: update correct value
        },
        'u_grid_length_4': {
            'rules': {'required': False, 'type': ['float', 'integer']},
            'info': "Length of the tick..",
            'default': 1.0  # TODO: update correct value
        },
        'u_text_size_0': {
            'rules': {'required': False, 'check_with': check_pyx_text_size_type},
            'info': "Length of the tick..",
            'default': 1.0  # TODO: update correct value
        },
        'u_text_size_1': {
            'rules': {'required': False, 'check_with': check_pyx_text_size_type},
            'info': "Length of the tick..",
            'default': 1.0  # TODO: update correct value
        },
        'u_text_size_2': {
            'rules': {'required': False, 'check_with': check_pyx_text_size_type},
            'info': "Length of the tick..",
            'default': 1.0  # TODO: update correct value
        },
        'u_text_size_3': {
            'rules': {'required': False, 'check_with': check_pyx_text_size_type},
            'info': "Length of the tick..",
            'default': 1.0  # TODO: update correct value
        },
        'u_text_size_4': {
            'rules': {'required': False, 'check_with': check_pyx_text_size_type},
            'info': "Length of the tick..",
            'default': 1.0  # TODO: update correct value
        },
        'u_text_size_log_0': {
            'rules': {'required': False, 'check_with': check_pyx_text_size_type},
            'info': "Length of the tick..",
            'default': 1.0  # TODO: update correct value
        },

        'u_text_size_log_1': {
            'rules': {'required': False, 'check_with': check_pyx_text_size_type},
            'info': "Length of the tick..",
            'default': 1.0  # TODO: update correct value
        },

        'u_text_size_log_2': {
            'rules': {'required': False, 'check_with': check_pyx_text_size_type},
            'info': "Length of the tick..",
            'default': 1.0  # TODO: update correct value
        },
        """
    """
    'u_full_angle': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': ' If true, text can be upside down, otherwise +- 90 degrees from horizontal.'
                ' Good for example for full circle scales.',
        'default': True
    },

    'u_extra_angle': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'Angle to rotate tick text from horizontal along tick.',
        'default': 0.0
    },
    'u_text_horizontal_align_center': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': 'Aligns tick text horizontally to center. Good when text rotated 90 degrees.',
        'default': True
    },"""
    'u_axis_color': {
        'rules': {'required': False, 'check_with': check_pyx_color_param},
        'info': "Color of axis.",
        'default': color.rgb.black
    },
    'u_text_color': {
        'rules': {'required': False, 'check_with': check_pyx_color_param},
        'info': "Color of axis.",
        'default': color.rgb.black
    },
    'u_title_color': {
        'rules': {'required': False, 'check_with': check_pyx_color_param},
        'info': "Color of axis.",
        'default': color.rgb.black
    },
    'u_values': {
        'rules': {'required': True,
                  'type': 'list',  # list of strings
                  'schema': {'type': ['float', 'integer']}},
        'info': 'List of plotted u values.',
        'default': []
    },
    # v
    'v_title': {
        'rules': {'required': False, 'type': 'string'},
        'info': 'Title for u-scale',
        'default': '',
    },
    'v_title_draw_center': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': 'Title is drawn to center of line.',
        'default': False
    },
    'v_title_distance_center': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "When 'u_title_draw_center' is 'True' sets distance of title from axis.",
        'default': 0.5
    },
    # wd
    'wd_tag': {
        'rules': {'required': False, 'type': 'string'},
        'info': 'Aligning tag for u-scale',
        'default': 'none',
    },
    'wd_title': {
        'rules': {'required': False, 'type': 'string'},
        'info': 'Title for u-scale',
        'default': '',
    },
    'scale_type_wd': {
        'rules': {'required': False, 'type': 'string', 'allowed': scale_type_strings},
        'info': 'Scale-type for u-axis.',
        'default': 'linear'
    },
    'wd_tick_side': {
        'rules': {'required': False, 'type': 'string', 'allowed': ['right', 'left']},
        'info': 'Tick and text side in final paper.',
        'default': 3
    },
    'wd_reference': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': ' If axis is treated as reference line that is a turning point..',
        'default': 3
    },
    'wd_manual_axis_data': {
        'rules': {'required': False, 'check_with': check_manual_axis_data},
        'info': ' If axis is treated as reference line that is a turning point..',
        'default': 3
    },
    'wd_title_draw_center': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': 'Title is drawn to center of line.',
        'default': False
    },
    'wd_title_distance_center': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "When 'u_title_draw_center' is 'True' sets distance of title from axis.",
        'default': 0.5
    },
    'wd_title_opposite_tick': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': ' Title in opposite direction w.r.t ticks.',
        'default': True
    },
    'wd_align_func': {
        'rules': {'required': False, 'check_with': is_1_param_function},
        'info': 'Function to align different scales.',
        'default': lambda u: u
    },
    'wd_align_x_offset': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "If axis is aligned with other axis, this value x offsets final scale.",
        'default': 0.0
    },
    'wd_align_y_offset': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': "If axis is aligned with other axis, this value y offsets final scale.",
        'default': 0.0
    },
    """
    # does not exist
    'wd_text_format': {
        'rules': {'required': False, 'check_with': check_text_format_string},
        'info': "If axis is aligned with other axis, this value y offsets final scale.",
        'default': 0.0
    },"""
    'wd_axis_color': {
        'rules': {'required': False, 'check_with': check_pyx_color_param},
        'info': "Color of axis.",
        'default': color.rgb.black
    },
    'wd_text_color': {
        'rules': {'required': False, 'check_with': check_pyx_color_param},
        'info': "Color of axis.",
        'default': color.rgb.black
    },
    'wd_title_color': {
        'rules': {'required': False, 'check_with': check_pyx_color_param},
        'info': "Color of axis.",
        'default': color.rgb.black
    },
    'wd_values': {
        'rules': {'required': True,
                  'type': 'list',  # list of strings
                  'schema': {'type': ['float', 'integer']}},
        'info': 'List of plotted u values.',
        'default': []
    }
}
# type 6 specific block params
block_schema_type_6 = {
    'type': {
        'rules': {
            'type': 'string',
            'allowed': ['parallel', 'orthogonal']
        },
        'info': "Block type, parallel or orthogonal"},
    'x_empty': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'If orthogonal, how much fractional space before start of x-axis.',
        'default': 0.2
    },
    'y_empty': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'If orthogonal, how much fractional space before start of y-axis.',
        'default': 0.2
    },
    'curve_const': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'Sets the length of angle of Bezier curve. low value = straigh line, high value = curved line.',
        'default': 0.0
    },
    'f1_params': {
        'rules': {'required': True, 'check_with': check_general_axis_params},
        'info': 'Axis parameters defining first scale.',
        'default': None
    },
    'f2_params': {
        'rules': {'required': True, 'check_with': check_general_axis_params},
        'info': 'Axis parameters defining first scale.',
        'default': None
    },
    'ladder_color': {
        'rules': {'required': False, 'check_with': check_pyx_color_param},
        'info': 'Color of reference lines.',
        'default': color.rgb.black
    },
}
# type 7 specific block params
block_schema_type_7 = {
    'f1_params': {
        'rules': {'required': True, 'check_with': check_general_axis_params},
        'info': 'Axis parameters defining first scale.',
        'default': None
    },
    'f2_params': {
        'rules': {'required': True, 'check_with': check_general_axis_params},
        'info': 'Axis parameters defining second scale.',
        'default': None
    },
    'f3_params': {
        'rules': {'required': True, 'check_with': check_general_axis_params},
        'info': 'Axis parameters defining third scale.',
        'default': None
    },
    'angle_u': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'Angle between u1 and u3. Note: later transformations may alter the angle.',
        'default': 45.0
    },
    'angle_v': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'Angle between u2 and u3. Note: later transformations may alter the angle.',
        'default': 45.0
    }
}
# type 8 specific block params
block_schema_type_8 = {
    'f1_params': {
        'rules': {'required': True, 'check_with': check_type_8_axis_params},
        'info': 'Axis parameters defining first scale.',
        'default': None
    },
    'length': {
        'rules': {'required': False, 'type': ['float', 'integer']},
        'info': 'Length of axis.',
        'default': 10.0
    },
}
# type 9 specific block params
block_schema_type_9 = {
    'f1_params': {
        'rules': {'required': True, 'check_with': check_type_9_axis_params},
        'info': 'Axis parameters defining first scale or grid.',
        'default': None
    },
    'f2_params': {
        'rules': {'required': True, 'check_with': check_type_9_axis_params},
        'info': 'Axis parameters defining second scale or grid.',
        'default': None
    },
    'f3_params': {
        'rules': {'required': True, 'check_with': check_type_9_axis_params},
        'info': 'Axis parameters defining third scale or grid.',
        'default': None
    },
    'transform_ini': {
        'rules': {'required': False, 'type': 'boolean'},
        'info': 'Mirror block w.r.t y-axis when drawn originally.',
        'default': False
    }
}
# type 10 specific block params
block_schema_type_10 = {
    'f1_params': {
        'rules': {'required': True, 'check_with': check_general_axis_params},
        'info': 'Axis parameters defining first scale or grid.',
        'default': None
    },
    'f2_params': {
        'rules': {'required': True, 'check_with': check_general_axis_params},
        'info': 'Axis parameters defining second scale or grid.',
        'default': None
    },
    'f3_params': {
        'rules': {'required': True, 'check_with': check_type_10_w_axis_params},
        'info': 'Axis parameters defining third scale or grid.',
        'default': None
    }
}