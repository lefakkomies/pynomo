#!/usr/bin/env python3

# nomogen example program

import sys
import math

import inspect
import os

sys.path.insert(0, "..")

from nomogen import Nomogen
from pynomo.nomographer import Nomographer

# get current file name
myfile = os.path.basename(inspect.stack()[0][1]).replace(".py", "")

# alternative with no external dependencies - it works most of the time
#  myfile =  __name__ == "__main__" and (__file__.endswith(".py") and __file__.replace(".py", "") or "nomogen")
#             or __name__,



########################################
#
#  this is the target function,
#  - the limits of the variables
#  - the function that the nonogram implements
#
#  format is m = m(l,r), where l, m & r are respectively the values
#                        for the left, middle & right hand axes
########################################


# simple example
def sq(u, v):
    return 1/math.hypot(u, v)
#    return 1/(u*u * v*v) / 2  # FIXME: drawing scale bug
#    return (u*u * v*v) / 2  # FIXME: drawing scale bug


umin = 2
umax = 10
vmin = 2
vmax = 10
wmin = sq(umax, vmax)
wmax = sq(umin, vmin)

###############################################################
#
# nr Chebyshev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors
NN = 10

##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

left_axis = {
    'u_min': umin,
    'u_max': umax,
    'title': r'u value',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

right_axis = {
    'u_min': vmin,
    'u_max': vmax,
    'title': r'v scale',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

middle_axis = {
    'u_min': wmin,
    'u_max': wmax,
    'title': r'w scale',
    'scale_type': 'log smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_axis,
    'f2_params': middle_axis,
    'f3_params': right_axis,
    'transform_ini': False,
    'isopleth_values': [[(left_axis['u_min'] + left_axis['u_max']) / 2, \
                         'x', \
                         (right_axis['u_min'] + right_axis['u_max']) / 2]]
}

main_params = {
    'filename': myfile,
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 7.0,
    'title_y': 2.0,
    'title_box_width': 8.0,
    'title_str': r'$w = FIXME:$', #r'$w = {1 \over {2(uv)^2}$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'npoints': NN
}

print("calculating the nomogram ...")
Nomogen(sq, main_params)  # generate nomogram for yrs function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
