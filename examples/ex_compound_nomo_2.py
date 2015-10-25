"""
    ex_compound_nomo_2.py

    Compound nomograph: q = u**v+w

    Copyright (C) 2007-2009  Leif Roschier

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

sys.path.insert(0, "..")
from pynomo.nomographer import *

# N
u_params = {
    'u_min': 1.0,
    'u_max': 10.0,
    'function': lambda u: log(u),
    'title': r'$u$',
    'tick_levels': 4,
    'tick_text_levels': 3,
    'tick_side': 'left',
    'scale_type': 'linear smart',
}

v_params = {
    'u_min': 0.1,
    'u_max': 20.0,
    'function': lambda v: 1.0 / v,
    'title': r'$v$',
    'scale_type': 'log',
    'tick_levels': 0,
    'tick_text_levels': 0,
    'extra_params': [{
        'u_min': 0.1,
        'u_max': 0.9,
        'tick_levels': 3,
        'tick_text_levels': 2,
        'tick_side': 'left'
    },
        {
            'u_min': 1.0,
            'u_max': 20.0,
            'tick_levels': 4,
            'tick_text_levels': 2,
            'tick_side': 'right'
        }
    ]
}

R_params = {
    'u_min': 1.0,
    'u_max': 10.0,
    'function': lambda r: log(r),
    'title': r'',
    'tick_levels': 0,
    'tick_text_levels': 0,
    'tag': 'ra',
}

block_params_1 = {
    'block_type': 'type_2',
    'width': 10.0,
    'height': 10.0,
    'f1_params': u_params,
    'f2_params': v_params,
    'f3_params': R_params,
    'isopleth_values': [[6, 0.5, 'x']]
}
# Ladder
R_params_a = {
    'u_min': 1.0,
    'u_max': 10.0,
    'function': lambda u: log(u),
    'title': 'r',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'tick_side': 'left',
    'tag': 'ra',
}

R_params_b = {
    'u_min': 0.0,
    'u_max': 10.0,
    'function': lambda u: u,
    'title': 'r',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'tag': 'rb'
}

block_params_2 = {
    'block_type': 'type_6',
    'f1_params': R_params_a,
    'f2_params': R_params_b,
    'width': 5.0,
    'height': 10.0,
    'mirror_x': True,
    'isopleth_values': [['x', 'x']]
}
# type 1: q-w-r=0
r_params_c = {
    'u_min': 0.0,
    'u_max': 10.0,
    'function': lambda u: -u,
    'title': r'$r$',
    'tick_levels': 2,
    'tick_text_levels': 1,
    'tag': 'rb'
}

w_params = {
    'u_min': -10.0,
    'u_max': 10.0,
    'function': lambda u: -u,
    'title': r'$w$',
    'tick_levels': 3,
    'tick_text_levels': 1,
}

q_params = {
    'u_min': 0.0,
    'u_max': 10.0,
    'function': lambda u: u,
    'title': r'$q$',
    'tick_levels': 3,
    'tick_text_levels': 1,
}

block_params_3 = {
    'block_type': 'type_1',
    'width': 10.0,
    'height': 10.0,
    'f1_params': r_params_c,
    'f2_params': w_params,
    'f3_params': q_params,
    'mirror_x': False,
    'isopleth_values': [['x', 3, 'x']]
}

main_params = {
    'filename': 'ex_compound_nomo_2.pdf',
    'paper_height': 13.0,
    'paper_width': 20.0,
    'block_params': [block_params_1, block_params_2, block_params_3],
    'transformations': [('rotate', 0.01), ('scale paper',)],
}
Nomographer(main_params)
