#!/usr/bin/python3

"""
    nomogen.py

    auto generator for nomograms

    Copyright (C) 2021  Trevor Blight

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys

import math;
import numpy as np;
import scipy;
import scipy.optimize;
from scipy import integrate;


# enable logging
# "trace_init" "trace_circ" "trace_cost" "trace_alignment" "trace_result"
log = { };

class Nomogen:
    """
    determine nomogram from an equation
    inputs:
             func(a,b), return value is middle scale,
                        a & b are values on left and right scales
             params     as in Nomographer, with the addition of 'nlinearity',
                        where 'nlinearity' is a measure of how many points are
                        needed to define each sclae line in the nomogram
    """

    def __init__(self, w,  main_params):

        # NN = nr Chebychev nodes for the scales
        # the nodes have an index in the range 0 .. NN-1
        if 'nlinearity' not in main_params:
            print("nlinearity parameter not provided, using defualt = 9")
            NN = 9
        elif not isinstance(main_params['nlinearity'], int):
            print("nlinearity parameter must be an integer, using defualt = 9")
            NN = 9
        else:
            NN = main_params['nlinearity']
            if NN % 2 == 0:
                NN = NN+1
                print("nr In this program, the number of Chebychev nodes must be odd, using ", NN, " nodes");
            if NN < 3:
                print("nlinearity must be >= 3");
                sys.exit("quitting")
        print("the number of Chebychev nodes is ", NN);

        params_u = main_params['block_params'][0]['f1_params']
        umin = params_u['u_min'];
        umax = params_u['u_max'];

        params_v = main_params['block_params'][0]['f3_params']
        vmin = params_v['u_min'];
        vmax = params_v['u_max'];

        params_w = main_params['block_params'][0]['f2_params']
        wmin = params_w['u_min'];
        wmax = params_w['u_max'];

        if "trace_init" in log:
            print("umin is", wmin, ", umax is ", wmax)
            print("vmin is", wmin, ", vmax is ", wmax)
            print("wmin is", wmin, ", wmax is ", wmax)

        #sanity checks
        if umax < umin:
            sys.exit("error: umax is less than umin")
        if vmax < vmin:
            sys.exit("error: vmax is less than vmin")
        if wmax < wmin:
            sys.exit("error: wmax is less than wmin")
        wvalue = w(umin, vmin)
        if wvalue < wmin:
            wmin = wvalue
        if wvalue > wmax:
            wmax = wvalue
        wvalue = w(umax, vmin)
        if wvalue < wmin:
            wmin = wvalue
        if wvalue > wmax:
            wmax = wvalue
        wvalue = w(umin, vmax)
        if wvalue < wmin:
            wmin = wvalue
        if wvalue > wmax:
            wmax = wvalue
        wvalue = w(umax, vmax)
        if wvalue < wmin:
            wmin = wvalue
        if wvalue > wmax:
            wmax = wvalue

        width = 10 * main_params['paper_width'];  # convert cm -> mm
        height = 10 * main_params['paper_height'];

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
        #print(" kappaAcc is ", kappaAcc);

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
                print()

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

            # alpha controls the scaling part of the optimisatin
            # alpha = 1 => tie the ends of the outer scales to the corners of
            #              the unit square (measured by eFitPoints)
            # alpha = 0 => make the areas bounded by the pairs of scales as large
            #              as possible, while still keeping accuracy and inside
            #              the unit square (measured by eFitI)
            # the points method is much faster,
            # the Area method might be useful iftying th epoints to the corners
            # restricts the shape of the nomogram too much
            alpha = 1 # eFitPoints / eFitI proportion
            eFitI = 0
            if alpha < 1:
                # enable Areas
                swu = calcAB(wnodes, wx,wy, unodes, ux, uy);
                if "trace_circ" in log:
                    print("swu integral Area is ", swu)

                swv = calcAB(wnodes, wx,wy, vnodes, vx, vy);
                if "trace_circ" in log:
                    print("swv integral Area is ", swv);
                if swv > 0 and "trace_cost" in log:
                    print("coords are (", wx[0], ", ", wy[0], "), (", vx[0], ", ", vy[0], "), (", vx[-1], ", ", vy[-1], "), (", wx[-1], ", ", wy[-1], ")");
                #swv += 10*(1-swv*swv)*math.exp(-swv*swv*100)
                #print("swv integral Area is adjusted", swv);

                suv = calcAB(unodes, ux,uy, vnodes, vx, vy);
                if "trace_circ" in log:
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
            print("\reAcc cost is {:.2e}".format( eAcc), end = '' );
            if alpha > 0:
                print(", eFitPoints cost is {:.2e}".format( eFitPoints), end = '' );
            if alpha < 1:
                print( ' eFitI cost is {:.2e}'.format( eFitI ), end = '');

            #alpha = math.exp(-swv*swv*14);
            return  eAcc + alpha*eFitPoints + (1-alpha)*eFitI/kappaAcc
        #    return  eAcc + eFitPoints

        if "trace_result" in log:
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

        print( );
        if "trace_result" in log:
            print(res);
        else:
            print( "after ", res.nit, " iterations, ", res.message );

        if True or res.success:  # xxx res.success crashes for some methods
            ux, uy, vx, vy, wx, wy = np.array_split( res.x, 6);

            if "trace_result" in log:
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
                print("This nomogram used ", NN, " nodes.")
                print("Try increasing non-linearity, or reduce the range of one or more scales")


            # return the resulting scale lines into the nomogram parameters
            params_u.update({'f': lambda u: evaluate(u, unodes, ux),
                             'g': lambda u: evaluate(u, unodes, uy),
                             'h': lambda u: 1.0,
                             })
            params_v.update({'f': lambda v: evaluate(v, vnodes, vx),
                             'g': lambda v: evaluate(v, vnodes, vy),
                             'h': lambda v: 1.0,
                             })
            params_w.update({'f': lambda w: evaluate(w, wnodes, wx),
                             'g': lambda w: evaluate(w, wnodes, wy),
                             'h': lambda w: 1.0,
                             })

            if -0.2 < calcAB(wnodes, wx,wy, vnodes, vx, vy):
                # the w scale line is close to the v scale line
                # => put the w ticks on the left side
                params_w.update({'tick_side':'left'})
            elif -0.2 < calcAB(wnodes, wx,wy, unodes, ux, uy):
                # the w scale line is close to the u scale line
                # => put the u ticks on the left side
                params_u.update({'tick_side':'left'})


