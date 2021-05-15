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

###############################################
# compound pendulum example
# from Allcock & Jones, example xii, p93
def pendulum(u,v):
    return (v**2 + u**2)/(u+v)

umin = 0.25; umax = 1;
vmin = 0.25; vmax = 1;
wmin = pendulum(umin, vmin);
wmax = pendulum(umax, vmax);


###############################################################
#
# nr Chebychev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors
NN = 7


##############################################
#
# definitions for the scales for pyNomo
# dictionary with key:value pairs

left_scale = {
    'u_min': umin,
    'u_max': umax,
    'title': r'$u \thinspace distance$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

right_scale = {
    'u_min': vmin,
    'u_max': vmax,
    'title': r'$v \thinspace distance$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

middle_scale = {
    'u_min': wmin,
    'u_max': wmax,
    'title': r'$L \thinspace distance$',
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
    'isopleth_values': [[0.7, 'x', 0.9]]
}

main_params = {
    'filename': 'pendulum.pdf',
    'paper_height': 10, # units are cm
    'paper_width': 10,
    'title_x': 2.5,
    'title_y': 9.0,
    'title_box_width': 8.0,
    'title_str':r'$L = {{u^2 + v^2} \over {u + v}}$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'nlinearity': NN
}

print("calculating the nomogram ...")
Nomogen(pendulum, main_params);  # generate nomogram for pendulim() function

print("printing the nomogram ...")
Nomographer(main_params);
