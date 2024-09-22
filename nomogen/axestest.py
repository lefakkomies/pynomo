#!/usr/bin/env python3

'''
 nomogen test program
 verify orientation of axes, for all combinations of:
    v & w axis up/down
    linear/log scales
    symetrical/non-symetrical cases

 usage:

      axestest n
      where n is an integer denoting a test number

'''
# pylint: disable=C

import sys
import platform
import subprocess
import os

sys.path.insert(0, "..")

from nomogen import Nomogen
from pynomo.nomographer import Nomographer


###############################################################
#
# nr Chebyshev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value is faster, makes a smoother curve,
#     but could be less accurate
NN = 3


# simple axes tests for each test case ...

for test_nr in range(1,17):

    if test_nr == 1:
        w = lambda u,v: u+v
        scale_type = 'linear smart'
        title_str = r'$w = u + v$'
    elif test_nr == 2:
        w = lambda u, v: u - v
        scale_type = 'linear smart'
        title_str = r'$w = u - v$'
    elif test_nr == 3:
        w = lambda u, v: -(u + v)
        scale_type = 'linear smart'
        title_str = r'$w = -(v + u)$'
    elif test_nr == 4:
        w = lambda u, v: v - u
        scale_type = 'linear smart'
        title_str = r'$w = v - u$'
    elif test_nr == 5:
        w = lambda u, v: u*v
        scale_type = 'log smart'
        title_str = r'$w  uv$'
    elif test_nr == 6:
        w = lambda u, v: u / v
        scale_type = 'log smart'
        title_str = r'$w = {u \over v}$'
    elif test_nr == 7:
        w = lambda u, v: 1 / (u*v)
        scale_type = 'log smart'
        title_str = r'$w = {1 \over {uv}}$'
    elif test_nr == 8:
        w = lambda u, v: v / u
        scale_type = 'log smart'
        title_str = r'$w = {v \over u}$'
    elif test_nr == 9:
        w = lambda u,v: u*u+v
        scale_type = 'linear smart'
        title_str = r'$w = u^2 + v$'
    elif test_nr == 10:
        w = lambda u, v: u*u - v
        scale_type = 'linear smart'
        title_str = r'$w = u^2-v$'
    elif test_nr == 11:
        w = lambda u, v: -(u*u + v)
        scale_type = 'linear smart'
        title_str = r'$w = -(u^2 + v)$'
    elif test_nr == 12:
        w = lambda u, v: v - u*u
        scale_type = 'linear smart'
        title_str = r'$w = v - u^2$'
    elif test_nr == 13:
        w = lambda u, v: u*u*v
        scale_type = 'log smart'
        title_str = r'$w = u^2v$'
    elif test_nr == 14:
        w = lambda u, v: u*u / v
        scale_type = 'log smart'
        title_str = r'$w = {u^2 \over v}$'
    elif test_nr == 15:
        w = lambda u, v: 1 / (u*u*v)
        scale_type = 'log'                            # log smart -> bug in printing!
        title_str = r'$w = {1 \over {u^2v}}$'
    elif test_nr == 16:
        w = lambda u, v: v / u / u
        scale_type = 'log smart'
        title_str = r'$w = {v \over {u^2}}$'
    else:
        sys.exit( 'there is no test number ({})'.format(test_nr) )

    test_name = 'axtest{}'.format(test_nr)

    t = test_nr - 1
    symStr = 'symmetrical' if t %16 < 8 else 'non-symmetrical'
    scaleStr = 'linear' if t % 8 < 4 else 'log'
    wStr = 'up' if t % 4 < 2 else 'down'
    vStr = 'up' if t % 2 == 0 else 'down'

    print( 'test "{}", {}, {}, w scale {}, v scale {}'.format(test_name, symStr, scaleStr, wStr, vStr) )

    # range for the u scale
    umin = 1
    umax = 5

    # range for the v scale
    vmin = 1
    vmax = 5

    # automagically get the w scale range
    tmp = [ w(umin, vmin), w(umax, vmin), w(umin, vmax), w(umax, vmax) ]
    wmin = min(tmp)
    wmax = max(tmp)

    #print( 'wmin, wmax is ', wmin, wmax)

    ##############################################
    #
    # definitions for the axes for pyNomo
    # dictionary with key:value pairs

    left_axis = {
        'u_min': umin,
        'u_max': umax,
        'title': r'$u$',
        'scale_type': scale_type,
        'tick_levels': 3,
        'tick_text_levels': 2,
    }

    right_axis = {
        'u_min': vmin,
        'u_max': vmax,
        'title': r'$v$',
        'scale_type': scale_type,
        'tick_levels': 3,
        'tick_text_levels': 2,
    }

    middle_axis = {
        'u_min': wmin,
        'u_max': wmax,
        'title': r'$w$',
        'scale_type': scale_type,
        'tick_levels': 3,
        'tick_text_levels': 2,
    }

    # assemble the above 3 axes into a block
    block_params0 = {
        'block_type': 'type_9',
        'f1_params': left_axis,
        'f2_params': middle_axis,
        'f3_params': right_axis,

        # the isopleth connects the mid values of the outer axes
        # edit this for different values
        'isopleth_values': [[(left_axis['u_min'] + left_axis['u_max']) / 2, \
                             'x', \
                             (right_axis['u_min'] + right_axis['u_max']) / 2]]
    }

    # the nomogram parameters
    main_params = {
        'filename': test_name,
        'paper_height': 10,  # units are cm
        'paper_width': 10,
        'title_x': 7.0,
        'title_y': 2.0,
        'title_box_width': 8.0,
        'title_str': title_str,
        'block_params': [block_params0],
        'transformations': [('scale paper',)],
        'npoints': NN,

        # text to appear at the foot of the nomogram
        # make this null string for nothing
        # a default string will appear if this is omitted
        'footer_string': '{}: {}, {}, w {}, v {}'.format(test_name, symStr, scaleStr, wStr, vStr)
    }

    print("calculating the nomogram ...")
    Nomogen(w, main_params)  # generate nomogram for the target function

    main_params['filename'] += '.pdf'
    print("printing ", main_params['filename'], " ...")
    Nomographer(main_params)

    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', main_params['filename']))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(main_params['filename'])
    else:                                   # linux variants
        subprocess.call(('xdg-open', main_params['filename']))

# TODO: check that axes are as expected


