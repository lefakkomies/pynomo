#!/usr/bin/env python3

"""
    nomogen.py

    auto generator for nomograms

    use numerical techniques to derive a nomogram for a given function
    generate the pdf with pynomo


    Copyright (C) 2021-2024  Trevor Blight

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

# TODO:
# add error report
# investigate crooked tic marks at end of scales
# investigate infinite derivative problem


import sys
import datetime

import math
import numpy as np

import scipy
from scipy import interpolate

import functools


# relevant only for python >= 3.6
# pylint: disable=consider-using-f-string

# pylint: disable=invalid-name


# enable logging
# "trace_init" "trace_circ" "trace_cost" "trace_alignment" "trace_result"
log = {}

itNr = 0
eAcc = eDeru = eDerv = eShape = 0
old_cost = cost = 0


class Nomogen:
    """
    class Nomogen - numerically determine a nomogram from an equation
    inputs:
             func(a,b), return value is middle scale,
                        a & b are values on left and right scales
             params     as in Nomographer, but with these additions

                        'npoints' :
                         a measure of how many points are needed to
                         define each scale line in the nomogram

                        'muShape' :
                        set to non-zero so the ends of the outer axes
                        are not fixed to the corners of the unit square
    """

    def __init__( self, func, main_params ):


        #########################################
        # first have a look at the inputs
        #########################################

        if main_params['block_params'][0]['block_type'] != 'type_9':
            sys.exit( '''
            'type_9' block expected, found '{}'
            '''.format(main_params['block_params'][0]['block_type']) )

        # NN = nr Chebyshev nodes for the scales
        # the nodes have an index in the range 0 .. NN-1
        if 'pdegree' in main_params:
            pstr = 'pdegree'
            NN = main_params['pdegree']
            print( '''
            WARNING: parameter 'pdegree' has been renamed 'npoints' to more accurately describe its use.
            Please update your code.
            ''')
        else:
            pstr = 'npoints'
            if 'npoints' in main_params:
                NN = main_params['npoints']
            else:
                print( "\n'npoints' parameter not provided,", end=' ' )
                NN = 9

        if not isinstance(NN, int):
            print( "\n'{}' parameter must be an integer, found {} - ".format(pstr, type(NN)), end = ' ' )
            NN = 9
        else:
            if NN < 3:
                sys.exit( "{} must be >= 3 - quitting".format(pstr) )
        print( "using", NN, "Chebyshev points" )


        if 'muShape' not in main_params:
            muShape = 0
        else:
            muShape = 1.0e-14
            print( 'setting nomogram for best measureability, muShape is', muShape )

        global itNr
        itNr = 0


        # get the min & max input values
        # check for sanity
        # plotted values are log or linear, maybe one day exponential
        # convert between plotted and user values
        # if log scale, use log of corresponding variable
        # define plot * user conversion functions

        params_u = main_params['block_params'][0]['f1_params']
        umin_user = params_u['u_min']
        umax_user = params_u['u_max']
        if umax_user < umin_user:
            sys.exit("error: umax ({}) is less than umin ({})".format(umax_user, umin_user))
        if 'scale_type' in params_u and 'log' in params_u['scale_type']:
            if umin_user <= 0:
                sys.exit("error: cannot have umin ({}) <= 0 for log scale".format(umin_user))
            u_user = math.exp
            u_plot = math.log
        else:
            u_user = u_plot = lambda t: t

        params_v = main_params['block_params'][0]['f3_params']
        vmin_user = params_v['u_min']
        vmax_user = params_v['u_max']
        if vmax_user < vmin_user:
            sys.exit("error: vmax ({}) is less than vmin ({})".format(vmax_user, vmin_user))
        if 'scale_type' in params_v and 'log' in params_v['scale_type']:
            if vmin_user <= 0:
                sys.exit("error: cannot have vmin ({}) <= 0 for log scale".format(vmin_user))
            v_user = math.exp
            v_plot = math.log
        else:
            v_user = v_plot = lambda t: t

        params_w = main_params['block_params'][0]['f2_params']
        wmin = params_w['u_min']
        wmax = params_w['u_max']
        # get check the w scale range
        wval = [ wmin, wmax, func(umin_user, vmin_user), func(umax_user, vmin_user),
                 func(umin_user, vmax_user), func(umax_user, vmax_user) ]
        wmin_user = min(wval)
        wmax_user = max(wval)
        #print( 'wmin_user is', wmin_user, ', wmax_user is ', wmax_user )
        if 'scale_type' in params_w and 'log' in params_w['scale_type']:
            if wmin_user <= 0:
                sys.exit("error: cannot have wmin ({}) <= 0 for log scale".format(wmin_user))
            w_user = math.exp
            w_plot = math.log
        else:
            w_user = w_plot = lambda t: t

        # convert from user to plot values
        umin = u_plot(umin_user)
        umax = u_plot(umax_user)
        vmin = v_plot(vmin_user)
        vmax = v_plot(vmax_user)
        wmin = w_plot(wmin_user)
        wmax = w_plot(wmax_user)

        #######################################
        # call nomogram function
        # convert between plotted units and user-defined units
        # u, v and returned value are plot values,
        # call func with user-defined values
        def w(u, v):
            r = func( u_user(u), v_user(v) )
            return w_plot(r)

        width = 10 * main_params['paper_width']  # convert cm -> mm
        height = 10 * main_params['paper_height']

        # allow nomogram tolerance == +/- 0.1 mm
        # this is how many dots 0.1mm square fit into the nomogram area
        resolution = 10 * 10 * width * height



        ######################################################
        #
        # the nomogram is built inside a unit square
        # pynomo scales it at the point of output.
        #
        #####################################################


        #########################################
        #
        # initialise the calculations ....
        #
        ##########################################

        # grid for NN chebyshev points scaled to the interval [0,1]
        chebyGrid = (1 - np.cos(np.linspace(0, math.pi, NN)))/2
        unodes = umin + (umax - umin) * chebyGrid
        vnodes = vmin + (vmax - vmin) * chebyGrid
        wnodes = wmin + (wmax - wmin) * chebyGrid

        if "trace_init" in log:
            print("unodes is ", unodes)
            print("vnodes is ", vnodes)
            print("wnodes is ", wnodes)


        # the u scale has umax at the top, but which way up are the w & v scales?
        w0 = w(umin, vmin)
        w1 = w(umax, vmin)
        w2 = w(umin, vmax)
        w3 = w(umax, vmax)

        # w scale is max up (aligned to u scale) iff w1 > w0
        # v scale is max up (aligned to u scale) iff (w1 > w0) xor (w2 > w0)

        if (w1 > w0) == (w2 > w0):
            # vmax is at the top
            wB = w0   # bottom of w scale
            wE = w3   # top of w scale
            wG = w1   # intersection of TL-BR diagonal and w wsale
            wH = w2   # intersection of TR-BL diagonal and w wsale
            yv0 = 0   # y coord of vmin
            yv2 = 1   # y coord of vmax
        else:
            # vmax is at the bottom
            wB = w2   # bottom of w scale
            wE = w1   # top of w scale
            wG = w3   # intersection of TL-BR diagonal and w wsale
            wH = w0   # intersection of TR-BL diagonal and w wsale
            yv0 = 1   # y coord of vmin
            yv2 = 0   # y coord of vmax

        if wE > wB:
            yw0 = 0   # y coord of wmin
            yw2 = 1   # y coord of vmax
        else:
            yw0 = 1   # y coord of wmin
            yw2 = 0   # y coord of vmax

        if "trace_init" in log:
            print( "wB is ", wB, ", wE is ", wE, ", wG is ", wG, ", wH is ", wH )


        ####################################################
        # the initial condition is a nomogram where
        # - the u & v scales vary linearly from (0,0) to (0,1) along the
        #   left and right edges of the unit square
        # - an initial estimate for the w scale needs to be determined

        xu = np.zeros(NN)
        yu = chebyGrid
        xv = np.ones(NN)
        yv = yv0 + (yv2-yv0)*chebyGrid

        # find an initial position and slope for the xw scale
        if math.isclose( wG, wH ):
            # the diagonal index lines meet near the middle of the nomogram
            # this is a degenerate case, so just use a vertical line
            xw = np.full(NN, 0.5)

            # yw(w) goes thru (wB,0), (wG,0.5) & (wE,1)
            # Note: the wX might not be in increasing order (ie wB might be wmax)
            yw = np.array( [scipy.interpolate.interp1d( [wB, wG, wE], [0, 0.5, 1] )(w) \
                            for w in wnodes] )

            # check the calcs ...
            ywB, ywG, ywE = scipy.interpolate.barycentric_interpolate(wnodes, yw, [wB, wG, wE])
            if "trace_init" in log:
                print("yw is ", yw)
                print( 'evaluated wB, wG, wE are ', ywB, ywG, ywE )

            if not math.isclose( ywB, 0.0, abs_tol= 10*sys.float_info.epsilon ):
                sys.exit( "initial w scale failed for ywB test ({}, expected 0) - quitting".format(ywB) )
            #if not math.isclose(ywG, 0.5):
            #    sys.exit("initial y scale failed for ywG test - quitting")
            if not math.isclose(ywE, 1.0):
                sys.exit( "initial w scale failed for ywE test ({}, expected 1) - quitting".format(ywB) )
        else:
            # we can use a linear estimate
            alphaxw = (wE - wG - wH + wB) / (wE - wB) / (wG - wH)
            xwB = (wH - wB) / (wE - wB) - alphaxw * (wH - wB)
            xwE = xwB + alphaxw * (wE - wB)
            if "trace_init" in log:
                print("linear initial estimate found")
                print("xwB is ", xwB, ", xwE is ", xwE)

            # clip to unit square
            if xwE > 1:
                xwE = 1
            elif xwE < 0:
                xwE = 0
            if xwB > 1:
                xwB = 1
            elif xwB < 0:
                xwB = 0

            xw =  xwB + chebyGrid * (xwE - xwB)
            yw = yw0 + (yw2-yw0)*chebyGrid


        #################################################
        #
        # evaluate function at a,
        # given an array of Chebyshev nodes and function values
        # a   - perform barycentric interpolation at position a
        # an  - array of nodes
        # fan - array of function values at the nodes an

        def evaluate(a, an, fan):

            # special case: a is one of the grid points
            if a in an:
                return fan[np.searchsorted(an, a)]

            # apply correction factors
            # - first and last terms have weight 1/2,
            # - even terms have opposite sign
            if len(an) % 2 == 0:
                sumA = (fan[0]/(a - an[0]) - fan[-1]/(a - an[-1])) / 2
                sumB = (1/(a - an[0]) - 1/(a - an[-1])) / 2
            else:
                sumA = (fan[0] / (a - an[0]) + fan[-1] / (a - an[-1])) / 2
                sumB = (1 / (a - an[0]) + 1 / (a - an[-1])) / 2

            # barycentric interpolation on a Chebyshev grid ...
            for tan, tfan in zip(an, fan):
                t = 1 / (a - tan)
                sumA = t * tfan - sumA
                sumB = t - sumB
            return sumA / sumB


        ############################################################
        #
        # calculate derivative matrix for a chebyshev grid
        # see cheb.m in "Spectral Methods in Matlab", Ch 6, by Lloyd N. Trefethen
        # x: the chebyshev grid
        # return the derivative matrix
        def diffmat(x):

            n = len(x)

            # deal with the pathological case
            if n == 0:
                return 0

            # replicate the Chebyshev grid onto a nxn matrix
            XX = np.tile( x, (n,1) )

            # coefficients, alternating 1/-1/..., first & last entries are +/-2
            c = np.empty((n,1))  # column vector
            c[::2] = 1            # evens
            c[1::2] = -1          # odds
            c[0] = 2; c[-1] *= 2  # first * last

            D = c * (1/c).T  # nxn matrix

            # off diagonal entries
            dXX = XX.T - XX + np.eye(n)
            D = D / dXX

            # diagonal entries - subtract sum of each row
            for ii in range(n):
                D[ii][ii] -= D[ii].sum()

            return D


        #############################################################
        #
        # find the derivative of function f at position x
        # detect range and value errors
        # x1 & x0 are max * min values of x, used to calculate step size
        #
        # formulas taken from Fornberg:
        # "Generation of Finite Difference Formulas on Arbitrarily Spaced Grids",
        # Mathematics of Computation, Vol 51, nr 184, Oct 1988, pp 699-706

        def derivative(f, x, x1, x0):
            try:
                h = 1.0e-4*(x1-x0)
                r = (f(x-2*h) - 8*f(x-h) + 8*f(x+h) - f(x+2*h))/(12*h)
                if math.isnan(r):
                    # try a one sided derivative (does not work well, commented out)
                    # assume error is caused by exceding valid domain of f
                    # magically gives h the correct sign, assuming x is one of {x0, x1}
                    #h = ((x1+x0) - 2*x)*1e-4
                    #r = (-25*f(x) + 48*f(x+h) - 36*f(x+2*h) + 16*f(x+3*h) - 3*f(x+4*h))/(12*h)
                    print( 'derivative nan at x={}, max={}, min={}, result={}'.format(x, x1,x0, r) )
            except ValueError:
                # magically gives h the correct sign, assuming x is one of {x0, x1}
                #h = ((x1+x0) - 2*x)*1e-4
                #r = (-25*f(x) + 48*f(x+h) - 36*f(x+2*h) + 16*f(x+3*h) - 3*f(x+4*h))/(12*h)
                r = math.nan
                print( 'derivative exception at x={}, max={}, min={}, result={}'.format(x, x1,x0, r) )
            return r


        #############################################################
        #
        # these arrays define the x & y coordinates of the scales
        #
        baryu = scipy.interpolate.BarycentricInterpolator(unodes)
        baryv = scipy.interpolate.BarycentricInterpolator(vnodes)
        baryw = scipy.interpolate.BarycentricInterpolator(wnodes)

        w_values = np.array([[w(u, v) for v in vnodes] for u in unodes])  # L141

        dwdu_values = np.array( [[ derivative(lambda uu: w(uu, v), u, umax, umin ) \
                                   for v in vnodes] for u in unodes])

        dwdv_values = np.array( [[derivative(lambda vv: w(u, vv), v, vmax, vmin ) \
                                  for v in vnodes] for u in unodes])

        diffmatu = diffmat( unodes )
        diffmatv = diffmat( vnodes )
        diffmatw = diffmat( wnodes )


        #######################################
        #
        # this is the optimisation function
        #
        def calc_cost(dummy):

            """
            find cost of candidate nomogram
            cost has components, alignment accuracy, slope accuracy and area optimisation
            - max error in accuracy is < 0.1 mm
            - must fill size (height x width) as much as possible,
              so too small or too big are errors

            the accuracy component is comprised of
            - position error
            - gradient error

            the size component is optional
            - depends on muShape being non-zero
            It calculates a measurability score: a combination of
            - the scale of the axes
            - the angle of the index lines
            There is a cost of exceeding the nomogram boundary

            normalise each error
            - per point pair, and
            - per range
            """

            if muShape != 0:
                lxu, lyu, lxv, lyv, lxw, lyw =  np.array_split(dummy, 6)  # qqq

                # the cost of straying outside the unit square:
                # the exp function gets big quickly as the points approach
                # & exceed the boundaries of the unit square.
                # apply this function to each point in the u & v axes
                aa = 40
                cost_pos_u = np.exp(aa*(-0.3-lxu)) + np.exp(aa*(lxu-1.3)) + \
                    np.exp(aa*(-0.3-lyu)) + np.exp(aa*(lyu-1.3)) + 1
                cost_pos_v = np.exp(aa*(-0.3-lxv)) + np.exp(aa*(lxv-1.3)) + \
                    np.exp(aa*(-0.3-lyv)) + np.exp(aa*(lyv-1.3)) + 1

            else:
                # the corner coordinates are fixed, so don't use them
                lxu, lyu, lxv, lyv, lyw = xu, yu, xv, yv, yw
                lxu[1:-1], lyu[1:-1], lxv[1:-1], lyv[1:-1], lxw, lyw[1:-1] = \
                np.array_split( dummy, [NN-2, 2*NN-4, 3*NN-6, 4*NN-8, 5*NN-8]) #qqq

            if "trace_cost" in log:
                print("\ntry")
                print("lxu is ", lxu)
                print("lyu is ", lyu)
                print("lxv is ", lxv)
                print("lyv is ", lyv)
                print("lxw is ", lxw)
                print("lyw is ", lyw)
                print()

            global eAcc, eDeru, eDerv
            global eShape
            eAcc = eDeru = eDerv = eShape = 0


            # estimate position & derivative error

            fdxdu = diffmatu @ lxu
            fdydu = diffmatu @ lyu
            fdxdv = diffmatv @ lxv
            fdydv = diffmatv @ lyv
            fdxdw = diffmatw @ lxw
            fdydw = diffmatw @ lyw


            # precalculate coordinates and derivatives for w outside loop for speedup
            baryw.set_yi(lxw)
            txwa = baryw(w_values)
            baryw.set_yi(lyw)
            tywa = baryw(w_values)
            baryw.set_yi(fdxdw)
            dxdwa = baryw(w_values)
            baryw.set_yi(fdydw)
            dydwa = baryw(w_values)


            for iu in range(len(unodes)):
                txu = lxu[iu]
                tyu = lyu[iu]
                dxdu = fdxdu[iu]
                dydu = fdydu[iu]

                u = unodes[iu]

                for iv in range(len(vnodes)):
                    txv = lxv[iv]
                    tyv = lyv[iv]
                    dxdv = fdxdv[iv]
                    dydv = fdydv[iv]

                    txw = txwa[iu][iv]
                    tyw = tywa[iu][iv]
                    dxdw = dxdwa[iu][iv]
                    dydw = dydwa[iu][iv]

                    v = vnodes[iv]
                    tx = txu - txv
                    ty = tyu - tyv
                    td2 = tx * tx + ty * ty
                    td = math.sqrt(td2)
                    e0 = (tx * (tyu - tyw) - (txu - txw) * ty) / td #[d]
                    if td2 * resolution > 1:
                        eAcc += e0*e0                               #[d^2]

                    tmp = ty * dxdw - tx * dydw                     #[xy]/[w]
                    tuc = e0 * (tx * dxdu + ty * dydu) / td2        # [d]/[u]
                    tvc = e0 * (tx * dxdv + ty * dydv) / td2        # [d]/[v]


                    ### these values are predefined for speedup L141
                    dwdu = dwdu_values[iu][iv]
                    quitOnNan = True               # bravely carrying on doesn't work well
                    if not math.isnan(dwdu):
                        dedu = ((dwdu * tmp + (tyv - tyw) * dxdu - (txv - txw) * dydu)) / td - tuc #[d]/[u] - [d]/[u]
                        eDeru += dedu ** 2         #[d^2]/[u^2]
                    elif quitOnNan:
                        sys.exit( """
error: the u scale line around the region u = {} cannot be represented by a finite polynomial!
       please reduce limits on this scale and try again
                                 """.format(u_user(u)) )

                    dwdv = dwdv_values[iu][iv]
                    if not math.isnan(dwdv):
                        dedv = ((dwdv * tmp + (tyw - tyu) * dxdv - (txw - txu) * dydv)) / td + tvc  #[d]/[v] + [d]/[v]
                        eDerv += dedv ** 2
                    elif quitOnNan:
                        sys.exit( """
error: the v scale line around the region v = {} cannot be represented by a finite polynomial!
       try again with reduced limits on this scale
                                 """.format(v_user(v)) )

                    check = True  # checks are slow
                    check = False
                    if check:
                        def gete0(au, av):
                            xau = evaluate(au, unodes, lxu)
                            yau = evaluate(au, unodes, lyu)
                            xav = evaluate(av, vnodes, lxv)
                            yav = evaluate(av, vnodes, lyv)
                            tw = w(au, av)
                            xtw = evaluate(tw, wnodes, lxw)
                            ytw = evaluate(tw, wnodes, lyw)
                            return (xau * yav + xtw * (yau - yav) + (xav - xau) * ytw - xav * yau) \
                                / math.hypot((xau - xav), (yau - yav))

                        if not math.isclose(e0, gete0(u, v), rel_tol=1e-05, abs_tol=1e-7):
                            sys.exit("gete0() error")

                        aa = v
                        tu = derivative( lambda uu: gete0(uu, aa), u, umax, umin )
                        if not math.isclose(tu, dedu, rel_tol=1e-05, abs_tol=1e-7):
                            print("(u,v) is (", u, ",", v, "), \
                            dedu is ", dedu, ", tu is ", tu, ", tuc is ", tuc)
                            sys.exit("dedu error")

                        aa = u
                        tv = derivative( lambda vv: gete0(aa, vv), v, vmax , vmin )
                        if not math.isclose(tv, dedv, rel_tol=1e-05, abs_tol=1e-7):
                            print("(u,v) is (", u, ",", v, "), dedv is ", dedv, ", tv is ", tv)
                            sys.exit("dedv error")


                    # calculate cost of shape
                    # include cost of position
                    # u & v axes
                    # divide by range of u to make eShape independent of u units, etc
                    if muShape != 0:
                        t = 0.01*(umax-umin)*(umax-umin) + u*u
                        uShape = ((dxdu*ty - dydu*tx))**2 * t   #[x^2 y^2 / u^2] * [u^2]
                        t = 0.01*(vmax-vmin)*(vmax-vmin) + v*v
                        vShape = ((dxdv*ty - dydv*tx))**2 * t
                        tShape = td2 * ( 1/uShape + 1/vShape)         # 1/[d^2]

                        tShape *= cost_pos_u[iu] + cost_pos_v[iv]
                        eShape += tShape

            # make eDeru independent of the scale of u,
            # so multiply by range of u to cancel units
            # eDeru has units (xy/u)**2
            eDeru *= (umax - umin) ** 2                      # [d^2]
            eDerv *= (vmax - vmin) ** 2                      # [d^2]

            eShape *= muShape

            # mu sets relative priority of eAcc & eDerx
            # TODO:
            #       investigate a good value for mu
            #
            # there is one error term for each pair of points
            # so normalise to average error per point pair.
            mu = 1
            global cost
            cost = (eAcc + \
                    mu * (eDeru + eDerv) + \
                    eShape) / \
                    (len(unodes) * len(vnodes))
            return cost


        # run this function whenever the optimise function enters a
        # new iteration
        def newStep(xk):
            global itNr
            global old_cost

            itNr += 1
            print("\r", main_params['filename'], " costs: {:3d}".format(itNr), sep="", end="")
            print(", eAcc {:.2e}".format(eAcc), end='')
            print(", eDer {:.2e}, {:.2e}".format(eDeru, eDerv), end='')
            if muShape != 0:
                print(", eShape {:.2e}".format(eShape), end='')
            if old_cost != 0 and cost < old_cost:
                print(", cost improvement is {:2.0f}%".format(100 * (old_cost - cost) / old_cost), end='')
            old_cost = cost

        #
        # the nomogram is given by the coordinates of the node points that
        # minimises the error
        #

        # prefer BFGS or L-BFGS, then Powell and Nelder-Mead, both gradient-free methods
        #
        # scipy.optimize.minimize(fun, x0, args=(), method=None, jac=None, hess=None, hessp=None, bounds=None, constraints=(), tol=None, callback=None, options=None)

        assert len(xu) == NN
        if muShape != 0:
            x0 = np.concatenate([xu, yu, xv, yv, xw, yw])  # qqq
        else:
            x0 = np.concatenate([xu[1:-1], yu[1:-1], \
                                 xv[1:-1], yv[1:-1], \
                                 xw, yw[1:-1]])  # qqq


        # increase gtol if this terminates due to loss of precision
        res = scipy.optimize.minimize( calc_cost, x0, callback=newStep,
                options={'disp': False, 'gtol': 1e-4, 'maxiter': None},
                tol=1e-4 )


        ########################################
        #
        # check & report results
        #
        ########################################

        print()
        if "trace_result" in log:
            print(res)
        else:
            # print( "after ", res.nit, " iterations, ")
            print("cost function is {:.2e}, ".format(res.fun), res.message, sep='')

        #        if not ("success" in res.keys()) or res.success:  # xxx res.success crashes for some methods
        if True or res.success:  # xxx lack of precision still gives a result
            if muShape != 0:
                xu, yu, xv, yv, xw, yw = \
                    np.array_split(res.x, 6)  # qqq
            else:
                xu[1:-1], yu[1:-1], xv[1:-1], yv[1:-1], xw, yw[1:-1] = \
                    np.array_split(res.x, \
                                   [NN - 2, 2 * NN - 4, 3 * NN - 6, \
                                    4 * NN - 8, 5 * NN - 8])  # qqq

            if "trace_result" in log:
                print("solution is ...")
                print("xu is ", xu)
                print("yu is ", yu)
                print("xv is ", xv)
                print("yv is ", yv)
                print("xw is ", xw)
                print("yw is ", yw)


            # check derivatives at each node pair...
            fdxdu = diffmatu @ xu
            fdydu = diffmatu @ yu
            fdxdv = diffmatv @ xv
            fdydv = diffmatv @ yv
            fdxdw = diffmatw @ xw
            fdydw = diffmatw @ yw

            maxerr = 0

            baryw.set_yi(fdxdw)
            dxdwa = baryw(w_values)
            baryw.set_yi(fdydw)
            dydwa = baryw(w_values)
            baryw.set_yi(xw)
            xwcoorda = baryw(w_values)
            baryw.set_yi(yw)
            ywcoorda = baryw(w_values)

            for i in range(len(unodes)):
                xucoord = xu[i]
                yucoord = yu[i]
                dxdu = fdxdu[i]
                dydu = fdydu[i]

                for j in range(len(vnodes)):
                    xvcoord = xv[j]
                    yvcoord = yv[j]
                    dxdv = fdxdv[j]
                    dydv = fdydv[j]
                    wvalue = w_values[i][j]

                    xwcoord = xwcoorda[i,j]
                    ywcoord = ywcoorda[i,j]
                    dxdw = dxdwa[i,j]
                    dydw = dydwa[i,j]

                    dwdu = dwdu_values[i][j]
                    dwdv = dwdv_values[i][j]
                    lhs = dwdu * ((xucoord - xvcoord) * dydw - (yucoord - yvcoord) * dxdw)
                    rhs = (xwcoord - xvcoord) * dydu - (ywcoord - yvcoord) * dxdu
                    t = abs(lhs - rhs)*(umax-umin)
                    if t > maxerr:
                        maxerr = t

                    lhs = dwdv * ((xucoord - xvcoord) * dydw - (yucoord - yvcoord) * dxdw)
                    rhs = (xucoord - xwcoord) * dydv - (yucoord - ywcoord) * dxdv
                    t = abs(lhs - rhs)*(vmax-vmin)
                    if t > maxerr:
                        maxerr = t

                    lhs = dwdv * ((xwcoord - xvcoord) * dydu - (ywcoord - yvcoord) * dxdu)
                    rhs = dwdu * ((xucoord - xwcoord) * dydv - (yucoord - ywcoord) * dxdv)
                    t = abs(lhs - rhs)*(umax-umin)*(vmax-vmin)/(wmax-wmin)
                    if t > maxerr:
                        maxerr = t
            print("max derivative errror is {:.2g}".format(maxerr))



            # now iterate over the length of the u & v scales,
            # verifying the nomogram at each step

            # verify alignment every d mm
            d = 1  # choose d
            print("checking solution every ", d, "mm, ")
            ds = d / math.sqrt(height * width)  # step size as fraction of the unit square

            baryfdxdu = scipy.interpolate.BarycentricInterpolator(unodes, fdxdu)
            baryfdydu = scipy.interpolate.BarycentricInterpolator(unodes, fdydu)
            upoints = []
            u = umin
            while u <= umax:
                #print("u is ", u, 100*(u-umin)/(umax-umin), "%")
                upoints.append(u)
                dx = baryfdxdu( u )
                dy = baryfdydu( u )
                # next u:
                dd = ds / math.hypot(dx, dy)
                if u + dd > umax and u < umax:
                    u = umax
                else:
                    u = u+dd


            baryfdxdv = scipy.interpolate.BarycentricInterpolator(vnodes, fdxdv)
            baryfdydv = scipy.interpolate.BarycentricInterpolator(vnodes, fdydv)
            vpoints = []
            v = vmin
            while v <= vmax:
                #print("v is ", v, 100*(v-vmin)/(vmax-vmin), "%")
                vpoints.append(v)
                dx = baryfdxdv( v )
                dy = baryfdydv( v )
                # next v:
                dd = ds / math.hypot(dx, dy)
                if v + dd > vmax and v < vmax:
                    v = vmax
                else:
                    v = v+dd


            baryu.set_yi(xu)
            xucoorda = baryu(upoints)
            baryu.set_yi(yu)
            yucoorda = baryu(upoints)

            baryv.set_yi(xv)
            xvcoorda = baryv(vpoints)
            baryv.set_yi(yv)
            yvcoorda = baryv(vpoints)

            maxdiff = 0
            for u, xucoord, yucoord in zip( upoints, xucoorda, yucoorda ):
                for v, xvcoord, yvcoord in zip( vpoints, xvcoorda, yvcoorda ):
                    def report_alignment(difference, xwcoord, ywcoord):
                        print("u is ", u_user(u), " at pos (", xucoord, ",", yucoord, ")")
                        print("v is ", v_user(v), " at pos (", xvcoord, ",", yvcoord, ")")
                        print("w is ", w_user(wvalue), " at pos (", xwcoord, ",", ywcoord, ")")
                        print( "alignment difference is {:5.2g} about {:5.2f} mm".format(difference, difference * math.sqrt(width * height)) )

                    wvalue = w(u, v)
                    xwcoord = evaluate(wvalue, wnodes, xw)
                    ywcoord = evaluate(wvalue, wnodes, yw)
                    difference = abs((xucoord - xvcoord) * (yucoord - ywcoord) - (xucoord - xwcoord) * (yucoord - yvcoord)) / \
                        math.hypot(xucoord - xvcoord, xvcoord - yvcoord)

                    if wvalue < wmin and not math.isclose(wvalue, wmin, rel_tol = 0.01):
                        report_alignment(difference, xwcoord, ywcoord)
                        print( "scale range error, please check w scale min limits", \
                               "\nw({:g}, {:g}) = {:g} < wmin, {:g}".format(u_user(u), v_user(v), w_user(wvalue), wmin_user))
                        #sys.exit("scale range error, please check w scale min limits"
                              #   "\nw({:g}, {:g}) = {} < wmin, {}".format(u, v, wvalue, wmin))
                    elif wvalue > wmax and not math.isclose(wvalue, wmax, rel_tol = 0.01):
                        report_alignment(difference, xwcoord, ywcoord)
                        print("scale range error, please check w scale max limits", \
                              "\nw({:g}, {:g}) = {:g} > wmax, {:g}".format(u_user(u), v_user(v), w_user(wvalue), wmax_user))
                        #sys.exit("scale range error, please check w scale max limits"
                               #  "\nw({:g}, {:g}) = {} > wmax, {}".format(u, v, wvalue, wmax))

                    if difference > maxdiff:
                        maxdiff = difference
                        if "trace_alignment" in log:
                            report_alignment(difference, xwcoord, ywcoord)


            aler = maxdiff * math.sqrt(width * height)
            print("alignment error is estimated at less than {:5.2g} mm".format(aler))
            if aler > 0.2:
                print("alignment errors are possible - please check.")
                print( "This nomogram used a polynomial defined with {} points ".format(NN) )
                print("Try increasing this, or reduce the range of one or more scales")

            # return the resulting axes into the nomogram parameters
            params_u.update({'f': lambda u: evaluate(u_plot(u), unodes, xu),
                             'g': lambda u: evaluate(u_plot(u), unodes, yu),
                             'h': lambda u: 1.0,
                             })
            params_v.update({'f': lambda v: evaluate(v_plot(v), vnodes, xv),
                             'g': lambda v: evaluate(v_plot(v), vnodes, yv),
                             'h': lambda v: 1.0,
                             })
            params_w.update({'f': lambda w: evaluate(w_plot(w), wnodes, xw),
                             'g': lambda w: evaluate(w_plot(w), wnodes, yw),
                             'h': lambda w: 1.0,
                             })

            # get & print footer info
            if 'footer_string' in main_params:
                txt = r'\tiny \hfil {} \hfil'.format( main_params['footer_string'])
            else:
                datestr = datetime.datetime.now().strftime("%d %b %y")
                if aler > 0.1:
                    tolstr = r", est tolerance {:5.2g} mm".format(aler)
                else:
                    tolstr = ""

                # '\' char is escape, '_' char is subscript, '$' is math mode, etc
                escapes = "".maketrans({ '\\': r'$ \backslash $',
                                         '^': r'\^{}',
                                         '_': r'\_',
                                         '~': r'$ \sim $',
                                         '$': r'\$',
                                         '#': r'\#',
                                         '%': r'\%',
                                         '&': r'\&',
                                         '{': r'\{',
                                         '}': r'\}' })
                txt = r'\tiny \hfil {}: created by nomogen {} {} \hfil'. \
                      format( main_params['filename'].translate(escapes), datestr, tolstr)
                #print("txt is \"", txt, "\"", sep='')

            footerText = {'x': 0,
                          'y': 0.0,
                          'text': txt,
                          'width': width/10,
                      }
            if 'extra_texts' not in main_params:
                main_params['extra_texts'] = [footerText]
            else:
                main_params['extra_texts'].append(footerText)


            ##################################################
            # check if the tic marks on the scales clash
            # swap sides if the w scale is too close to one of the outer scales
            # unless the user has already specified a preference ...

            # account for v & w scales increasing downwards
            if yw[0] > yw[-1]:
                txw = xw[::-1]
                wEast = 'left'
                wWest = 'right'
            else:
                txw = xw
                wEast = 'right'
                wWest = 'left'
            if yv[0] > yv[-1]:
                txv = xv[::-1]
                vEast = 'left'
            else:
                txv = xv
                vEast = 'right'

            # the distance between axes
            distuw = txw - xu
            distvw = txv - txw

            if not 'tick_side' in params_u and np.min(distuw) < 0.2:
                print('putting u scale ticks on left side')
                params_u.update({'tick_side': 'left'})

            if (not 'tick_side' in params_v) and (np.min(distvw) < 0.2):
                print( 'putting v scale ticks on {} side'.format(vEast) )
                params_v.update({'tick_side': vEast})
                params_v.update({'turn_relative': True})


            #print( 'vw norm is ', np.linalg.norm(xv - xw), ', uw norm is ', np.linalg.norm(xw - xu) )
            if not 'tick_side' in params_w:
                if np.linalg.norm(distuw) > np.linalg.norm(distvw):
                    # the w scale line is closer to the v scale line
                    params_w.update({'tick_side': wWest})
                else:
                    # the w scale line is closer to the u scale line
                    params_w.update({'tick_side': wEast})
                params_w.update({'turn_relative': True})
                print( 'putting w scale ticks on {} side'.format(params_w['tick_side']) )


            # check for dual scales
            # the first block holds the type_9 axes, (params_u, etc)
            # then type_8 or maybe type_9 blocks follow with the dual scales

            ## TODO:
            # atm the dual scales are considered after calculating the axes.
            # in a future version, more than a single equation might be allowed,
            # so the blocks should be analysed before the scales are calculated

            for params in [params_u, params_v, params_w]:
                if 'tag' in params:
                    # look for a matching tag
                    # check and copy the newly calculated functions across
                    ltag = params['tag']
                    for b in main_params['block_params'][1:]:
                        if b['block_type'] == 'type_8':
                            if not 'f_params' in b:
                                sys.exit('''
                                dual axis tag '{}' should have an 'f_params' parameter
                                '''.format(ltag) )
                            laxis = b['f_params']
                            if 'tag' in laxis and laxis['tag'] == ltag:
                                # don't copy function if the user has already defined one
                                if not 'function_x' in laxis:
                                    print( 'dual scales found for axes with tag \'{}\''.format(ltag) )
                                    if not 'align_func' in laxis:
                                        sys.exit('''
                                        dual axis tag '{}' must have an 'align_func' parameter
                                        '''.format(ltag) )
                                    fal = laxis['align_func']
                                    # params & fal must be evaluated now, not when 'fuction_?' is called
                                    laxis['function_x'] = functools.partial(lambda u, p, f: p['f'](f(u)),
                                                                            p=params, f=fal)
                                    laxis['function_y'] = functools.partial(lambda u, p, f: p['g'](f(u)),
                                                                            p=params, f=fal)

                        elif b['block_type'] == 'type_9':
                            for fp in [ 'f1_params', 'f2_params', 'f3_params' ]:
                                if not fp in b:
                                    sys.exit('''
                                    dual axis tag '{}' should have an '{}' parameter
                                    '''.format(ltag, fp) )
                                laxis = b[fp]
                                # don't copy function if the user has already defined one
                                if not 'f' in laxis:
                                    if 'tag' in laxis and laxis['tag'] == ltag:
                                        print( 'dual scales found for axes with tag \'{}\''.format(ltag) )
                                        if not 'align_func' in laxis:
                                            sys.exit('''
                                            dual axis tag '{}' must have an 'align_func' parameter
                                            '''.format(ltag) )
                                        fal = laxis['align_func']
                                        # params & fal must be evaluated now, not when 'fuction_?' is called
                                        laxis['f'] = functools.partial(lambda u, p, f: p['f'](f(u)),
                                                                                p=params, f=fal)
                                        laxis['g'] = functools.partial(lambda u, p, f: p['g'](f(u)),
                                                                                p=params, f=fal)
                                        laxis['h'] = params['h']


     # end of __init__

######################### end of nomogen.py ########################
