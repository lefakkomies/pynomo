# ex_axes_2.py

N_params = {'u_min': 1.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'u',
            'tick_levels': 3,        # <-
            'tick_text_levels': 2,   # <-
            'tick_side': 'left',     # <-
            }

block_params = {'block_type': 'type_8',
                'f_params': N_params,
                'width': 5.0,
                'height': 10.0,
                }

main_params = {'filename': 'ex_axes_2.pdf',
                'paper_height': 10.0,
                'paper_width': 5.0,
                'block_params': [block_params],
                'transformations': [('scale paper',)]
               }

Nomographer(main_params)
