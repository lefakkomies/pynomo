# ex_axes_3.py

N_params = {'u_min': 1.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'u',
            'tick_levels': 3,
            'tick_text_levels': 2,
            'tick_side': 'left',
            'title_x_shift': -1.0,   # <-
            'title_y_shift': 0.5     # <-
            }

block_params = {'block_type': 'type_8',
                'f_params': N_params,
                'width': 5.0,
                'height': 10.0,
                }

main_params = {'filename': 'ex_axes_3.pdf',
               'paper_height': 10.0,
               'paper_width': 5.0,
               'block_params': [block_params],
               'transformations': [('scale paper',)]
               }

Nomographer(main_params)
