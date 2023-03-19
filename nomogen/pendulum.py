#!/usr/bin/python3

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
#                        for the left, middle & right hand scales
########################################

###############################################
# compound pendulum example
# from Allcock & Jones, example xii, p93
def pendulum(u, v):
    return (u ** 2 + v ** 2) / (u + v)


umin = 0.25
umax = 2
vmin = umin
vmax = umax
wmin = pendulum(umin, vmin)
wmax = pendulum(umax, vmax)

###############################################################
#
# nr Chebychev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors
# for the pendulum function, the scale lines are neither linear nor logarithmic,
# so a high degree polynomial is needed
# NN == 5 or 6 * umax should be OK
NN = 11

##############################################
#
# definitions for the scales for pyNomo
# dictionary with key:value pairs

left_scale = {
    'u_min': umin,
    'u_max': umax,
    'title': r'$u \thinspace distance$',
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
    'grid': False
}

right_scale = {
    'u_min': vmin,
    'u_max': vmax,
    'title': r'$v \thinspace distance$',
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
    'grid': False
}

middle_scale = {
    'u_min': wmin,
    'u_max': wmax,
    'title': r'$L \thinspace distance$',
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
    'grid': False
}

block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_scale,
    'f2_params': middle_scale,
    'f3_params': right_scale,
    'transform_ini': False,
    'isopleth_values': [[left_scale['u_max'] * 0.95, \
                         'x', \
                         right_scale['u_max'] * 0.9 ]]
    #    'isopleth_values': [[0.7, 'x', 0.9]]
}

main_params = {
    'filename': __name__ == "__main__" and (
                __file__.endswith(".py") and __file__.replace(".py", "") or "nomogen") or __name__,
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 1.5,
    'title_y': 2.0,
    'title_box_width': 3.0,
    'title_str': r'$L = {{u^2 + v^2} \over {u + v}}$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'muShape': 5,
    'pdegree': NN
}

print("calculating the nomogram ...")
Nomogen(pendulum, main_params)  # generate nomogram for pendulum() function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
