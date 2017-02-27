"""
    ex_rfset.py

    Sensitivity of radio-frequency single electron transistor (RF-SET).

    Copyright (C) 2007-2015  Leif Roschier
    Copyright (C) 2017       Jonas Stein

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
R_sigma = 60e3
Z_tr = 800.0
t = 0.2
k_b = 1.3806504e-23
T_0 = 4.0
Z_T = 50.0
E_C = 2.0 * k_b
e = 1.3806504e-19
T = t * E_C / k_b

d_q = 2.0 * (3.0 * R_sigma / Z_tr + Z_tr / Z_T) * sqrt(k_b * T_0 * Z_T) / \
    (2.0 * 0.41 * t ** (-1.74) * 0.9 * E_C / e ** 2) / e


def f_dq(q):
    return -log(q * 1e-6) - 14.0  # additional const for helping scale alignment


def f_t0(t0):
    return 0.5 * log(k_b * t0 * Z_T) + 14.0  # additional const for helping scale alignment


def f_ec(ec):  # [K]
    return -log(0.9 * (k_b * ec) ** 2.74) - 150.0  # additional const for helping scale alignment


def f_t(t):
    return -log(0.41 * (k_b * t) ** -1.74 / e) + 150.0  # additional const for helping scale alignment


def f_rs(rs):
    return rs * 1e3


def f_ztr(x, ztr):
    return (exp(x) - ztr / Z_T) * ztr / 3.0


block_contour_params = {
    'width': 10.0,
    'height': 5.0,
    'block_type': 'type_5',
    'u_func': f_rs,
    'v_func': f_ztr,
    'u_values': [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0],
    'v_values': [100.0, 200.0, 400.0, 800.0, 1600.0],
    'wd_tag': 'AA',
    'u_title': '$R_\Sigma (k\Omega )$',
    'v_title': r'$Z_{TR}$',
    'v_text_format': r"$%3.0f \Omega$ ",
    'u_text_format': r"$%3.0f$ ",
    'mirror_y': False,
    'wd_tick_levels': 0,
    'wd_tick_text_levels': 0,
    'isopleth_values': [[R_sigma / 1e3, Z_tr, 'x']]
}

# this is non-obvious trick to find bottom edge coordinates of the grid in order
# to align it with N nomogram
block1_dummy = Nomo_Block_Type_5(mirror_x=False)
block1_dummy.define_block(block_contour_params)
block1_dummy.set_block()

x_params = {
    'u_min': block1_dummy.grid_box.params_wd['u_min'],
    'u_max': block1_dummy.grid_box.params_wd['u_max'],
    'function': lambda u: u,
    'title': '',
    'tag': 'AA',
    'tick_side': 'right',
    'reference': False,
    'tick_levels': 0,
    'tick_text_levels': 0,
    'title_draw_center': True,
    'text_format': r"$%3.2f$ "
}

N_params_1 = {
    'u_min': 0.5,
    'u_max': 20.0,
    'function': f_ec,
    'title': r'$E_C (K)$',
    'tick_levels': 4,
    'tick_text_levels': 4,
    'scale_type': 'log smart',
}
N_params_2 = {
    'u_min': 0.1,
    'u_max': 20.0,
    'function': f_t,
    'title': r'$T (K)$',
    'tick_levels': 4,
    'tick_text_levels': 4,
    'scale_type': 'log smart',
}
N_params_3 = {
    'u_min': 0.5,
    'u_max': 100.0,
    'function': f_dq,
    'title': r'$\delta q (\mu e/\sqrt{Hz})$',
    'tick_levels': 4,
    'tick_text_levels': 4,
    'scale_type': 'log smart',
}
N_params_4 = {
    'u_min': 0.1,
    'u_max': 20.0,
    'function': f_t0,
    'title': r'$T_0 (K)$',
    'tick_levels': 4,
    'tick_text_levels': 4,
    'scale_type': 'log smart',
}

block_1_params = {
    'block_type': 'type_3',
    'width': 5.0,
    'height': 10.0,
    'mirror_x': True,
    'reference_padding': 0.0,
    'f_params': [N_params_1, N_params_2, N_params_3,
                 N_params_4, x_params],
    'isopleth_values': [[E_C / k_b, T, 'x', T_0, 'x']]
}

main_params = {
    'filename': 'ex_rfset.pdf',
    'paper_height': 20.0,
    'paper_width': 20.0,
    'block_params': [block_1_params, block_contour_params],
    'transformations': [('rotate', -0.01), ('scale paper',)],
    'title_str': r''
}
Nomographer(main_params)
