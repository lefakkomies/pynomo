"""
    ex_second_order_eq.py

    Second order equation: z**2+p*z+q=0

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
        'u_min':-10.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$q$',
        'tick_levels':3,
        'tick_text_levels':2,
        'tick_side':'left'
                }

N_params_2={
        'u_min':-10.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$p$',
        'tick_levels':3,
        'tick_text_levels':2,
        'tick_side':'right',
                }

N_params_3={
        'u_min':0.0,
        'u_max':12.0,
        'function_3':lambda u:u,
        'function_4':lambda u:u**2,
        'title':r'$z$',
        'tick_levels':0,
        'tick_text_levels':0,
        'title_draw_center':True,
        'title_opposite_tick':False,
        'extra_params':[{'tick_side':'left',
                         'scale_type':'linear smart',
                         'u_min':0.1,
                         'u_max':12.0,
                         'tick_text_levels':4,
                         'tick_levels':4
                         }]
                }

block_1_params={
             'block_type':'type_10',
             'width':10.0,
             'height':10.0,
             'f1_params':N_params_1,
             'f2_params':N_params_2,
             'f3_params':N_params_3,
             'isopleth_values':[[2,-7,'x']]
             }

main_params={
              'filename':'ex_second_order_eq.pdf',
              'paper_height':10.0,
              'paper_width':10.0,
              'block_params':[block_1_params],
              'transformations':[('rotate',0.01),('scale paper',)],
              'title_str':r'$z^2+pz+q=0$'
              }
Nomographer(main_params)