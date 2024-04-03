#!/usr/bin/env python3

# nomogen example program

# pylint: disable=C

import sys
import math

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


# simple example
# return value is the middle scale
# u & v are respectively the values on the left and right scales
def test1(u, v):
    return (9 * u + v) / (8 * (u - v) + 10)


# range for the u scale (the left scale)
umin = 0
umax = 1

# range for the v scale (the right scale)
vmin = 0
vmax = 1

# range for the w scale (the middle scale)
wmin = test1(umin, vmin)
wmax = test1(umax, vmax)


###############################################################
#
# nr points (Chebyshev nodes) needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value is faster and makes a smoother curve,
#     but could be less accurate
NN = 3


##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

left_axis = {
    'u_min': umin,
    'u_max': umax,
    'title': r'$u \enspace scale$',
    'title_x_shift': 0.5,
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

right_axis = {
    'u_min': vmin,
    'u_max': vmax,
    'title': r'$v \thinspace scale$',
    'title_x_shift': 0.5,
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

middle_axis = {
    'u_min': wmin,
    'u_max': wmax,
    'title': r'$w \thinspace scale$',
    'title_x_shift': -0.2,
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

# assemble the above 3 axes into a block
block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_axis,
    'f2_params': middle_axis,
    'f3_params': right_axis,

    # the isopleth connects the mid values of the outer axes
    # edit this for different values
    'isopleth_values': [[(left_axis['u_min'] + left_axis['u_max']) / 2, \
                         'x', \
                         (right_axis['u_min'] + right_axis['u_max']) / 2]]
}

# the nomogram parameters
main_params = {
    'filename': 'test1',
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 7.0,
    'title_y': 2.0,
    'title_box_width': 8.0,
    'title_str': r'$w = {{9u + v} \over {8(u-v) + 10}}$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],

    'npoints': NN,

    # instead of forcing the ends of the axes to the corners of the unit square,
    # nomogen can shape the nomogram to minimise parallax errors
    # uncomment the following line to select this option
    #'muShape': 0,

    # text to appear at the foot of the nomogram
    # note tha latex rules apply
    # a default string will appear if this is omitted
    # make this an empty string to have no footer text
    'footer_string': r'$\tiny test1 \enspace project \enspace footer \enspace string$'
}

print("calculating the nomogram ...")
Nomogen(test1, main_params)  # generate nomogram for the target function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
