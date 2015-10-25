"""
    ex_isopleth_1.py

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
        'u_max':6.0,
        'function':lambda u:u**2,
        'title':r'$u_1$',
        'tick_levels':1,
        'tick_text_levels':1,
        'scale_type':'linear smart',
        'tick_side':'left',
                }

N_params_2={
        'u_min':0.0,
        'u_max':8.0,
        'function':lambda u:-u**2,
        'title':r'$u_2$',
        'tick_levels':1,
        'tick_text_levels':1,
        'scale_type':'linear smart',
                }

N_params_3={
        'u_min':0.0,
        'u_max':6.0,
        'function':lambda u:u**2,
        'title':r'$u_3$',
        'tick_levels':1,
        'tick_text_levels':1,
        'scale_type':'linear smart',
                }

block_1_params={
             'block_type':'type_1',
             'width':10.0,
             'height':10.0,
             'f1_params':N_params_1,
             'f2_params':N_params_2,
             'f3_params':N_params_3,
             'isopleth_values':[[1,'x',1],[2,'x',2],[3,'x',3],[3,'x',4],[4,'z',3],
                                [4,'unknown',5],[5,'x',3],[5,'x',4],[6,'cat',4],
                                [5,'known?',6],[3,'x',5],[6,'x',5],[4,'dog',6]],
             }

main_params={
              'filename':'ex_isopleth_1.pdf',
              'paper_height':10.0,
              'paper_width':10.0,
              'block_params':[block_1_params],
              'transformations':[('rotate',0.01),('scale paper',)],
              'title_str':r'$u_1^2-u_2^2+u_3^2=0$',
              'isopleth_params':[{'color':'Orange',
                                  'linewidth':'thin',
                                  'linestyle':'solid'},
                                  {'color':'VioletRed',
                                  'linewidth':'THICK',
                                  'linestyle':'solid'},
                                  {'color':'Fuchsia',
                                  'linewidth':'normal',
                                  'linestyle':'solid'},
                                  {'color':'Sepia',
                                  'linewidth':'THin',
                                  'linestyle':'dashed'},
                                  {'color':'Tan',
                                  'linewidth':'THick',
                                  'linestyle':'dashed'},
                                  {'color':'Orchid',
                                  'linewidth':'THIn',
                                  'linestyle':'dashed'},
                                  {'color':'Lavender',
                                  'linewidth':'THIck',
                                  'linestyle':'dotted'},
                                  {'color':'Rhodamine',
                                  'linewidth':'thin',
                                  'linestyle':'dotted'},
                                  {'color':'Bittersweet',
                                  'linewidth':'normal',
                                  'linestyle':'dashdotted'},
                                  {'color':'BrickRed',
                                  'linewidth':'THICK',
                                  'linestyle':'dashdotted',
                                  'circle_size':0.5},
                                  {'color':'Periwinkle',
                                  'linewidth':'THIN',
                                  'linestyle':'dashdotted'},
                                  {'color':'MidnightBlue',
                                  'linewidth':'THICK',
                                  'linestyle':'dashdotted',
                                  'transparency':0.2},
                                  {'color':'Orange',
                                  'linewidth':'THIN',
                                  'linestyle':'dashdotted',
                                  'transparency':0.9}]
              }
Nomographer(main_params)