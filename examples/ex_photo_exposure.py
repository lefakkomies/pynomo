"""
    ex_photo_exposure.py

    Photgraph exposure.

    Copyright (C) 2007-2008  Leif Roschier

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
import sys
sys.path.insert(0, "..")
from pynomo.nomographer import *
"""
functions for solartime taken from solareqns.pdf from
http://www.srrb.noaa.gov/highlights/sunrise/solareqns.PDF
"""


# fractional year
def gamma(day):
    return 2 * pi / 365.0 * (day - 1 + 0.5)
# equation of time


def eq_time(day):
    gamma0 = gamma(day)
    return 229.18 * (0.000075 + 0.001868 * cos(gamma0) - 0.032077 * sin(gamma0)\
                   - 0.014615 * cos(2 * gamma0) - 0.040849 * sin(2 * gamma0))

# mean correction, with constant correction we make less than 17 minutes  error
# in time axis
temp_a = arange(0, 365.0, 0.1)
temp_b = eq_time(temp_a)
correction = mean(temp_b) # this is 0.0171885 minutes


# declination
def eq_declination(day):
    g0 = gamma(day)
    return 0.006918 - 0.399912 * cos(g0) + 0.070257 * sin(g0) - 0.006758 * cos(2 * g0)\
            + 0.000907 * sin(2 * g0) - 0.002697 * cos(3 * g0) + 0.00148 * sin(3 * g0)


def f1(dummy):
    return 0.0


def g1(fii):
    return cos(fii*pi/180.0)


def f2(lat, day):
    dec = eq_declination(day)
    return (cos(lat * pi / 180.0) * cos(dec)) / (1.0 + (cos(lat * pi / 180.0) * cos(dec)))


def g2(lat, day):
    dec = eq_declination(day)  # in radians
    return (sin(lat * pi / 180.0) * sin(dec)) / (1.0 + (cos(lat * pi / 180.0) * cos(dec)))


def f3(dummy):
    return 1


def g3(h):
    hr = (h * 60.0 + correction) / 4.0 - 180.0
    return -1.0 * cos(hr * pi / 180.0)

days_in_month = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
times1=[]
for idx in range(0, 12):
    times1.append(sum(days_in_month[0:idx])+1)

time_titles = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

phi_params = {'u_min': 0.0,
              'u_max': 90.0,
              'u_min_trafo': 0.0,
              'u_max_trafo': 90.0,
              'f': f1,
              'g': g1,
              'h': lambda u: 1.0,
              'title': r'Solar zenith angle $\phi$',
              'title_x_shift': 0.0,
              'title_y_shift': 0.25,
              'scale_type': 'linear smart',
              'tick_levels': 4,
              'tick_text_levels': 2,
              'tick_side': 'right',
              'tag': 'phi',
              'grid': False,
              }
time_params = {'u_min': 0.0,
               'u_max': 23.0,
               'u_min_trafo': 0.0,
               'u_max_trafo': 12.0,
               'f': f3,
               'g': g3,
               'h':lambda u: 1.0,
               'title': r'Hour (h)',
               'title_x_shift': 0.0,
               'title_y_shift': 0.25,
               'scale_type': 'linear',
               'tick_levels': 2,
               'tick_text_levels': 1,
               'tick_side': 'right',
               'tag': 'none',
               'grid': False,
               }
lat_day_params = {'ID': 'none',  # to identify the axis
                  'tag': 'none',  # for aligning block wrt others
                  'title': 'Grid',
                  'title_x_shift': 0.0,
                  'title_y_shift': 0.25,
                  'title_distance_center': 0.5,
                  'title_opposite_tick': True,
                  'u_min': 20.0,  # for alignment
                  'u_max': 80.0,  # for alignment
                  'f_grid': f2,
                  'g_grid': g2,
                  'h_grid': lambda u, v: 1.0,
                  'u_start': 30.0,
                  'u_stop': 80.0,
                  'v_start': times1[0],  # day
                  'v_stop': times1[-1],
                  'u_values': [30.0, 40.0, 50.0, 60.0, 70.0, 80.0],
                  'u_texts': ['30', '40', '50', 'Latitude = 60', '70', '80'],
                  'v_values': times1,
                  'v_texts': time_titles,
                  'grid': True,
                  'text_prefix_u': r'',
                  'text_prefix_v': r'',
                  'text_distance': 0.5,
                  'v_texts_u_start': False,
                  'v_texts_u_stop': True,
                  'u_texts_v_start': False,
                  'u_texts_v_stop': True,
                  }
block_params = {'block_type': 'type_9',
                'f1_params': phi_params,
                'f2_params': lat_day_params,
                'f3_params': time_params,
                'transform_ini': True,
                'isopleth_values': [['x', [60, times1[4]], 14.0]]
                }


# limiting functions are to avoid NaN in contour construction that uses optimization
def limit_xx(x):
    x1 = x
    return x1


def limit_x(x):
    x1 = x
    return x1

const_A = 0.33766
const_B = -13.656

block_params_weather = {'block_type': 'type_5',
                        'u_func': lambda u: u,
                        'v_func':lambda x, v: const_A + const_B * log10(limit_x(x)) + v,
                        'u_values': [1.0, 25.0],
                        'u_manual_axis_data': {1.0: '',
                                               25.0: ''},
                        'v_values': [0.0, 1.0, 3.0, 6.0, 9.0, 12.0],
                        'v_manual_axis_data': {0.0: ['Clear sky, Cumulus clouds',
                                                     {'x_corr': 0.5,
                                                      'y_corr': 0.0,
                                                      'draw_line': False}],
                                               1.0: 'Clear sky',
                                               3.0: 'Sun through clouds',
                                               6.0: 'Sky light gray',
                                               9.0: 'Sky dark gray',
                                               12.0: 'Thunder-clouds cover sky'},
                        'v_text_distance': 0.5,
                        'wd_tick_levels': 0,
                        'wd_tick_text_levels': 0,
                        'wd_tick_side': 'right',
                        'wd_title': '',
                        'manual_x_scale': True,
                        'x_min': 0.06,
                        'x_max': 0.99,
                        'u_title': '',
                        'v_title': '',
                        'wd_title_opposite_tick': True,
                        'wd_title_distance_center': 2.5,
                        'wd_align_func': lambda L: acos(limit_xx(10.0**((L - const_A) / const_B))) * 180.0 / pi,  # phi as L
                        'wd_func': lambda L: 10.0**((L - const_A) / const_B),  # x as L
                        'wd_func_inv': lambda x: const_A+const_B * log10(x),  # L as x
                        'wd_tag': 'phi',
                        'mirror_y': True,
                        'mirror_x': False,
                        'width': 10.0,
                        'height': 10.0,
                        'u_scale_opposite': True,
                        'u_tag': 'AA',
                        'horizontal_guides': True,
                        'isopleth_values': [['x', 9.0, 'x']],
                        }
block_params_scene = {'block_type': 'type_5',
                      'u_func': lambda u: u,
                      'v_func': lambda x, v: x + v,
                      'u_values': [1.0, 25.0],
                      'u_manual_axis_data': {1.0: '',
                                             25.0: ''},
                      'u_tag': 'AA',
                      'wd_tag': 'EV',
                      'v_values': [-4.0, -1.0, 2.0, 5.0, 7.0, 9.0, 11.0, 13.0, 15.0],
                      'v_manual_axis_data': {-6.0: 'Person under trees',
                                             -4.0: 'Inside forest',
                                             -1.0: 'Person in shadow of wall',
                                             2.0: 'Person at open place; alley under trees',
                                             5.0: 'Buildings; street',
                                             7.0: 'Landscape and front matter',
                                             9.0: 'Open landscape',
                                             11.0: 'Snow landscape and front matter; beach',
                                             13.0: 'Snow field; open sea',
                                             15.0: 'Clouds',
                                             },
                      'wd_tick_levels': 0,
                      'wd_tick_text_levels': 0,
                      'wd_tick_side': 'right',
                      'wd_title': '',
                      'u_title': '',
                      'v_title': '',
                      'wd_title_opposite_tick': True,
                      'wd_title_distance_center': 2.5,
                      'mirror_x': True,
                      'horizontal_guides': True,
                      'u_align_y_offset': -0.9,
                      'isopleth_values': [['x', 2.0, 'x']],
                      }
camera_params_1 = {'u_min': -10.0,
                   'u_max': 15.0,
                   'function': lambda u: u,
                   'title': r'',
                   'tick_levels': 0,
                   'tick_text_levels': 0,
                   'tag': 'EV',
                   }
camera_params_2 = {'u_min': 10.0,
                   'u_max': 25600.0,
                   'function': lambda S: -(10 * log10(S) + 1.0),
                   'title': r'Film speed',
                   'manual_axis_data': {10.0: 'ISO 10',
                                        20.0: 'ISO 20',
                                        50.0: 'ISO 50',
                                        100.0: 'ISO 100',
                                        200.0: 'ISO 200',
                                        400.0: 'ISO 400',
                                        800.0: 'ISO 800',
                                        1600.0: 'ISO 1600',
                                        3200.0: 'ISO 3200',
                                        6400.0: 'ISO 6400',
                                        12800.0: 'ISO 12800',
                                        25600.0: 'ISO 25600',
                                        },
                   'scale_type': 'manual line'
                   }
camera_params_3 = {'u_min': 0.1,
                   'u_max': 10000.0,
                   'function': lambda t: -10 * log10((1.0 / t) / (1.0 / 10.0)) - 30,
                   'manual_axis_data': {1/10.0: '10',
                                        1/7.0: '7',
                                        1/5.0: '5',
                                        1/3.0: '3',
                                        1/2.0: '2',
                                        1.0: '1',
                                        2.0: '1/2',
                                        3.0: '1/3',
                                        5.0: '1/5',
                                        7.0: '1/7',
                                        10.0: '1/10',
                                        20.0: '1/20',
                                        30.0: '1/30',
                                        50.0: '1/50',
                                        70.0: '1/70',
                                        100.0: '1/100',
                                        200.0: '1/200',
                                        300.0: '1/300',
                                        500.0: '1/500',
                                        700.0: '1/700',
                                        1000.0: '1/1000',
                                        2000.0: '1/2000',
                                        3000.0: '1/3000',
                                        5000.0: '1/5000',
                                        7000.0: '1/7000',
                                        10000.0: '1/10000',
                             },
                   'scale_type': 'manual line',
                   'title': r't (s)',
                   'text_format': r"1/%3.0f s",
                   'tag': 'shutter',
                   'tick_side': 'left',
                   }
camera_params_4 = {'u_min': 1.0,
                   'u_max': 22.0,
                   'function': lambda N: 10 * log10((N / 3.2)**2) + 30,
                   'manual_axis_data': {1.0: '$f$/1',
                                        1.2: '$f$/1.2',
                                        1.4: '$f$/1.4',
                                        1.7: '$f$/1.7',
                                        2.0: '$f$/2',
                                        2.4: '$f$/2.4',
                                        2.8: '$f$/2.8',
                                        3.3: '$f$/3.3',
                                        4.0: '$f$/4',
                                        4.8: '$f$/4.8',
                                        5.6: '$f$/5.6',
                                        6.7: '$f$/6.7',
                                        8.0: '$f$/8',
                                        9.5: '$f$/9.5',
                                        11.0 :'$f$/11',
                                        13.0 :'$f$/13',
                                        16.0 :'$f$/16',
                                        19.0 :'$f$/19',
                                        22.0 :'$f$/22',
                                        },
                   'scale_type': 'manual line',
                   'title': r'Aperture',
                   }
block_params_camera = {'block_type': 'type_3',
                       'width': 10.0,
                       'height': 10.0,
                       'f_params': [camera_params_1, camera_params_2, camera_params_3,
                                    camera_params_4],
                       'mirror_x': True,
                       'isopleth_values': [['x', 100.0, 'x', 4.0]],
                       }


def old_EV(EV):  # C2(EV100) in wiki
    return (-EV + 13.654) / 0.3322

EV_para = {'tag': 'EV',
           'u_min': 4.0,
           'u_max': 19.0,
           'function': lambda u: old_EV(u),
           'title': r'EV$_{100}$',
           'tick_levels': 1,
           'tick_text_levels': 1,
           'align_func': old_EV,
           'title_x_shift': 0.5,
           'tick_side': 'right',
           }
EV_block = {'block_type': 'type_8',
            'f_params': EV_para,
            'isopleth_values': [['x']],
            }
# maximum focal length
FL_t_para={'u_min': 0.1,
           'u_max': 10000.0,
           'function': lambda t:-10 * log10((1.0 / t) / (1.0 / 10.0)) - 30,
           'scale_type': 'linear',
           'tick_levels': 0,
           'tick_text_levels': 0,
           'title': r't (s)',
           'text_format': r"1/%3.0f s",
           'tag': 'shutter',
           }
FL_factor_params_2 = {'u_min': 1.0/4.0,
                      'u_max': 3.0/2.0,
                      'function': lambda factor: -10 * log10(factor / 10.0) + 0,
                      'title': r'Sensor, IS',
                      'scale_type': 'manual point',
                      'manual_axis_data': {1.0/(2.0/3.0): 'DSLR',
                                           1.0/(1.0): '35mm',
                                           1.0/(8.0/3.0): 'DSLR IS',
                                           1.0/(4.0): '35mm IS',
                      },
                      'tick_side':'left',
                      'text_size_manual': text.size.footnotesize,  # pyx directive
                      }
FL_fl_params = {'u_min': 20.0,
                'u_max': 1000.0,
                'function': lambda FL:-10 * log10(FL) + 30,
                'title': r'Max focal length',
                'tick_levels': 3,
                'tick_text_levels': 2,
                'tick_side': 'left',
                'scale_type': 'manual line',
                'manual_axis_data': {20.0: '20mm',
                                     35.0: '35mm',
                                     50.0: '50mm',
                                     80.0: '80mm',
                                     100.0: '100mm',
                                     150.0: '150mm',
                                     200.0: '200mm',
                                     300.0: '300mm',
                                     400.0: '400mm',
                                     500.0: '500mm',
                                     1000.0: '1000mm'}
                }

FL_block_params = {'block_type': 'type_1',
                   'width': 12.0,
                   'height': 10.0,
                   'f1_params': FL_t_para,
                   'f2_params': FL_factor_params_2,
                   'f3_params': FL_fl_params,
                   'mirror_x': True,
                   'proportion': 0.5,
                   'isopleth_values': [['x', 1.0/(8.0/3.0), 'x']],
                   }

main_params = {'filename': ['ex_photo_exposure.pdf', 'ex_photo_exposure.eps'],
               'paper_height': 35.0,
               'paper_width': 35.0,
               'block_params': [block_params, block_params_weather, block_params_scene,
                                block_params_camera, EV_block, FL_block_params],
               'transformations': [('rotate', 0.01), ('scale paper',)],
               'title_x': 7,
               'title_y': 34,
               'title_box_width': 10,
               'title_str': r'\LARGE Photography exposure (Setala 1940) \par \copyright Leif Roschier  2009 '
              }
Nomographer(main_params)
