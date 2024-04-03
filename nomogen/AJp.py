#!/usr/bin/env python3

# nomogen example program

import sys

sys.path.insert(0, "..")

from math import *

from nomogen import Nomogen
from pynomo.nomographer import Nomographer


########################################
#
#  this is the target function,
#  - the limits of the variables
#  - the function that the nonogram implements
#
#  format is m = m(l,r), where l, m & r are respectively the values
#                        for the left, middle & right hand axes
########################################

###############################################
#
# from Allcock & Jones, example xv, p112..117
# "the classical example of a nomogram consisting of three curves ..."
# Load on a retaining wall
# (1+L)*h**2 - L*h*(1+p) - (1-L)*(1+2*p)/3 == 0
#
def AJcheck(L, h, p):
    return (1 + L) * h ** 2 - L * h * (1 + p) - (1 - L) * (1 + 2 * p) / 3


# this version has inverted h & p scales
# produces nearly linear scales
def AJp(L, h):
    p = ((1 + L) * h ** 2 - L * h - (1 - L) / 3) / (L * h + 2 * (1 - L) / 3)
    # print("result is ", (1+L)*h**2 - L*h*(1+p) - (1-L)*(1+2*p)/3)
    if not isclose(AJcheck(L, h, p), 0, abs_tol=1e-10):
        print("AJp equation failed")
        sys.exit("quitting")
    return p


Lmin = 0.5;
Lmax = 1.0;
hmin = 0.75;
hmax = 1.0;
pmin = AJp(Lmax, hmin);  # <-- this clips the p scale, alternatively pmin = AJp(Lmin, hmin);
pmax = AJp(Lmin, hmax);

# print('pmin is ', pmin, ', pmax is ', pmax);

###############################################################
#
# nr Chebyshev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors
NN = 3

##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

left_axis = {
    'u_min': Lmin,
    'u_max': Lmax,
    'title': r'$L$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

right_axis = {
    'u_min': hmin,
    'u_max': hmax,
    'title_x_shift': 0.5,
    'title': r'$h$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

middle_axis = {
    'u_min': pmin,
    'u_max': pmax,
    'title_x_shift': -0.5,
    'title': r'$p$',
    'scale_type': 'linear smart',
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
    'filename': 'AJp',
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 5,
    'title_y': 9.0,
    'title_box_width': 8.0,
    'title_str': r'\scriptsize $(1+L)h^2 - Lh(1+p) - {1 \over 3} (1-L)(1+2p) = 0$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'npoints': NN
}

print("calculating the nomogram ...")
Nomogen(AJp, main_params)  # generate nomogram for AJp function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
