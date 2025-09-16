#!/usr/bin/env python3
'''

 evaluate a polynomial with horner's method and barycentric interpolation
 plot errors to show instability and rounoff erors

 with no argument random polynomials are generated from a made up seed.
 use this seed as an argument to reproduce a previous set of plots - at least
 in the same environment.

 for horners method, rounoff errors increase for higher order polynmials and
 larger x
 degree 10 polynomial => when x==100 there is 100^10 term
 so polynomial is very sensitive to small changes in x
 near the roots, the relative error becomes large because function value is small

 these plots demonstrate that barycentric interpolation is more robust for both
 rounding errors and stability especially for higher order polynomials

'''

import sys
import math
import decimal
import pprint

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolours

print()
print( "\ntesting polynomial with horner's method and barycentric interpolation\n" )


decimal.getcontext().prec = 200

def hornerDec(ap, ax):
    '''
    evaluate a polynomial using decimal types for high precision
    ap - list of coefficients (float)
    ax - argument (float)
    '''
    poly_dec = map(decimal.Decimal,ap)
    x = decimal.Decimal(ax)
    #print( f'{x=}' )
    s = decimal.Decimal(0.0)
    for cc in poly_dec:
        s = s*x + cc
        #print( f'{s=}' )
    return float(s)


def horner(ap, ax):
    '''
    use horner's method to evaluate a polynomial
    ap - list of coefficients (float)
    ax - argument
    '''
    #print( f'{x=}' )
    s = 0.0
    for cc in ap:
        s = s*ax + cc
        #print( f'{s=}' )
    return s

# check that horner is correct
if horner( [3,2,1], 10 ) != 321:
    print( 'horner() failed' )
    sys.exit()


def bary(ax, an, fan):
    '''
    evaluate polynomial using barycentric interpolation on Chebyshev grid
    '''
    # special case: a is one of the grid points
    if ax in an:
        return fan[np.searchsorted(an, ax)]

    # apply correction factors
    # - first and last terms have weight 1/2,
    # - even terms have opposite sign
    if len(an) % 2 == 0:
        sumA = (fan[0]/(ax - an[0]) - fan[-1]/(ax - an[-1])) / 2
        sumB = (1/(ax - an[0]) - 1/(ax - an[-1])) / 2
    else:
        sumA = (fan[0]/(ax - an[0]) + fan[-1]/(ax - an[-1])) / 2
        sumB = (1 / (ax - an[0]) + 1 / (ax - an[-1])) / 2

    # barycentric interpolation on a Chebyshev grid ...
    for tan, tfan in zip(an, fan):
        t = 1 / (ax - tan)
        sumA = t * tfan - sumA
        sumB = t - sumB
    return sumA / sumB


def rms(a):
    '''
    return rms of vector a
    '''
    return np.sqrt(np.mean(a*a))


xmin=0; xmax=100
eps = np.finfo(float).eps


# log test environment & configuration
print( f'using python {sys.version} on {sys.platform}' )


# some versions of numpy do not support unicode
try:
    np.polynomial.set_default_printstyle('unicode')
except (ValueError, AttributeError) as e:
    print( f'{e}, using default instead' )

# set up the random number generator
# we need a seed so this run can be exactly reproduced later
if len(sys.argv) > 1:
    # user provided seed
    myseed =int( sys.argv[1] )
else:
    # make up a random seed
    myseed = np.random.randint( np.iinfo(int).max )
print( f'seed is {myseed}' )
rng = np.random.default_rng( seed=myseed )

# test & plot errors for polynomials of increasing degree
for degree in range(3,15):        # the polynomial degree

    print( '\n', '-'*15, f' testing polynomial degree {degree}' )

    npoints = degree+1
    #print( 'npoints =', npoints )

    # Chebyshev grid
    cheb = (xmin+xmax)/2 - (xmax-xmin)/2*np.cos(np.linspace(0,math.pi,npoints))
    #print( 'cheb is ', cheb )


    # make a random polynomial on a Chebyshev grid
    points_y = rng.uniform( -1, 1, npoints ) # range is -1 .. +1
    # print( 'polynomial points are ', list( zip(cheb, points_y) ) )
    # print( 'polynomial points are ', )
    # pprint.pprint( list(zip(cheb, points_y)), indent=4 )

    # get coefficients from points
    # p0 is the test polynomial
    # different environments might generate different polynomials from the same seed
    # TODO: to reproduce a specific test, read the coefficients
    #       from the corresponding log file instead
    p0 = np.polynomial.polynomial.polyfit(cheb, points_y, deg=degree)
    p0Str = np.polynomial.Polynomial(p0)
    print( 'polynomial is ', p0Str )
    with np.printoptions( floatmode='unique' ):
        print( 'exact polynomial cooefficients are' ); pprint.pprint( p0, indent=4 )
    p0 = p0[::-1] # reverse array
    #print( f'p0 is {p0}' )

    def fp(t):
        '''
        evaluate polynomial p0 exactly
        allow t to be scalar or array
        '''
        if np.ndim(t)==0:
            return hornerDec(p0,t)                          # scalar
        return np.array([hornerDec(p0,tt) for tt in t])     # array


    fcheb = fp(cheb)
    #print( 'fcheb is ', fcheb )

    # plot the function
    x = np.linspace( xmin, xmax, 500)
    l0 = plt.plot( x, fp(x), label='p(x)' )
    plt.xlabel("$x$")
    l1 = plt.scatter(cheb,  fcheb, color='red', s=30, marker='o', label='cheb grid')
    plt.ylabel(f"$p_{{ {degree} }}(x)$")


    plt.title( p0Str )
    plt.axhline(y=0,
                color=mcolours.TABLEAU_COLORS['tab:gray'],
                linestyle='--') # dashed line at y==0

    print()


    ############## plot errors for the polynomial

    N = 3000
    x = np.linspace( xmin, xmax, num=N)
    f0 = fp(x)
    fh = horner(p0,x)
    fc = np.array([bary(xx,cheb,fcheb) for xx in x])
    errh = abs((fh-f0)/(f0+eps))
    erre = abs((fc-f0)/(f0+eps))
    print( f'rms error for horner is {rms(errh):8.2e}, '
           f'max error is {max(errh):8.2e}' )
    print( f'rms error for evaluate is {rms(erre):8.2e}, '
           f'max error is {max(erre):8.2e}' )

    # plot errors
    err = plt.twinx()  # instantiate a second y axis that shares the same x-axis
    err.scatter( x,  np.log10(errh/eps+1), color='blue', s=1, marker='.' )
    err.scatter( x,  np.log10(erre/eps+1), color='red',  s=1, marker='.' )
    err.set_ylabel("lost significant digits")
    l2 = err.scatter([],  [], color='blue', s=20, marker='.', label='horner')
    l3 = err.scatter([],  [], color='red',  s=20, marker='.', label='barycentric')
    plt.legend(handles=[l1,l2,l3])

    plt.savefig( f'figure_{degree}.pdf' )
    plt.tight_layout()   # so equation is not chopped
    plt.show()
    print()

##################### end of pdemo.py #####################


