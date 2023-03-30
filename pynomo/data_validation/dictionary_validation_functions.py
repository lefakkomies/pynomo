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
import re

import pyx
from cerberus import Validator
from inspect import isfunction, signature

from pyx import color


def is_1_param_function(field, value, error):
    if len(signature(value).parameters) != 1:
        error(field, "Must be one parameter function")


def is_2_param_function(field, value, error):
    if len(signature(value).parameters) != 2:
        error(field, "Must be two parameter function")


def check_general_axis_params(field, value, error):
    # TODO:
    pass


def check_type_1_axis_params(field, value, error):
    check_general_axis_params(field, value, error)


def check_type_2_axis_params(field, value, error):
    check_general_axis_params(field, value, error)


def check_type_3_axis_params(field, value, error):
    check_general_axis_params(field, value, error)


def check_type_4_axis_params(field, value, error):
    check_general_axis_params(field, value, error)


def check_type_5_axis_params(field, value, error):
    # TODO run checker for type 5 axis params
    pass


def check_type_6_axis_params(field, value, error):
    check_general_axis_params(field, value, error)


def check_type_7_axis_params(field, value, error):
    # TODO run checker for type 7 axis params
    pass


def check_type_8_axis_params(field, value, error):
    # TODO run checker for type 8 axis params
    pass


def check_type_9_axis_params(field, value, error):
    # TODO run checker for type 9 axis params
    pass


def check_type_10_w_axis_params(field, value, error):
    # TODO run checker for type 9 axis params
    pass


def check_pyx_color_param(field, value, error):
    return isinstance(value, type(pyx.color.rgb.black))


def check_pyx_linewidth_param(field, value, error):
    return isinstance(value, type(pyx.style.linewidth.normal))


def check_pyx_text_size_type(field, value, error):
    return isinstance(value, type(pyx.text.size.tiny))


def check_manual_axis_data(field, value, error):
    # TODO: check manual-axis data parameters are correct
    pass


def check_text_format_string(field, value, error):
    pattern = r"\$%[\d\.]+[a-zA-Z]\$"
    if not re.match(pattern, value):
        error(field, f"{value} does not match the required format")


def check_extra_params(field, value, error):
    # TODO: check extra-params dictionary
    pass


def check_extra_titles(field, value, error):
    # TODO: check
    pass


schema = {
    'name': {
        'type': 'string'
    },
    'age': {
        'type': 'integer'
    },
    'data': {
        'type': 'integer',
        'required': False
    },
    'data_object': {
        'type': 'integer',
        'required': False
    },
    'test_function': {
        'check_with': is_2_param_function
    }

}

scale_type_strings = ['linear', 'smart linear', 'smart log', 'log', 'manual point', 'manual line']
tick_level_integers = [0, 1, 2, 3, 4, 5]
"""
block_schema = {
    'block_type': {
        'type': 'string',
        'allowed': ['type_1', 'type_2', 'type_3', 'type_4', 'type_5',
                    'type_6', 'type_7', 'type_8', 'type_9', 'type_10']
    },
    'f1_params': {'required': False},
    'f2_params': {'required': False},
    'f3_params': {'required': False},
    'f4_params': {'required': False},
    'f_params': {'required': False},  # type 8
    'mirror_x': {'required': False, 'type': 'boolean'},
    'mirror_y': {'required': False, 'type': 'boolean'},
    'proportion': {'required': False},  # type 1
    'isopleth_values': {'required': False, 'type': 'list'},
    'height': {'required': False, 'type': ['float', 'integer']},
    'width': {'required': False, 'type': ['float', 'integer']},
    'reference_padding': {'required': False, 'type': ['float', 'integer']},  # type 3
    'reference_titles': {'required': False, 'type': ['float', 'integer']},  # type 3
    'reference_color': {'required': False},  # type 3
    'padding': {'required': False, 'type': ['float', 'integer']},  # type 4
    'float_axis': {'required': False, 'type': 'string'},
    'u_func': {'required': False, 'check_with': is_1_param_function},  # type 5
    'v_func': {'required': False, 'check_with': is_1_param_function},  # type 5
    'wd_func': {'required': False, 'check_with': is_1_param_function},  # type 5
    'wd_func_inv': {'required': False, 'check_with': is_1_param_function},  # type 5
    'u_tag': {'required': False, 'type': 'string'},  # type 5
    'u_title': {'required': False, 'type': 'string'},  # type 5
    'u_title_x_shift': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_title_y_shift': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_scale_type': {'required': False, 'type': 'string', 'allowed': scale_type_strings},  # type 5
    'u_tick_levels': {'required': False, 'type': 'integer'},  # type 5
    'u_tick_text_levels': {'required': False, 'type': 'integer'},  # type 5
    'u_tick_side': {'required': False, 'type': 'string', 'allowed': ['right', 'left']},  # type 5
    'u_reference': {'required': False, 'type': 'boolean'},  # type 5
    'u_title_draw_center': {'required': False, 'type': 'boolean'},  # type 5
    'u_title_distance_center': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_title_opposite_tick': {'required': False, 'type': 'boolean'},  # type 5
    'u_align_func': {'required': False, 'check_with': is_1_param_function},  # type 5
    'u_align_x_offset': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_align_y_offset': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_text_format': {'required': False, 'type': 'string'},  # type 5
    'u_extra_params': {'required': False, 'type': 'dict'},  # type 5
    'u_text_distance_0': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_text_distance_1': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_text_distance_2': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_text_distance_3': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_text_distance_4': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_grid_length_0': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_grid_length_1': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_grid_length_2': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_grid_length_3': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_grid_length_4': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_text_size_0': {'required': False},  # type 5
    'u_text_size_1': {'required': False},  # type 5
    'u_text_size_2': {'required': False},  # type 5
    'u_text_size_3': {'required': False},  # type 5
    'u_text_size_4': {'required': False},  # type 5
    'u_text_size_log_0': {'required': False},  # type 5
    'u_text_size_log_1': {'required': False},  # type 5
    'u_text_size_log_2': {'required': False},  # type 5
    'u_full_angle': {'required': False, 'type': 'boolean'},  # type 5
    'u_extra_angle': {'required': False, 'type': ['float', 'integer']},  # type 5
    'u_text_horizontal_align_center': {'required': False, 'type': 'boolean'},  # type 5
    'u_axis_color': {'required': False},  # type 5
    'u_text_color': {'required': False},  # type 5
    'v_values': {'required': False, 'type': 'list'},  # type 5
    'v_title': {'required': False, 'type': 'string'},  # type 5,
    'v_title_draw_center': {'required': False, 'type': 'boolean'},  # type 5,
    'v_title_distance_center': {'required': False, 'type': ['float', 'integer']},  # type 5
    'v_title_opposite_tick': {'required': False, 'type': 'boolean'},  # type 5
    # wd
    'wd_tag': {'required': False, 'type': 'string'},  # type 5
    'wd_title': {'required': False, 'type': 'string'},  # type 5
    'wd_title_x_shift': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_title_y_shift': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_scale_type': {'required': False, 'type': 'string', 'allowed': scale_type_strings},  # type 5
    'wd_tick_levels': {'required': False, 'type': 'integer'},  # type 5
    'wd_tick_text_levels': {'required': False, 'type': 'integer'},  # type 5
    'wd_tick_side': {'required': False, 'type': 'string', 'allowed': ['right', 'left']},  # type 5
    'wd_reference': {'required': False, 'type': 'boolean'},  # type 5
    'wd_title_draw_center': {'required': False, 'type': 'boolean'},  # type 5
    'wd_title_distance_center': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_title_opposite_tick': {'required': False, 'type': 'boolean'},  # type 5
    'wd_align_func': {'required': False, 'check_with': is_1_param_function},  # type 5
    'wd_align_x_offset': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_align_y_offset': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_text_format': {'required': False, 'type': 'string'},  # type 5
    'wd_extra_params': {'required': False, 'type': 'dict'},  # type 5
    'wd_text_distance_0': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_text_distance_1': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_text_distance_2': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_text_distance_3': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_text_distance_4': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_grid_length_0': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_grid_length_1': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_grid_length_2': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_grid_length_3': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_grid_length_4': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_text_size_0': {'required': False},  # type 5
    'wd_text_size_1': {'required': False},  # type 5
    'wd_text_size_2': {'required': False},  # type 5
    'wd_text_size_3': {'required': False},  # type 5
    'wd_text_size_4': {'required': False},  # type 5
    'wd_text_size_log_0': {'required': False},  # type 5
    'wd_text_size_log_1': {'required': False},  # type 5
    'wd_text_size_log_2': {'required': False},  # type 5
    'wd_full_angle': {'required': False, 'type': 'boolean'},  # type 5
    'wd_extra_angle': {'required': False, 'type': ['float', 'integer']},  # type 5
    'wd_text_horizontal_align_center': {'required': False, 'type': 'boolean'},  # type 5
    'wd_axis_color': {'required': False},  # type 5
    'wd_text_color': {'required': False},  # type 5
    'horizontal_guides': {'required': False, 'type': 'boolean'},  # type 5
    'vertical_guides': {'required': False, 'type': 'boolean'},  # type 5
    'vertical_guide_nr': {'required': False, 'type': 'boolean'},  # type 5
    'type': {'required': False,
             'type': 'string',
             'allowed': ['parallel', 'linear']
             },  # type 6
    'x_empty': {'required': False, 'type': ['float', 'integer']},  # type 6
    'y_empty': {'required': False, 'type': ['float', 'integer']},  # type 6
    'curve_const': {'required': False, 'type': ['float', 'integer']},  # type 6
    'ladder_color': {'required': False, 'type': ['float', 'integer']},  # type 6
    'angle_u': {'required': False, 'type': ['float', 'integer']},  # type 7
    'angle_v': {'required': False, 'type': ['float', 'integer']},  # type 7
    'transform_ini': {'required': False, 'type': 'boolean'},  # type 9
}

axis_schema = {
    'ID': {'required': False, 'type': 'string'},  # 'none',  # to identify the axis
    'tag': {'required': False, 'type': 'string'},  # 'none',  # for aligning block wrt others
    'dtag': {'required': False, 'type': 'string'},  # 'none',  # double alignment
    'u_min': {'required': True, 'type': ['float', 'integer']},  # 0.1,
    'u_max': {'required': True, 'type': ['float', 'integer']},  # 1.0,
    'u_min_trafo': {'required': False, 'type': ['float', 'integer']},  # type 9
    'u_max_trafo': {'required': False, 'type': ['float', 'integer']},  # type 9
    'F': {'required': False, 'check_with': is_1_param_function},  # lambda u: u,  # x-coordinate
    'G': {'required': False, 'check_with': is_1_param_function},  # lambda u: u, y-coordinate
    'f_grid': {'required': False, 'check_with': is_2_param_function},  #
    'title': {'required': False, 'type': 'string'},  # 'no title given',
    'title_x_shift': {'required': False, 'type': ['float', 'integer']},  # 0.0,
    'title_y_shift': {'required': False, 'type': ['float', 'integer']},  # 0.25,
    'scale_type': {'required': False, 'type': 'string', 'allowed': scale_type_strings},
    # 'linear',  # 'linear' 'log' 'manual point' 'manual line'
    'tick_levels': {'required': False, 'type': 'integer'},  # 10,
    'tick_text_levels': {'required': False, 'type': ['float', 'integer']},  # 10,
    'tick_side': {'required': False, 'type': 'string', 'allowed': ['right', 'left']},
    'reference': {'required': False, 'type': 'boolean'},  # False,
    'grid': {'required': False, 'type': 'boolean'},  # False,
    'reference_padding': {'required': False, 'type': ['float', 'integer']},
    # 0.20,  # fraction of reference line over other lines
    'manual_axis_data': {'required': False, 'type': 'dict'},  # {},
    'title_distance_center': {'required': False, 'type': ['float', 'integer']},  # 0.5,
    'title_opposite_tick': {'required': False, 'type': 'boolean'},  # True,
    'align_func': {'required': False, 'check_with': is_1_param_function},
    # lambda u: u,  # function to align different scalings
    'align_x_offset': {'required': False, 'type': ['float', 'integer']},  # 0.0,
    'align_y_offset': {'required': False, 'type': ['float', 'integer']},  # 0.0,
    'aligned': {'required': False, 'type': 'boolean'},  # False,
    'base_start': {'required': False, 'type': ['float', 'integer'], 'nullable': True},
    # None,
    'base_stop': {'required': False, 'type': ['float', 'integer'], 'nullable': True},
    # None,
    'scale_max': {'required': False, 'type': ['float', 'integer'], 'nullable': True},
    # None,
    'extra_params': {'required': False, 'type': 'list'},  # [],  # additional axis params
    'debug': {'required': False, 'type': 'boolean'},  # False,  # print dictionary
    'tick_distance_smart': {'required': False, 'type': ['float', 'integer']},  # 0.05,
    'full_angle': {'required': False, 'type': 'boolean'},  # False,
    'extra_angle': {'required': False, 'type': ['float', 'integer']},  # 0.0,
    'turn_relative': {'required': False, 'type': 'boolean'}  # False,
}
"""



# common axis params
# type 1 specific axis params
# type 2 specific axis params
# type 3 specific axis params
# type 4 specific axis params
# type 5 specific axis params
# type 6 specific axis params
# type 7 specific axis params
# type 8 specific axis params
# type 9 specific axis params


# main params




# print(block_validator.validate(my_profile))
# print(block_validator.errors)

# check main params
# for block in blocks:
#   check block params common
#   check block params specific
#   for axis in axes:
#       check axis params common
#       check axis params specific
