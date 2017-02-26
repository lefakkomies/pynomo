"""
    ex_isopleth_2.py

    Copyright (C) 2007-2009  Leif Roschier
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
from pynomo.nomographer import *

isopleth_value_list = []
color_list = []
for number1 in range(1, 11):
    for number2 in range(1, 11):
        # for number1 in arange(1,10.2,0.2):
        #    for number2 in arange(1,10.2,0.2):
        isopleth_value_list.append([number1 * number2, number1, number2])
        color_list.append({'color_cmyk': [(number1 * number2) / 100.0, number1 / 10.0, number2 / 10.0, 0.1],
                           'linestyle': 'solid',
                           'transparency': 0.5})

N_params_1 = {
    'u_min': 1.0,
    'u_max': 100.0,
    'function': lambda u: u,
    'title': r'$u_1$',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'scale_type': 'linear smart',
    'tick_side': 'left',
}

N_params_2 = {
    'u_min': 1.0,
    'u_max': 10.0,
    'function': lambda u: u,
    'title': r'$u_2$',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'scale_type': 'linear smart'
}

N_params_3 = {
    'u_min': 1.0,
    'u_max': 10.0,
    'function': lambda u: u,
    'title': r'$u_3$',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'scale_type': 'linear smart'
}

block_1_params = {
    'block_type': 'type_2',
    'width': 10.0,
    'height': 10.0,
    'f1_params': N_params_1,
    'f2_params': N_params_2,
    'f3_params': N_params_3,
    'isopleth_values': isopleth_value_list,
}

main_params = {
    'filename': 'ex_isopleth_2.pdf',
    'paper_height': 10.0,
    'paper_width': 10.0,
    'block_params': [block_1_params],
    'transformations': [('rotate', 0.01), ('scale paper',)],
    'title_str': r'$u_1=u_2\times u_3$',
    'isopleth_params': color_list,
}
Nomographer(main_params)
