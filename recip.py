#!/usr/bin/python3

#nomogen example program

import sys

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

#########################################################
# resistors in parallel, focal length, etc
def recip(u,v):
    return 1/(1/u + 1/v)

umin = 5; umax = 50;
vmin = 5; vmax = 50;
wmin = (umin*vmin)/(umin+vmin); wmax = (umax*vmax)/(umax+vmax);


###############################################################
#
# nr Chebychev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors
NN = 13


##############################################
#
# definitions for the scales for pyNomo
# dictionary with key:value pairs

left_scale = {
    'u_min': umin,
    'u_max': umax,
    'title': r'$R_1$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

right_scale = {
    'u_min': vmin,
    'u_max': vmax,
    'title': r'$R_2$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

middle_scale = {
    'u_min': wmin,
    'u_max': wmax,
    'title': r'$R$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_scale,
    'f2_params': middle_scale,
    'f3_params': right_scale,
    'transform_ini': False,
    'isopleth_values': [[7, 'x', 8]]
}

main_params = {
    'filename': __file__.endswith(".py") and __file__.replace(".py", ".pdf") or "nomogen.pdf",
    'paper_height': 10, # units are cm
    'paper_width': 10,
    'title_x': 3.0,
    'title_y': 9.0,
    'title_box_width': 8.0,
    'title_str':r'${1 \over R} = {1 \over R_1} + {1 \over R_2}$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'pdegree': NN
}

print("calculating the nomogram ...")
Nomogen(recip, main_params);  # generate nomogram for yrs function

print("printing the nomogram ...")
Nomographer(main_params);
