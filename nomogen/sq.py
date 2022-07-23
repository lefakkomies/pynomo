#!/usr/bin/python3

# nomogen example program

import sys

sys.path.insert(0, "..")

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
def sq(u, v):
    return (u * v) ** 2 / 2


umin = 2
umax = 10
vmin = 1
vmax = 5
wmin = sq(umin, vmin)
wmax = sq(umax, vmax)

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
    'title': r'$u \enspace value$',
    'scale_type': 'log smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

right_scale = {
    'u_min': vmin,
    'u_max': vmax,
    'title': r'$v \enspace scale$',
    'scale_type': 'log smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

middle_scale = {
    'u_min': wmin,
    'u_max': wmax,
    'title': r'$w \thinspace scale$',
    'scale_type': 'log smart',
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
    'isopleth_values': [[(left_scale['u_min'] + left_scale['u_max']) / 2, \
                         'x', \
                         (right_scale['u_min'] + right_scale['u_max']) / 2]]
}

main_params = {
    'filename': __name__ == "__main__" and (
                __file__.endswith(".py") and __file__.replace(".py", "") or "nomogen") or __name__,
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 7.0,
    'title_y': 2.0,
    'title_box_width': 8.0,
    'title_str': r'$w = {(uv)^2 \over 2}$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'pdegree': NN
}

print("calculating the nomogram ...")
Nomogen(sq, main_params)  # generate nomogram for yrs function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
