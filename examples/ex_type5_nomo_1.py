"""
    ex_type5_nomo_1.py

    Simple nomogram of type 5.

    In this example: wd = u-v

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



block_params={
   'block_type':'type_5',
   'u_func':lambda u:u,
   'v_func':lambda x,v:x+v,
   'u_values':[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],
   'v_values':[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],
   'wd_tick_levels':2,
   'wd_tick_text_levels':1,
   'wd_tick_side':'right',
   'wd_title':'wd = u-v',
   'u_title':'u',
   'v_title':'v',
   'wd_title_opposite_tick':True,
   'wd_title_distance_center':2.5,
   'isopleth_values':[[6.5,7,'x']],
 }


main_params={
              'filename':'ex_type5_nomo_1.pdf',
              'paper_height':10.0,
              'paper_width':10.0,
              'block_params':[block_params],
              'transformations':[('rotate',0.01),('scale paper',)]
              }

Nomographer(main_params)
