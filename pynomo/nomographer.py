# -*- coding: utf-8 -*-
#    This file is part of PyNomo -
#    a program to create nomographs with Python (https://github.com/lefakkomies/pynomo)
#
#    Copyright (C) 2007-2019  Leif Roschier  <lefakkomies@users.sourceforge.net>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .isopleth import Isopleth_Wrapper
from .nomo_wrapper import Nomo_Wrapper
from .nomo_wrapper import Nomo_Block_Type_1
from .nomo_wrapper import Nomo_Block_Type_2
from .nomo_wrapper import Nomo_Block_Type_3
from .nomo_wrapper import Nomo_Block_Type_4
from .nomo_wrapper import Nomo_Block_Type_5
from .nomo_wrapper import Nomo_Block_Type_6
from .nomo_wrapper import Nomo_Block_Type_7
from .nomo_wrapper import Nomo_Block_Type_8
from .nomo_wrapper import Nomo_Block_Type_9
from .nomo_wrapper import Nomo_Block_Type_10
from .nomo_axis import Nomo_Axis
from .nomo_axis import find_linear_ticks
from pprint import pprint

import pyx
import numpy as np


class Nomographer:
    """
    Top-level class to build nomographs
    """

    def __init__(self, params):
        """
        params hold all information to build the nomograph
        """
        self._check_params_(params)  # sets default values for misnp.sing keys
        wrapper = Nomo_Wrapper(params=params,
                               paper_width=params['paper_width'],
                               paper_height=params['paper_height'],
                               filename=params['filename'])
        blocks = []
        isopleths = Isopleth_Wrapper(params)
        for block_para in params['block_params']:
            # TYPE 1
            if block_para['block_type'] == 'type_1':
                self._check_block_type_1_params_(block_para)
                blocks.append(Nomo_Block_Type_1(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f1_params'])
                self._check_axis_params_(block_para['f2_params'])
                self._check_axis_params_(block_para['f3_params'])
                blocks[-1].define_F1(block_para['f1_params'])
                blocks[-1].define_F2(block_para['f2_params'])
                blocks[-1].define_F3(block_para['f3_params'])
                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'],
                                     proportion=block_para['proportion'])
                wrapper.add_block(blocks[-1])
                isopleths.add_isopleth_block(blocks[-1], block_para)
            # TYPE 2
            if block_para['block_type'] == 'type_2':
                self._check_block_type_2_params_(block_para)
                blocks.append(Nomo_Block_Type_2(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f1_params'])
                self._check_axis_params_(block_para['f2_params'])
                self._check_axis_params_(block_para['f3_params'])
                blocks[-1].define_F1(block_para['f1_params'])
                blocks[-1].define_F2(block_para['f2_params'])
                blocks[-1].define_F3(block_para['f3_params'])
                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'])
                wrapper.add_block(blocks[-1])
                isopleths.add_isopleth_block(blocks[-1], block_para)
            # TYPE 3
            if block_para['block_type'] == 'type_3':
                self._check_block_type_3_params_(block_para)
                blocks.append(Nomo_Block_Type_3(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                for axis_params in block_para['f_params']:
                    self._check_axis_params_(axis_params)
                    blocks[-1].add_F(axis_params)
                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'],
                                     reference_padding=block_para['reference_padding'],
                                     reference_titles=block_para['reference_titles'],
                                     reference_color=block_para['reference_color'])
                wrapper.add_block(blocks[-1])
                isopleths.add_isopleth_block(blocks[-1], block_para)
            # TYPE 4
            if block_para['block_type'] == 'type_4':
                self._check_block_type_4_params_(block_para)
                blocks.append(Nomo_Block_Type_4(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f1_params'])
                self._check_axis_params_(block_para['f2_params'])
                self._check_axis_params_(block_para['f3_params'])
                self._check_axis_params_(block_para['f4_params'])
                blocks[-1].define_F1(block_para['f1_params'])
                blocks[-1].define_F2(block_para['f2_params'])
                blocks[-1].define_F3(block_para['f3_params'])
                blocks[-1].define_F4(block_para['f4_params'])
                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'],
                                     float_axis=block_para['float_axis'],
                                     padding=block_para['padding'],
                                     reference_color=block_para['reference_color'])
                wrapper.add_block(blocks[-1])
                isopleths.add_isopleth_block(blocks[-1], block_para)
            # TYPE 5
            if block_para['block_type'] == 'type_5':
                self._check_block_type_5_params_(block_para)
                blocks.append(Nomo_Block_Type_5(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                blocks[-1].define_block(block_para)
                blocks[-1].set_block()
                wrapper.add_block(blocks[-1])
                isopleths.add_isopleth_block(blocks[-1], block_para)
            # TYPE 6
            if block_para['block_type'] == 'type_6':
                self._check_block_type_6_params_(block_para)
                blocks.append(Nomo_Block_Type_6(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                blocks[-1].define(params1=block_para['f1_params'],
                                  params2=block_para['f2_params'])
                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'],
                                     type=block_para['type'],
                                     x_empty=block_para['x_empty'],
                                     y_empty=block_para['y_empty'],
                                     curve_const=block_para['curve_const'],
                                     ladder_color=block_para['ladder_color'])
                wrapper.add_block(blocks[-1])
                isopleths.add_isopleth_block(blocks[-1], block_para)
            # TYPE 7
            if block_para['block_type'] == 'type_7':
                self._check_block_type_7_params_(block_para)
                blocks.append(Nomo_Block_Type_7(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f1_params'])
                self._check_axis_params_(block_para['f2_params'])
                self._check_axis_params_(block_para['f3_params'])
                blocks[-1].define_F1(block_para['f1_params'])
                blocks[-1].define_F2(block_para['f2_params'])
                blocks[-1].define_F3(block_para['f3_params'])
                blocks[-1].set_block(width_1=block_para['width_1'],
                                     angle_u=block_para['angle_u'],
                                     angle_v=block_para['angle_v'])
                wrapper.add_block(blocks[-1])
                isopleths.add_isopleth_block(blocks[-1], block_para)
            # TYPE 8
            if block_para['block_type'] == 'type_8':
                self._check_block_type_8_params_(block_para)
                blocks.append(Nomo_Block_Type_8(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f_params'])
                blocks[-1].define_F(block_para['f_params'])
                blocks[-1].set_block(length=block_para['length'])
                wrapper.add_block(blocks[-1])
                isopleths.add_isopleth_block(blocks[-1], block_para)
            # TYPE 9
            if block_para['block_type'] == 'type_9':
                self._check_block_type_9_params_(block_para)
                blocks.append(Nomo_Block_Type_9(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f1_params'])
                self._check_axis_params_(block_para['f2_params'])
                self._check_axis_params_(block_para['f3_params'])
                blocks[-1].define_determinant(block_para['f1_params'],
                                              block_para['f2_params'],
                                              block_para['f3_params'],
                                              transform_ini=block_para['transform_ini'])

                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'],
                                     ignore_transforms=block_para['ignore_transforms'])
                wrapper.add_block(blocks[-1])
                isopleths.add_isopleth_block(blocks[-1], block_para)
            # TYPE 10
            if block_para['block_type'] == 'type_10':
                self._check_block_type_10_params_(block_para)
                blocks.append(Nomo_Block_Type_10(mirror_x=block_para['mirror_x'],
                                                 mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f1_params'])
                self._check_axis_params_(block_para['f2_params'])
                self._check_axis_params_(block_para['f3_params'])
                blocks[-1].define_F1(block_para['f1_params'])
                blocks[-1].define_F2(block_para['f2_params'])
                blocks[-1].define_F3(block_para['f3_params'])
                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'])
                wrapper.add_block(blocks[-1])
                isopleths.add_isopleth_block(blocks[-1], block_para)
            # always save a handle
            blocks[-1].ref_block_params = block_para
        wrapper.align_blocks()
        wrapper.build_axes_wrapper()  # build structure for transformations
        # do transformations
        for trafo in params['transformations']:
            if len(trafo) > 1:
                wrapper.do_transformation(method=trafo[0], params=trafo[1])
            else:
                wrapper.do_transformation(method=trafo[0])
        # transformations done
        c = pyx.canvas.canvas()
        if params['make_grid']:
            self._make_grid_(params, c)
        if params['pre_func'] is not None:
            params['pre_func'](c)
        if params['draw_lines']:
            self._draw_lines_(params, c)
        if params['draw_isopleths']:
            # draw isopleths
            isopleths.draw(c)
        else:  # calculate points
            for block in blocks:
                for atom in block.atom_stack:
                    # calculates lines (list of coordinates)
                    atom.calc_line_and_sections()
                    # pass
        # draw the nomogram
        wrapper.draw_nomogram(c, params['post_func'])
        self.blocks = blocks  # save for debugging
        for block in params['block_params']:
            if block['debug']:
                print("##### np.sinGLE BLOCK PARAMS #######")
                pprint(block)
        if params['debug']:
            print("##### MAIN PARAMS #######")
            pprint(params)
        self.wrapper = wrapper
        self.canvas = c

    def _make_grid_(self, params, c):
        """
        makes a grid to help position titles, etc.
        """
        axis_offset = 3.0  # how much scales are aside
        axis_color = pyx.color.cmyk.Brown
        Nomo_Axis(func_f=lambda u: u,
                  func_g=lambda u: 0.0 - axis_offset + u * 1e-5,
                  start=-axis_offset, stop=params['paper_width'] + axis_offset, turn=-1, title='',
                  tick_levels=3, tick_text_levels=2,
                  canvas=c, type='linear', side='right', axis_appear={'turn_relative': True,
                                                                      'axis_color': axis_color,
                                                                      'text_color': axis_color})
        Nomo_Axis(func_f=lambda u: u,
                  func_g=lambda u: params['paper_height'] +
                  axis_offset + u * 1e-5,
                  start=-axis_offset, stop=params['paper_width'] + axis_offset, turn=-1, title='',
                  tick_levels=3, tick_text_levels=2,
                  canvas=c, type='linear', side='left', axis_appear={'turn_relative': True,
                                                                     'axis_color': axis_color,
                                                                     'text_color': axis_color})
        Nomo_Axis(func_f=lambda u: 0.0 - axis_offset + u * 1e-5,
                  func_g=lambda u: u,
                  start=-axis_offset, stop=params['paper_height'] + axis_offset, turn=-1, title='',
                  tick_levels=3, tick_text_levels=2,
                  canvas=c, type='linear', side='left', axis_appear={'turn_relative': True,
                                                                     'axis_color': axis_color,
                                                                     'text_color': axis_color})
        Nomo_Axis(func_f=lambda u: params['paper_width'] + axis_offset + u * 1e-5,
                  func_g=lambda u: u,
                  start=-axis_offset, stop=params['paper_height'] + axis_offset, turn=-1, title='',
                  tick_levels=3, tick_text_levels=2,
                  canvas=c, type='linear', side='right', axis_appear={'turn_relative': True,
                                                                      'axis_color': axis_color,
                                                                      'text_color': axis_color})
        tick_0_list_v, tick_1_list_v, tick_2_list_v, tick_3_list_v, tick_4_list_v, \
            start_ax, stop_ax = find_linear_ticks(
                -axis_offset, params['paper_height'] + axis_offset)
        tick_0_list_h, tick_1_list_h, tick_2_list_h, tick_3_list_h, tick_4_list_h, \
            start_ax, stop_ax = find_linear_ticks(
                -axis_offset, params['paper_width'] + axis_offset)
        grid_color_0 = pyx.color.cmyk.Brown
        grid_color_1 = pyx.color.cmyk.Gray
        grid_color_2 = pyx.color.cmyk.Tan
        for tick in tick_0_list_v:
            c.stroke(pyx.path.line(-axis_offset, tick, params['paper_width'] + axis_offset, tick),
                     [grid_color_0, pyx.style.linewidth.THin])
        for tick in tick_1_list_v:
            c.stroke(pyx.path.line(-axis_offset, tick, params['paper_width'] + axis_offset, tick),
                     [grid_color_1, pyx.style.linewidth.THIN])
        for tick in tick_2_list_v:
            c.stroke(pyx.path.line(-axis_offset, tick, params['paper_width'] + axis_offset, tick),
                     [grid_color_2, pyx.style.linewidth.THIN])
        for tick in tick_0_list_h:
            c.stroke(pyx.path.line(tick, -axis_offset, tick, params['paper_height'] + axis_offset),
                     [grid_color_0, pyx.style.linewidth.THin])
        for tick in tick_1_list_h:
            c.stroke(pyx.path.line(tick, -axis_offset, tick, params['paper_height'] + axis_offset),
                     [grid_color_1, pyx.style.linewidth.THIN])
        for tick in tick_2_list_h:
            c.stroke(pyx.path.line(tick, -axis_offset, tick, params['paper_height'] + axis_offset),
                     [grid_color_2, pyx.style.linewidth.THIN])

    def _draw_lines_(self, params, c):
        """
        draws (isopleth) lines according to given coordinates
        """
        for line_defs in params['line_params']:
            # line style
            if 'line_style' in line_defs:
                line_style = line_defs['line_style']
            else:
                line_style = self.line_defs_default['line_style']
            # circle size
            if 'circle_size' in line_defs:
                circle_size = line_defs['circle_size']
            else:
                circle_size = self.line_defs_default['circle_size']
            # circle color
            if 'circle_color' in line_defs:
                circle_color = line_defs['circle_color']
            else:
                circle_color = self.line_defs_default['circle_color']
            # do lines and circles
            for line in line_defs['coords']:
                c.stroke(pyx.path.line(
                    line[0], line[1], line[2], line[3]), line_style)
                c.fill(pyx.path.circle(
                    line[0], line[1], circle_size), [circle_color])
                c.fill(pyx.path.circle(
                    line[2], line[3], circle_size), [circle_color])

    def _check_params_(self, params):
        """
        checks if main params ok and adds default values
        """
        self.line_defs_default = {'coords': [[0, 0, 1, 1], [2, 2, 3, 3]],
                                  'line_style': [pyx.color.cmyk.Black,
                                                 pyx.style.linewidth.thick,
                                                 pyx.style.linestyle.dashed],
                                  'circle_size': 0.0005,
                                  'circle_color': pyx.color.cmyk.Black,
                                  }
        params_default = {
            'filename': 'pynomo_default.pdf',
            'paper_height': 20.0,
            'paper_width': 20.0,
            # 'block_params':[test1_block1_params,test1_block2_params],
            'transformations': [('rotate', 0.01), ('scale paper',)],
            'title_color': pyx.color.rgb.black,
            'make_grid': False,
            'draw_lines': False,  # to draw manual lines
            'line_params': [self.line_defs_default],
            'pre_func': None,  # function(pyx.canvas) to draw first
            'post_func': None,  # function(pyx.canvas) to draw last
            'debug': False,
            'draw_isopleths': True,  # draws isopleths
            'isopleth_params': [{'color': 'Black',
                                 'linestyle': 'Dashed',
                                 'lineweight': 'thick',
                                 'circle_size': 0.05}],  # isopleth values
        }
        for key in params_default:
            if not key in params:
                params[key] = params_default[key]

    def _check_block_type_1_params_(self, params):
        """
        checks if block type 1 params ok and adds default values
        """
        params_default = {
            'mirror_x': False,
            'mirror_y': False,
            'width': 10.0,
            'height': 10.0,
            'proportion': 1.0,
            'debug': False,
            'isopleth_values': [],
        }
        for key in params_default:
            if not key in params:
                params[key] = params_default[key]

    def _check_block_type_2_params_(self, params):
        """
        checks if block type 2 params ok and adds default values
        """
        params_default = {
            'mirror_x': False,
            'mirror_y': False,
            'width': 10.0,
            'height': 10.0,
            'debug': False,
            'isopleth_values': [],
        }
        for key in params_default:
            if not key in params:
                params[key] = params_default[key]

    def _check_block_type_3_params_(self, params):
        """
        checks if block type 3 params ok and adds default values
        """
        params_default = {
            'mirror_x': False,
            'mirror_y': False,
            'width': 10.0,
            'height': 10.0,
            'reference_padding': 0.2,
            'reference_titles': [],
            'reference_color': pyx.color.rgb.black,
            'debug': False,
            'isopleth_values': [],
        }
        for key in params_default:
            if not key in params:
                params[key] = params_default[key]

    def _check_block_type_4_params_(self, params):
        """
        checks if block type 4 params ok and adds default values
        """
        params_default = {
            'mirror_x': False,
            'mirror_y': False,
            'width': 10.0,
            'height': 10.0,
            'float_axis': 'F1 or F2',
            'padding': 0.9,
            'reference_color': pyx.color.rgb.black,
            'debug': False,
            'isopleth_values': [],
        }
        for key in params_default:
            if not key in params:
                params[key] = params_default[key]

    def _check_block_type_5_params_(self, params):
        """
        checks if block type 5 params ok and adds default values
        """
        params_default = {
            'mirror_x': False,
            'mirror_y': False,
            'width': 10.0,
            'height': 10.0,
            # 'u_func':lambda u:u,
            # 'v_func':lambda x,v:x+v,
            # 'u_values':[10.0,15.0,20.0,25.0,30.0,40.0,50.0,60.0],
            # 'v_values':[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],
            'v_tick_side': 'left',
            'u_title': '',
            'v_title': '',
            'u_reference': False,  # manual labels
            'v_reference': False,
            'w_reference': False,
            'wd_reference': False,
            'wd_tick_levels': 0,
            'wd_tick_text_levels': 0,
            'wd_tag': 'none',
            'w_tick_levels': 0,
            'w_tick_text_levels': 0,
            'horizontal_guides': False,
            'debug': False,
            'isopleth_values': [],
        }
        for key in params_default:
            if not key in params:
                params[key] = params_default[key]

    def _check_block_type_6_params_(self, params):
        """
        checks if block type 6 params ok and adds default values
        """
        params_default = {
            'mirror_x': False,
            'mirror_y': False,
            'width': 10.0,
            'height': 10.0,
            'type': 'parallel',
            'x_empty': 0.2,
            'y_empty': 0.2,
            'curve_const': 0.0,
            'ladder_color': pyx.color.rgb.black,
            'debug': False,
            'isopleth_values': [],
        }
        for key in params_default:
            if not key in params:
                params[key] = params_default[key]

    def _check_block_type_7_params_(self, params):
        """
        checks if block type 7 params ok and adds default values
        """
        params_default = {
            'mirror_x': False,
            'mirror_y': False,
            'width_1': 10.0,
            'angle_u': 45.0,
            'angle_v': 45.0,
            'debug': False,
            'isopleth_values': [],
        }
        for key in params_default:
            if not key in params:
                params[key] = params_default[key]

    def _check_block_type_8_params_(self, params):
        """
        checks if block type 8 params ok and adds default values
        """
        params_default = {
            'mirror_x': False,
            'mirror_y': False,
            'length': 10.0,
            'debug': False,
            'isopleth_values': [],
        }
        for key in params_default:
            if not key in params:
                params[key] = params_default[key]

    def _check_block_type_9_params_(self, params):
        """
        checks if block type 9 params ok and adds default values
        """
        params_default = {
            'mirror_x': False,
            'mirror_y': False,
            'width': 10.0,
            'height': 10.0,
            'transform_ini': False,
            'grid': False,
            'v_texts_u_start': False,
            'v_texts_u_stop': True,
            'u_texts_v_start': False,
            'u_texts_v_stop': True,
            'debug': False,
            'isopleth_values': [],
            'ignore_transforms': False,
        }
        for key in params_default:
            if not key in params:
                params[key] = params_default[key]

    def _check_block_type_10_params_(self, params):
        """
        checks if block type 10 params ok and adds default values
        """
        params_default = {
            'mirror_x': False,
            'mirror_y': False,
            'width': 10.0,
            'height': 10.0,
            'debug': False,
            'isopleth_values': [],
        }
        for key in params_default:
            if not key in params:
                params[key] = params_default[key]

    def _check_axis_params_(self, params):
        """
        checks (TODO: if axis params ok) and adds default values
        """
        params_default = {
            'ID': 'none',  # to identify the axis
            'tag': 'none',  # for aligning block wrt others
            # 'u_min':0.1,
            # 'u_max':1.0,
            # 'F':lambda u:u, # x-coordinate
            # 'G':lambda u:u, # y-coordinate
            'title': '',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'scale_type': 'linear',  # 'linear' 'log' 'manual point' 'manual line'
            'tick_levels': 4,
            'tick_text_levels': 3,
            'tick_side': 'right',
            'reference': False,
            'reference_padding': 0.20,  # fraction of reference line over other lines
            'manual_axis_data': {},
            'title_distance_center': 0.5,
            'title_opposite_tick': True,
            'title_draw_center': False,
            'grid': False
        }
        for key in params_default:
            if not key in params:
                params[key] = params_default[key]


if __name__ == '__main__':
    """
    tests
    """
    test1 = False
    if test1:
        test1_f1_para = {
            'u_min': 1.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'F1',
            'tick_levels': 3,
            'tick_text_levels': 2,
        }
        test1_f2_para = {
            'u_min': 0.1,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'F2',
            'tick_levels': 3,
            'tick_text_levels': 2,
            'scale_type': 'log',
        }
        test1_f3_para = {
            'u_min': 1.0,
            'u_max': 10.0,
            # 'function':lambda u:u*12.0,
            'function': lambda u: u,
            'title': 'F3',
            'tag': 'A',
            'tick_side': 'right'
        }
        test1_f4_para = {
            'u_min': -10.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'F2',
            'tick_levels': 3,
            'tick_text_levels': 2,
        }
        test1_block1_params = {
            'block_type': 'type_1',
            'width': 10.0,
            'height': 10.0,
            'proportion': 0.5,
            'f1_params': test1_f1_para,
            'f2_params': test1_f2_para,
            'f3_params': test1_f3_para}

        test1_block7_params = {
            'block_type': 'type_7',
            'width_1': 10.0,
            'angle_u': 60.0,
            'angle_v': 60.0,
            'f1_params': test1_f1_para,
            'f2_params': test1_f2_para,
            'f3_params': test1_f3_para}

        test1_params = {
            'filename': 'test1.pdf',
            'paper_height': 20.0,
            'paper_width': 20.0,
            'block_params': [test1_block1_params, test1_block7_params],
            'transformations': [('rotate', 0.01), ('scale paper',)]
        }
        Nomographer(test1_params)

        test2_block2_params = {
            'block_type': 'type_2',
            'width': 10.0,
            'height': 10.0,
            'proportion': 0.5,
            'f1_params': test1_f1_para,
            'f2_params': test1_f2_para,
            'f3_params': test1_f3_para}

        test2_params = {
            'filename': 'test2.pdf',
            'paper_height': 20.0,
            'paper_width': 20.0,
            'block_params': [test2_block2_params],
            'transformations': [('rotate', 0.01), ('scale paper',)]
        }
        Nomographer(test2_params)

        test3_block3_params = {
            'block_type': 'type_3',
            'width': 10.0,
            'height': 10.0,
            'f_params': [test1_f1_para, test1_f1_para,
                         test1_f1_para, test1_f1_para, test1_f4_para]
        }

        test3_params = {
            'filename': 'test3.pdf',
            'paper_height': 20.0,
            'paper_width': 20.0,
            'block_params': [test3_block3_params],
            'transformations': [('rotate', 0.01), ('scale paper',)]
        }
        Nomographer(test3_params)

        test4_block4_params = {
            'block_type': 'type_4',
            'f1_params': test1_f1_para,
            'f2_params': test1_f2_para,
            'f3_params': test1_f3_para,
            'f4_params': test1_f1_para,
        }

        test4_params = {
            'filename': 'test4.pdf',
            'paper_height': 20.0,
            'paper_width': 20.0,
            'block_params': [test4_block4_params],
            'transformations': [('rotate', 0.01), ('scale paper',)]
        }

        Nomographer(test4_params)

        def f1(x, u):
            # return log(log(x/(x-u/100.0))/log(1+u/100.0))
            return np.log(np.log(x / (x - u / (100.0 * 12.0))) / np.log(1 + u / (100.0 * 12.0)))

        test5_block5_params = {
            'block_type': 'type_5',
            'u_func': lambda u: np.log(u * 12.0),
            'v_func': f1,
            'u_values': [10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0],
            'v_values': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        }

        test5_params = {
            'filename': 'test5.pdf',
            'paper_height': 20.0,
            'paper_width': 20.0,
            'block_params': [test5_block5_params],
            'transformations': [('rotate', 0.01), ('scale paper',)]
        }

        Nomographer(test5_params)

        test6_block6_params = {
            'block_type': 'type_6',
            'f1_params': test1_f1_para,
            'f2_params': test1_f2_para,
        }
        test6_params = {
            'filename': 'test6.pdf',
            'paper_height': 20.0,
            'paper_width': 20.0,
            'block_params': [test6_block6_params],
            'transformations': [('rotate', 0.01), ('scale paper',)]
        }
        Nomographer(test6_params)

    F_start = -40.0
    F_stop = 90.0
    C_start = -40.0
    C_stop = 30.0

    def celcius(fahrenheit):
        return (fahrenheit - 32.0) / 1.8

    test8_f1_para = {
        'tag': 'A',
        'u_min': F_start,
        'u_max': F_stop,
        'function': lambda u: celcius(u),
        'title': r'$^\circ$ F',
        'tick_levels': 4,
        'tick_text_levels': 3,
        'align_func': celcius,
        'title_x_shift': 0.5
    }
    test8_f1c_para = {
        'tag': 'A',
        'u_min': F_start,
        'u_max': F_stop,
        'function': lambda u: celcius(u),
        'title': r'$^\circ$ F',
        'tick_levels': 4,
        'tick_text_levels': 3,
        'align_func': celcius,
        'title_x_shift': 0.5,
        'align_x_offset': 7.0
    }
    test8_f2_para = {
        'tag': 'A',
        'u_min': C_start,
        'u_max': C_stop,
        'function': lambda u: u,
        'title': r'$^\circ$ C',
        'tick_levels': 5,
        'tick_text_levels': 3,
        'scale_type': 'linear',
        'tick_side': 'left',
        'title_x_shift': -0.5
    }

    test8_block8a_params = {
        'block_type': 'type_8',
        'f_params': test8_f1_para
    }
    test8_block8c_params = {
        'block_type': 'type_8',
        'f_params': test8_f1c_para
    }
    test8_block8b_params = {
        'block_type': 'type_8',
        'length': 5.0,
        'f_params': test8_f2_para
    }
    test8_params = {
        'filename': 'test8.pdf',
        'paper_height': 20.0,
        'paper_width': 2.0,
        'block_params': [test8_block8b_params, test8_block8a_params,
                         test8_block8c_params],
        'transformations': [('scale paper',)]
    }
    Nomographer(test8_params)

    # test 9
    test9_f1_para = {
        'u_min': 0.5,
        'u_max': 1.0,
        'u_min_trafo': 0.5,
        'u_max_trafo': 1.0,
        'f': lambda u: 2 * (u * u - 1.0),
        'g': lambda u: 3 * u * (u + 1.0),
        'h': lambda u: (-u * (u - 1.0)),
        'title': 'p',
        'tick_side': 'left',
        'tick_levels': 4,
        'tick_text_levels': 2
    }
    test9_f2_para = {
        'u_min': 1.0,
        'u_max': 0.75,
        'u_min_trafo': 1.0,
        'u_max_trafo': 0.75,
        'f': lambda v: v,
        'g': lambda v: 1.0,
        'h': lambda v: (-v * v),
        'title': 'h',
        'tick_side': 'right',
        'tick_levels': 3,
        'tick_text_levels': 2
    }
    test9_f3_para = {
        'u_min': 1.0,
        'u_max': 0.5,
        'u_min_trafo': 1.0,
        'u_max_trafo': 0.75,
        'f': lambda w: 2.0 * (2.0 * w + 1.0),
        'g': lambda w: 3.0 * (w + 1.0),
        'h': lambda w: (-(w + 1.0) * (2.0 * w + 1.0)),
        'title': 'L',
        'tick_side': 'left',
        'tick_levels': 4,
        'tick_text_levels': 2
    }
    test9_block_params = {
        'block_type': 'type_9',
        'f1_params': test9_f1_para,
        'f2_params': test9_f2_para,
        'f3_params': test9_f3_para,
        'transform_ini': True,
    }

    test9_params = {
        'filename': 'test9.pdf',
        'paper_height': 10.0,
        'paper_width': 10.0,
        'block_params': [test9_block_params],
        'transformations': [('scale paper',)]
    }
    Nomographer(test9_params)

    # test 9 b
    test9b_f1 = {
        'u_min': 3.0,
        'u_max': 10.0,
        'f': lambda u: 0,
        'g': lambda u: u,
        'h': lambda u: 1.0,
        'title': 'A',
        'title_x_shift': 0.0,
        'title_y_shift': 0.25,
        'scale_type': 'linear',
        'tick_levels': 3,
        'tick_text_levels': 2,
        'tick_side': 'right',
        'tag': 'none',
        'grid': False}

    test9b_f2 = {
        'u_min': 3.0,
        'u_max': 10.0,
        'f': lambda u: 4.0,
        'g': lambda u: u,
        'h': lambda u: 1.0,
        'title': 'B',
        'title_x_shift': 0.0,
        'title_y_shift': 0.25,
        'scale_type': 'linear',
        'tick_levels': 3,
        'tick_text_levels': 2,
        'tick_side': 'right',
        'tag': 'none',
        'grid': False}

    test9b_f3 = {
        'ID': 'none',  # to identify the axis
        'tag': 'none',  # for aligning block wrt others
        'title': 'Grid',
        'title_x_shift': 0.0,
        'title_y_shift': 0.25,
        'title_distance_center': 0.5,
        'title_opposite_tick': True,
        'u_min': 0.0,  # for alignment
        'u_max': 1.0,  # for alignment
        'f_grid': lambda u, v: u + 2.0,
        'g_grid': lambda u, v: 2 * v,
        'h_grid': lambda u, v: 1.0,
        'u_start': 0.0,
        'u_stop': 1.0,
        'v_start': 0.0,
        'v_stop': 1.0,
        'u_values': [0.0, 0.25, 0.5, 0.75, 1.0],
        'v_values': [0.0, 0.25, 0.5, 0.75, 1.0],
        'grid': True
    }
    test9b_block_params = {
        'block_type': 'type_9',
        'f1_params': test9b_f1,
        'f2_params': test9b_f2,
        'f3_params': test9b_f3,
        'transform_ini': False,
    }

    test9b_params = {
        'filename': 'test9b.pdf',
        'paper_height': 10.0,
        'paper_width': 10.0,
        'block_params': [test9b_block_params],
        'transformations': [('rotate', 0.01), ('scale paper',)]
    }
    Nomographer(test9b_params)

    # test 9 c
    test9c_f1 = {
        'u_min': 0.0,
        'u_max': 100.0,
        'f': lambda u: 0,
        'g': lambda u: u,
        'h': lambda u: 1.0,
        'title': 'm',
        'title_x_shift': 0.0,
        'title_y_shift': 0.25,
        'scale_type': 'linear',
        'tick_levels': 3,
        'tick_text_levels': 2,
        'tick_side': 'left',
        'tag': 'none',
        'grid': False}

    test9c_f2 = {
        'u_min': 0.0,
        'u_max': 100.0,
        'f': lambda u: 100.0,
        'g': lambda u: 100.0 - u,
        'h': lambda u: 1.0,
        'title': 'L',
        'title_x_shift': 0.0,
        'title_y_shift': 0.25,
        'scale_type': 'linear',
        'tick_levels': 3,
        'tick_text_levels': 2,
        'tick_side': 'right',
        'tag': 'none',
        'grid': False}

    test9c_f3 = {
        'ID': 'none',  # to identify the axis
        'tag': 'none',  # for aligning block wrt others
        'title': 'Grid',
        'title_x_shift': 0.0,
        'title_y_shift': 0.25,
        'title_distance_center': 0.5,
        'title_opposite_tick': True,
        'u_min': 0.0,  # for alignment
        'u_max': 1.0,  # for alignment
        'f_grid': lambda u, v: 100 * np.cos(u * np.pi / 180.0) / (1.0 + np.cos(u * np.pi / 180.0)),
        'g_grid': lambda u, v: (v * np.sin(u * np.pi / 180.0) + 100.0 * np.cos(u * np.pi / 180.0)) / (
            1.0 + np.cos(u * np.pi / 180.0)),
        'h_grid': lambda u, v: 1.0,
        'u_start': 15.0,
        'u_stop': 75.0,
        'v_start': 0.0,
        'v_stop': 100.0,
        'u_values': [15.0, 30.0, 45.0, 60.0, 75.0],
        'v_values': [0.0, 20.0, 40.0, 60.0, 80.0, 100.0],
        'grid': True,
        'text_prefix_u': r'$\theta$=',
        'text_prefix_v': r'k=',
        'text_distance': 0.5,
    }
    test9c_block_params = {
        'block_type': 'type_9',
        'f1_params': test9c_f1,
        'f2_params': test9c_f2,
        'f3_params': test9c_f3,
        'transform_ini': False,
    }

    test9c_params = {
        'filename': 'test9c.pdf',
        'paper_height': 10.0,
        'paper_width': 10.0,
        'block_params': [test9c_block_params],
        'transformations': [('rotate', 0.01), ('polygon',), ('scale paper',)]
    }
    Nomographer(test9c_params)

    # test 9 d
    test9d_f1 = {
        'u_min': 5.0,
        'u_max': 15.0,
        'f': lambda u: 0,
        'g': lambda s: s,
        'h': lambda u: 1.0,
        'title': 's',
        'title_x_shift': 0.0,
        'title_y_shift': 0.25,
        'scale_type': 'linear',
        'tick_levels': 3,
        'tick_text_levels': 2,
        'tick_side': 'left',
        'tag': 'none',
        'grid': False}

    test9d_f2 = {
        'u_min': 0.0,
        'u_max': 10.0,
        'f': lambda u: 1.0,
        'g': lambda u: -u,
        'h': lambda u: 1.0,
        'title': 'v',
        'title_x_shift': 0.0,
        'title_y_shift': 0.25,
        'scale_type': 'linear',
        'tick_levels': 3,
        'tick_text_levels': 2,
        'tick_side': 'right',
        'tag': 'none',
        'grid': False}

    test9d_f3 = {
        'ID': 'none',  # to identify the axis
        'tag': 'none',  # for aligning block wrt others
        'title': 'Grid',
        'title_x_shift': 0.0,
        'title_y_shift': 0.25,
        'title_distance_center': 0.5,
        'title_opposite_tick': True,
        'u_min': 0.0,  # for alignment
        'u_max': 1.0,  # for alignment
        'f_grid': lambda u, v: u / (u + 1.0),
        'g_grid': lambda u, v: 0.5 * v * u ** 2 / (u + 1.0),
        'h_grid': lambda u, v: 1.0,
        'u_start': 1.0,
        'u_stop': 3.0,
        'v_start': 0.0,
        'v_stop': 4.0,
        'u_values': [1.0, 2.0, 3.0],
        'v_values': [0.0, 1.0, 2.0, 3.0, 4.0],
        'text_prefix_u': r't=',
        'text_prefix_v': r'a=',
        'text_distance': 0.45,
        'grid': True,
        'v_texts_u_start': True,
        'v_texts_u_stop': False,
    }
    test9d_block_params = {
        'block_type': 'type_9',
        'f1_params': test9d_f1,
        'f2_params': test9d_f2,
        'f3_params': test9d_f3,
        'transform_ini': False,
    }

    test9d_params = {
        'filename': 'test9d.pdf',
        'paper_height': 10.0,
        'paper_width': 10.0,
        'block_params': [test9d_block_params],
        'transformations': [('rotate', 0.01), ('polygon',), ('scale paper',)]
    }
    Nomographer(test9d_params)

    # test type 10
    test_10_f1 = {
        'u_min': -25.0,
        'u_max': 0.0,
        'function': lambda u: u,
        'title': 'F1',
        'tag': 'none',
        'tick_side': 'right',
        'tick_levels': 2,
        'tick_text_levels': 1
    }
    test_10_f2 = {
        'u_min': -5.0,
        'u_max': 0.0,
        'function': lambda u: u,
        'title': 'F2',
        'tag': 'none',
        'tick_side': 'right',
        'tick_levels': 2,
        'tick_text_levels': 1
    }
    test_10_f3 = {
        'u_min': 0.5,
        'u_max': 5.0,
        'function_3': lambda u: u,
        'function_4': lambda u: u ** 2,
        'title': 'F3',
        'tag': 'none',
        'tick_side': 'right',
        'tick_levels': 2,
        'tick_text_levels': 1
    }
    test10_block_params = {
        'block_type': 'type_10',
        'f1_params': test_10_f1,
        'f2_params': test_10_f2,
        'f3_params': test_10_f3,
    }

    test10_params = {
        'filename': 'test10.pdf',
        'paper_height': 10.0,
        'paper_width': 10.0,
        'block_params': [test10_block_params],
        'transformations': [('rotate', 0.01), ('scale paper',)]
    }
    Nomographer(test10_params)
