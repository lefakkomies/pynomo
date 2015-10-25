# ex_axes_4_1.py

N_params = {'u_min': 1.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'title',
            'tick_levels': 2,
            'tick_text_levels': 1,
            'tick_side': 'left',
            'title_draw_center': True,
            'text_format': r"$%3.1f$ ",                              # <- format numbers as %3.1f
            'axis_color': color.cmyk.Orange,
            'text_color': color.cmyk.Plum,
            'title_color': color.cmyk.Plum,
            'extra_params': [{'u_min': 5.0,
                              'u_max': 10.0,
                              'tick_levels': 3,
                              'tick_text_levels': 2,
                              'axis_color': color.cmyk.Red,
                              },
                             {'u_min': 9.0,
                              'u_max': 10.0,
                              'tick_levels': 4,
                              'tick_text_levels': 2,
                              'axis_color': color.cmyk.Blue,
                              }
                            ],
            'extra_titles': [{'dx': 1.0,                                          # <- 1st extra title
                              'dy': 1.0,                                          # <-
                              'text': 'extra title 1',                            # <-
                              'width': 5,                                         # <-
                              'pyx_extra_defs': [color.rgb.red, text.size.tiny]   # <-
                              },
                            {'dx': 0.0,                                           # <- 2nd extra title
                             'dy': 2.0,                                           # <-
                             'text': 'extra title 2',                             # <-
                             'width': 5,                                          # <-
                             'pyx_extra_defs': [color.rgb.green]                  # <-
                             },
                            {'dx': -1.0,                                          # <- 3rd extra title
                             'dy': 1.0,                                           # <-
                             'text': r"extra  \par title 3",                      # <- \par = newline
                             'width': 5,                                          # <-
                             'pyx_extra_defs': [color.rgb.blue]                   # <-
                             }]
            }
block_params = {'block_type': 'type_8',
                'f_params': N_params,
                'width': 5.0,
                'height': 10.0,
                }
main_params = {'filename': 'ex_axes_4_1.pdf',
               'paper_height': 10.0,
               'paper_width': 5.0,
               'block_params': [block_params],
               'transformations': [('scale paper',)]
               }
Nomographer(main_params)
