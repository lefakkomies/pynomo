# ex_axes_4.py

N_params = {'u_min': 1.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'title',
            'tick_levels': 2,
            'tick_text_levels': 1,
            'tick_side': 'left',
            'title_draw_center': True,                 # <-
            'extra_params': [{'u_min': 5.0,            # <- range 1
                              'u_max': 10.0,           # <-
                              'tick_levels': 3,        # <-
                              'tick_text_levels': 2,   # <-
                              },                       # <-
                             {'u_min': 9.0,            # <- range 2
                              'u_max': 10.0,           # <-
                              'tick_levels': 4,        # <-
                              'tick_text_levels': 2,   # <-
                              }                        # <-
                             ]                         # <-
            }
block_params = {'block_type': 'type_8',
                'f_params': N_params,
                'width': 5.0,
                'height': 10.0,
                }
main_params = {'filename': 'ex_axes_4.pdf',
               'paper_height': 10.0,
               'paper_width': 5.0,
               'block_params': [block_params],
               'transformations': [('scale paper',)]
               }
Nomographer(main_params)
