#!/usr/bin/python3

# nomogen example program

import sys

sys.path.insert(0, "..")

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

###############################################
#
# from Allcock & Jones, example v, p44..47
# air flow thru a circular duct
# Q = pi/4 * d**2 * v
#
def Q(d, v):
    return d * d * v * math.pi / 4


dmin = 0.1;
dmax = 0.3;  # metres
vmin = 0.3;
vmax = 4.5;  # meters/sec

Qmin = Q(dmin, vmin)
Qmax = Q(dmax, vmax)

print('Qmin is ', Qmin, ', Qmax is ', Qmax);
###############################################################
#
# nr Chebychev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors
NN = 9

##############################################
#
# definitions for the scales for pyNomo
# dictionary with key:value pairs

left_scale = {
    'u_min': dmin,
    'u_max': dmax,
    'title': r'$d$',
    'scale_type': 'log smart',
    'tick_levels': 5,
    'tick_text_levels': 4,
    'grid': False
}

right_scale = {
    'u_min': vmin,
    'u_max': vmax,
    'title_x_shift': 0.5,
    'title': r'$v$',
    'scale_type': 'log smart',
    'tick_levels': 4,
    'tick_text_levels': 2,
    'grid': False
}

middle_scale = {
    'u_min': Qmin,
    'u_max': Qmax,
    'title_x_shift': -0.5,
    'title': r'$Q$',
    'scale_type': 'log',  # 'log smart' crashes pynomo
    'tick_levels': 4,
    'tick_text_levels': 2,
    'grid': False
}

block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_scale,
    'f2_params': middle_scale,
    'f3_params': right_scale,
    'transform_ini': False,
    'isopleth_values': [[(left_scale['u_min'] + left_scale['u_max']) / 2, \
                         'x', \
                         (right_scale['u_min'] + right_scale['u_max']) / 2]]
}

main_params = {
    'filename': __name__ == "__main__" and (
                __file__.endswith(".py") and __file__.replace(".py", "") or "nomogen") or __name__,
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 2,
    'title_y': 9.0,
    'title_box_width': 8.0,
    'title_str': r'\small $ Q = {\pi \over 4} d^2 v $',
    'extra_texts': [
        {'x': 3,
         'y': 10,
         'text': r'$Air \thinspace flow \thinspace through \thinspace a \thinspace circular \thinspace duct $',
         'width': 7,
         }],
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'pdegree': NN
}

print("calculating the nomogram ...")
Nomogen(Q, main_params)  # generate nomogram for Q function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
