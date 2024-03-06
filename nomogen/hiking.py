#!/usr/bin/env python3

"""
energy expended while hiking, accounting for slope and speed
use dual scales for speed & energy axes

 https://getpocket.com/explore/item/this-is-how-many-calories-you-burn-on-a-hilly-hike?utm_source=pocket-newtab-global-en-GB

 https://pubmed.ncbi.nlm.nih.gov/30973477/

"""

# pylint: disable=C

import sys

sys.path.insert(0, "..")

from nomogen import Nomogen
from pynomo.nomographer import Nomographer


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
    S *= 10.0 / 36.0
    t1 = 1.94 * S**0.43
    t2 = 0.24*S**4
    t3 = 0.34*S*G*(1-1.05**(1-1.11**(G+32)))

    return 1.44 + t1 + t2 + t3



# range for speed km/hr
Smin = 0.1 * 36 /10        # 0.1 m/s -> km/hr
Smax = 3 * 36 /10          # 3 m/s -> km/hr

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
NN = 15



##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

# km/hr scale of the left axis
left_axis = {
    'tag': 'left',            # link to alternative scale
    'u_min': Smin,
    'u_max': Smax,
    'title': r'$walking \thinspace speed$',
    'extra_titles':[
        {'dx':-2.5,
         'dy':-0.0,
         'text':r'$\small km \thinspace hr^{-1}$',
         'width':5,
         }],
    'scale_type': 'linear smart',
    'tick_levels': 6,
    'tick_text_levels': 3,
    'tick_side': 'left',
}

right_axis = {
    'u_min': Gmin,
    'u_max': Gmax,
    'title': r'$gradient \thinspace \%$',
    'title_x_shift': 0.6,
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
    'tick_side': 'left',
}

middle_axis = {
    'tag': 'middle',            # link to alternative scale
    'u_min': EEmin,
    'u_max': EEmax,
    'title': r'$\small Wkg^{-1}$',
    'title_draw_center': True,
    'title_distance_center': -1.5,
    'extra_titles':[
        {'dx':-2.0,
         'dy':0.25,
         'text': r'$Expended \thinspace energy$',
         }],
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
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
    'isopleth_values': [[7, 'x', 0]]
}


######## the second scales ##############

# mph scale for left axis

km_per_mile = 63360 * 25.4 * 1e-6 # inches per mile * mm per inch * km per mm = 1.609344
left_axis_mph = {
    'tag': 'left',
    'u_min': left_axis['u_min'] / km_per_mile,
    'u_max': left_axis['u_max'] / km_per_mile,
    'extra_titles':[
        {'dx':-0.1,
         'dy':0.0,
         'text':r'$\small mph$',
         }],
    'align_func': lambda m: m*km_per_mile,
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
    'tick_side': 'right'
}

block_1_params={
    'block_type':'type_8',
    'f_params': left_axis_mph,
    'isopleth_values':[['x']],
}


# calorie scale for middle axis

# 1 nutrition calorie Cal 	= 4186.80 	joules J
# 1 kg = 2.20462262 lbs
# kilo-calories per hour for 70kg hiker

# weight of hiker in kg & lbs
wkg = 80
wlbs = round(80*2.20462262)

watts_per_calph = 4186.80*1000/wkg/3600

middle_axis_cal = {
    'tag': 'middle',
    'u_min': middle_axis['u_min'] / watts_per_calph,
    'u_max': middle_axis['u_max'] / watts_per_calph,
    'title':r'$\small kcal/hr ({}kg/{}lbs)$'.format(wkg,wlbs),
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
    'f_params': middle_axis_cal,
    'isopleth_values':[['x']],
}


# the nomogram parameters
main_params = {
    'filename': __name__ == "__main__" and (
                __file__.endswith(".py") and __file__.replace(".py", "") or "nomogen") or __name__,
    'paper_height': 24,  # units are cm
    'paper_width': 16,
    'title_x': 7.0,
    'title_y': 1.0,
    'title_box_width': 8.0,
    'title_str': r'$energy \thinspace expended \thinspace hiking$',

    # first block is the type_9 nomogram, the dual scale type_8 blocks follow
    'block_params': [block_params0, block_1_params, block_2_params],

    'transformations': [('scale paper',)],
    'muShape': 0,
    'npoints': NN,

    # text to appear at the foot of the nomogram
    # make this null string for nothing
    # a default string will appear if this is omitted
#    'footer_string': r'$\tiny test1 \enspace project \enspace configuration \enspace string$'
}

print("calculating the nomogram ...")
Nomogen(EE, main_params)  # generate nomogram for EE function


main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
