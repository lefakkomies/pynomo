#!/usr/bin/python3

import sys

import math;
import numpy as np;
import scipy;
import scipy.optimize;
from scipy import integrate;

from pynomo.nomographer import Nomographer

# enable logging
# "trace_init" "trace_circ" "trace_cost" "trace_alignment"
log = { "trace_init" };
#log = True;

########################################
#
#  this is the target function,
#  - the limits of the variables
#  - the function that the nonogram implements
#  - the width & height of the nomogram (in mm)
#  - nr nodes to use
#
########################################

# print size, in mm
width  = 100;
height = 100;

#colebrook equation, friction in pipes:
# return relative roughness, k/D
# Re = Reynolds nr
# f = friction coefficient
class colebrook0:
    def colebrook(f, Re):
        sqrtf = math.sqrt(f)
        return 3.72*(10**(-0.5/sqrtf) - 2.51/Re/sqrtf)
    def func(self,u,v):
        return colebrook0.colebrook(u,v)
    NN = 7
    fmin = 0.018; fmax = 0.024;
    Remin = 1e5; Remax = 1.5e5;
    kondmin = 0.00010; kondmax = 0.0006;
    umin = fmin; umax = fmax;
    vmin = Remin; vmax = Remax;
    def __init__(self):
        self.wmax = colebrook0.colebrook(self.umax, self.vmax);
        self.wmin = colebrook0.colebrook(self.umin, self.vmin);

# similar to above, but f is implicit
# so use a loop to solve for f numerically
class colebrook1:
    def colebrook(kond, Re):
        f = 0.02
        for i in range(5): # loop 5 times
            sqrtf = math.sqrt(f)
            t = -2 * math.log10(2.51/(Re*sqrtf) + kond/3.72)
            f = 1/(t*t)
#            print("f is ", f)
        return f
    def func(self,u,v):
        return colebrook1.colebrook(u,v)
    NN = 7
    Remin = 1e5; Remax = 1.5e5;
    kondmin = 0.000010; kondmax = 0.0018;
    fmin = 0.01; fmax = 0.024;
    umin = kondmin; umax = kondmax;
    vmin = Remin; vmax = Remax;
    def __init__(self):
        self.wmax = colebrook1.colebrook(self.umax, self.vmin);
        self.wmin = colebrook1.colebrook(self.umin, self.vmax);


###############################################
#
# from Allcock & Jones, example xv, p112..117
# "the classical example of a nomogram consisting of three curves ..."
# Load on a retaining wall
# (1+L)*h**2 - L*h*(1+p) - (1-L)*(1+2*p)/3 == 0
#
def AJcheck(L,h,p):
    return (1+L)*h**2 - L*h*(1+p) - (1-L)*(1+2*p)/3

class AJh:
    def h(L,p):
        a = 1+L;
        b = -L*(1+p)
        c = -(1-L)*(1+2*p)/3
        h = ( -b + math.sqrt(b**2 - 4*a*c) ) / (2*a)
        #print("result is ", (1+L)*h**2 - L*h*(1+p) - (1-L)*(1+2*p)/3)
        if abs(AJcheck(L,h,p)) > 1e-10:
            print("AJh equation failed")
            sys.exit("quitting")
        return h
    def func(self,u,v):
        return AJh.h(u,v)
    NN = 9
    umin = 0.5; umax = 1.0;
    vmin = 0.5; vmax = 1.0;
    def __init__(self):
        self.wmin = AJh.h(self.umax, self.vmin);
        self.wmax = AJh.h(self.umin, self.vmax);

class AJp:
    # this version has inverted w & v scales
    # produces nearly linear scales
    def p(L,h):
        p = ( (1+L)*h**2 - L*h - (1-L)/3 )/( L*h + 2*(1-L)/3 )
        #print("result is ", (1+L)*h**2 - L*h*(1+p) - (1-L)*(1+2*p)/3)
        if abs(AJcheck(L,h,p)) > 1e-10:
            print("AJp equation failed")
            sys.exit("quitting")
        return p
    def func(self,u,v):
        return AJp.p(u,v)
    NN = 9
    umin = 0.5; umax = 1.0;
    vmin = 0.75; vmax = 1.0;
    def __init__(self):
        self.wmin = AJp.p(self.umin, self.vmin);
        self.wmax = AJp.p(self.umin, self.vmax);


#########################################################
# resistors in parallel, focal length, etc
class recip:
    def func(self,u,v):
        return 1/(1/u + 1/v)
    NN = 5
    umin = 5; umax = 10;
    vmin = 6; vmax = 12;
    wmin = 30/11; wmax = 120/22;


########################################
# example taken from "Creating Nomograms with the PyNomo Software", Ron Doerfler
class RD:
    def func(self,u,v):
        return  0.74 * v * (u + 0.64)**0.58
    NN = 5
    umin = 1; umax = 3.5;
    vmin = 1; vmax = 2;
    wmin = 0.986; wmax = 3.374;
    def __init__(self):
        self.wmin = self.func(self.umin, self.vmin);
        self.wmax = self.func(self.umax, self.vmax);


# simple example
class sq:
    def func(self,u,v):
        return (u*v)**2 / 2
    NN = 11
    umin = 2; umax = 10;
    vmin = 1; vmax = 5;
    def __init__(self):
        self.wmin = self.func(self.umin, self.vmin);
        self.wmax = self.func(self.umax, self.vmax);

###############################################
# pendulum example
# from Allcock & Jones, example xii, p93
class pendulum:
    def func(self,u,v):
        return (v**2 + u**2)/(u+v)
    NN = 7
    umin = 0.25; umax = 1;
    vmin = 0.25; vmax = 1;
    def __init__(self):
        self.wmin = self.func(self.umin, self.vmin);
        self.wmax = self.func(self.umax, self.vmax);


###################
# exponential growth: investments, epidemics, etc
class roi:
    def func(self,u,v):
        # u = % rate pa, v = nr years
        i = u/100
        return (1 + i/365) ** (365*v)
    NN = 11
    umin = 1   ; umax = 5
    vmin = 1   ; vmax = 5
    def __init__(self):
        self.wmin = self.func(self.umin, self.vmin);
        self.wmax = self.func(self.umax, self.vmax);


####################################################
# future value of $1 invested each year
class fv:
    def func(self,u,v):
        # u = % rate pa, v = nr years
        i = u/100
        return (((1 + i) ** v) - 1)/i
    NN = 9
    umin = 0.5; umax = 5
    vmin = 1;   vmax = 20
    def __init__(self):
        self.wmin = self.func(self.umin, self.vmin);
        self.wmax = self.func(self.umax, self.vmax);

# nr years to achieve value v ...
class yrs:
    def func(self,u,v):
        # v = % rate pa, u = fv
        i = v/100
        fv = u
        y = math.log(fv*i + 1)/math.log(i+1)
        if abs((((1 + i) ** y) - 1)/i - u) > 1e-10:
            print("yrs: equation fault, y = ", y, ", i is ", i, ", fv is ", fv);
            sys.exit("quitting")
        return y

    NN = 11
    umin = 1;   umax = 33
    vmin = 0.5; vmax = 5
    def __init__(self):
        self.wmin = self.func(self.umin, self.vmin);
        self.wmax = self.func(self.umax, self.vmin);


testNomo = yrs()

def w(u,v):
    return testNomo.func(u,v)

umin = testNomo.umin; umax = testNomo.umax
vmin = testNomo.vmin; vmax = testNomo.vmax
wmin = testNomo.wmin; wmax = testNomo.wmax

# NN = nr Chebychev nodes for the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors
# the nodes have an index in the range 0 .. NN-1
NN = testNomo.NN

if NN % 2 == 0:
    NN = NN+1
    print("nr In this program, the number of Chebychev nodes must be odd, using ", NN, " nodes");

if "trace_init" in log:
    print("wmax is", wmax, ", wmin is ", wmin)

#sanity checks
if umax < umin:
    sys.exit("error: umax is less than umin")
if vmax < vmin:
    sys.exit("error: vmax is less than vmin")
if wmax < wmin:
    sys.exit("error: wmax is less than wmin")
wvalue = w(umin, vmin)
if wvalue < wmin:
    print( "w(umin, vmin) = ", wvalue, " is less than wmin");
    sys.exit("quitting")
if wvalue > wmax:
    print( "w(umin, vmin) = ", wvalue, " is greater than wmax");
    sys.exit("quitting")
wvalue = w(umax, vmin)
if wvalue < wmin:
    print( "w(umax, vmin) = ", wvalue, " is less than wmin");
    sys.exit("quitting")
if wvalue > wmax:
    print( "w(umax, vmin) = ", wvalue, " is greater than wmax");
    sys.exit("quitting")
wvalue = w(umin, vmax)
if wvalue < wmin:
    print( "w(umin, vmax) = ", wvalue, " is less than wmin");
    sys.exit("quitting")
if wvalue > wmax:
    print( "w(umin, vmax) = ", wvalue, " is greater than wmax");
    sys.exit("quitting")
wvalue = w(umax, vmin)
if wvalue < wmin:
    print( "w(umax, vmax) = ", wvalue, " is less than wmin");
    sys.exit("quitting")
if wvalue > wmax:
    print( "w(umax, vmax) = ", wvalue, " is greater than wmax");
    sys.exit("quitting")


# allow nomogram tolerance == +/- 0.1 mm
# this is how many dots 0.1mm square fit into the nomogram area
resolution = 10*10 * width * height;

#######################################
#
# these arrays define the x & y coordinates of the u, v & w scales
#
# the nomogram is built inside a unit square, to be scaled at the point of output.

#unodes = np.array([umin + (umax-umin)/2 * (1 - math.cos(math.pi*k/(NN-1))) for k in range(0, NN)]);
unodes = umin + (umax-umin)/2 * (1-np.cos(np.linspace(0,math.pi,NN)))
vnodes = vmin + (vmax-vmin)/2 * (1-np.cos(np.linspace(0,math.pi,NN)))
wnodes = wmin + (wmax-wmin)/2 * (1-np.cos(np.linspace(0,math.pi,NN)))

if "trace_init" in log:
    print("unodes is ", unodes);
    print("vnodes is ", vnodes);
    print("wnodes is ", wnodes);

# the coordinates,
# the initial condition is a nomogram where
# - the u & v scales vary linearly from (0,0) to (0,1) along the
#   left and right edges of the unit square
# - the w scale lies between these 2
# the strategy is the optimiser will make the nomogram more accurate while
# still keeping a working solution

# the u scale has umax at the top, but which way up are the w & v scales?
w0 = w(umin, vmin);
w1 = w(umax, vmin);
w2 = w(umin,vmax);

# w scale is max up (aligned to u scale) iff w1 > w0
# v scale is max up (aligned to u scale) iff (w1 > w0) xor (w2 > w0)

ux = np.zeros(NN);
uy = (1 - np.cos(np.linspace(0,math.pi,NN)))/2;
vx = np.ones(NN);
if (w1>w0) == (w2>w0):
    # vmax is at the top
    vtop, vbottom  = vmax, vmin
    vy = (1 - np.cos(np.linspace(0,math.pi,NN)))/2;
    vyInit = 0
else:
    vtop, vbottom  = vmin, vmax
    vy = (1 - np.cos(np.linspace(math.pi,0,NN)))/2;
    vyInit = 1

wB = w(umin, vbottom)
wE = w(umax, vtop)
wG = w(umax, vbottom)
wH = w(umin, vtop)

# guess an initial position and slope for the wx scale
if "trace_init" in log:
    print("wB is ", wB, ", wE is ", wE, "wG is ", wG, ", wH is ", wH)
    if wG == wH:
        wxB = wxE = 0.5
    else:
        alphawx = (wE - wG - wH + wB) / (wE - wB) / (wG - wH)
        wxB = (wH - wB) / (wE - wB) - alphawx * (wH - wB)
        wxE = wxB + alphawx*(wE - wB)
if "trace_init" in log:
    print("wxB is ", wxB, ", wxE is ", wxE)

if wE > wB:
    wy = (1 - np.cos(np.linspace(0,math.pi,NN)))/2;
else:
    wy = (1 - np.cos(np.linspace(math.pi,0,NN)))/2;

if True:
    # clip to unit square
    if wxE > 1:
        wxE = 1
    elif wxE < 0:
        wxE = 0
    if wxB > 1:
        wxB = 1
    elif wxB < 0:
        wxB = 0
    #wx =  np.array([wxB + ((wxE-wxB)/(wmax-wmin))*(wnodes[k]-wmin) for k in range(0, NN)]);
    wx = wxB + (wnodes.copy() - wmin)*(wxE-wxB)/(wmax-wmin)

else:
    # under development ...
    if "trace_init" in log:
        print( "trying quadratic approximation for wx" )
    R = (wE - wG - wH + wB)/(wG-wH)/(wE-wB)
    S = 2*wB - wG - wH
    P = (wH - wB)*(1/(wE-wB) - R)
    Q = -(wH-wB)*(S + (wH-wB))

    if R != alphawx:
        print("R evaluation problem")
        sys.exit("quitting");
    if P != wxB:
        print("P evaluation problem")
        sys.exit("quitting");

    # test solution
    for b in [-2, -1, 0, 1, 2]:
        c = P + Q*b
        alphawx = R + S*b
        t1 = c + (wH-wB)*(alphawx + b*(wH-wB)) - (wH-wB)/(wE-wB)
        if abs(t1) > 1e-12:
            print("eqn1 evaluation problem for b = ", b)
            sys.exit("quitting")
        t1 = c + (wG-wB)*(alphawx + b*(wG-wB)) - 1 + (wG-wB)/(wE-wB)
        if abs(t1) > 1e-12:
            print("eqn2 evaluation problem for b = ", b)
            sys.exit("quitting")

    bmin = -P/Q
    bmax = (1-P)/Q
    if "trace_init" in log:
        print("wB constraint -> bmin is ", bmin, ", bmax is ", bmax);
    t = -(P + R*(wE-wB))/(Q + (wE-wB)*(S + wE - wB))
    if "trace_init" in log:
        print("wE constraint -> bmin is ", t);
    if t > bmin:
        bmin = t
    t = (1 - P - R*(wE-wB))/(Q + (wE-wB)*(S + wE - wB))
    if "trace_init" in log:
        print("wE constraint -> bmax is ", t);
    if t < bmax:
        bmax = t

    b = (bmin + bmax)/2
    alphawx = R + b*S
    c = P + Q*b
    if "trace_init" in log:
        print("c is ", c, ", alphawx is ", alphawx, ", b is ", b)

    if bmin > bmax:
        print("bmin > bmax, quadratic approximation is not feasible, bmin is ", bmin, ", bmax is ", bmax);
        wxB = c
        wxE = c + (wE-wB)*(alphawx + b*(wE-wB))
        print("wxB is ", wxB, ", wxE is ", wxE)
        # rescale from wxB .. wxE -> 0.05 .. 0.95
        if wxE > wxB:
            wx =  np.array([0.05 + (0.9/(wxE-wxB))*(c + (wnodes[k]-wmin)*(alphawx + b*(wnodes[k]-wmin)) - wxB) for k in range(0, NN)]);
        else:
            wx =  np.array([0.95 - (0.9/(wxE-wxB))*(c + (wnodes[k]-wmin)*(alphawx + b*(wnodes[k]-wmin)) - wxB) for k in range(0, NN)]);
    else:
        wx =  np.array([c + (wnodes[k]-wmin)*(alphawx + b*(wnodes[k]-wmin)) for k in range(0, NN)]);

if "trace_init" in log:
    print("wx is ", wx)

#################################################
#
# evaluate function at a, given an array of Chebyshev nodes and function values
# an  - array of nodes
# fan - array of values at the nodes an
# perform barycentric interpolation at a ...

def evaluate(a, an, fan):
    if a in an:
        return fan[np.searchsorted(an,a)];

    max = len(an)-1;
    sumA = (fan[0]/(a-an[0]) + fan[max]/(a-an[max]))/2;
    sumB = (1/(a-an[0]) + 1/(a-an[max]))/2;
    for k in range(0, max+1):
        t = 1/(a-an[k]);
        sumA = t*fan[k] - sumA;
        sumB = t - sumB;
    return sumA / sumB;


########################################################
#
# differentiate the function defined by
# xn  = Chebyshev nodes
# fxn = values at nodes
# return array of value of derivative at each of the nodes
#
def differentiate( xn, fxn ):
    n = len(xn);
    dfx = [0] * n;
    for i in range(n):
        ldj = [0]*n;
        for j in range(n):
            if i != j:
                if ((j+i) % 2) == 0:
                    ldj[j] = + 1/(xn[i] - xn[j])
                else:
                    ldj[j] = - 1/(xn[i] - xn[j])
                if i==0 or i==n-1:
                    # adjust for weights of first and last elements
                    ldj[j] *= 2;
                    # another adjustment
                    # these values should be zero anyway when i=0 or i=n-1
        if i != 0:
            ldj[0] /= 2;
        if i != n-1:
            ldj[n-1] /= 2;

        # the ith element is -ve sum of all the others...
        for j in range(n):
            if j != i:
                ldj[i] -= ldj[j];

        for j in range(n):
            dfx[i] += ldj[j] * fxn[j];

    return dfx;



##############################################
#
# definitions for the scales for pyNomo

  # the u scale
  # dictionary with key:value pairs
params_u = {
    'u_min': umin,
    'u_max': umax,
    'f': lambda u: evaluate(u, unodes, ux),
    'g': lambda u: evaluate(u, unodes, uy),
    'h': lambda u: 1.0,
    'title': r'$u scale$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False}

params_v = {
    'u_min': vmin,
    'u_max': vmax,
    'f': lambda u: evaluate(u, vnodes, vx),
    'g': lambda u: evaluate(u, vnodes, vy),
    'h': lambda u: 1.0,
    'title': r'$v scale$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

params_w = {
    'u_min': wmin,
    'u_max': wmax,
    'f': lambda u: evaluate(u, wnodes, wx),
    'g': lambda u: evaluate(u, wnodes, wy),
    'h': lambda u: 1.0,
    'title': r'$w scale$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False}


block_params = {
    'block_type': 'type_9',
    'f1_params': params_u,
    'f2_params': params_w,
    'f3_params': params_v,
    'transform_ini': False,
    'isopleth_values': [[math.sqrt(umin*umax), w(math.sqrt(umin*umax), math.sqrt(vmin*vmax)), math.sqrt(vmin*vmax)]]
}

main_params = {
    'filename': 'nomogen.pdf',
    'paper_height': height/10, # units appear to be cm
    'paper_width': width/10,
    'block_params': [block_params],
    'transformations': [('scale paper',)]
}



##############################################
#
# determine accuracy of a scale line
# - find the distance between an index line and
#   the corresponding point on the w scale line
#
# the index line is defined by the iu- & iv- th node points on the u & v scale lines
# the error is the square of the distance

def accuracy(iu, iv):
    tux = ux[iu];
    tuy = uy[iu];
    tvx = vx[iv];
    tvy = vy[iv];

    w1 = w(unodes[iu], vnodes[iv]);
    wx1 = evaluate(w1, wnodes, wx);
    wy1 = evaluate(w1, wnodes, wy);

    d2 = (tux - tvx)**2 + (tuy - tvy)**2;
    if d2*resolution <= 1:
        print( "u & v scale lines touch or cross at (", tux, ",", tuy, ")" );
        errsq = 0;
    else:
        errsq = ((tux - tvx)*(tuy - wy1) - (tux - wx1)*(tuy - tvy)) / d2;
    return errsq;



########################################
#
# calculate anti-clockwise circular integral for scales A & B,
# and the straight lines joinong them
#
# arguments are nodes and values of the scale lines
#
def calcAB(An, Ax, Ay, Bn, Bx, By):

    # choose fd st curl fd() == fc(), (par F2/ par x) - (par F1/ par y) == fc()
    def fd(x,y):
        #        return -y*(20*x/9 - 10/9)**4 + y, x*(20*y/9 - 10/9)**4;
        return [y - y*(2*x - 1)**4, x*(2*y - 1)**4];

    # dot product of a and b vectors
    def dotp(a, b):
        return a[0]*b[0] + a[1]*b[1]

    #straight line integral of cost function from point a to point b
    def lint(a, b):
        # integrating function is dot product of fd and line vector
        # t varies from 0 .. 1 along the line from a to b
        return scipy.integrate.quad( lambda t: \
                                     dotp( fd(a[0] + t*(b[0] - a[0]), a[1] + t*(b[1] - a[1])),
                                           [b[0] - a[0], b[1] - a[1]]), \
                                     0, 1 );

    #line integral over a scale line of cost function from point a_min to a_max
    def sint(An, Ax, Ay):
        Axd = differentiate(An, Ax);
        Ayd = differentiate(An, Ay);
        return scipy.integrate.quad( lambda t: \
                                     dotp( fd(evaluate(t, An, Ax), evaluate(t, An, Ay)), \
                                           [evaluate(t, An, Axd), evaluate(t, An, Ayd)] ), \
                                          An[0], An[-1] );


    # A0 = coords min value, A1 = coords max value
    # B0 = coords min value, B1 = coords max value
    A0 = [Ax[0], Ay[0]]; A1 = [Ax[-1], Ay[-1]];
    B0 = [Bx[0], By[0]]; B1 = [Bx[-1], By[-1]];

    vertices = [A0, B0, B1, A1]

    # given 2 nomogram scales, put the 4 ends (vertices) in anti-clockwise order
    # assume the order is    A0  -> B0 -> B1 -> A1
    # verify or mark changes needed
    #
    #   there are 2 possible circuits:
    #   * A0 -> B0 -> B1 -> A!, or
    #   * A0 -> B1 -> B0 -> A1
    #
    #   choose the one with the shortest perimeter
    #
    swapb = False
    s1 = (A0[0] - B0[0])**2 + (A0[1] - B0[1])**2 + (A1[0] - B1[0])**2 + (A1[1] - B1[1])**2
    s2 = (A0[0] - B1[0])**2 + (A0[1] - B1[1])**2 + (A1[0] - B0[0])**2 + (A1[1] - B0[1])**2
    if s1 > s2:
        # it's A0 - B1 - B0 - A1
        swapb = True
        vertices[1], vertices[2] =  vertices[2], vertices[1];
    elif s1 == s2:
        # keep going
        pass
    if "trace_circ" in log:
        print("swapb is ", swapb);

    #   find least x-y, the bottom left vertex
    #   this is a convex point, so check its angle to see if the order is anti clockwise
    #   the other 3 points are in direction 3pi/4 .. -pi/4 (toward the north east half of the xy plane)
    #   this avoids funny business with comparing angles either side of the +/- pi axis
    #
    minc = vertices[0][0] - vertices[0][1];
    bln = 0
    for i in range(1,4):
        vertex = vertices[i];
        t = vertex[0] - vertex[1]
        if t < minc:
            minc = t;
            bln = i
        elif t == minc:
            #  2 (or more) vertices lie on the same NW-SE line
            # choose the one with the least y value
            if vertex[1] < vertices[bln][1]:
                bln = i
            elif vertex[1] == vertices[bln][1]:
                # 2 vertices on top of each other - now what????
                #            TBD
                #
                pass

    # bl is bottom left vertex
    next_vertex = (bln+1) % 4
    prev_vertex = (bln+3) % 4

    # vector cross product < 0 for anti clockwise
    v1x = vertices[bln][0] - vertices[prev_vertex][0];
    v1y = vertices[bln][1] - vertices[prev_vertex][1];
    v2x = vertices[next_vertex][0] - vertices[bln][0];
    v2y = vertices[next_vertex][1] - vertices[bln][1];
    reverse =  v1x*v2y < v1y*v2x;
    if "trace_circ" in log:
        print("reverse is ", reverse)

    s1 = sint(An, Ax, Ay); # negative of integral from A1 to A0
    s2 =  sint(Bn, Bx, By); # integrate from B0 to B1

    if swapb:
        s3 = lint(A0, B1)  #integrate from A0 to B1
        s4 = lint(B0, A1)  #integrate from B0 to A1
        result = -s1[0] - s2[0] + s3[0] +s4[0];
    else:
        s3 = lint(A0, B0)  #integrate from A0 to B0
        s4 = lint(B1, A1)  #integrate from B1 to A1
        # if A1 -> A0 is (1,1) -> (0,1) then s1 should be  0.0
        # if B0 -> B1 is (1,0) -> (1,1) then s2 should be  0.2
        # if A0 -> B0 is (1,0) -> (1,0) then s3 should be  0.0
        # if B1 -> A1 is (1,1) -> (0,1) then s4 should be -0.8
        assert not (B1[0] == 1 and B1[1] == 1 and A1[0] == 0 and A1[1] == 1) or abs(s4[0] + 0.8) <= s4[1]
        result = -s1[0] + s2[0] + s3[0] + s4[0];

#    print("s4 is ", s4);
    if "trace_circ" in log:
        print("s1 is ", s1, "s2 is ", s2, "s3 is ", s3, ", s4 is ", s4);

    if reverse:
        result = -result
    return result



########################################
#
# find cost of candidate nomogram
# cost has 2 components, accuracy and area
# - max error in accuracy is < 0.1 mm
# - must fill size (height x width) as much as possible,
#   so to small or too big are errors
# normalise each error to unity
#

#kappaAcc = NN*NN * resolution;
kappaAcc = resolution/(NN**2);
#kappaAcc = 1;
print(" kappaAcc is ", kappaAcc);

def cost(dummy):

    ux, uy, vx, vy, wx, wy = np.array_split( dummy, 6);
    if "trace_cost" in log:
        print("\ntry");
        print( "ux is ", ux);
        print( "uy is ", uy);
        print( "vx is ", vx);
        print( "vy is ", vy);
        print( "wx is ", wx);
        print( "wy is ", wy);

    eAcc = 0;
    for iu in range(0,NN):
        for iv in range(0,NN):

            tux = ux[iu];
            tuy = uy[iu];
            tvx = vx[iv];
            tvy = vy[iv];

            w1 = w(unodes[iu], vnodes[iv]);
            wx1 = evaluate(w1, wnodes, wx);
            wy1 = evaluate(w1, wnodes, wy);

            d2 = (tux - tvx)**2 + (tuy - tvy)**2;
            if d2*resolution > 1:
                errsq = ((tux - tvx)*(tuy - wy1) - (tux - wx1)*(tuy - tvy))**2 / d2;
            else:
                errsq = 0; #1/resolution           ;
            eAcc = eAcc + errsq;

    print()
    eFitI = 0
    if False:
        # disable Areas
        swu = calcAB(wnodes, wx,wy, unodes, ux, uy);
        print("swu integral Area is ", swu)

        swv = calcAB(wnodes, wx,wy, vnodes, vx, vy);
        print("swv integral Area is ", swv);
        if swv > 0 and "trace_cost" in log:
            print("coords are (", wx[0], ", ", wy[0], "), (", vx[0], ", ", vy[0], "), (", vx[-1], ", ", vy[-1], "), (", wx[-1], ", ", wy[-1], ")");
        #swv += 10*(1-swv*swv)*math.exp(-swv*swv*100)
        #print("swv integral Area is adjusted", swv);

        suv = calcAB(unodes, ux,uy, vnodes, vx, vy);
        print("suv integral Area is ", suv)

        # a nomogram that perfectly fits the unit square has eFit = -0.6
        # take geometric mean to force all areas to be about the same
        eFitI = swu*swv*suv/(swu*swv + suv*swu + swv*suv)
        #eFitI = swu + swv + suv + 10*(1-(vy[0] - vy[-1])**2)*math.exp(-swv*swv*14)
        #eFitI += 10*(1 - (wx[0] - vx[0])**2 - (vy[0] - vy[-1])**2)*math.exp(-swv*swv*14)

    # for now, force the u & v scales to start and end at the corners of the unit square.
    eFitPoints = ux[0]**2 + uy[0]**2 \
        + ux[-1]**2 + (uy[-1] - 1)**2 \
        + (vx[0] - 1)**2 + (vy[0] - vyInit)**2 \
        + (vx[-1] - 1)**2 + (vy[-1] - 1 + vyInit)**2;

#    eFit =  eFitPoints*(2- eFitI/0.3) + eFitI*(eFitI/0.3 -1)
    print("eAcc cost is {:.2e}, eFitI cost is {:.2e}, eFitPoints cost is {:.2e}".format( eAcc, eFitI, eFitPoints ));
    #alpha = math.exp(-swv*swv*14);
    alpha = 1
    return  eAcc + alpha*eFitPoints + (1-alpha)*eFitI/kappaAcc
#    return  eAcc + eFitPoints


#print("ux is ", ux);
print( "pos u(", umin, ") is (", evaluate(umin, unodes, ux), ", ", evaluate(umin, unodes, uy), ")");
print( "pos u(", umin + 0.01, ") is (", evaluate(umin + 0.01, unodes, ux), ", ", evaluate(umin + 0.01, unodes, uy), ")");
print( "pos u(", umax, ") is (", evaluate(umax, unodes, ux), ", ", evaluate(umax, unodes, uy), ")");
print( "pos u(", umax - 0.01, ") is (", evaluate(umax - 0.01, unodes, ux), ", ", evaluate(umax - 0.01, unodes, uy), ")");
print( "pos v(", vmin, ") is (", evaluate(vmin, vnodes, vx), ", ", evaluate(vmin, vnodes, vy), ")");
print( "pos v(", vmin + 0.01, ") is (", evaluate(vmin + 0.01, vnodes, vx), ", ", evaluate(vmin + 0.01, vnodes, vy), ")");
print( "pos v(", vmax, ") is (", evaluate(vmax, vnodes, vx), ", ", evaluate(vmax, vnodes, vy), ")");
print( "pos v(", vmax - 0.01, ") is (", evaluate(vmax - 0.01, vnodes, vx), ", ", evaluate(vmax - 0.01, vnodes, vy), ")");



#
# the nomogram is given by the coordinates of the node points that
# minimises the error
#

# prefer BFGS or L-BFGS, then Powell and Nelder-Mead, both gradient-free methods
#
#scipy.optimize.minimize(fun, x0, args=(), method=None, jac=None, hess=None, hessp=None, bounds=None, constraints=(), tol=None, callback=None, options=None)

x0 = np.concatenate( [ux, uy, vx, vy, wx, wy] );
res = scipy.optimize.minimize( cost, x0 );
#res = scipy.optimize.basinhopping(cost, x0, niter=100 );
#res = scipy.optimize.minimize(cost, x0, method="Nelder-Mead" );
#res = scipy.optimize.minimize( cost, x0, method='L-BFGS-B' );
#res = scipy.optimize.minimize(cost, x0, method='Nelder-Mead' );
#res = scipy.optimize.minimize(cost, x0, method='Powell' );

print( "after ", res.nit, " iterations, ", res.message );
#print(res);
if True or res.success:  # xxx res.success crashes for some methods
    ux, uy, vx, vy, wx, wy = np.array_split( res.x, 6);

    print("solution is ...");
    print( "ux is ", ux);
    print( "uy is ", uy);
    print( "vx is ", vx);
    print( "vy is ", vy);
    print( "wx is ", wx);
    print( "wy is ", wy);

    # nc is nr checks needed so the check is of the order of every d mm
    d = 1
    nc = int(math.sqrt(height*width)/d);
    print( "checking solution every ", d, "mm, ", nc*nc, " combinations ...");
    maxdiff = 0;
    for i in range(0,nc+1):
        for j in range(0,nc+1):
            def report_alignment():
                print( "u is ", u, " at pos (", uxcoord, ",", uycoord, ")" );
                print( "v is ", v, " at pos (", vxcoord, ",", vycoord, ")" );
                print( "w is ", wvalue, " at pos (", wxcoord, ",", wycoord, ")" );
                print( "alignment difference is {:5.2g} about {:5.2f} mm".format( difference, difference*math.sqrt(width*height) ));

            u = umin + (umax - umin)*i/nc;
            v = vmin + (vmax - vmin)*j/nc;
            uxcoord = evaluate(u, unodes, ux);
            uycoord = evaluate(u, unodes, uy);
            vxcoord = evaluate(v, vnodes, vx);
            vycoord = evaluate(v, vnodes, vy);
            wvalue = w(u,v);
            wxcoord = evaluate(wvalue, wnodes, wx);
            wycoord = evaluate(wvalue, wnodes, wy);
            difference = abs( (uxcoord-vxcoord) * (uycoord - wycoord) - (uxcoord - wxcoord) * (uycoord - vycoord) ) / math.sqrt((uxcoord-vxcoord)**2 + (vxcoord-vycoord)**2);

            if wvalue < wmin:
                print("w(", u, ", ", v, ") = ", wvalue, " < wmin, ", wmin);
                report_alignment();
                sys.exit("scale range error, please check scale min & max limits");
            elif wvalue > wmax:
                print("w(", u, ", ", v, ") = ", wvalue, " > wmax, ", wmax);
                report_alignment();
                sys.exit("scale range error, please check scale min & max limits");

            if difference > maxdiff:
                maxdiff = difference;
                if "trace_alignment" in log:
                    report_alignment()

    aler = maxdiff*math.sqrt(width*height)
    print( "alignment error is estimated at less than {:5.2g} mm".format( aler ));
    if aler > 0.2:
        print("alignment errors are possible - please check.")
        print("This nomogram used ", NN, " nodes.  Try increasing it")

    # print the nomogram

    if -0.2 < calcAB(wnodes, wx,wy, vnodes, vx, vy):
        # the w scale line is close to the v scale line
        # => put the w ticks on the left side
        params_w.update({'tick_side':'left'})
    elif -0.2 < calcAB(wnodes, wx,wy, unodes, ux, uy):
        # the w scale line is close to the u scale line
        # => put the u ticks on the left side
        params_u.update({'tick_side':'left'})

    Nomographer(main_params);
