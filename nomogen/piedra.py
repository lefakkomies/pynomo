#!/usr/bin/env python3

# reference:
# https://victoryepes.blogs.upv.es/2023/02/

# pylint: disable=C

import sys

sys.path.insert(0, "..")

# se ha modificado la siguiente linea que era 'from nomogen.nomogen import Nomogen' para que se ejecute bien.

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

#####################################################
# Ecuacion de la piedra:
# return piedra, V en (m)
# RC = Resistencia compresion roca (MPa)
# D = Diametro barreno (mm))
def piedra(RC, D):
    return (0.19+((120-RC)/2000))*(D**0.63)


RCmin = 10
RCmax = 250
Dmin = 50
Dmax = 450

Vmax = piedra(RCmax, Dmax)
Vmin = piedra(RCmin, Dmin)

###############################################################
#
# nr Chebyshev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve,
#    but could introduce errors
NN = 7


##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

# MPa side of a dual scale line
left_axis = {
    'tag': 'left',               # link to psi side
    'u_min': RCmin,
    'u_max': RCmax,
    'title': r'$RC$',
    'title_x_shift': 0.1,
    'title_y_shift': 0.5,
    'extra_titles':[             #  extra title for units
        {'dx':-1.3,
         'dy':0.11,
         'text': r'$\small MPa$',
         'width':5,
         }],
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'tick_side': 'left',
}

right_axis = {
    'tag': 'right',
    'u_min': Dmin,
    'u_max': Dmax,
    'title': r'$D$',
    'title_x_shift': 0.1,
    'title_y_shift': 0.5,
    'extra_titles':[             #  extra title for units
        {'dx':-1.3,
         'dy':0.11,
         'text': r'$\small in$',
         'width':5,
         }],
    'scale_type': 'log smart',
    'tick_levels': 4,
    'tick_text_levels': 3,
    'tick_side': 'right',
}

middle_axis = {
    'tag': 'middle',
    'u_min': Vmin,
    'u_max': Vmax,
    'title': r'$V$',
    'extra_titles':[
        {'dx':-1.4,
         'dy':0.11,
         'text':r'$\small m$',
         'width':5,
         }],
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'tick_side': 'left',
}

block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_axis,
    'f2_params': middle_axis,
    'f3_params': right_axis,
    'isopleth_values': [[RCmin+(RCmax-RCmin)/12, 'x', Dmin+(Dmax-Dmin)/8]],
}


######## the second scales ##############
# this is another type 9 nomogram with the axes overlaid on the above nomogram

#conversion factors
psi_per_MPa = 145.038/1000
mm_per_inch = 25.4
feet_per_metre = 1000/25.4/12 # mm per metre / mm per inch / inches per foot


left_axis_psi = {
    'tag': 'left',
    'u_min': left_axis['u_min'] * psi_per_MPa,
    'u_max': left_axis['u_max'] * psi_per_MPa,
    'extra_titles':[
        {'dx':-0.1,
         'dy':0.11,
         'text':r'$\small psi$',
         'width':5,
         }],
    'align_func': lambda u: u / psi_per_MPa,
    'scale_type': 'linear smart',
    'text_format':r"$%3.0fk$",
    'tick_levels': 5,
    'tick_text_levels': 3,
    'tick_side': 'right',
}

right_axis_in = {
    'tag': 'right',
    'u_min': Dmin/mm_per_inch,
    'u_max': Dmax/mm_per_inch,
    'extra_titles':[
        {'dx':-0.1,
         'dy':0.11,
         'text':r'$\small mm$',
         'width':5,
         }],
    'align_func': lambda u: u * mm_per_inch,
    'scale_type': 'log smart',
    'tick_levels': 4,
    'tick_text_levels': 3,
    'tick_side': 'left',
}


middle_axis_feet = {
    'tag': 'middle',
    'u_min': middle_axis['u_min'] * feet_per_metre,
    'u_max': middle_axis['u_max'] * feet_per_metre,
    'extra_titles':[
        {'dx':-0.1,
         'dy':0.11,
         'text':r'$\small ft$',
         'width':5,
         }],
    'align_func': lambda u: u / feet_per_metre,
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
    'tick_side': 'right',
}


block_1_params={
    'block_type':'type_9',
    'f1_params': left_axis_psi,
    'f2_params': middle_axis_feet,
    'f3_params': right_axis_in,
    'isopleth_values': [[ 'x','x','x' ]]
}


main_params = {
    'filename': 'piedra',
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 4.0,
    'title_y': 9.0,
    'title_box_width': 8.0,
    'title_str': r'$piedra \thinspace en \thinspace voladuras$',
    'extra_texts': [
        {'x': 2,
         'y': 8,
         'text': r'$V=({0.19+({{{120-RC}\over{2000}}})})\times D^{0.63}$',
         'width': 6,
         }],

    # first block is the type_9 nomogram, the dual scale type_9 block follows
    'block_params': [block_params0, block_1_params],

    'transformations': [('scale paper',)],
    'npoints': NN
}

print("calculating the nomogram ...")
Nomogen(piedra, main_params)  # generate nomogram for function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)

sys.exit()

# check function for both sides of dual scales:
for i in [left_axis, left_axis_psi, right_axis, right_axis_in]:
    for k in range(11):
        t = i['u_min']*(10-k)/10 + i['u_max']*k/10
        if 'f' in i:
            print( i['tick_side'], ",", ":", t, i['f'](t), i['g'](t) )
        elif 'function_x' in i:
            print( i['tick_side'], ",", ":", t, \
                   i['function_x'](t), i['function_y'](t) )
        else:
            print( "'f' not in ", i['tick_side'] )




