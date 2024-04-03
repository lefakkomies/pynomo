#!/usr/bin/env python3

"""

 generate a nomogram for a simple model of a pension plan:
 - invest an amount (= amt) every month
 - investment grows at 3.5% pa (= i), after inflation + costs
   so, after y years, the total value of the investment is
      total = (12*amt) * ((1 + i)**y - 1) / i
      where i = 3.5
 - at retirement draw an annual pension of 4% of total investment
   so,
      pension = total * 0.04

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
########################################

####################################################
# savings needed per month to achieve required annual pension
#
# - rq is required anual pension
# - y  is years to retirement
# - i  is growth rate
#
#   future value:
#   fv = ((1 + i)**y - 1) / i
#

def amt(rq, y):

    # i = net growth (ie growth above costs + inflation)
    # total =  Total pension pot = 25 * rq
    # y = nr years to retirement
    # amt_pa is yearly contribution

    i = 3.5/100
    total = rq*25   # required future value at retirement

    # invest this much each year to reach total after y years
    amt_pa = (i * total) / ((1+i)**y -1)

    return amt_pa / 12


# range for required pension
rmin = 10
rmax = 50

# range for years to retirement
ymin = 10
ymax = 40

# range for investment per month
amtmin = amt(rmin, ymax)
amtmax = amt(rmax, ymin)
#print(amtmin, amtmax)

###############################################################
#
# nr Chebyshev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve,
# but could be less accurate
NN = 7

##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

left_axis = {
    'u_min': rmin,
    'u_max': rmax,
    'title_x_shift': 1.0,
    'title': r'$pa \enspace pension$',
    'scale_type': 'linear smart',
    'tick_levels': 5,
    'tick_text_levels': 3,
}

right_axis = {
    'u_min': ymin,
    'u_max': ymax,
    'title': r'$years \enspace to \enspace retirement$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

middle_axis = {
    'u_min': amtmin,
    'u_max': amtmax,
    'title': r'$monthly \enspace contribution$',
    'scale_type': 'log smart',
    'tick_levels': 4,
    'tick_text_levels': 2,
}

# group the scales into a block
block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_axis,
    'f2_params': middle_axis,
    'f3_params': right_axis,
    'isopleth_values': [[(left_axis['u_min'] + left_axis['u_max']) / 2, \
                         'x', \
                         (right_axis['u_min'] + right_axis['u_max']) / 2]]
}

# the nomogram parameters
main_params = {
    'filename': __name__ == "__main__" and (
                __file__.endswith(".py") and __file__.replace(".py", "") or "nomogen") or __name__,
    'paper_height': 25,  # units are cm
    'paper_width': 16,
    'title_box_width': 8.0,
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'npoints': NN
}

print("calculating the nomogram ...")
Nomogen(amt, main_params);  # generate nomogram for fv() function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params);
