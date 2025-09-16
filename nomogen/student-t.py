#!/usr/bin/env python3

'''
nomogen example to plot Student-T percent point function
'''

# pylint: disable=C

import sys
import math
import pyx     # allow colours
from datetime import datetime  # for adding timestamp

import inspect
import os

sys.path.insert(0, "..")

from nomogen import Nomogen
from pynomo.nomographer import Nomographer

# get current file name
myfile = os.path.basename(inspect.stack()[0][1]).replace(".py", "")



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

from scipy.stats import t

# return the critical t value for student's t distribution
# alpha significance, confidence level. tail area, probability
# v degrees of freedom = sample size - 1
# alpha and v are respectively the values on the left and right scales
def tvalue(alpha, v):
    return t.ppf(1 - alpha/2, v) # two tailed test


# range for the u scale (the left scale)
alpha_min = 0.001
alpha_max = 0.1

# range for the v scale (the right scale)
df_min = 1
df_max = 40

# range for the w scale (the middle scale)
t_min = tvalue(alpha_max, df_max)
t_max = 100 #tvalue(alpha_min, df_min)


###############################################################
#
# nr points (Chebyshev nodes) needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value is faster and makes a smoother curve,
#     but could be less accurate
NN = 13


##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

left_axis = {
    'tag': 'left',            # link to 1-tail scale
    'u_min': alpha_min,
    'u_max': alpha_max,
    'title': 'two-tail',
    'title_draw_center': True,
    'title_distance_center': 1.5,
     'title_extra_angle': 180,
    'extra_titles':[
        {'dx':-2.3,
         'dy':0.4,
         'text': r'$\alpha$ significance level',
         }],
    'scale_type': 'log smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
    'text_distance_smart': 0.6, # min distance between tick texts
    'tick_side': 'right'
}

right_axis = {
    'u_min': df_min,
    'u_max': df_max,
    'title': r'$v$ degrees of freedom',
    'title_x_shift': -0.4,
    'scale_type': 'log smart',
    'anamorphosis': {'func': math.atan, 'inv': math.tan},
    'tick_levels': 2,
    'tick_text_levels': 2,
    'extra_params': [{'u_min': 10.0,           # reduce tic levels here
                      'u_max': df_max,
                      'tick_levels': 4,
                      'tick_text_levels': 3,
                      },
                     ],
    'tick_side': 'left'
}

middle_axis = {
    'u_min': t_min,
    'u_max': t_max,
    'title': r'critical value $t_{\alpha , v}$',
    'title_x_shift': 0,
    'scale_type': 'log smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
    'extra_params': [{'u_min': t_min,
                      'u_max': 3,
                      'tick_text_levels': 4,
                      },
                     ],
}

# assemble the above 3 axes into a block
block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_axis,
    'f2_params': middle_axis,
    'f3_params': right_axis,

    # the isopleth connects the mid values of the outer axes
    # edit this for different values
    'isopleth_values': [[ 0.05, 'x', 6]],

    # log alignment errors
    # If this is missing or False then alignment error logs are disabled
    'LogAlignment': False,
}


######## the second scale one tail ##############

# single tail scale for left axis

left_axis_single = {
    'tag': 'left',
    'u_min': left_axis['u_min'] / 2,
    'u_max': left_axis['u_max'] / 2,
    'title': 'one-tail',
    'title_distance_center': -1.5,
    'title_draw_center': True,
    'title_extra_angle': 180,
    'title_color': pyx.color.cmyk.Orange,
    'axis_color': pyx.color.cmyk.Orange,
    'text_color': pyx.color.cmyk.Orange,
    'align_func': lambda m: m*2,
    'scale_type': left_axis['scale_type'],
    'tick_levels': left_axis['tick_levels'],
    'tick_text_levels': left_axis['tick_text_levels'],
    'text_distance_smart': 0.6,  # min distance between tick texts
    'tick_side': 'left'
}

block_1_params={
    'block_type':'type_8',
    'f_params': left_axis_single,
    'isopleth_values':[['x']],
}


# the nomogram parameters

main_params = {
    'filename': myfile,

    # a4 page, with margins approx 2cm
    'paper_height': 25,  # units are cm
    'paper_width':  16,

    'title_x': 7.0,
    'title_y': 1.0,
    'title_box_width': 8.0,
    'title_str': r"\Large Student's t distribution",
    'block_params': [block_params0,
                     block_1_params
                     ],
    'isopleth_params': [{'color': 'Red'}],
    'transformations': [('scale paper',)],

    'npoints': NN,

    # text to appear at the foot of the nomogram
    # note that latex rules apply
    # a default string will appear if this is omitted
    # make this an empty string to have no footer text
    'footer_string': f'student-t: ({datetime.now().strftime("%d%b%y, %H:%M:%S")})'
}

print("calculating the nomogram ...")
Nomogen(tvalue, main_params)  # generate nomogram for the target function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)

################################ end of student-t.py ##########################
