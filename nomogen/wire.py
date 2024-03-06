#!/usr/bin/env python3

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
#                        for the left, middle & right hand axes
########################################

###############################################
#
# from Allcock & Jones, example (vi), p53..56
# breaking strain of a wire
# W = 1000*m /(pi/4 * d**2)
#
#  converted to SI units
#
def W(m, d):
    return 1000 * m / (d * d * math.pi / 4)


dmin = 1.5
dmax = 5  # mm
mmin = 0.6
mmax = 9  # kNewtons

Wmin = W(mmin, dmax)  # MPa
Wmax = W(mmax, dmin)

#print('Wmin is ', Wmin, ', Wmax is ', Wmax)
###############################################################
#
# nr Chebyshev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors
NN = 11

##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

left_axis = {
    'u_min': mmin,
    'u_max': mmax,
    'title': r'$m \thinspace kN$',
    'scale_type': 'log smart',
    'tick_levels': 5,
    'tick_text_levels': 4,
}

right_axis = {
    'u_min': dmin,
    'u_max': dmax,
    #    'title_x_shift': 0.5,
    'title': r'$d \thinspace mm$',
    'scale_type': 'log smart',
    'tick_levels': 5,
    'tick_text_levels': 4,
}

middle_axis = {
    'u_min': Wmin,
    'u_max': Wmax,
    #    'title_x_shift': -0.5,
    'title': r'$W \thinspace MPa$',
    'scale_type': 'log smart',
    'tick_levels': 4,
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
    'filename': __name__ == "__main__" and (
                __file__.endswith(".py") and __file__.replace(".py", "") or "nomogen") or __name__,
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 7,
    'title_y': 8.1,
    'title_box_width': 8.0,
    'title_str': r'\small $ W = {m \over {{\pi \over 4} d^2 }}$',
    'extra_texts': [
        {'x': 5.2,
         'y': 8.8,
         'text': r'\small $breaking \thinspace strain \thinspace of \thinspace a \thinspace wire $',
         'width': 7,
         }],
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'npoints': NN
}

print("calculating the nomogram ...")
Nomogen(W, main_params)  # generate nomogram for Q function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
