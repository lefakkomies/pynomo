#
#    LC_Filter.py
#
#    LC-filter example.
#
#    This file is part of PyNomo -
#    a program to create nomographs with Python (http://pynomo.sourceforge.net/)
#
#    Copyright (C) 2007-2015  Leif Roschier  <lefakkomies@users.sourceforge.net>
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

import sys

sys.path.insert(0, "..")
from pynomo.nomographer import Nomographer
from scipy.constants import mu_0
import pyx
import numpy as np

# python3 uses later PyX with different command to use latex.
if sys.version_info >= (3, 0):
    pyx.text.set(pyx.text.LatexRunner)  # assumes PyX > 14.0
    pyx.text.preamble(r"\usepackage[utf8]{inputenc}")  # latex preamble
else:
    pyx.text.set(mode="latex")  # assumes PyX 12.x


def v_func(x, v):
    R = np.exp(x) * 1e-3  # mm
    L = v * 1e-3  # mm
    return np.log(9.0 * R + 10.0 * L) - 2.0 * np.log(R)


L_min = 2.0
L_max = 20.0
R_min = 0.5
R_max = 20.0
u_min_value = np.exp(v_func(np.log(R_min), L_min))
u_max_value = np.exp(v_func(np.log(R_max), L_max))

block_params = {
    'block_type': 'type_5',
    'u_func': lambda u: np.log(u),
    'v_func': v_func,
    'u_values': [u_min_value, u_max_value],  #
    'u_manual_axis_data': {u_min_value: '',
                           u_max_value: ''},
    'v_values': [2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 30.0, 50.0, 100.0, 200.0, 300.0],  # L
    'wd_tick_levels': 5,
    'wd_tick_text_levels': 5,
    #'u_tick_text_levels': 0,  # not implemented
    'wd_tick_side': 'right',
    'wd_title': r'$R$ (mm)',
    'u_tag': 'AA',
    'manual_x_scale': True,
    'x_min': np.log(R_min),
    'x_max': np.log(R_max),
    'wd_func': lambda x: np.log(x),
    'wd_func_inv': lambda x: np.exp(x),
    'scale_type_wd': 'log smart',
    'u_title': '',
    'v_title': r'$l$ (mm)   ',
    'wd_title_opposite_tick': True,
    'wd_title_distance_center': 2.0,
    'isopleth_values': [['x', 10.0, 2.0]],
    'horizontal_guides': False,
    'vertical_guides': False,
    'width': 20,
    'scale_type_v': 'log smart',
    'allow_additional_v_scale': True,  # to get handle
    'v_scale_u_value': u_min_value,
    'v_tick_levels': 3,
    'v_tick_text_levels': 3,
    'v_min': 2.0,
    'v_max': 300.0,
    'x_func': lambda d, L: np.log((9.0 + np.sqrt(81.0 + 40.0 * d * L * 1e-3)) / (2.0 * d) * 1e3),
}

N_params_1 = {  # N
    'u_min': 1.0,
    'u_max': 10000.0,
    'function': lambda N: -2.0 * np.log(N) - np.log(10.0 * np.pi * mu_0),
    'title': r'$N$',
    'tick_levels': 4,
    'tick_text_levels': 4,
    'scale_type': 'log smart',
    'text_format': r"{%6.6g}",
    'tick_side': 'right',
}

N_params_2 = {  # dummy align
    'u_min': u_min_value,
    'u_max': u_max_value,
    'function': lambda y: np.log(y),  # *1e6
    'title': r'',
    'tick_levels': 0,
    'tick_text_levels': 0,
    'scale_type': 'linear',
    'tag': 'AA',
}

N_params_3 = {  # L
    'u_min': 0.01,
    'u_max': 100000.0,
    'function': lambda ind: np.log(ind * 1e-6),
    'title': r'$L$ ($\mu$H)',
    'tick_levels': 4,
    'tick_text_levels': 4,
    'scale_type': 'log smart',
    'tick_side': 'left',
    'text_format': r"$%6.6g$ ",
    'tag': 'L',
}

block_1_params = {  # inductance from N and contour
    'block_type': 'type_1',
    'width': 4.0,
    'height': 15.0,
    'f1_params': N_params_3,
    'f2_params': N_params_1,
    'f3_params': N_params_2,
    'proportion': 0.5,
    'isopleth_values': [['x', 'x', 'x']],
}

# f(L,C)
N_params_1a = {
    'u_min': 0.1,
    'u_max': 100000.0,
    'function': lambda ind: np.log(ind * 1e-6),
    'title': r'$L$ ($\mu$H)',
    'tick_levels': 4,
    'tick_text_levels': 4,
    'scale_type': 'log smart',
    'tick_side': 'left',
    'text_format': r"$%6.6g$ ",
    # 'tag':'L',
    'dtag': 'L',
}

N_params_2a = {
    'u_min': 0.1,
    'u_max': 10000.0,
    'function': lambda f: 2.0 * np.log(3.1415 * f * 1e3),
    'title': r'$f$ (kHz)',
    'tick_levels': 5,
    'tick_text_levels': 5,
    'scale_type': 'log smart',
    'tick_side': 'left',
    'text_format': r"$%6.6g$ ",
}

N_params_3a = {
    'u_min': 1.0,
    'u_max': 10000.0,
    'function': lambda c: np.log(c * 1e-9),
    'title': r'$C$ (nF)',
    'tick_levels': 4,
    'tick_text_levels': 4,
    'scale_type': 'log smart',
    'text_format': r"$%6.6g$ ",
    'tag': 'C',
}

block_1_params_a = {
    'block_type': 'type_1',
    'width': 10.0,
    'height': 15.0,
    'f1_params': N_params_1a,  # L
    'f2_params': N_params_2a,  # f
    'f3_params': N_params_3a,  # C
    'isopleth_values': [['x', 'x', 'x']],
    'mirror_x': True,
}

## R = sqrt(L/C)
N_params_1b = {  # L
    'u_min': 0.1,
    'u_max': 100000.0,
    'function': lambda ind: -np.log(ind * 1e-6),
    'title': r'$L$ ($\mu$H)',
    'tick_levels': 4,
    'tick_text_levels': 4,
    'scale_type': 'log smart',
    'tick_side': 'left',
    'text_format': r"$%6.6g$ ",
    'tag': 'L',
    'dtag': 'L',
}

N_params_2b = {  # R
    'u_min': 10.0,
    'u_max': 400.0,
    'function': lambda R: 2.0 * np.log(R),
    'title': r'$R$ ($\Omega$)',
    'tick_levels': 5,
    'tick_text_levels': 5,
    'tick_side': 'right',
    'scale_type': 'log smart',
}

N_params_3b = {  # C
    'u_min': 1.0,
    'u_max': 10000.0,
    'function': lambda c: np.log(c * 1e-9),
    'title': r'$C$ (nF)',
    'tick_levels': 4,
    'tick_text_levels': 4,
    'scale_type': 'log smart',
    'text_format': r"$%6.6g$ ",
    'tag': 'C',
}

block_1_params_b = {
    'block_type': 'type_1',
    'width': 15.5,
    'height': 15.0,
    'f1_params': N_params_2b,  # R
    'f2_params': N_params_1b,  # L
    'f3_params': N_params_3b,  # C
    'proportion': 1.4,
    'isopleth_values': [[50.0, 'x', 40.0]],
    'mirror_x': True,
}

main_params = {
    'filename': 'LC_filter.pdf',
    'paper_height': 15.0,
    'paper_width': 25.0,
    'block_params': [block_1_params, block_params, block_1_params_b, block_1_params_a],
    'transformations': [('rotate', 0.01), ('scale paper',)],
    'extra_texts': [{'x': 17.0,
                     'y': 13.0,
                     'text': r'$L = \frac{10 \pi \mu_0 N^2 R^2}{9R+10l}$ \par $f = \frac{1}{\pi \sqrt{LC}}$ \par $R = \sqrt{\frac{L}{C}}$',
                     'width': 7,
                     'pyx_extra_defs': [pyx.text.size.Large]
                     }],
}

Nomographer(main_params)
