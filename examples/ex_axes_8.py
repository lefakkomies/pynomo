# ex_axes_8.py

import sys

sys.path.insert(0, "..")
from pynomo.nomographer import Nomographer
import numpy as np

N_params = {'u_min': 0.0,
            'u_max': 300.0,
            'function_x': lambda u: 3 * np.sin(u / 180.0 * np.pi),
            'function_y': lambda u: 3 * np.cos(u / 180.0 * np.pi),
            'title': 'u',
            'tick_levels': 3,
            'tick_text_levels': 1,
            'title_x_shift': -0.5,
            }
block_params = {'block_type': 'type_8',
                'f_params': N_params,
                'width': 5.0,
                'height': 15.0,
                }
main_params = {'filename': 'ex_axes_8.pdf',
               'paper_height': 10.0,
               'paper_width': 10.0,
               'block_params': [block_params],
               'transformations': [('scale paper',)]
               }
Nomographer(main_params)
