#!/usr/bin/env python3

# nomogen example program

# pylint: disable=C

import sys

sys.path.insert(0, "..")

from nomogen import Nomogen
from pynomo.nomographer import Nomographer


########################################
#
#  this is the target function,
#  - the function that the nomogram implements
#  - add the limits of the variables below
#
#  format is m = m(l,r), where l, m & r are respectively the values
#                        for the left, middle & right hand axes
#
#
########################################

#########################################################
# resistors in parallel, focal length, etc
def recip(u, v):
    return 1 / (1 / u + 1 / v)


umin = 1
umax = 100
vmin = 1
vmax = 100
wmin = (umin * vmin) / (umin + vmin)
wmax = (umax * vmax) / (umax + vmax)

###############################################################
#
# nr Chebyshev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value is faster, makes a smoother curve,
#     but could be less accurate
NN = 7


##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

left_axis = {
    'u_min': umin,
    'u_max': umax,
    'title': r'$R_1$',
    'scale_type': 'log smart',
    'tick_levels': 5,
    'tick_text_levels': 2,
}

right_axis = {
    'u_min': vmin,
    'u_max': vmax,
    'title': r'$R_2$',
    'scale_type': 'log smart',
    'tick_levels': 5,
    'tick_text_levels': 2,
}

middle_axis = {
    'u_min': wmin,
    'u_max': wmax,
    'title': r'$R$',
    'scale_type': 'log smart',
    'tick_levels': 5,
    'tick_text_levels': 2,
}

# assemble the above 3 axes into a block
block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_axis,
    'f2_params': middle_axis,
    'f3_params': right_axis,
    'transform_ini': False,
    'isopleth_values': [[(left_axis['u_min'] ** 2 * left_axis['u_max']) ** (1 / 3), \
                         'x', \
                         (right_axis['u_min'] * right_axis['u_max'] ** 2) ** (1 / 3)]]
}

# the nomogram parameters
main_params = {
    'filename': __name__ == "__main__" and (
                __file__.endswith(".py") and __file__.replace(".py", "") or "nomogen") or __name__,
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 3.0,
    'title_y': 9.0,
    'title_box_width': 8.0,
    'title_str': r'${1 \over R} = {1 \over R_1} + {1 \over R_2}$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'muShape': 4,
    'npoints': NN
}

print("calculating the nomogram ...")
Nomogen(recip, main_params)  # generate nomogram for target function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
