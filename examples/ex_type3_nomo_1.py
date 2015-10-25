"""
    ex_type3_nomo_1.py

    Simple nomogram of type 3: F1+F2+...+FN=0

    This example has N=6: F1+F2+F3+F4+F5+F6=0

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
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$u_1$',
        'tick_levels':2,
        'tick_text_levels':1,
                }
N_params_2={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$u_2$',
        'tick_levels':2,
        'tick_text_levels':1,
                }
N_params_3={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$u_3$',
        'tick_levels':2,
        'tick_text_levels':1,
                }
N_params_4={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$u_4$',
        'tick_levels':2,
        'tick_text_levels':1,
                }
N_params_5={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$u_5$',
        'tick_levels':2,
        'tick_text_levels':1,
                }
N_params_6={
        'u_min':-20.0,
        'u_max':0.0,
        'function':lambda u:u,
        'title':r'$u_6$',
        'tick_levels':2,
        'tick_text_levels':1,
        'tick_side':'right',
                }

block_1_params={
             'block_type':'type_3',
             'width':10.0,
             'height':10.0,
             'f_params':[N_params_1,N_params_2,N_params_3,
                         N_params_4,N_params_5,N_params_6],
             'isopleth_values':[[3,2,1,0,3,'x']],
             }

main_params={
              'filename':'ex_type3_nomo_1.pdf',
              'paper_height':20.0,
              'paper_width':20.0,
              'block_params':[block_1_params],
              'transformations':[('rotate',0.01),('scale paper',)],
              'title_str':r'$u_1+u_2+u_3+u_4+u_5+u_6=0$',
              'title_y':21.0,
              }
Nomographer(main_params)
