#!/usr/bin/env python3

# generate a nomogen for the circumference of an elipse
# reference:
# http://web.tecnico.ulisboa.pt/~mcasquilho/compute/com/,ellips/PerimeterOfEllipse.pdf

# demonstrate generation of a nomogram from a difficult equation


# pylint: disable=C

import sys
import math

sys.path.insert(0, "..")

import scipy.special as sc

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

# return value is circumference, the middle scale
# a & b are the semi-major & semi-minor axes and respectively the values on the left and right scales

# circumference of ellipse, using hypergeometric function
# perimeter = 2*a*pi*hgf(-0.5, 0.5, 1, 1 - b*b/a*a)

def circEllipse(a, b):
    aa = abs(a)
    bb = abs(b)
    if aa < bb:
        aa, bb = bb, aa

    # aa is semi-major axis, bb is semi-minor axis
    if bb == 0:
        return 4*aa

    ksq = 1 - bb*bb/(aa*aa)
    return 2 * aa * math.pi * sc.hyp2f1(-0.5, 0.5, 1, ksq)


# range for the a scale (the left scale)
amin = 0.01
amax = 1

# range for the b scale (the right scale)
bmin = amin
bmax = amax

# range for the w scale (the middle scale)
wmin = circEllipse(amin, bmin)
wmax = circEllipse(amax, bmax)


###############################################################
#
# nr points (Chebyshev nodes) needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value is faster, makes a smoother curve, but could be less accurate
NN = 8


##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

left_axis = {
    'u_min': amin,
    'u_max': amax,
    'title': r'$a \enspace axis$',
    'title_x_shift': 0.5,
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

right_axis = {
    'u_min': bmin,
    'u_max': bmax,
    'title': r'$b \thinspace axis$',
    'title_x_shift': 0.5,
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

middle_axis = {
    'u_min': wmin,
    'u_max': wmax,
    'title': r'$circumference$',
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
    'filename': 'ellipse',
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 7.4,
    'title_y': 8.6,
    'title_box_width': 8.0,
    'title_str': r'$circumference \thinspace of \thinspace an \thinspace ellipse$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],

    'npoints': NN,

    # instead of forcing the ends of the axes to the corners of the unit square,
    # nomogen can shape the nomogram to minimise parallax errors
    # uncomment the following line to select this option
    #'muShape': 3,

    # text to appear at the foot of the nomogram
    # make this null string for nothing
    # a default string will appear if this is omitted
    #'footer_string': r'$\tiny circ \enspace project \enspace configuration \enspace string$'
}

print("calculating the nomogram ...")
Nomogen(circEllipse, main_params)  # generate nomogram for the target function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
