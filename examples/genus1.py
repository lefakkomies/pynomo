#!/usr/bin/env python3

# genus I, 3rd class nomogram, 2 parallel lines, one curve
# reference: "The Nomogram", Allcock & Jones, Example (ix), p79

# plotting the equation:
#   w**3 + vw + u = 0
#
# in this plot, the w axis has 2 scales - w and 9w


# determinant is
#  | 0                     p+a*u                 1 |   <-- left scale (u)
#  |                                               |
#  | aw/(aw+c)   (p*c + awb - a*c*w**3)/(aw+c)   1 |   <-- middle scale (w)
#  |                                               |
#  | 1                     b+c*v                 1 |   <-- right scale (v)

#    ^                      ^                    ^
#    |                      |                    +-- constant
#    |                      +------------------- y coordinate
#    +------------------------------------------ x coordinate

# where:
# a = u scale
# p = u offset
# c = v scale
# b = v offset

# pylint: disable=C


import sys

sys.path.insert(0, "..")

import math
import scipy.optimize

from pynomo.nomographer import Nomographer


# return w as a function of u & v
def fw(u,v):
    # offset by -1 to force bracket values either side of zero
    r = scipy.optimize.root_scalar( lambda w: (w+1)**3 + v*(w+1) +u, \
                                    method = 'bisect', \
                                    bracket = [-1, 6] )
    #print(r)
    return r.root + 1

u_min = -40
u_max =   0
v_min = -40
v_max =   0
w_min = fw(u_max, v_max)
w_max = fw(u_min, v_min)

# fit the left & right scales to the unit square
scale_u = 1/(u_max-u_min)
offset_u = -u_min * scale_u

scale_v = 1/(v_max-v_min)
offset_v = -v_min * scale_v


########################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs
# functions f,g,h taken from the determinant
# other values defined above


# Note for 'tick_side':
# Left and right is undefined in middle scale that goes horizontally.
# ’turn_relative’ parameter defines if ticks are on left or right
# when starting from ’u_min’ towards ’u_max’ a small step.

left_axis = {
    'u_min': u_min,
    'u_max': u_max,
    'f': lambda u: 0,                       # x coordinate
    'g': lambda u: offset_u + scale_u*u,    # y coordinate
    'h': lambda u: 1,                       # constant
    'title': r'u',
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
}

right_axis = {
    'u_min': v_min,
    'u_max': v_max,
    'f': lambda v: 1,
    'g': lambda v: offset_v + scale_v*v,
    'h': lambda v: 1,
    'title': r'v',
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
}

middle_axis = {
    'tag': 'middle',            # link to alternative scale
    'u_min': w_min,
    'u_max': w_max,
    'f': lambda w: (scale_u * w/(scale_u*w+scale_v)),
    'g': lambda w: ( offset_u*scale_v + scale_u*offset_v*w \
                     - scale_u*scale_v*w**3 ) / (scale_u*w+scale_v),
    'h': lambda w: 1,
    'title': r'w',
    'title_x_shift': 10,
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
    'turn_relative': True,
    'tick_side': 'left',
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

# add a second scale onto the middle axis, scaled by 9
alt_per_orig = 9
middle_axis_alt = {
    'tag': 'middle',
    'u_min': middle_axis['u_min'] * alt_per_orig,
    'u_max': middle_axis['u_max'] * alt_per_orig,
    'function_x': lambda u: middle_axis['f'](u/alt_per_orig),
    'function_y': lambda u: middle_axis['g'](u/alt_per_orig),
    'align_func': lambda u: u / alt_per_orig,
    'title': r'9w',
    'title_x_shift': 7,
    'title_y_shift': -3,
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
    'turn_relative': True,
    'tick_side': 'right',
}

block_2_params={
    'block_type':'type_8',
    'f_params': middle_axis_alt,
    'isopleth_values':[['x']],
}


main_params = {
    'filename': 'genus1.pdf',

    # a4 page, with margins approx 2cm
    'paper_height': 25,  # units are cm
    'paper_width':  15,

    # title coordinates are cm from lower left corner
    'title_x': 7.0,
    'title_y': 2.0,
    'title_box_width': 8.0,
    'title_str': r'$ w^3 \thinspace + \thinspace vw \thinspace + \thinspace u \thinspace = \thinspace 0$',

    # build the nomogram from the blocks above
    'block_params': [block_params0, block_2_params],

    # the nomogram is scaled to the unit square
    # transform the nomogram so it fits the page
    'transformations': [('scale paper',)],

}

print("printing ", main_params['filename'], " ...")
Nomographer(main_params)


# check values

N=10
res = 'passed'
for i in range( N+1 ):
    uu = u_min + (u_max-u_min)*i/N
    for j in range( N+1 ):
        vv = v_min + (v_max-v_min)*j/N
        xu = left_axis['f'](uu)
        yu = left_axis['g'](uu)
        xv = right_axis['f'](vv)
        yv = right_axis['g'](vv)
        ww = fw(uu,vv)
        xw = middle_axis['f'](ww)
        yw = middle_axis['g'](ww)
        tl = (xw-xu) * (yv - yu)
        tr = (xv-xu) * (yw - yu)
        if not math.isclose(tl, tr, abs_tol = 10e-12):
            print( "check failed, u, v, w is ", uu, " ,", vv, " ,",  ww, \
                   ", left, right is", tl, tr, "error is ", tl-tr )
            print( "u is (", xu, ",", yu, "), ", \
                   "v is (", xv, ",", yv, "), ", \
                   "w is (", xw, ",", yw, ")", sep='' )
            res = 'failed'

print( "nomogram check", res )

