#!/usr/bin/python3

#nomogen example program

import sys
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
# w = u * c**v
#

c = 3.5

def w(u,v):
    return u* c**v

umin = 0.06; umax = 9.192;
vmin = 0.7;   vmax = 5;

wmin = w(umin,vmin)
wmax = w(umax,vmax)


print('wmin is ', wmin, ', wmax is ', wmax);
###############################################################
#
# nr Chebychev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors
NN = 5


##############################################
#
# definitions for the scales for pyNomo
# dictionary with key:value pairs

left_scale = {
    'u_min': umin,
    'u_max': umax,
    'title': r'$u$',
    'scale_type': 'log smart',
    'tick_levels':5,
    'tick_text_levels': 4,
    'grid': False
}

right_scale = {
    'u_min': vmin,
    'u_max': vmax,
    #'title_x_shift': 0.5,
    'title': r'$v$',
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 4,
    'grid': False
}

middle_scale = {
    'u_min': wmin,
    'u_max': wmax,
    #'title_x_shift': -0.5,
    'title': r'$w$',
    'scale_type': 'log smart',
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
    'isopleth_values': [[(left_scale['u_min'] + left_scale['u_max'])/2, \
                         'x', \
                         (right_scale['u_min'] + right_scale['u_max'])/2]]
}

main_params = {
    'filename': __name__ == "__main__" and (__file__.endswith(".py") and __file__.replace(".py", "") or "nomogen") or __name__,
    'paper_height': 10, # units are cm
    'paper_width': 10,
    'title_x': 3,
    'title_y': 9.0,
    'title_box_width': 8.0,
    'title_str': r'\small $ w = {u c^v }$'.replace("c", str(c)),
#    'extra_texts':[
#        {'x':3,
#         'y':10,
#         'text':r'$breaking \thinspace strain \thinspace of \thinspace a \thinspace wire $',
#         'width':7,
#         }],
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'pdegree': NN
}

print("calculating the nomogram ...")
Nomogen(w, main_params);  # generate nomogram for Q function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params);
