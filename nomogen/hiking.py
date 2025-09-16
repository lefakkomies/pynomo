#!/usr/bin/env python3

"""
energy expended while hiking, accounting for slope and speed
use dual scales for speed & energy axes

references:
 https://getpocket.com/explore/item/this-is-how-many-calories-you-burn-on-a-hilly-hike
 https://pubmed.ncbi.nlm.nih.gov/30973477/

"""

# pylint: disable=C
import sys

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
#  - the function that the nonogram implements
#  - add the limits of the variables below
#
#  format is m = m(l,r), where l, m & r are respectively the values
#                        for the left, middle & right hand axes
#
#
########################################

"""
return energy expended W/kg of body mass
S is  walking speed km/hr
G is  gradient %
"""


def EE(S,G):

    # S is km/hr, need m/s
    S *= 1000.0 / 3600.0
    t1 = 1.94 * S**0.43
    t2 = 0.24*S**4
    t3 = 0.34*S*G*(1-1.05**(1-1.11**(G+32)))

    return 1.44 + t1 + t2 + t3


# range for speed km/hr
# note that Smin = 0 is invalid in the function EE
# nomogen evaluates derivatives by calculating
# the function marginally beyond the Smin..Smax range
Smin = 0.1 * 3600 / 1000      # m/s -> km/hr
Smax = 3 * 3600 / 1000          # m/s -> km/hr

# range for slope
Gmax = +25
Gmin = -Gmax

# range for energy expended
EEmin = 1.44 #EE(Smin, Gmin)
EEmax = EE(Smax, Gmax)


###############################################################
#
# nr Chebyshev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value is faster, makes a smoother curve,
#     but could be less accurate
NN = 16



##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

# km/hr scale of the speed axis
speed_axis = {
    'tag': 'speed',            # link to alternative scale
    'u_min': Smin,
    'u_max': Smax,
    'title': 'walking speed',
    'extra_titles':[
        {'dx':-2.5,
         'dy':-0.0,
         'text':r'$km \thinspace hr^{-1}$',
         'width':5,
         }],
    'scale_type': 'linear smart',
    'tick_levels': 6,
    'tick_text_levels': 3,
    'tick_side': 'left',
}

gradient_axis = {
    'u_min': Gmin,
    'u_max': Gmax,
    'title': 'gradient %',
    'title_x_shift': 0.6,
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
    'tick_side': 'left',
}

energy_axis = {
    'tag': 'energy',            # link to alternative scale
    'u_min': EEmin,
    'u_max': EEmax,
    'title': r'$W kg^{-1}$',
    'title_draw_center': True,
    'title_distance_center': -1.5,
    'extra_titles':[
        {'dx':-2.0,
         'dy':0.25,
         'text': r'Expended energy',
         }],
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
    'tick_side': 'left',
}

# assemble the above 3 axes into a block
block_params0 = {
    'block_type': 'type_9',
    'f1_params': speed_axis,     # left axis
    'f2_params': energy_axis,    # middle
    'f3_params': gradient_axis,  # right

    # the isopleth connects the mid values of the outer axes
    # edit this for different values
    'isopleth_values': [[(Smin+Smax)/2, 'x', 0]],

    # log alignment errors
    # If this is missing or False then alignment error logs are disabled
    'LogAlignment': True,
}


######## the second scales ##############

# mph scale for speed axis

km_per_mile = 63360 * 25.4 * 1e-6 # inches per mile * mm per inch * km per mm = 1.609344
speed_axis_mph = {
    'tag': 'speed',
    'u_min': speed_axis['u_min'] / km_per_mile,
    'u_max': speed_axis['u_max'] / km_per_mile,
    'extra_titles':[
        {'dx':-0.1,
         'dy':0.0,
         'text':r'$mph$',
         }],
    'align_func': lambda m: m*km_per_mile,
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
    'tick_side': 'right'
}

block_1_params={
    'block_type':'type_8',
    'f_params': speed_axis_mph,
    'isopleth_values':[['x']],
}


# calorie scale for energy axis

# 1 nutrition calorie Cal 	= 4186.80 	joules J
# 1 kg = 2.20462262 lbs
# kilo-calories per hour for 70kg hiker

# weight of hiker in kg & lbs
wkg = 80
wlbs = round(80*2.20462262)

watts_per_calph = 4186.80*1000/wkg/3600

energy_axis_cal = {
    'tag': 'energy',
    'u_min': energy_axis['u_min'] / watts_per_calph,
    'u_max': energy_axis['u_max'] / watts_per_calph,
    'title':r'$kcal/hr ({}kg/{}lbs)$'.format(wkg,wlbs),
    'title_distance_center': 2.0,
    'title_draw_center': True,
    'align_func': lambda c: c*watts_per_calph,
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 1,
    'tick_side': 'right'
}

block_2_params={
    'block_type':'type_8',
    'f_params': energy_axis_cal,
    'isopleth_values':[['x']],
}


# the nomogram parameters
main_params = {
    'filename': myfile,
    'paper_height': 24,  # units are cm
    'paper_width': 16,
    'title_x': 7.0,
    'title_y': 1.0,
    'title_box_width': 8.0,
    'title_str': r'energy expended hiking',

    # first block is the type_9 nomogram, the dual scale type_8 blocks follow
    'block_params': [block_params0, block_1_params, block_2_params],

    'transformations': [('scale paper',)],
    'isopleth_params': [{'color': 'Red'}],

    # instead of forcing the ends of the axes to the corners of the unit square,
    # nomogen can shape the nomogram to minimise parallax errors
    # uncomment the following line to select this option
    'muShape': 1,
    'npoints': NN,

    # the trace parameter can be set to enable tracing various phases
    # of generating the nomogram
    #'trace': 'trace_result',

    # text to appear at the foot of the nomogram
    # make this null string for nothing
    # a default string will appear if this is omitted
#    'footer_string': r'hiking project configuration string'
}

print("calculating the nomogram ...")
Nomogen(EE, main_params)  # generate nomogram for EE function


main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
