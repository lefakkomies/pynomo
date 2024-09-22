#!/usr/bin/env python3

# nomogen example program

import sys

import inspect
import os

sys.path.insert(0, "..")

import math

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

###############################################
#
# from Allcock & Jones, example xv, p112..117
# "the classical example of a nomogram consisting of three curves ..."
# Load on a retaining wall
# (1+L)*h**2 - L*h*(1+p) - (1-L)*(1+2*p)/3 == 0
#
def AJcheck(L, h, p):
    return (1 + L) * h ** 2 - L * h * (1 + p) - (1 - L) * (1 + 2 * p) / 3


def AJh(L, p):
    a = 1 + L
    b = -L * (1 + p)
    c = -(1 - L) * (1 + 2 * p) / 3
    h = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    # print("result is ", (1+L)*h**2 - L*h*(1+p) - (1-L)*(1+2*p)/3)
    if not math.isclose(AJcheck(L, h, p), 0, abs_tol=1e-10):
        print("AJh equation failed")
        sys.exit("quitting")
    return h


Lmin = 0.5
Lmax = 1.0
pmin = 0.5
pmax = 1.0
hmin = AJh(Lmax, pmin)
hmax = AJh(Lmin, pmax)

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
    'tick_text_levels': 2
}

right_axis = {
    'u_min': pmin,
    'u_max': pmax,
    'title': r'$p$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2
}

middle_axis = {
    'u_min': hmin,
    'u_max': hmax,
    'title': r'$h$',
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
    'filename': myfile,
    'paper_height': 15,  # units are cm
    'paper_width': 10,
    'title_x': 4.5,
    'title_y': 1.5,
    'title_box_width': 8.0,
    'title_str': r'$ \scriptsize (1+L)h^2 - Lh(1+p) - {1 \over 3} (1-L)(1+2p) = 0$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'npoints': NN
}

print("calculating the nomogram ...")
Nomogen(AJh, main_params)  # generate nomogram for AJh function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
