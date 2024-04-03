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
#  - the limits of the variables
#  - the function that the nonogram implements
#
#  format is m = m(l,r), where l, m & r are respectively the values
#                        for the left, middle & right hand axes
#
#  also need to specify the limits of the variables
#
########################################

####################################################
# future value of $1 invested each year
# - fv  is return value and will be the middle scale,
# - first argument is r and will become the right scale
# - second argument is years and will become the left scale, and
#
#   fv = ((1 + i)**y - 1) / i
#
def fv(r, y):
    # r = % rate pa, y = nr years
    i = r / 100
    return (((1 + i) ** y) - 1) / i


rmin = 0.1
rmax = 10
ymin = 1
ymax = 40
fvmin = fv(rmin, ymin)
fvmax = fv(rmax, ymax)

###############################################################
#
# nr Chebyshev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value is faster, makes a smoother curve,
#     but could be less accurate
NN = 8


##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

left_axis = {
    'u_min': rmin,
    'u_max': rmax,
    'title': r'$\% \enspace rate$',
    'scale_type': 'log smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
}

right_axis = {
    'u_min': ymin,
    'u_max': ymax,
    'title': r'$years$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

middle_axis = {
    'u_min': fvmin,
    'u_max': fvmax,
    'title_x_shift': 1.0,
    'title': r'$future \enspace value$',
    'scale_type': 'log smart',
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
    'filename': 'fv',
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 5.0,
    'title_y': 1.0,
    'title_box_width': 8.0,
    'title_str': r'$future \thinspace value \thinspace of \thinspace \$1 \thinspace invested \thinspace each \thinspace year$',
    'extra_texts': [
        {'x': 2,
         'y': 2,
         'text': r'$FV = {(1+i)^y-1 \over i}$',
         'width': 5,
         }],
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'npoints': NN
}

print("calculating the nomogram ...")
Nomogen(fv, main_params);  # generate nomogram for fv() function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
