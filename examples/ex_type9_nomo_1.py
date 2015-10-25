"""
    ex_type9_nomo_1.py

    Simple nomogram of type 9: determinant

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
            'u_min':3.0,
            'u_max':10.0,
            'f':lambda u:0,
            'g':lambda u:u,
            'h':lambda u:1.0,
            'title':r'$u_1$',
            'scale_type':'linear',
            'tick_levels':3,
            'tick_text_levels':2,
            'grid':False}

N_params_2={
        'u_min':0.0, # for alignment
        'u_max':1.0,  # for alignment
        'f_grid':lambda u,v:u+2.0,
        'g_grid':lambda u,v:2*v+5.0,
        'h_grid':lambda u,v:1.0,
        'u_start':0.0,
        'u_stop':1.0,
        'v_start':0.0,
        'v_stop':1.0,
        'u_values':[0.0,0.25,0.5,0.75,1.0],
        'v_values':[0.0,0.25,0.5,0.75,1.0],
        'grid':True,
        'text_prefix_u':r'$u_2$=',
        'text_prefix_v':r'$v_2$=',
        }

N_params_3={
            'u_min':3.0,
            'u_max':10.0,
            'f':lambda u:4.0,
            'g':lambda u:u,
            'h':lambda u:1.0,
            'title':r'$u_3$',
            'scale_type':'linear',
            'tick_levels':3,
            'tick_text_levels':2,
            'grid':False
            }

block_params={
             'block_type':'type_9',
             'f1_params':N_params_1,
             'f2_params':N_params_2,
             'f3_params':N_params_3,
             'transform_ini':False,
             'isopleth_values':[[7,[0.75,0.5],'x']]
             }

main_params={
              'filename':'ex_type9_nomo_1.pdf',
              'paper_height':10.0,
              'paper_width':10.0,
              'block_params':[block_params],
              'transformations':[('rotate',0.01),('scale paper',)]
              }
Nomographer(main_params)
