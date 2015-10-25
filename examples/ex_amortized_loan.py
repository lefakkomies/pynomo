"""
    ex_amortized_loan.py

    Amortized loan calculator

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

# Type 5 contour
def f1(x,u):
    return log(log(x/(x-u/(100.0*12.0)))/log(1+u/(100.0*12.0)))

block_1_params={
            'width':10.0,
           'height':5.0,
           'block_type':'type_5',
           'u_func':lambda u:log(u*12.0),
           'v_func':f1,
           'u_values':[10.0,11.0,12.0,13.0,14.0,15.0,20.0,25.0,30.0,40.0,50.0,60.0],
           'v_values':[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],
           'wd_tag':'A',
           'u_title':'years',
           'v_title':r'interest rate = ',
           'u_text_format':r"$%3.0f$ ",
           'v_text_format':r"$%3.0f$ \%% ",
           'isopleth_values':[[21,5,'x']]
             }

# this is non-obvious trick to find bottom edge coordinates of the grid in order
# to align it with N nomogram
block1_dummy=Nomo_Block_Type_5(mirror_x=False)
block1_dummy.define_block(block_1_params)
block1_dummy.set_block()

# Let's define the N-nomogram
N_params_3={
        'u_min':block1_dummy.grid_box.params_wd['u_min'],
        'u_max':block1_dummy.grid_box.params_wd['u_max'],
        'function':lambda u:u,
        'title':'',
        'tag':'A',
        'tick_side':'right',
        'tick_levels':2,
        'tick_text_levels':2,
        'reference':False,
        'tick_levels':0,
        'tick_text_levels':0,
        'title_draw_center':True
                }
N_params_2={
        'u_min':30.0,
        'u_max':1000.0,
        'function':lambda u:u,
        'title':'Loan',
        'tag':'none',
        'tick_side':'left',
        'tick_levels':4,
        'tick_text_levels':3,
        'title_draw_center':True,
        #'text_format':r"$%3.0f$ ",
        'scale_type':'linear smart',
                }
N_params_1={
        'u_min':0.2,
        'u_max':3.0,
        'function':lambda u:u,
        'title':'monthly payment',
        'tag':'none',
        'tick_side':'right',
        'tick_levels':3,
        'tick_text_levels':2,
        'title_draw_center':True
                }

block_2_params={
             'block_type':'type_2',
             'width':10.0,
             'height':20.0,
             'f1_params':N_params_1,
             'f2_params':N_params_2,
             'f3_params':N_params_3,
             'isopleth_values':[['x',200,'x']]
             }

main_params={
              'filename':'amortized_loan.pdf',
              'paper_height':20.0,
              'paper_width':20.0,
              'block_params':[block_1_params,block_2_params],
              'transformations':[('rotate',0.01),('scale paper',)],
                'title_str':r'Amortized loan calculator    \copyright    Leif Roschier  2009',
                'title_x': 17,
                'title_y': 21,
                'title_box_width': 5
              }
Nomographer(main_params)
