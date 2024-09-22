#!/usr/bin/env python3

# nomogen example program
# compound pendulum example from Allcock & Jones, example (xii), p93

# plotting the equation:
#   L = (a**2 * b**2) / (a + b)
#
# pylint: disable=C

import sys

import inspect
import os

sys.path.insert(0, "..")

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
# compound pendulum equation
def pendulum(a, b):
    return (a ** 2 + b ** 2) / (a + b)


umin = 0.25
umax = 2
vmin = umin
vmax = umax
wmin = pendulum(umin, vmin)
wmax = pendulum(umax, vmax)

###############################################################
#
# nr Chebyshev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors
# for the pendulum function, the axes are neither linear nor logarithmic,
# so a high degree polynomial is needed
# NN == 5 or 6 * umax should be OK
NN = 12

##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

# the numbers on the left and right scales are on the inside of a tight curve,
# so get squeezed together
# pynomo can increase the tick levels of selected regions, but doesn't reduce them (bug?)
# specify zero for tick_text_level generally,
# and increase this for regions away from the curve
left_axis = {
    'u_min': umin,
    'u_max': umax,
    'title': r'a distance',
    'scale_type': 'linear smart',
    'tick_levels': 4,
    'tick_text_levels': 0,
    'tick_side': 'left',
    'extra_params': [{'u_min': umin,
                      'u_max': 0.5,
                      'tick_levels': 3,
                      'tick_text_levels': 2,
                      },
                     {'u_min': 1,
                      'u_max': umax,
                      'tick_levels': 4,
                      'tick_text_levels': 2,
                      }
                     ],
}

right_axis = {
    'u_min': vmin,
    'u_max': vmax,
    'title': r'b distance',
    'scale_type': 'linear smart',
    'tick_levels': 4,
    'tick_text_levels': 0,
    'tick_side': 'right',
    'extra_params': [{'u_min': umin,
                      'u_max': 0.5,
                      'tick_levels': 3,
                      'tick_text_levels': 2,
                      },
                     {'u_min': 1,
                      'u_max': umax,
                      'tick_levels': 4,
                      'tick_text_levels': 2,
                      }
                     ],
}

middle_axis = {
    'u_min': wmin,
    'u_max': wmax,
    'title': r'L distance',
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
}

block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_axis,
    'f2_params': middle_axis,
    'f3_params': right_axis,
    'transform_ini': False,
    'isopleth_values': [[left_axis['u_max'] * 0.9, \
                         'x', \
                         right_axis['u_max'] * 0.95 ]]
    #    'isopleth_values': [[0.7, 'x', 0.9]]
}

main_params = {
    'filename': myfile,
    # a4 page, with margins approx 2cm
    'paper_height': 25,  # units are cm
    'paper_width':  16,

    'title_x': 5.6,
    'title_y': 24.0,
    'title_box_width': 3.0,
    'title_str': r'$L = {{a^2 + b^2} \over {a + b}}$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'muShape': 1,
    'npoints': NN
}

print("calculating the nomogram ...")
Nomogen(pendulum, main_params)  # generate nomogram for pendulum() function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
