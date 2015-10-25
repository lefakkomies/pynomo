# ex_axes_1.py

import sys
sys.path.insert(0, "..")
from pynomo.nomographer import *

# axis definitions
N_params = {'u_min': 1.0,            # axis start value
            'u_max': 10.0,           # axis stop value
            'function': lambda u: u, # axis function
            'title': 'u',            # axis titles
            }

# block definitons defining one block of type 8
block_params = {'block_type': 'type_8',
                'f_params': N_params,
                'width': 5.0,
                'height': 15.0,
                }

# nomograph generation definitions
main_params = {'filename': 'ex_axes_1.pdf',
                'paper_height': 15.0,
                'paper_width': 5.0,
                'block_params': [block_params],
                'transformations': [('scale paper',)]
              }

# actual code that builds the nomograph
Nomographer(main_params)
