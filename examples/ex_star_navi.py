"""
    ex_star_navi.py

    Star navigation.

    Equation: cos(a) = (sin(d)-sin(b)sin(h))/(cos(b)cos(h))

    Copyright (C) 2007-2015  Leif Roschier

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
from pynomo.nomo_wrapper import *
from pynomo.nomographer import *

# for testing
d = 40.0 * pi / 180.0
h = 30.0 * pi / 180.0
b = 60.0 * pi / 180.0
# print acos((sin(d)-sin(b)*sin(h))/(cos(b)*cos(h)))*180.0/pi
# print arange(0.0,40.0,1.0,dtype=double).tolist()

a_params = {
    'u_min': 0.0,
    'u_max': 90.0,
    'f': lambda u: 1,
    'g': lambda u: -cos(u * pi / 180.0),
    'h': lambda u: -1.0,
    'title': 'a',
    'title_x_shift': 0.0,
    'title_y_shift': 0.25,
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 5,
    'tick_side': 'right',
    'tag': 'none',
    'grid': False,
}

d_params = {
    'u_min': 0.0,
    'u_max': 90.0,
    'f': lambda u: 0.0,
    'g': lambda u: -sin(u * pi / 180.0),
    'h': lambda u: 1.0,
    'title': 'd',
    'title_x_shift': 0.0,
    'title_y_shift': 0.25,
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 5,
    'tick_side': 'right',
    'tag': 'none',
    'grid': False,
}

bh_params = {
    'ID': 'none',  # to identify the axis
    'tag': 'none',  # for aligning block wrt others
    'title': 'Grid',
    'title_x_shift': 0.0,
    'title_y_shift': 0.25,
    'title_distance_center': 0.5,
    'title_opposite_tick': True,
    'u_min': 0.0,  # for alignment
    'u_max': 1.0,  # for alignment
    'f_grid': lambda u, v: -cos(u * pi / 180.0) * cos(v * pi / 180.0),
    'g_grid': lambda u, v: -sin(u * pi / 180.0) * sin(v * pi / 180.0),
    'h_grid': lambda u, v: 1.0 + cos(u * pi / 180.0) * cos(v * pi / 180.0),
    'u_start': 0.0,
    'u_stop': 90.0,
    'v_start': 0.0,
    'v_stop': 90.0,
    'u_values': [0.0, 15.0, 30.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0],
    'v_values': [0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 85.0],
    'grid': True,
    'text_prefix_u': r'',
    'text_prefix_v': r'',
    'text_distance': 0.5,
    'v_texts_u_start': True,
    'v_texts_u_stop': False,
    'u_texts_v_start': True,
    'u_texts_v_stop': False,
    'extra_params': [{
        'u_start': 0.0,
        'u_stop': 40.0,
        'v_start': 60.0,
        'v_stop': 89.9,
        'u_values': arange(0.0, 41.0, 1.0, dtype=double).tolist(),
        'v_values': arange(60.0, 91.0, 1.0, dtype=double).tolist(),
        'v_texts_u_start': False,
        'v_texts_u_stop': False,
        'u_texts_v_start': False,
        'u_texts_v_stop': False,
        'u_line_color': color.cmyk.Sepia,
        'v_line_color': color.cmyk.Sepia,
    }
    ]
}

block_params = {
    'block_type': 'type_9',
    'f1_params': a_params,
    'f2_params': bh_params,
    'f3_params': d_params,
    'transform_ini': False,
    'isopleth_values': [[50, [75, 15], 'x']]
}

main_params = {
    'filename': 'ex_star_navi.pdf',
    'paper_height': 20.0,
    'paper_width': 20.0,
    'block_params': [block_params],
    'transformations': [('rotate', 0.01), ('polygon',), ('scale paper',)]
}
b = Nomographer(main_params)
