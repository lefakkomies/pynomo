#!/usr/bin/env python3

'''
verify that a good initial estimate is for a
non vertical w axis that passes thru (0.5,0.5)
'''

# pylint: disable=C

import sys
import math

import inspect
import os
import scipy.optimize

sys.path.insert(0, "..")

from nomogen import Nomogen
from pynomo.nomographer import Nomographer

# get current file name
myfile = os.path.basename(inspect.stack()[0][1]).replace(".py", "")


# tehse allow combinations the v & w axes to be up or down
wup = vup = None


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

# return value is the middle scale
# u & v are respectively the values on the left and right scales
# for this test, we require w(umin, vmax) == w(umax,vmin)
# so the lines intersect at the centre

# this function is constructed so that the w axis
# varies linearly from (0,4,0) tp (0.6,1)

def centre(au,av):
    u = au
    v = av
    if not vup:
        v = 1-v
    w = (6*u + 4*v) / (2*(u-v) + 10)
    if not wup:
        w = 1-w
    return w


# range for the u scale (the left scale)
umin = 0
umax = 1

# range for the v scale (the right scale)
vmin = 0
vmax = 1



###############################################################
#
# nr points (Chebyshev nodes) needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value is faster and makes a smoother curve,
#     but could be less accurate
NN = 5


##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

left_axis = {
    'u_min': umin,
    'u_max': umax,
    'title': 'u scale',
    'title_x_shift': 0.5,
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

right_axis = {
    'u_min': vmin,
    'u_max': vmax,
    'title': 'v scale',
    'title_x_shift': 0.5,
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

middle_axis = {
#    'u_min': wmin,
#    'u_max': wmax,
    'title': 'w scale',
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
    'isopleth_values': [[(left_axis['u_min'] + left_axis['u_max']) / 3, \
                         'x', \
                         (right_axis['u_min'] + right_axis['u_max']) / 1.5]],

    # log alignment errors
    # If this is missing or False then alignment error logs are disabled
    'LogAlignment': False,
}

# the nomogram parameters

main_params = {
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 7.0,
    'title_y': 2.0,
    'title_box_width': 8.0,
    'block_params': [block_params0],

    # set the colour of the ispleth/index line here
    'isopleth_params': [ {'color': 'Red'}, ],

    'transformations': [('scale paper',)],

    'npoints': NN,

    # instead of forcing the ends of the axes to the corners of the unit square,
    # nomogen can shape the nomogram to minimise parallax errors
    # uncomment the following line to select this option
    #'muShape': 1,

    # text to appear at the foot of the nomogram
    # note that latex rules apply
    # a default string will appear if this is omitted
    # make this an empty string to have no footer text
    'footer_string': 'centre test {vstr} {wstr}'
}

for vup in [True, False]:
    vstr = 'vup' if vup else 'vdown'
    for wup in [True, False]:
        wstr = 'wup' if wup else 'wdown'
        main_params['filename'] = myfile
        main_params['title_str'] = f'{vstr} {wstr}'

        # range for the w scale (the middle scale)
        #wvals = [centre(umin, vmin), centre(umin, vmax), centre(umax, vmin), centre(umax, vmax)]
        wvals = [centre(uu,vv) for uu in [umin, umax] for vv in [vmin, vmax]]
        wmin = min(wvals)
        wmax = max(wvals)
        middle_axis['u_min'] = wmin
        middle_axis['u_max'] = wmax
        #print( f"wmin, wmax is {middle_axis['u_min']}, {middle_axis['u_max']}" )

        print( f"calculating the nomogram {vstr} {wstr} ...")
        Nomogen(centre, main_params)  # generate nomogram for the target function

        main_params['filename'] += f'.{vstr}.{wstr}.pdf'
        print("printing ", main_params['filename'], " ...")
        Nomographer(main_params)


        ### check where the w axis intercepts the top & bottom index lines

        if not math.isclose(wmin, 0, abs_tol = 1e-5):
            print( f'************ unexpected w min value, ({wmin}) ************ ' )
            continue

        if not math.isclose(wmax, 1, abs_tol = 1e-5):
            print( f'************ unexpected w max value, ({wmin}) ************ ' )
            continue

        t0 = middle_axis['f'](wmin) # the x coordinate of w at the bottom
        t1 = middle_axis['f'](wmax) # and at the top
        if wup:
            if not math.isclose( t0, 0.4, abs_tol = 1e-6 ):
                print( '*************** w axis inttersects bottom index line,'
                       f' at {t0:.4g}, expected 0.4 *************' )
            if not math.isclose( t1, 0.6, abs_tol = 1e-6 ):
                print( '*************** w axis inttersects top index line,'
                       f' at {t0:.4g}, expected 0.6 *************' )
        else:
            if not math.isclose( t1, 0.4, abs_tol = 1e-6 ):
                print( '*************** w axis inttersects bottom index line,'
                       f' at {t0:.4g}, expected 0.4 *************' )
            if not math.isclose( t0, 0.6, abs_tol = 1e-6 ):
                print( '*************** w axis inttersects top index line,'
                       f' at {t0:.4g}, expected 0.6 *************' )

        print()
