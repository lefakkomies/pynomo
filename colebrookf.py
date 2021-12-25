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

#####################################################
#colebrook equation, friction in pipes:
# return relative roughness, k/D
# Re = Reynolds nr
# f = friction coefficient
# Note: f is implicit, so use a loop to solve for f numerically
def colebrookf(kond, Re):
    f = 0.02
    for i in range(5): # loop 5 times
        sqrtf = math.sqrt(f)
        t = -2 * math.log10(2.51/(Re*sqrtf) + kond/3.72)
        f = 1/(t*t)
    #            print("f is ", f)
    return f

Remin = 1e5; Remax = 1.5e5;
kondmin = 0.000010; kondmax = 0.0018;

fmax = colebrookf(kondmax, Remin);
fmin = colebrookf(kondmin, Remax);

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
    'u_min': kondmin,
    'u_max': kondmax,
    'title': r'${\kappa/D}$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

right_scale = {
    'u_min': Remin,
    'u_max': Remax,
    'title': r'$Reynolds \enspace nr$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

middle_scale = {
    'u_min': fmin,
    'u_max': fmax,
    'title': r'$f$',
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
    'isopleth_values': [[0.001, 'x', 130000]]
}

main_params = {
    'filename': 'colebrookf.pdf',
    'paper_height': 10, # units are cm
    'paper_width': 10,
    'title_x': 6.0,
    'title_y': 9.0,
    'title_box_width': 8.0,
    'title_str':r'$friction \thinspace in \thinspace pipes$',
    'extra_texts':[
        {'x':4,
         'y':8,
         'text':r'${1 \over \sqrt f} = -2 log_{10} ({2.51 \over Re \sqrt f} + {\kappa / D \over 3.72})$',
         'width':5,
         }],
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'pdegree': NN
}

print("calculating the nomogram ...")
Nomogen(colebrookf, main_params);  # generate nomogram for yrs function

print("printing the nomogram ...")
Nomographer(main_params);
