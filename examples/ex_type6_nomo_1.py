"""
    ex_type6_nomo_1.py

    Simple nomogram of type 6.

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
        'function':lambda u:u**0.5,
        'title':'u',
        'tick_levels':3,
        'tick_text_levels':2,
        'tick_side':'left',
        }

N_params_2={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:log(u),
        'title':'u',
        'tick_levels':3,
        'tick_text_levels':2,
        }

block_params={
              'block_type':'type_6',
              'f1_params':N_params_1,
              'f2_params':N_params_2,
              'width':5.0,
              'height':10.0,
              'isopleth_values':[[2.2,'x']],
              #'curve_const':0.01
                     }

main_params={
              'filename':'ex_type6_nomo_1.pdf',
              'paper_height':10.0,
              'paper_width':5.0,
              'block_params':[block_params],
              'transformations':[('rotate',0.01),('scale paper',)]
              }

Nomographer(main_params)
