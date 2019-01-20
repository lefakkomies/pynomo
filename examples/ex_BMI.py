"""
    ex_BMI.py

    Body mass index BMI = w(kg) / h(m)**2

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
from pynomo.nomographer import Nomographer

N_params_1 = {
    'u_min': 1.40,
    'u_max': 2.2,
    'function': lambda u: u ** 2,
    'title': r'(feet)  height (m)',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'tag': 'height',
    # 'title_x_shift':0.8,
}

N_params_2 = {
    'u_min': 15.0,
    'u_max': 55.0,
    'function': lambda u: 1.0 / u,
    'title': r'BMI',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'tick_side': 'left',
    'title_draw_center': True,
    'title_opposite_tick': False,
}

N_params_3 = {
    'u_min': 30.0,
    'u_max': 200.0,
    'function': lambda u: u,
    'title': r'(lbs)  weight (kg)',
    'tick_levels': 3,
    'tick_text_levels': 1,
    'tag': 'mass',
    # 'title_x_shift':0.8,
}

block_1_params = {
    'block_type': 'type_2',
    'width': 10.0,
    'height': 10.0,
    'f1_params': N_params_1,
    'f2_params': N_params_2,
    'f3_params': N_params_3,
    'isopleth_values': [[1.84, 'x', 85]]
}

weight_params_lbs = {
    'tag': 'mass',
    'u_min': 30.0 * 2.2,
    'u_max': 200.0 * 2.2,
    'function': lambda u: u,
    # 'title':r'm (lbs)',
    'tick_levels': 3,
    'align_func': lambda u: u / 2.2,
    'tick_text_levels': 2,
    'tick_side': 'left',
    'scale_type': 'linear',
    'title_x_shift': -0.8,
}

block_2_params = {
    'block_type': 'type_8',
    'f_params': weight_params_lbs,
    'isopleth_values': [['x']]
}

height_params_inch = {
    'tag': 'height',
    'u_min': 140.0 / (2.54 * 12),
    'u_max': 220.0 / (2.54 * 12),
    'function': lambda u: u ** 2,
    # 'title':r'h (inch)',
    'tick_levels': 2,
    'align_func': lambda u: u / 100.0 * 2.54 * 12,
    'tick_text_levels': 1,
    'tick_side': 'right',
    'scale_type': 'linear',
    'title_x_shift': -0.8,
    'tick_side': 'left',
}

block_3_params = {
    'block_type': 'type_8',
    'f_params': height_params_inch,
    'isopleth_values': [['x']]
}

main_params = {
    'filename': 'ex_BMI.pdf',
    'paper_height': 12.0,
    'paper_width': 8.0,
    'block_params': [block_1_params, block_2_params, block_3_params],
    'transformations': [('rotate', 0.01), ('scale paper',)],
    'title_str': r"Body mass index $BMI=W($kg$)/H($m$)^2$"
}
Nomographer(main_params)
