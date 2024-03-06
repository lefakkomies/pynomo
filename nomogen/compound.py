#!/usr/bin/env python3

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
#                        for the left, middle & right hand axes
########################################

###################
# compound interest, epidemics, etc
def compound(r, y):
    # r = % rate pa, y = nr years
    i = r / 100
    return (1 + i / 365) ** (365 * y)


imin = 1;
imax = 5
ymin = 1;
ymax = 25
wmin = compound(imin, ymin);
wmax = compound(imax, ymax);

###############################################################
#
# nr Chebyshev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors

NN = 9

##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

# the u scale
# dictionary with key:value pairs
left_axis = {
    'u_min': imin,
    'u_max': imax,
    'title': r'$interest \thinspace rate$',
    'scale_type': 'log smart',
    'tick_levels': 4,
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
    'u_min': wmin,
    'u_max': wmax,
    'title': r'$final \thinspace value$',
    'scale_type': 'log smart',
    'tick_levels': 5,
    'tick_text_levels': 4,
}

block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_axis,
    'f2_params': middle_axis,
    'f3_params': right_axis,
    'transform_ini': False,
    'isopleth_values': [[(imin * imax * imax) ** (1 / 3), 'x', (ymin + ymax) / 2]]
}

main_params = {
    'filename': __name__ == "__main__" and (
                __file__.endswith(".py") and __file__.replace(".py", "") or "nomogen") or __name__,
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 5.0,
    'title_y': 1.0,
    'title_box_width': 8.0,
    'title_str': r'$final \thinspace value = (1 + {i \over 365}) ^ {365y}$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'npoints': NN
}

print("calculating the nomogram ...")
Nomogen(compound, main_params)  # generate nomogram for yrs function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
