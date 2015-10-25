"""
    ex_type4_nomo_1.py

    Simple nomogram of type 4: F1/F2=F3/F4

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
        'title':r'$u_1$',
        'tick_levels':3,
        'tick_text_levels':1,
        'tick_side':'left',
                }
N_params_2={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$u_2$',
        'tick_levels':3,
        'tick_text_levels':1,
        'tick_side':'right',
                }
N_params_3={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$u_3$',
        'tick_levels':3,
        'tick_text_levels':1,
        'tick_side':'right',
        'title_draw_center':True,
        'title_opposite_tick':False,
                }
N_params_4={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$u_4$',
        'tick_levels':3,
        'tick_text_levels':1,
        'tick_side':'left',
        'title_draw_center':True,
        'title_opposite_tick':False,
                }

block_1_params={
                'block_type':'type_4',
                'f1_params':N_params_1,
                'f2_params':N_params_2,
                'f3_params':N_params_3,
                'f4_params':N_params_4,
                'isopleth_values':[[7,6,2,'x']],
                             }

main_params={
              'filename':'ex_type4_nomo_1.pdf',
              'paper_height':10.0,
              'paper_width':10.0,
              'block_params':[block_1_params],
              'transformations':[('rotate',0.01),('scale paper',)],
              'title_str':r'$u_1/u_2=u_3/u_4$',
              'title_y':8.0,
              }
Nomographer(main_params)
