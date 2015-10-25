"""
    ex_compound_nomo_1.py

    Compound nomograph: (A+B)/E=F/(CD)

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

# type 1
A_params={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$A$',
        'tick_levels':2,
        'tick_text_levels':1,
                }

B_params={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$B$',
        'tick_levels':2,
        'tick_text_levels':1,
                }

R1a_params={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:-u,
        'title':'',
        'tick_levels':0,
        'tick_text_levels':0,
        'tag':'r1'
                }
block_1_params={
             'block_type':'type_1',
             'width':10.0,
             'height':10.0,
             'f1_params':A_params,
             'f2_params':B_params,
             'f3_params':R1a_params,
             'isopleth_values':[[1,7,'x']]
             }
# type 4
R1b_params={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$R_1$',
        'tick_levels':0,
        'tick_text_levels':0,
        'tick_side':'right',
        'title_draw_center':True,
        'title_opposite_tick':False,
        'tag':'r1'
                }
E_params={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$E$',
        'tick_levels':3,
        'tick_text_levels':1,
        'tick_side':'right',
        'title_draw_center':True,
        'title_opposite_tick':False,
                }
F_params={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$F$',
        'tick_levels':3,
        'tick_text_levels':1,
        'tick_side':'left',
        'title_draw_center':True,
        'title_opposite_tick':True,
                }
R2a_params={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$R_2$',
        'tick_levels':0,
        'tick_text_levels':0,
        'tick_side':'left',
        'title_draw_center':True,
        'title_opposite_tick':False,
        'tag':'r2'
                }

block_2_params={
                'block_type':'type_4',
                'f1_params':R1b_params,
                'f2_params':E_params,
                'f3_params':F_params,
                'f4_params':R2a_params,
                'mirror_x':True,
                'isopleth_values':[['x',9,4,'x']]
                             }
# type 2 N
R2b_params={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$$',
        'tick_levels':0,
        'tick_text_levels':0,
        'tag':'r2'
                }

C_params={
        'u_min':0.5,
        'u_max':5.0,
        'function':lambda u:u,
        'title':r'$C$',
        'tick_levels':3,
        'tick_text_levels':1,
        'tick_side':'left',
        'scale_type':'linear smart',
                }

D_params={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$D$',
        'tick_levels':3,
        'tick_text_levels':1,
                }

block_3_params={
             'block_type':'type_2',
             'width':10.0,
             'height':10.0,
             'f1_params':R2b_params,
             'f2_params':C_params,
             'f3_params':D_params,
             'mirror_y':True,
             'isopleth_values':[['x',1,'x']]
             }

main_params={
              'filename':'ex_compound_nomo_1.pdf',
              'paper_height':10.0,
              'paper_width':10.0,
              'block_params':[block_1_params,block_2_params,block_3_params],
              'transformations':[('rotate',0.01),('scale paper',)],
              }
Nomographer(main_params)
