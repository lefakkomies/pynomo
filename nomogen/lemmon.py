#!/usr/bin/python3

# Lemmon equations
# "Revised Standardized Equation for Hydrogen Gas Densities for Fuel Consumption Applications"
# Journal of Research of the National Institute of Standards and Technology, 2008 Nov-Dec; 113(6): 341–350.
# Eric W. Lemmon, Jacob W. Leachman and Marcia L. Huber

import sys

sys.path.insert(0, "..")

from nomogen import Nomogen
from pynomo.nomographer import Nomographer

import math

# Constants associated with the density equation for normal hydrogen
# i       ai	         bi	ci
# 1  0.058 884 60	1.325	1.0
# 2 −0.061 361 11	1.87	1.0
# 3 −0.002 650 473	2.5	2.0
# 4  0.002 731 125	2.8	2.0
# 5  0.001 802 374	2.938	2.42
# 6 −0.001 150 707	3.14	2.63
# 7  0.958 852 8 × 10−4	3.37	3.0
# 8 −0.110 904 0 × 10−6	3.75	4.0
# 9  0.126 440 3 × 10−9	4.0	5.0

a = [0.05888460, -0.06136111, -0.002650473, 0.002731125, 0.001802374, -0.001150707, 0.9588528E-4, -0.1109040E-6,
     0.1264403E-9]

b = [1.325, 1.87, 2.5, 2.8, 2.938, 3.14, 3.37, 3.75, 4.0]

c = [1.0, 1.0, 2.0, 2.0, 2.42, 2.63, 3.0, 4.0, 5.0]

M = 2.01588  # Molar Mass, g/mol
R = 8.314472  # Universal Gas Constant,  J/(mol · K)


# p pressure in mPa
# T degrees K
def Z(p, T):
    s = 1
    for i in range( len(a) ):
        s = s + a[i] * (100 / T) ** b[i] * (p) ** c[i]
    return s


pmin = 1
pmax = 200
Tmin = 200
Tmax = 500
Zmin = 1
Zmax = Z(pmax, Tmin)


# Test points for validating
# T(K)	p(MPa)	    Z	         ρ (mol/1)
# 200	  1	1.00675450	0.59732645
# 300	  10	1.05985282	3.78267048
# 400	  50	1.24304763	12.09449023
# 500	  200	1.74461629	27.57562673
# 200	  200	2.85953449	42.06006952

correct = True
if not math.isclose(Z(1, 200), 1.00675450, abs_tol=5e-09):
    print("Z(1,200) fails")
    correct = False

if not math.isclose(Z(10, 300), 1.05985282, abs_tol=5e-09):
    print("Z(10,300) fails")
    correct = False

if not math.isclose(Z(50, 400), 1.24304763, abs_tol=5e-09):
    print("Z(50,400) fails")
    correct = False

if not math.isclose(Z(200, 500), 1.74461629, abs_tol=5e-09):
    print("Z(200,500) fails")
    correct = False

if not math.isclose(Z(200, 200), 2.85953449, abs_tol=5e-09):
    print("Z(200,200) fails")
    correct = False

if not correct:
    # print(  Z(1,200), Z(10,300), Z(50,400), Z(200,500), Z(200,200) )
    print("test points for Z(p,T) failed")
    sys.exit()


###############################################################
#
# nr Chebychev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors
NN = 9

##############################################
#
# definitions for the scales for pyNomo
# dictionary with key:value pairs

left_scale = {
    'u_min': pmin,
    'u_max': pmax,
    'title': r'$pressure \enspace MPa$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'tick_side' : 'left',
    'grid': False
}

right_scale = {
    'u_min': Tmin,
    'u_max': Tmax,
    'title': r'$Temperature \enspace ^\circ K$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'tick_side' : 'left',
    'grid': False
}

middle_scale = {
    'u_min': Zmin,
    'u_max': Zmax,
    'title': r'$Z$',
    'scale_type': 'log smart',
    'tick_levels': 6,
    'tick_text_levels': 5,
    'tick_side' : 'right',
    'grid': False
}

block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_scale,
    'f2_params': middle_scale,
    'f3_params': right_scale,
    'transform_ini': False,
    'isopleth_values': [[(left_scale['u_min'] + left_scale['u_max']) / 2, \
                         'x', \
                         (right_scale['u_min'] + right_scale['u_max']) / 2]]
}

main_params = {
    'filename': __name__ == "__main__" and (
                __file__.endswith(".py") and __file__.replace(".py", "") or "nomogen") or __name__,
    'paper_height': 25,  # units are cm
    'paper_width': 18,
    'title_x': 9.0,
    'title_y': 3.0,
    'title_box_width': 8.0,
    'title_str': r'$\Large Z = {p \over {\rho R T}}$',
    'extra_texts': [
        {'x': 6,
         'y': 4,
         'text': r'$compressibility \thinspace factor \thinspace for \thinspace hydrogen$',
         'width': 10,
         }],
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'pdegree': NN
}

print("calculating the nomogram ...")
Nomogen(Z, main_params)  # generate nomogram for yrs function
middle_scale.update({'tick_side': 'left'})

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)
