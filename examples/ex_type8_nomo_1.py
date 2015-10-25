"""
    ex_type8_nomo_1.py

    Simple nomogram of type 8.

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

N_params_1={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':'u',
        'tick_levels':3,
        'tick_text_levels':2,
        'tick_side':'left',
        }

block_params={
              'block_type':'type_8',
              'f_params':N_params_1,
              'width':5.0,
              'height':10.0,
              'isopleth_values':[[5]]
                     }

main_params={
              'filename':'ex_type8_nomo_1.pdf',
              'paper_height':10.0,
              'paper_width':5.0,
              'block_params':[block_params],
              'transformations':[]
              }

Nomographer(main_params)
