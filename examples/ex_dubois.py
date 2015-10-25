"""
    ex_dubois.py

    Body Surface Area (BSA) according to
    Du Bois & Du Bois, Arch Intern Med 1916;17:863:

    Body Surface Area = 0.007184* (Weight(kg)**0.425)*(Height(cm)**0.725)

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

# BSA (m2)
BSA_params = {
    'u_min': 0.6,
    'u_max': 3.0,
    'function': lambda u: -log(u / 0.007184),
    'title': r'BSA (m$^2$)',
    'tick_levels': 3,
    'tick_side': 'left',
    'tick_text_levels': 2,
    'scale_type': 'linear smart',
}

weight_params = {
    'tag': 'mass',
    'u_min': 15.0,
    'u_max': 200.0,
    'function': lambda u: log(u ** 0.425),
    'title': r'm (kg)',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'scale_type': 'linear smart',
    'title_x_shift': 0.8,
}

height_params = {
    'tag': 'height',
    'u_min': 75.0,
    'u_max': 220.0,
    'function': lambda u: log(u ** 0.725),
    'title': r'h (cm)',
    'tick_levels': 4,
    'tick_text_levels': 4,
    'tick_side': 'left',
    'title_x_shift': -0.8,
    'scale_type': 'linear smart',
}

block_1_params = {
    'block_type': 'type_1',
    'width': 10.0,
    'height': 10.0,
    'f2_params': BSA_params,
    'f1_params': weight_params,
    'f3_params': height_params,
    'isopleth_values': [[85, 'x', 183]]}

weight_params_lbs = {
    'tag': 'mass',
    'u_min': 15.0 * 2.2,
    'u_max': 200.0 * 2.2,
    'function': lambda u: log(u ** 0.425),
    'title': r'm (lbs)',
    'tick_levels': 4,
    'align_func': lambda u: u / 2.2,
    'tick_text_levels': 4,
    'tick_side': 'left',
    'scale_type': 'linear smart',
    'title_x_shift': -0.8,
}

block_2_params = {
    'block_type': 'type_8',
    'f_params': weight_params_lbs,
    'isopleth_values': [['x']]
}

height_params_inch = {
    'tag': 'height',
    'u_min': 75.0 / 2.54,
    'u_max': 220.0 / 2.54,
    'function': lambda u: log(u ** 0.725),
    'title': r'h (inch)',
    'tick_levels': 4,
    'align_func': lambda u: u * 2.54,
    'tick_text_levels': 4,
    'tick_side': 'right',
    'scale_type': 'linear smart',
    'title_x_shift': 0.8,
}

block_3_params = {
    'block_type': 'type_8',
    'f_params': height_params_inch,
    'isopleth_values': [['x']]
}

main_params = {
    'filename': 'ex_dubois.pdf',
    'paper_height': 20.0,
    'paper_width': 15.0,
    'block_params': [block_1_params, block_2_params, block_3_params],
    'transformations': [('rotate', 0.01), ('polygon',), ('scale paper',)],
    'title_str': r'Du Bois \& Du Bois:  $BSA = 0.007184 m^{0.425} h^{0.725}$'
}
Nomographer(main_params)
