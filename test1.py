#!/usr/bin/python3

#nomogen example program

import sys

import math
from nomogen import Nomogen
from pynomo.nomographer import Nomographer

########################################
#
#  this is the target function,
#  - the limits of the variables
#  - the function that the nonogram implements
#
#  format is m = m(l,r), where l, m & r are respectively the values
#                        for the left, middle & right hand scales
########################################


# simple example
def test1(u,tv):
    v = tv
    return (9*u + v) / (8*(u-v) + 10)

umin = 0; umax = 1;
vmin = 0; vmax = 1;
wmin = test1(umin, vmin);
wmax = test1(umax, vmax);

###############################################################
#
# nr Chebychev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors
NN = 3



##############################################
#
# definitions for the scales for pyNomo
# dictionary with key:value pairs

left_scale = {
    'u_min': umin,
    'u_max': umax,
    'title': r'$u \enspace scale$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

right_scale = {
    'u_min': vmin,
    'u_max': vmax,
    'title': r'$v \enspace scale$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

middle_scale = {
    'u_min': wmin,
    'u_max': wmax,
    'title': r'$w \thinspace scale$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_scale,
    'f2_params': middle_scale,
    'f3_params': right_scale,
    'transform_ini': False,
    'isopleth_values': [[(left_scale['u_min'] + left_scale['u_max'])/2, \
                         'x', \
                         (right_scale['u_min'] + right_scale['u_max'])/2 ]]
}

main_params = {
    'filename': __file__.endswith(".py") and __file__.replace(".py", ".pdf") or "nomogen.pdf",
    'paper_height': 10, # units are cm
    'paper_width': 10,
    'title_x': 7.0,
    'title_y': 2.0,
    'title_box_width': 8.0,
    'title_str':r'$w = {{9u + v} \over {8(u-v) + 10}}$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'pdegree': NN
}

print("calculating the nomogram ...")
Nomogen(test1, main_params);  # generate nomogram for test1 function

print("printing ", main_params['filename'], " ...")
Nomographer(main_params);
