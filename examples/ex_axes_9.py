# ex_axes_9.py

N_params = {'u_min': 1.0,
            'u_max': 10000.0,
            'function': lambda u: log(u),
            'title': 'u',
            'scale_type': 'log',
            }
block_params = {'block_type': 'type_8',
                'f_params': N_params,
                'width': 5.0,
                'height': 15.0,
                }
main_params = {'filename': 'ex_axes_9.pdf',
               'paper_height': 15.0,
               'paper_width': 5.0,
               'block_params': [block_params],
               'transformations': [('scale paper',)]
              }
Nomographer(main_params)
