#!/usr/bin/python3

"""
    nomogen.py

    auto generator for nomograms

    Copyright (C) 2021-2022  Trevor Blight

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
import datetime

import math;
import numpy as np;
import scipy;
import scipy.optimize;
from scipy import integrate;
from scipy.misc import derivative


# enable logging
# "trace_init" "trace_circ" "trace_cost" "trace_alignment" "trace_result"
log = { "trace_init" };

itNr = 0

class Nomogen:
    """
    determine nomogram from an equation
    inputs:
             func(a,b), return value is middle scale,
                        a & b are values on left and right scales
             params     as in Nomographer, with the addition of 'pdegree',
                        where 'pdegree' is a measure of how many points are
                        needed to define each scale line in the nomogram
    """

    def __init__(self, w,  main_params):

        # NN = nr Chebychev nodes for the scales
        # the nodes have an index in the range 0 .. NN-1
        if 'pdegree' not in main_params:
            print("pdegree parameter not provided, using defualt = 9")
            NN = 9
        elif not isinstance(main_params['pdegree'], int):
            print("pdegree parameter must be an integer, using defualt = 9")
            NN = 9
        else:
            NN = main_params['pdegree']
            if NN % 2 == 0:
                NN = NN+1
                print("nr In this program, the number of Chebychev nodes must be odd, using ", NN, " nodes");
            if NN < 3:
                print("pdegree must be >= 2");
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
            print("umin is", umin, ", umax is ", umax)
            print("vmin is", vmin, ", vmax is ", vmax)
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

        if (w1>w0) == (w2>w0):
            # vmax is at the top
            vtop, vbottom  = vmax, vmin
            yv0 = 0; yv2 = 1
        else:
            vtop, vbottom  = vmin, vmax
            yv0 = 1; yv2 = 0

        wB = w(umin, vbottom)
        wE = w(umax, vtop)
        wG = w(umax, vbottom)
        wH = w(umin, vtop)

        if wE > wB:
            yw0 = 0; yw2 = 1
            wbottom, wtop = wmin, wmax
        else:
            yw0 = 1;  yw2 = 0;
            wbottom, wtop = wmax, wmin

        # guess an initial position and slope for the xw scale
        if "trace_init" in log:
            print("wB is ", wB, ", wE is ", wE, "wG is ", wG, ", wH is ", wH)
        if math.isclose(wG, wH):
            xwB = xwE = 0.5
            xu = np.zeros(NN);
            yu = (1 - np.cos(np.linspace(0,math.pi,NN)))/2;
            xv = np.ones(NN);
            yv = (1 - np.cos(np.linspace(yv0 * math.pi, yv2 * math.pi,NN)))/2;
            xw = np.empty(NN); xw.fill(0.5)

            # yw(w) is a quadratic, going thru (wb,0), (wG,0.5) & (wE,1)
            det = (wG-wB)*(wB-wE)*(wE-wG)
            a = ((wE+wB)/2 - wG)/det
            b = ((wG-wB)**2 - ((wE-wB)**2)/2 )/det
            mm = wnodes - wB
            yw = mm * (a*mm + b)

            ywE = (wE-wB)*(a*(wE-wB) + b)
            ywG = (wG-wB)*(a*(wG-wB) + b)
            ywB = (wB-wB)*(a*(wB-wB) + b)
            if "trace_init" in log:
                print( "a is ", a, ", b is ", b, ", det is ", det )
                print("yw is ", yw)
                print("yw(wG) is ", ywG, "yw(wE) is ", ywE, "yw(wB) is ", ywB )
            if not math.isclose(ywG, 0.5):
                print("y scale failed for ywG test")
                sys.exit("quitting")
            if not math.isclose(ywE, 1.0):
                print("y scale failed for ywE test")
                sys.exit("quitting")
        else:
            alphaxw = (wE - wG - wH + wB) / (wE - wB) / (wG - wH)
            xwB = (wH - wB) / (wE - wB) - alphaxw * (wH - wB)
            xwE = xwB + alphaxw*(wE - wB)
            if "trace_init" in log:
                print("xwB is ", xwB, ", xwE is ", xwE)

            if True:
                # clip to unit square
                if xwE > 1:
                    xwE = 1
                elif xwE < 0:
                    xwE = 0
                if xwB > 1:
                    xwB = 1
                elif xwB < 0:
                    xwB = 0

            if xwE <= 1 and xwE >= 0 and xwB <= 1 and xwB >= 0:
                if "trace_init" in log:
                    print("linear initial estimate found")
                xu = np.zeros(NN);
                yu = (1 - np.cos(np.linspace(0,math.pi,NN)))/2;
                xv = np.ones(NN);
                yv = (1 - np.cos(np.linspace(yv0 * math.pi, yv2 * math.pi,NN)))/2;
                xw = xwB + (wnodes.copy() - wmin)*(xwE-xwB)/(wmax-wmin)
                yw = (1 - np.cos(np.linspace(yw0*math.pi, yw2*math.pi,NN)))/2;
            elif True:
            # global optimise for curved lines defined by 3 points

                xu1i, yu1i, xw0i, xw1i, yw1i, xw2i, xv1i, yv1i = range(8)
                print("enums: ", xu1i, yu1i, xw0i, xw1i, yw1i, xw2i, xv1i, yv1i)

                # evaluate function defined by 3 points
                def eval3(x, x0, x1, x2, f0, f1, f2):
                    if False:
                    # 3-term barycentric interpolation
                        if x == x0:
                            return f0
                        elif x == x1:
                            return f1
                        elif x == x2:
                            return f2
                        else:
                            A = f0/(x-x0) - 2*f1/(x-x1) + f2/(x-x2)
                            B = 1/(x-x0) - 2/(x-x1) + 1/(x-x2)
                            return A/B
                    else:
                        # direct evaluation
                        d = x1 - x0
                        a = (f2 - 2*f1 + f0)/2/d/d
                        b = (f1 - f0  - a*d*(2*x0  + d))/d
                        c = f0 - x0*(a*x0 + b)
                        return c + x*(b + a*x)

                # differentiate function defined by 3 points
                def diff3(x, x0, x1, x2, f0, f1, f2):
                    # direct evaluation
                    d = x1 - x0
                    a = (f2 - 2*f1 + f0)/2/d/d
                    b = (f1 -f0  - a*d*(2*x0  + d))/d
                    return b + 2*a*x

                def cost3(tvec):
                    def check(dsq, x0, y0, x1, y1, x2, y2, msg):
                        if False and "trace_init" in log:
                            print("esq ", msg, " is ", dsq)
                        Area = x1*(y2-y0) + x2*(y0-y1) + x0*(y1-y2)
                        BaseSq = (x0-x1)**2 + (y0-y1)**2
                        hsq = Area*Area/BaseSq
#                       if abs(hsq - dsq) > 1e-13 and abs(hsq - dsq)/hsq > 1e-13:
                        if 1e10*abs(hsq - dsq) > 1 + hsq:
                            print("dsq fails", msg, ", error is ", hsq-dsq, ", limit is ", (1 + hsq)*1e-10 )
                            sys.exit("quitting")
                        return
                    print("tvec is ", tvec)
                    if False:
                        # confidence tests for check() & eval3()
                        for i in range(11):
                            for j in range(11):
                                check(j*j/100, 0,0,1,0,i/10,j/10,"test1{}{}".format(i, j))
                                check((10-j)**2/100, 0,1,1,1,i/10,j/10,"test2{}{}".format(i, j))
                                check((j-i)**2/200, 0,0,1,1,i/10,j/10,"test3{}{}".format(i, j))
                                check((j+i-10)**2/200, 0,1,1,0,i/10,j/10,"test4{}{}".format(i, j))
                            for i in range(11):
                                t = eval3(i/10, 0, 0.5, 1, 1, 2, 3)
                                if abs(t - 2*i/10 - 1) > 1e-13:
                                    print("eval3 1 failure, i is ", i)
                                    sys.exit("quitting")
                            t = eval3(i/5-1, -1, 0, 1, 1, 0, 1)
                            if abs(t - (i/5-1)**2) > 1e-13:
                                print("eval 2 failure, i is ", i)
                                sys.exit("quitting")

                    cost = 0

                    # create a small cost if any point strays outside the unit square
                    for t in tvec:
                        cost = cost + (t*(t-1))**2
                    print("xxx cost is ", cost)

                    wmid = (wmin+wmax)/2

                    # u0 v0
                    #cost == 0
                    dwdu = derivative(lambda uu: w(uu,vbottom), umin, dx=1e-6, order=5)
                    lhs = -diff3(wbottom, wmin, wmid, wmax, yw0, tvec[yw1i], yw2)*dwdu
                    rhs = -(eval3(wbottom, wmin, wmid, wmax, tvec[xw0i], tvec[xw1i], tvec[xw2i]) -1) \
                           * diff3(wbottom, wmin, wmid, wmax, yw0, tvec[yw1i], yw2)
                    print("lhs is ", lhs, ", rhs is ", rhs)
                    #cost = abs(lhs - rhs)/1000000

                    # u0, v1
                    xv1 = tvec[xv1i]
                    yv1 = tvec[yv1i]
                    wt = w(umin, (vmin+vmax)/2)
                    xwt = eval3(wt, wmin, wmid, wmax, tvec[xw0i], tvec[xw1i], tvec[xw2i])
                    ywt = eval3(wt, wmin, wmid, wmax, yw0, tvec[yw1i], yw2)
                    esq =((xv1*ywt - xwt*yv1)**2) / (xv1**2 + yv1**2);
                    check(esq, 0, 0, xv1, yv1, xwt, ywt, "u0, v1")
                    cost = cost + esq

                    # u0, v2
                    wt = w(umin, vtop)
                    xwt = eval3(wt, wmin, wmid, wmax, tvec[xw0i], tvec[xw1i], tvec[xw2i])
                    ywt = eval3(wt, wmin, wmid, wmax, yw0, tvec[yw1i], yw2)
                    esq = ((ywt - xwt)**2)/2;
                    check(esq, 0, 0, 1, 1, xwt, ywt, "u0, v2")
                    cost = cost + esq

                    # u1, v0
                    xu1 = tvec[xu1i]
                    yu1 = tvec[yu1i]
                    wt = w((umin+umax)/2, vbottom)
                    xwt = eval3(wt, wmin, wmid, wmax, tvec[xw0i], tvec[xw1i], tvec[xw2i])
                    ywt = eval3(wt, wmin, wmid, wmax, yw0, tvec[yw1i], yw2)
                    esq =(((xu1-1)*ywt - (xwt-1)*yu1)**2) / ((1-xu1)**2 + yu1**2);
                    check(esq, xu1, yu1, 1, 0, xwt, ywt, "u1, v0")
                    cost = cost + esq

                    # u1, v1
                    xu1 = tvec[xu1i]
                    yu1 = tvec[yu1i]
                    xv1 = tvec[xv1i]
                    yv1 = tvec[yv1i]
                    wt = w((umin+umax)/2, (vmin+vmax)/2)
                    xwt = eval3(wt, wmin, wmid, wmax, tvec[xw0i], tvec[xw1i], tvec[xw2i])
                    ywt = eval3(wt, wmin, wmid, wmax, yw0, tvec[yw1i], yw2)
                    esq = (((xu1-xv1)*(ywt-yv1) - (xwt-xv1)*(yu1-yv1))**2) / ((xu1-xv1)**2 + (yu1-yv1)**2);
                    check(esq, xu1, yu1, xv1, yv1, xwt, ywt, "u1, v1")
                    cost = cost + esq

                    # u1, v2
                    xu1 = tvec[xu1i]
                    yu1 = tvec[yu1i]
                    wt = w((umin+umax)/2, vtop)
                    xwt = eval3(wt, wmin, wmid, wmax, tvec[xw0i], tvec[xw1i], tvec[xw2i])
                    ywt = eval3(wt, wmin, wmid, wmax, yw0, tvec[yw1i], yw2)
                    esq =(((xu1-1)*(ywt-1) - (xwt-1)*(yu1-1))**2) / ((xu1-1)**2 + (yu1-1)**2);
                    check(esq, xu1, yu1, 1, 1, xwt, ywt, "u1, v2")
                    cost = cost + esq

                    # u2, v0
                    wt = w(umax, vbottom)
                    xwt = eval3(wt, wmin, wmid, wmax, tvec[xw0i], tvec[xw1i], tvec[xw2i])
                    ywt = eval3(wt, wmin, wmid, wmax, yw0, tvec[yw1i], yw2)
                    esq = (1 - ywt - xwt)**2 / 2;
                    check(esq, 0, 1, 1, 0, xwt, ywt, "u2, v0")
                    cost = cost + esq

                    # u2, v1
                    xv1 = tvec[xv1i]
                    yv1 = tvec[yv1i]
                    wt = w(umax, (vmin+vmax)/2)
                    xwt = eval3(wt, wmin, wmid, wmax, tvec[xw0i], tvec[xw1i], tvec[xw2i])
                    ywt = eval3(wt, wmin, wmid, wmax, yw0, tvec[yw1i], yw2)
                    esq =  (xv1*(1-ywt) - xwt*(1-yv1))**2 / (xv1**2 + (1-yv1)**2);
                    check(esq, 0, 1, xv1, yv1, xwt, ywt, "u2, v1")
                    cost = cost + esq

                    # u2, v2
                    #cost == 0

                    print("quadratic estimate: cost of fit is ", cost)
                    return cost

                if "trace_init" in log:
                    print("looking for best quadratic initial estimate")

                # initial conditions: mid points only, ends tied to unit square
                testv = np.array([0, 0.5,   # xu1, yu1
                                  0.5,      # xw0
                                  0.5, 0.5, # xw1, yw1
                                  0.5,      # xw2
                                  0.5, 1    # xv1, yv1
                                 ])
                res = scipy.optimize.basinhopping( cost3, testv, stepsize=0.01, niter=100 );
                if "trace_init" in log:
                    print("res is ", res)

                xu = np.array([eval3(unodes[k], umin, (umin+umax)/2, umax, 0, res.x[xu1i], 0) \
                               for k in range(0, NN)]);
                yu = np.array([eval3(unodes[k], umin, (umin+umax)/2, umax, 0, res.x[yu1i], 1) \
                               for k in range(0, NN)]);

                xv = np.array([eval3(vnodes[k], vmin, (vmin+vmax)/2, vmax, 1, res.x[xv1i], 1) \
                               for k in range(0, NN)]);
                yv = np.array([eval3(vnodes[k], vmin, (vmin+vmax)/2, vmax, yv0, res.x[yv1i], yv2) \
                               for k in range(0, NN)]);

                xw = np.array([eval3(wnodes[k], wmin, (wmin+wmax)/2, wmax, res.x[xw0i], res.x[xw1i], res.x[xw2i]) \
                               for k in range(0, NN)]);
                yw = np.array([eval3(wnodes[k], wmin, (wmin+wmax)/2, wmax, yw0, res.x[yw1i], yw2) \
                               for k in range(0, NN)]);

                if "trace_init" in log:
                    print("initial quadratic guess")
                    print(" xu is ", xu)
                    print(" yu is ", yu)
                    print(" xv is ", xv)
                    print(" yv is ", yv)
                    print(" xw is ", xw)
                    print(" yw is ", yw)

            else:
                # under development ...
                if "trace_init" in log:
                    print( "trying quadratic approximation for xw" )
                R = (wE - wG - wH + wB)/(wG-wH)/(wE-wB)
                S = 2*wB - wG - wH
                P = (wH - wB)*(1/(wE-wB) - R)
                Q = -(wH-wB)*(S + (wH-wB))

                if R != alphaxw:
                    print("R evaluation problem")
                    sys.exit("quitting");
                if P != xwB:
                    print("P evaluation problem")
                    sys.exit("quitting");

                # test solution
                for b in [-2, -1, 0, 1, 2]:
                    c = P + Q*b
                    alphaxw = R + S*b
                    t1 = c + (wH-wB)*(alphaxw + b*(wH-wB)) - (wH-wB)/(wE-wB)
                    if abs(t1) > 1e-12:
                        print("eqn1 evaluation problem for b = ", b)
                        sys.exit("quitting")
                    t1 = c + (wG-wB)*(alphaxw + b*(wG-wB)) - 1 + (wG-wB)/(wE-wB)
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
                alphaxw = R + b*S
                c = P + Q*b
                if "trace_init" in log:
                    print("c is ", c, ", alphaxw is ", alphaxw, ", b is ", b)

                if bmin > bmax:
                    print("bmin > bmax, quadratic approximation is not feasible, bmin is ", bmin, ", bmax is ", bmax);
                    xwB = c
                    xwE = c + (wE-wB)*(alphaxw + b*(wE-wB))
                    print("xwB is ", xwB, ", xwE is ", xwE)
                    # rescale from xwB .. xwE -> 0.05 .. 0.95
                    if xwE > xwB:
                        xw =  np.array([0.05 + (0.9/(xwE-xwB))*(c + (wnodes[k]-wmin)*(alphaxw + b*(wnodes[k]-wmin)) - xwB) for k in range(0, NN)]);
                    else:
                        xw =  np.array([0.95 - (0.9/(xwE-xwB))*(c + (wnodes[k]-wmin)*(alphaxw + b*(wnodes[k]-wmin)) - xwB) for k in range(0, NN)]);
                else:
                    xw =  np.array([c + (wnodes[k]-wmin)*(alphaxw + b*(wnodes[k]-wmin)) for k in range(0, NN)]);

                    if "trace_init" in log:
                        print("xw is ", xw)

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
            txu = xu[iu];
            tyu = yu[iu];
            txv = xv[iv];
            tyv = yv[iv];

            w1 = w(unodes[iu], vnodes[iv]);
            xw1 = evaluate(w1, wnodes, xw);
            yw1 = evaluate(w1, wnodes, yw);

            d2 = (txu - txv)**2 + (tyu - tyv)**2;
            if d2*resolution <= 1:
                print( "u & v scale lines touch or cross at (", txu, ",", tyu, ")" );
                errsq = 0;
            else:
                errsq = ((txu - txv)*(tyu - yw1) - (txu - xw1)*(tyu - tyv)) / d2;
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
        #   so too small or too big are errors
        # normalise each error to unity
        #

        #kappaAcc = NN*NN * resolution;
        kappaAcc = resolution/(NN**2);
        #kappaAcc = 1;
        #print(" kappaAcc is ", kappaAcc);

        def cost(dummy):
            xu[1:-1], yu[1:-1], xv[1:-1], yv[1:-1], xw, yw[1:-1] = np.array_split( dummy, [NN-2, 2*NN-4, 3*NN-6, 4*NN-8, 5*NN-8]); #qqq
            if "trace_cost" in log:
                print("\ntry");
                print( "xu is ", xu);
                print( "yu is ", yu);
                print( "xv is ", xv);
                print( "yv is ", yv);
                print( "xw is ", xw);
                print( "yw is ", yw);
                print()

            eDeru = eDerv = 0;
            eAcc = 0;
            # estimate position & derivative error

            fdxdu = differentiate(unodes, xu)
            fdydu = differentiate(unodes, yu)
            fdxdv = differentiate(vnodes, xv)
            fdydv = differentiate(vnodes, yv)
            fdxdw = differentiate(wnodes, xw)
            fdydw = differentiate(wnodes, yw)

            for iu in range(0,NN):
                txu = xu[iu];
                tyu = yu[iu];
                u = unodes[iu]
                dxdu = evaluate(u, unodes, fdxdu)
                dydu = evaluate(u, unodes, fdydu)

                for iv in range(0,NN):
                    txv = xv[iv];
                    tyv = yv[iv];
                    v = vnodes[iv]
                    dxdv = evaluate(v, vnodes, fdxdv)
                    dydv = evaluate(v, vnodes, fdydv)
                    dwdu = derivative(lambda uu: w(uu,v), u, dx=1e-6, order=5)
                    dwdv = derivative(lambda vv: w(u,vv), v, dx=1e-6, order=5)

                    w1 = w(u, v);
                    txw = evaluate(w1, wnodes, xw);
                    tyw = evaluate(w1, wnodes, yw);
                    dxdw = evaluate(w1, wnodes, fdxdw)
                    dydw = evaluate(w1, wnodes, fdydw)

                    tx = txu - txv
                    ty = tyu - tyv
                    td2 = tx*tx + ty*ty
                    td  = math.sqrt(td2)
                    e0 = (tx*(tyu - tyw) - (txu - txw)*ty) / td
                    if td2*resolution > 1:
                        eAcc += e0**2;

                    tmp = ty*dxdw - tx*dydw
                    tuc = e0 * (tx*dxdu + ty*dydu)/td2
                    tvc = e0 * (tx*dxdv + ty*dydv)/td2
                    #tuc = 0; tvc = 0
                    dedu = ((dwdu*tmp + (tyv-tyw)*dxdu - (txv-txw)*dydu))/td - tuc
                    dedv = ((dwdv*tmp + (tyw-tyu)*dxdv - (txw-txu)*dydv))/td + tvc

                    #check = True   # checks are slow
                    check = False
                    if check:
                        def gete0(au, av):
                            xau = evaluate(au, unodes, xu);
                            yau = evaluate(au, unodes, yu);
                            xav = evaluate(av, vnodes, xv);
                            yav = evaluate(av, vnodes, yv);
                            tw = w(au, av);
                            xtw = evaluate(tw, wnodes, xw);
                            ytw = evaluate(tw, wnodes, yw);
                            return (xau*yav + xtw*(yau - yav) + (xav - xau)*ytw - xav*yau) /  math.hypot((xau-xav), (yau-yav))


                        if not math.isclose(e0, gete0(u,v), rel_tol=1e-05, abs_tol=1e-7):
                            sys.exit("gete0() error")

                        tu = derivative(lambda uu: gete0(uu,v), u, dx=1e-6, order=5)
                        if not math.isclose(tu, dedu, rel_tol=1e-05, abs_tol=1e-7):
                            print( "(u,v) is (", u, ",", v, "), dedu is ", dedu, ", tu is ", tu, ", tuc is ", tuc )
                            sys.exit("dedu error")

                        tv = derivative(lambda vv: gete0(u,vv), v, dx=1e-6, order=5)
                        if not math.isclose(tv, dedv, rel_tol=1e-05, abs_tol=1e-7):
                            print( "(u,v) is (", u, ",", v, "), dedv is ", dedv, ", tv is ", tv )
                            sys.exit("dedv error")

                    eDeru += dedu**2
                    eDerv += dedv**2


            # alpha controls the scaling part of the optimisatin
            # alpha = 1 => tie the ends of the outer scales to the corners of
            #              the unit square (measured by eFitPoints)
            # alpha = 0 => make the areas bounded by the pairs of scales as large
            #              as possible, while still keeping accuracy and inside
            #              the unit square (measured by eFitI)
            # the points method is much faster,
            # the Area method might be useful if tying the points to the corners
            # restricts the shape of the nomogram too much
            alpha = 1 # eFitPoints / eFitI proportion
            eFitI = 0
            if alpha < 1:
                # enable Areas
                swu = calcAB(wnodes, xw,yw, unodes, xu, yu);
                if "trace_circ" in log:
                    print("swu integral Area is ", swu)

                swv = calcAB(wnodes, xw,yw, vnodes, xv, yv);
                if "trace_circ" in log:
                    print("swv integral Area is ", swv);
                if swv > 0 and "trace_cost" in log:
                    print("coords are (", xw[0], ", ", yw[0], "), (", xv[0], ", ", yv[0], "), (", xv[-1], ", ", yv[-1], "), (", xw[-1], ", ", yw[-1], ")");
                #swv += 10*(1-swv*swv)*math.exp(-swv*swv*100)
                #print("swv integral Area is adjusted", swv);

                suv = calcAB(unodes, xu,yu, vnodes, xv, yv);
                if "trace_circ" in log:
                    print("suv integral Area is ", suv)

                # a nomogram that perfectly fits the unit square has eFit = -0.6
                # take geometric mean to force all areas to be about the same
                eFitI = swu*swv*suv/(swu*swv + suv*swu + swv*suv)
                #eFitI = swu + swv + suv + 10*(1-(yv[0] - yv[-1])**2)*math.exp(-swv*swv*14)
                #eFitI += 10*(1 - (xw[0] - xv[0])**2 - (yv[0] - yv[-1])**2)*math.exp(-swv*swv*14)

            eFitPoints = 0
            print("\reAcc cost is {:.2e}".format( eAcc), end = '' );
            print(", eDer cost is {:.2e}, {:.2e}".format( eDeru, eDerv), end = '' );
            #if alpha > 0:
            #    print(", eFitPoints cost is {:.2e}".format( eFitPoints), end = '' );
            #if alpha < 1:
            #    print( ' eFitI cost is {:.2e}'.format( eFitI ), end = '');

        #    return  eAcc + alpha*eFitPoints + (1-alpha)*eFitI/kappaAcc

            # mu sets relative priority of eAcc & eDerx
            # eDeru needs to be independent of the scale of u,
            # so multiply bu range of u
            #
            # there are NN**2 separate error terms, one for each pair of points
            # so normalise to average error per point pair.
            # TODO:
            #       investigate a good value for mu
            mu = 1
            return  (eAcc + mu*(eDeru*(umax-umin)**2 + eDerv*(vmax-vmin)**2))/(NN**2)
            #return  eAcc
        #    return  eAcc + eDer + alpha*eFitPoints + (1-alpha)*eFitI/kappaAcc

        if "trace_result" in log:
            #print("xu is ", xu);
            print( "pos u(", umin, ") is (", evaluate(umin, unodes, xu), ", ", evaluate(umin, unodes, yu), ")");
            print( "pos u(", umin + 0.01, ") is (", evaluate(umin + 0.01, unodes, xu), ", ", evaluate(umin + 0.01, unodes, yu), ")");
            print( "pos u(", umax, ") is (", evaluate(umax, unodes, xu), ", ", evaluate(umax, unodes, yu), ")");
            print( "pos u(", umax - 0.01, ") is (", evaluate(umax - 0.01, unodes, xu), ", ", evaluate(umax - 0.01, unodes, yu), ")");
            print( "pos v(", vmin, ") is (", evaluate(vmin, vnodes, xv), ", ", evaluate(vmin, vnodes, yv), ")");
            print( "pos v(", vmin + 0.01, ") is (", evaluate(vmin + 0.01, vnodes, xv), ", ", evaluate(vmin + 0.01, vnodes, yv), ")");
            print( "pos v(", vmax, ") is (", evaluate(vmax, vnodes, xv), ", ", evaluate(vmax, vnodes, yv), ")");
            print( "pos v(", vmax - 0.01, ") is (", evaluate(vmax - 0.01, vnodes, xv), ", ", evaluate(vmax - 0.01, vnodes, yv), ")");



        # run this function whenever the optimise function enters a
        # new iteration
        def newIt(xk):
            import __main__
            global itNr
            itNr += 1
            print(" ", __main__.__file__, ": iteration nr ", itNr, sep="", end = "" )

        #
        # the nomogram is given by the coordinates of the node points that
        # minimises the error
        #

        # prefer BFGS or L-BFGS, then Powell and Nelder-Mead, both gradient-free methods
        #
        #scipy.optimize.minimize(fun, x0, args=(), method=None, jac=None, hess=None, hessp=None, bounds=None, constraints=(), tol=None, callback=None, options=None)

        x0 = np.concatenate( [xu[1:-1], yu[1:-1], xv[1:-1], yv[1:-1], xw, yw[1:-1]] );  # qqq

        #increase gtol if this terminates due to loss of precision
        res = scipy.optimize.minimize( cost, x0, callback=newIt, options={'disp': True, 'gtol':2e-5 }, tol=1e-8 );
        #res = scipy.optimize.minimize( cost, x0, options={'ftol' : 1e-5, 'gtol':1e-5, 'eps':1e-6} );
        #res = scipy.optimize.minimize( cost, x0, method='SLSQP', bounds=bnds, options={'ftol' : 1e-5, 'gtol':1e-5, 'eps':1e-5} );
        #res = scipy.optimize.basinhopping(cost, x0, stepsize=0.01, niter=100 );
        #res = scipy.optimize.minimize(cost, x0, method="Nelder-Mead" );
        #res = scipy.optimize.minimize( cost, x0, method='L-BFGS-B' );
        #res = scipy.optimize.minimize(cost, x0, method='Powell' );
        #res = scipy.optimize.minimize(cost, x0, method='SLSQP' );

        print( );
        if "trace_result" in log:
            print(res);
        else:
            print( "after ", res.nit, " iterations, ", res.message, ", fun is ", res.fun );

#        if not ("success" in res.keys()) or res.success:  # xxx res.success crashes for some methods
        if True or res.success: # xxx lack of precision still gives a result
            xu[1:-1], yu[1:-1], xv[1:-1], yv[1:-1], xw, yw[1:-1] = np.array_split( res.x, [NN-2, 2*NN-4, 3*NN-6, 4*NN-8, 5*NN-8]); #qqq

            if "trace_result" in log:
                print("solution is ...");
                print( "xu is ", xu);
                print( "yu is ", yu);
                print( "xv is ", xv);
                print( "yv is ", yv);
                print( "xw is ", xw);
                print( "yw is ", yw);


            # check derivatives at each node pair...
            fdxdu = differentiate(unodes, xu)
            fdydu = differentiate(unodes, yu)
            fdxdv = differentiate(vnodes, xv)
            fdydv = differentiate(vnodes, yv)
            fdxdw = differentiate(wnodes, xw)
            fdydw = differentiate(wnodes, yw)
            maxerr = 0

            for i in range(NN):
                u = unodes[i]
                xucoord = evaluate(u, unodes, xu);
                yucoord = evaluate(u, unodes, yu);
                dxdu = evaluate(u, unodes, fdxdu)
                dydu = evaluate(u, unodes, fdydu)
                for j in range(NN):
                    v = vnodes[j]
                    xvcoord = evaluate(v, vnodes, xv);
                    yvcoord = evaluate(v, vnodes, yv);
                    dxdv = evaluate(v, vnodes, fdxdv)
                    dydv = evaluate(v, vnodes, fdydv)
                    wvalue = w(u,v);
                    xwcoord = evaluate(wvalue, wnodes, xw);
                    ywcoord = evaluate(wvalue, wnodes, yw);
                    dxdw = evaluate(wvalue, wnodes, fdxdw)
                    dydw = evaluate(wvalue, wnodes, fdydw)
                    dwdu = derivative(lambda uu: w(uu,v), u, dx=1e-6, order=5)
                    dwdv = derivative(lambda vv: w(u,vv), v, dx=1e-6, order=5)

                    lhs = dwdu*((xucoord-xvcoord)*dydw - (yucoord-yvcoord)*dxdw)
                    rhs = (xwcoord-xvcoord)*dydu - (ywcoord-yvcoord)*dxdu
                    t = abs(lhs - rhs)
                    if t > maxerr:
                        maxerr = t

                    lhs = dwdv*((xucoord-xvcoord)*dydw - (yucoord-yvcoord)*dxdw)
                    rhs = (xucoord-xwcoord)*dydv - (yucoord-ywcoord)*dxdv
                    t = abs(lhs - rhs)
                    if t > maxerr:
                        maxerr = t

                    lhs = dwdv*( (xwcoord-xvcoord)*dydu - (ywcoord-yvcoord)*dxdu  )
                    rhs = dwdu*( (xucoord-xwcoord)*dydv - (yucoord-ywcoord)*dxdv  )
                    t = abs(lhs - rhs)
                    if t > maxerr:
                        maxerr = t
            print("max derivative errror is {:.2g}".format( maxerr))



            # d is distance between checks needed so the check is of the order of every d mm
            d = 1
            print( "checking solution every ", d, "mm, ");
            ds = d/math.sqrt(height*width);   # fraction of the unit square
            maxdiff = 0;
            u = umin;
            while u <= umax:
                xucoord = evaluate(u, unodes, xu);
                yucoord = evaluate(u, unodes, yu);
                v = vmin
                while v <= vmax:
                    def report_alignment():
                        print( "u is ", u, " at pos (", xucoord, ",", yucoord, ")" );
                        print( "v is ", v, " at pos (", xvcoord, ",", yvcoord, ")" );
                        print( "w is ", wvalue, " at pos (", xwcoord, ",", ywcoord, ")" );
                        print( "alignment difference is {:5.2g} about {:5.2f} mm".format( difference, difference*math.sqrt(width*height) ));

                    xvcoord = evaluate(v, vnodes, xv);
                    yvcoord = evaluate(v, vnodes, yv);
                    wvalue = w(u,v);
                    xwcoord = evaluate(wvalue, wnodes, xw);
                    ywcoord = evaluate(wvalue, wnodes, yw);
                    difference = abs( (xucoord-xvcoord) * (yucoord - ywcoord) - (xucoord - xwcoord) * (yucoord - yvcoord) ) / math.hypot(xucoord-xvcoord, xvcoord-yvcoord);

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

                    # new v:
                    t1 = evaluate(v, vnodes, fdxdv)
                    t2 = evaluate(v, vnodes, fdydv)
                    v = v + ds/math.hypot( t1, t2)
                    #print("v is ", v, 100*(v-vmin)/(vmax-vmin), "%")

                # new u:
                t1 = evaluate(u, unodes, fdxdu)
                t2 = evaluate(u, unodes, fdydu)
                u = u + ds/math.hypot( t1, t2)
                #print("u is ", u, 100*(u-umin)/(umax-umin), "%")

            aler = maxdiff*math.sqrt(width*height)
            print( "alignment error is estimated at less than {:5.2g} mm".format( aler ));
            if aler > 0.2:
                print("alignment errors are possible - please check.")
                print("This nomogram used a polynomial of degree ", NN)
                print("Try increasing this, or reduce the range of one or more scales")


            # return the resulting scale lines into the nomogram parameters
            params_u.update({'f': lambda u: evaluate(u, unodes, xu),
                             'g': lambda u: evaluate(u, unodes, yu),
                             'h': lambda u: 1.0,
                             })
            params_v.update({'f': lambda v: evaluate(v, vnodes, xv),
                             'g': lambda v: evaluate(v, vnodes, yv),
                             'h': lambda v: 1.0,
                             })
            params_w.update({'f': lambda w: evaluate(w, wnodes, xw),
                             'g': lambda w: evaluate(w, wnodes, yw),
                             'h': lambda w: 1.0,
                             })

            #print config info
            datestr = datetime.datetime.now().strftime("%d %b %y")
            #print( "now is ", datestr )
            if aler > 0.01:
                tolstr =  r",\thinspace est \thinspace tolerance \thinspace {:5.2g} mm".format(aler)
            else:
                tolstr = ""

            txt = r'$\tiny \thinspace created \thinspace by \thinspace nomogen \tiny \thinspace {} {}$'.format(datestr, tolstr)
            #print("txt is \"", txt, "\"", sep='')

            idtext = {'x':2,
                     'y':0.0,
                      'text':txt,
                     'width':8,
                    }
            if 'extra_texts' not in main_params:
                main_params['extra_texts'] = [idtext]
            else:
                main_params['extra_texts'].append(idtext)


            # if the w scale is too close to one of the other scales,
            # the ticks on the scale lines could interfere
            # so swap sides unless the user has already done this ...
            if 'tick_side' not in params_w and -0.2 < calcAB(wnodes, xw,yw, vnodes, xv, yv):
                # the w scale line is close to the v scale line
                # => put the w ticks on the left side
                params_w.update({'tick_side':'left'})
            elif 'tick_side' not in params_u and -0.2 < calcAB(wnodes, xw,yw, unodes, xu, yu):
                # the w scale line is close to the u scale line
                # => put the u ticks on the left side
                params_u.update({'tick_side':'left'})


