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

####################################################
# future value of $1 invested each year
# - fv  is return value and will be the middle scale,
# - first argument is r and will become the right scale
# - second argument is years and will become the left scale, and
#
#   fv = ((1 + i)**y - 1) / i
#
def fv(r,y):
    # r = % rate pa, y = nr years
    i = r/100
    return (((1 + i) ** y) - 1)/i

rmin = 0.1; rmax = 5
ymin = 1;   ymax = 25
fvmin = fv(rmin, ymin);
fvmax = fv(rmax, ymax);

###############################################################
#
# nr Chebychev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors
NN = 7


##############################################
#
# definitions for the scales for pyNomo
# dictionary with key:value pairs

left_scale = {
    'u_min': rmin,
    'u_max': rmax,
    'title': r'$\% \enspace rate$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

right_scale = {
    'u_min': ymin,
    'u_max': ymax,
    'title': r'$years$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

middle_scale = {
    'u_min': fvmin,
    'u_max': fvmax,
    'title_x_shift': 1.0,
    'title': r'$future \enspace value$',
    'scale_type': 'linear smart',
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
    'isopleth_values': [[(left_scale['u_min'] + left_scale['u_max'])/2, \
                         'x', \
                         (right_scale['u_min'] + right_scale['u_max'])/2]]
}

main_params = {
    'filename': __name__ == "__main__" and (__file__.endswith(".py") and __file__.replace(".py", "") or "nomogen") or __name__,
    'paper_height': 10, # units are cm
    'paper_width': 10,
    'title_x': 5.0,
    'title_y': 1.0,
    'title_box_width': 8.0,
    'title_str':r'$future \thinspace value \thinspace of \thinspace \$1 \thinspace invested \thinspace each \thinspace year$',
    'extra_texts':[
        {'x':4,
         'y':2,
         'text':r'$FV = {(1+i)^y-1 \over i}$',
         'width':5,
         }],
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'pdegree': NN
}

print("calculating the nomogram ...")
Nomogen(fv, main_params);  # generate nomogram for fv() function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params);
