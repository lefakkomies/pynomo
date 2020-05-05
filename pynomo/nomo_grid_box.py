# -*- coding: utf-8 -*-
#
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

from scipy import optimize
import numpy as np
import pyx
import math
import time


class Nomo_Grid_Box(object):
    """
    class to calculate "grid boxes" according to (East)-German nomographic tradition
    """

    def __init__(self, params={}):
        """
        params = definitions
        """
        params_default_values = {'width': 10.0,
                                 'height': 10.0,
                                 'mirror_x': False,
                                 'mirror_y': False,
                                 'u_func': lambda u: u,
                                 'v_func': lambda x, para: x + para,
                                 'line_func': lambda x: x,  # function for centerline assuming square
                                 'draw_line': True,
                                 'w_func': lambda x: x,  # function for w axis
                                 'w_func_inv': lambda x: x,  # inverse function for w axis
                                 'w_min': 0.1,
                                 'w_max': 1.0,
                                 'manual_w_scale': False,
                                 'wd_func': lambda x: x,  # function for w axis
                                 'wd_func_inv': lambda x: x,  # inverse function for w axis
                                 'wd_min': 0.1,
                                 'wd_max': 1.0,
                                 'manual_wd_scale': False,
                                 'v_min': 0.1,  # not used typically
                                 'v_max': 1.0,  # not used typically
                                 'x_min': 0.1,
                                 'x_max': 1.0,
                                 'manual_x_scale': False,  # if inital x_scale is set manually, use two values above
                                 'u_values': [0.0, 0.25 * math.pi / 2, 0.5 * math.pi / 2, 0.75 * math.pi / 2,
                                              1.0 * math.pi / 2],
                                 'v_values': [0.0, 0.25 * math.pi / 2, 0.5 * math.pi / 2, 0.75 * math.pi / 2,
                                              1.0 * math.pi / 2],
                                 'wd_values': [],
                                 'w_values': [],
                                 'u_tag': 'none',  # manual labels
                                 'w_tag': 'none',
                                 'wd_tag': 'none',
                                 'u_reference': False,  # manual labels
                                 'v_reference': False,
                                 'w_reference': False,
                                 'wd_reference': False,
                                 'scale_type_u': 'manual line',
                                 'scale_type_w': 'linear',
                                 'scale_type_wd': 'linear',
                                 'scale_type_v': 'manual line',  # change in definition by own risk
                                 'u_title': '',
                                 'v_title': '',
                                 'w_title': '',
                                 'wd_title': '',
                                 'u_tick_side': None,  # can be overriden
                                 'u_tick_levels': 0,
                                 'u_tick_text_levels': 0,
                                 'v_tick_side': 'right',
                                 'v_tick_levels': 0,
                                 'v_tick_text_levels': 0,
                                 'w_tick_side': 'right',
                                 'w_tick_levels': 0,
                                 'w_tick_text_levels': 0,
                                 'wd_tick_side': 'left',
                                 'wd_tick_levels': 0,
                                 'wd_tick_text_levels': 0,
                                 'horizontal_guide_nr': 51,
                                 'horizontal_guides': True,
                                 'vertical_guide_nr': 51,
                                 'vertical_guides': True,
                                 'u_title_opposite_tick': False,
                                 'v_title_opposite_tick': False,
                                 'wd_title_opposite_tick': False,
                                 'w_title_opposite_tick': False,
                                 'u_title_distance_center': 1.5,
                                 'v_title_distance_center': 1.5,
                                 'wd_title_distance_center': 1.5,
                                 'w_title_distance_center': 1.5,
                                 'u_title_draw_center': True,
                                 'v_title_draw_center': True,
                                 'wd_title_draw_center': True,
                                 'w_title_draw_center': True,
                                 'u_text_format': r"$%4.4g$ ",
                                 'v_text_format': r"$%4.4g$ ",
                                 'u_align_func': lambda u: u,
                                 'wd_align_func': lambda u: u,
                                 'w_align_func': lambda u: u,
                                 'u_scale_opposite': False,
                                 'v_manual_axis_data': None,
                                 'u_manual_axis_data': None,
                                 'v_text_distance': 0.25,
                                 'u_align_x_offset': 0.0,
                                 'wd_align_x_offset': 0.0,
                                 'u_align_y_offset': 0.0,
                                 'wd_align_y_offset': 0.0,
                                 'u_axis_color': pyx.color.rgb.black,
                                 'u_text_color': pyx.color.rgb.black,
                                 'u_title_color': pyx.color.rgb.black,
                                 'v_axis_color': pyx.color.rgb.black,
                                 'v_text_color': pyx.color.rgb.black,
                                 'v_title_color': pyx.color.rgb.black,
                                 'wd_axis_color': pyx.color.rgb.black,
                                 'wd_text_color': pyx.color.rgb.black,
                                 'wd_title_color': pyx.color.rgb.black,
                                 'allow_additional_v_scale': False,  # to draw additional scale as atom
                                 # isopleths do not work
                                 'v_scale_u_value': 1.0,  # this value sets additional v_scale
                                 'x_func': lambda u, v: u + v  # gives x as a function of u and v
                                 }
        self.params = params_default_values
        self.params.update(params)
        # initial guesses
        self.u_func = self.params['u_func']
        self.v_func = self.params['v_func']
        self._build_v_lines_(self.v_func)
        self._calc_bound_box_ini_()
        self._build_u_lines_(self.u_func)
        # debug by looking pdf
        # self._draw_debug_ini_()
        # build scaled versions
        self._scale_and_mirror_()
        # self._draw_debug_ini_('after.pdf')

        self.give_u_data()
        self.give_v_data()
        self.give_w_data()
        self.give_wd_data()

    def give_u_data(self):
        """
        gives F(u),G(u)-functions and other params (left coordinate)
        """
        # calc func
        u_func = self.u_func  # defined in scaling
        u_manual_axis_data = {}
        if self.params['u_manual_axis_data'] == None:
            for u_value in self.params['u_values']:
                u_manual_axis_data[u_value] = self.params['u_text_format'] % u_value
        else:
            u_manual_axis_data = self.params['u_manual_axis_data']
        if self.params['u_scale_opposite']:
            x_coordinate = self.x_right
        else:
            x_coordinate = self.x_left
        self.params_u = {
            'u_min': min(self.params['u_values']),
            'u_max': max(self.params['u_values']),
            'F': lambda u: x_coordinate,  # x-coordinate
            'G': u_func,  # y-coordinate
            'title': self.params['u_title'],
            # 'linear' 'log' 'manual point' 'manual line'
            'scale_type': self.params['scale_type_u'],
            'manual_axis_data': u_manual_axis_data,
            'tick_side': self.params['u_tick_side'],
            'tag': self.params['u_tag'],  # for aligning block wrt others
            'reference': self.params['u_reference'],
            # not really used, yet
            'tick_levels': self.params['u_tick_levels'],
            # not really used, yet
            'tick_text_levels': self.params['u_tick_text_levels'],
            'title_opposite_tick': self.params['u_title_opposite_tick'],
            'title_distance_center': self.params['u_title_distance_center'],
            'title_draw_center': self.params['u_title_draw_center'],
            'align_func': self.params['u_align_func'],
            'align_x_offset': self.params['u_align_x_offset'],
            'align_y_offset': self.params['u_align_y_offset'],
            # 'text_format':self.params['u_text_format'],
            'axis_color': self.params['u_axis_color'],
            'text_color': self.params['u_text_color'],
            'title_color': self.params['u_title_color'],
        }
        return self.params_u

    def give_v_data(self):
        """
        givesgives F(u),G(u)-functions and other params (top coordinate)
        function is linear and values are set manually to correct places
        """
        v_manual_axis_data = {}
        # let's go through all lines and find x-coordinate of top points.
        for idx1, v_line in enumerate(self.v_lines):
            x_max, y_max = v_line[0]
            for idx2, (x, y) in enumerate(v_line):
                if y > y_max:
                    x_max = x
                    y_max = y
            v_value = self.params['v_values'][idx1]
            # v_manual_axis_data[v_value]='%f'%x_max
            v_manual_axis_data[x_max] = '%3.2f' % v_value
        # in case one wants better v-scale
        if self.params['allow_additional_v_scale']:
            v_min = self.params['v_min']
            v_max = self.params['v_max']
            # this value has to be set manually
            u_value = self.params['v_scale_u_value']
            def f_v(v): return self.x_func(u_value, v)
            def g_v(u): return self.u_func(u_value)
        else:  # assuming manual data
            v_min = self.x_left
            v_max = self.x_right
            def f_v(u): return u
            def g_v(u): return self.x_top
        self.params_v = {
            #            'u_min':self.x_left,
            #            'u_max':self.x_right,
            #            'F':lambda u:u, # x-coordinate
            #            'G':lambda u:self.y_top, # y-coordinate
            'u_min': v_min,
            'u_max': v_max,
            'F': f_v,
            'G': g_v,
            'title': self.params['v_title'],
            # 'scale_type':'manual line', #this have to be hard coded
            'scale_type': self.params['scale_type_v'],
            'manual_axis_data': v_manual_axis_data,
            'tick_side': self.params['v_tick_side'],
            'tag': 'none',  # this axis should not be aligned
            'reference': self.params['v_reference'],
            # not really used, yet
            'tick_levels': self.params['v_tick_levels'],
            # not really used, yet
            'tick_text_levels': self.params['v_tick_text_levels'],
            'title_opposite_tick': self.params['v_title_opposite_tick'],
            'title_distance_center': self.params['v_title_distance_center'],
            'title_draw_center': self.params['v_title_draw_center'],
            'text_format': self.params['v_text_format'],
            'axis_color': self.params['v_axis_color'],
            'text_color': self.params['v_text_color'],
            'title_color': self.params['v_title_color'],
        }
        return self.params_v

    def give_w_data(self):
        """
        gives x(w),y(w)-functions and w_min and w_max values.
        w = f2(f3(x))
        x = bottom coordinate of initial axes
        f3 = line func
        f2 = additional transformation
        """
        f3 = self.params['line_func']
        f2 = self.params['w_func']
        f2_inv = self.params['w_func_inv']
        w_manual_axis_data = {}
        if self.params['scale_type_w'] == 'manual line':
            for w_value in self.params['w_values']:
                w_manual_axis_data[w_value] = '%f' % w_value

        w_min = f2_inv(f3(self.x_left_ini))
        w_max = f2_inv(f3(self.x_right_ini))
        w_diff = w_max - w_min
        if self.params['mirror_y'] == True:
            y_factor = -1.0
        else:
            y_factor = 1.0
        self.params_w = {
            'u_min': w_min,  # this is w_min
            'u_max': w_max,  # this is w_max
            'F': lambda w: self.x_right,  # x-coordinate
            'G': lambda w: self.y_bottom + (f2(w) - f2(w_min)) / (f2(w_max) - f2(w_min)) \
            * self.params['height'] * y_factor,  # y-coordinate
            'title': self.params['w_title'],
            'scale_type': self.params['scale_type_w'],
            'manual_axis_data': w_manual_axis_data,
            'tick_side': self.params['w_tick_side'],
            'tag': self.params['w_tag'],  # for aligning block wrt others
            'reference': self.params['w_reference'],
            'tick_levels': self.params['w_tick_levels'],
            'tick_text_levels': self.params['w_tick_text_levels'],
            'title_opposite_tick': self.params['w_title_opposite_tick'],
            'title_distance_center': self.params['w_title_distance_center'],
            'title_draw_center': self.params['w_title_draw_center'],
            'align_func': self.params['w_align_func'],
        }
        return self.params_w

    def give_wd_data(self):
        """
        gives x(wd),y(wd)-functions and wd_min and wd_max values. (bottom coordinate)
        """
        wd_manual_axis_data = {}
        if self.params['scale_type_wd'] == 'manual line':
            for wd_value in self.params['wd_values']:
                wd_manual_axis_data[wd_value] = '%f' % wd_value
        f1 = self.params['wd_func']
        f1_inv = self.params['wd_func_inv']
        wd_min = f1_inv(self.x_left_ini)
        wd_max = f1_inv(self.x_right_ini)
        self.params_wd = {
            'u_min': wd_min,
            'u_max': wd_max,
            'F': lambda u: f1(u) * self.x_factor,  # x-coordinate
            'G': lambda u: self.y_bottom,  # y-coordinate
            'title': self.params['wd_title'],
            'scale_type': self.params['scale_type_wd'],
            'manual_axis_data': wd_manual_axis_data,
            'tick_side': self.params['wd_tick_side'],
            'tag': self.params['wd_tag'],  # for aligning block wrt others
            'reference': self.params['wd_reference'],
            'tick_levels': self.params['wd_tick_levels'],
            'tick_text_levels': self.params['wd_tick_text_levels'],
            'title_opposite_tick': self.params['wd_title_opposite_tick'],
            'title_distance_center': self.params['wd_title_distance_center'],
            'title_draw_center': self.params['wd_title_draw_center'],
            'align_func': self.params['wd_align_func'],
            'align_x_offset': self.params['wd_align_x_offset'],
            'align_y_offset': self.params['wd_align_y_offset'],
            'axis_color': self.params['wd_axis_color'],
            'text_color': self.params['wd_text_color'],
            'title_color': self.params['wd_title_color'],
        }
        return self.params_wd

    def give_contours(self):
        """
        gives contours to be drawn
        """
        pass

    def _scale_and_mirror_(self):
        """
        scales everything to width and height
        """
        if self.params['mirror_x'] == True:
            mirror_x = -1.0
        else:
            mirror_x = 1.0
        if self.params['mirror_y'] == True:
            mirror_y = -1.0
        else:
            mirror_y = 1.0
        # scales lines
        y_factor = mirror_y * self.params['height'] / self.BB_height_ini
        x_factor = mirror_x * self.params['width'] / self.BB_width_ini
        for idx1, u_line in enumerate(self.u_lines):
            for idx2, (x, y) in enumerate(u_line):
                x_new = x * x_factor
                y_new = y * y_factor
                self.u_lines[idx1][idx2] = (x_new, y_new)
        for idx1, v_line in enumerate(self.v_lines):
            for idx2, (x, y) in enumerate(v_line):
                x_new = x * x_factor
                y_new = y * y_factor
                self.v_lines[idx1][idx2] = (x_new, y_new)
        # scale functions
        self.u_func = lambda u: self.params['u_func'](u) * y_factor
        self.v_func = lambda x, v: self.params['v_func'](
            x / x_factor, v) * y_factor
        self.x_func = lambda u, v: self.params['x_func'](u, v) * x_factor
        self.x_left = self.x_left_ini * x_factor
        self.x_right = self.x_right_ini * x_factor
        self.y_bottom = self.y_bottom_ini * y_factor
        self.y_top = self.y_top_ini * y_factor
        self.x_factor = x_factor
        self.y_factor = y_factor

    def _build_u_scale_(self):
        """
        vertical scale on the left
        """
        pass

    def _build_v_scale_(self):
        """
        horizontal scale on the top
        """
        pass

    def _build_u_lines_(self, u_func):
        """
        lines starting from u scale
        """
        self.u_lines = []
        self.u_sections = []
        # g=self.u_func
        g = u_func
        for u in self.params['u_values']:
            line = [(self.x_left_ini, g(u))]
            line.append((self.x_left_ini, g(u)))
            line.append((self.x_right_ini, g(u)))
            section = [(self.x_left_ini, g(u), self.x_right_ini, g(u))]
            self.u_lines.append(line)
            self.u_sections.append(section)

    def _build_v_lines_(self, v_func):
        """
        build lines starting from top scale
        """
        self.v_lines = []
        self.v_sections = []
        for v in self.params['v_values']:
            line, sections = self._build_v_line_(v_func=v_func, v=v)
            self.v_lines.append(line)
            self.v_sections.append(sections)

    def _build_v_line_(self, v_func, v=1.0):
        """
        line starting from x scale
        code copied originally form nomo_axis_func.py: _calculate_points_
        v_func is the function(x,p)
        p is the parametric value of the top scale
        """
        # find top and bottom lines
        max_fu = self.u_func(self.params['u_values'][0])
        min_fu = max_fu
        for u in self.params['u_values']:
            fu = self.u_func(u)
            if fu > max_fu:
                max_fu = fu
            if fu < min_fu:
                min_fu = fu
        # functions to find x-values in paper
        func2 = v_func

        def func_top(x):
            value = func2(x.astype(complex), v)
            if value.imag > 0:
                return 1e10  # big number
            else:
                return (func2(x, v) - max_fu) ** 2

        def func_bottom(x):
            value = func2(x.astype(complex), v)
            if value.imag > 0:
                return 1e10  # big number
            else:
                return (func2(x, v) - min_fu) ** 2

        # func_top=lambda x:((func2(x.astype(complex),v)-max_fu)**2).real+1e8*((func2(x.astype(complex),v)-max_fu)**2).imag # minimum at height
        # func_bottom=lambda x:((func2(x.astype(complex),v)-min_fu)**2).real+1e8*((func2(x.astype(complex),v)-min_fu)**2).imag # minimum at 0.0
        def f(x): return x
        def g(x): return func2(x, v)
        # find point of scale to meet point 1.0
        x_guess_top = 1.0
        x_guess_bottom = 1.0
        if self.params['manual_x_scale'] == True:
            mean_x = (self.params['x_min'] + self.params['x_max']) / 2.0
            x_guess_top = mean_x
            x_guess_bottom = mean_x
        x_top = optimize.fmin(
            func_top, [x_guess_top], disp=0, ftol=1e-5, xtol=1e-5)[0]
        x_bottom = optimize.fmin(
            func_bottom, [x_guess_bottom], disp=0, ftol=1e-5, xtol=1e-5)[0]
        # print "x_top %f"%x_top
        # print "x_bottom %f" % x_bottom
        # print "g(x_top) %f"%g(x_top)
        # print "g(x_bottom) %f" %g(x_bottom)
        if self.params['manual_x_scale'] == True:
            x_min_limit = self.params['x_min']
            x_max_limit = self.params['x_max']
            if x_min_limit > x_max_limit:
                x_min_limit, x_max_limit = x_max_limit, x_min_limit
            if x_top > x_max_limit:
                x_top = x_max_limit
            if x_top < x_min_limit:
                x_top = x_min_limit
            if x_bottom > x_max_limit:
                x_bottom = x_max_limit
            if x_bottom < x_min_limit:
                x_bottom = x_min_limit
        start = min(x_top, x_bottom)
        stop = max(x_top, x_bottom)
        # if self.params['manual_x_scale']==True:
        #    start=min(self.params['x_min'],self.params['x_max'])
        #    stop=max(self.params['x_min'],self.params['x_max'])
        du = np.fabs(stop - start) * 1e-12
        # approximate line length is found
        line_length_straigth = max_fu - min_fu
        sections = 200.0  # number of sections
        section_length = line_length_straigth / sections
        line = [(f(start), g(start))]
        line.append((f(start), g(start)))
        u = start
        count = 1
        # print "v:%g"%v
        while True:
            if u < stop:
                count = 1
                dx = (f(u + du) - f(u))
                dy = (g(u + du) - g(u))
                dl = np.sqrt(dx ** 2 + dy ** 2)
                if dl > 0:
                    delta_u = du * section_length / dl
                else:
                    delta_u = du
                # let's calculate actual length
                # and iterate until length is in factor 2 from target
                while True:
                    count = count + 1
                    delta_x = f(u + delta_u) - f(u)
                    delta_y = g(u + delta_u) - g(u)
                    delta_l = np.sqrt(delta_x ** 2 + delta_y ** 2)
                    if delta_l > 2.0 * section_length:
                        delta_u = delta_u * 0.999
                        # print "v:%g, delta_x:%g delta_y:%g delta_l:%g, section_length:%g, delta_u math.pienenee:%g"%(v,delta_x,delta_y,delta_l,section_length,delta_u)
                    else:
                        if delta_l < section_length / 2.0:
                            delta_u = delta_u * 1.001
                            # print "v:%g, delta_x:%g delta_y:%g delta_l:%g, section_length:%g, delta_u kasvaa:%g"%(v,delta_x,delta_y,delta_l,section_length,delta_u)
                    if delta_l <= 2 * section_length and delta_l >= 0.5 * section_length:
                        # print "selvitty"
                        break
                    if count > 1e3:  # cancel if not solution
                        print("Warning no solution found in contour")
                        break

                u += delta_u
                # print u,stop
                if (u < stop and count < 1e3):
                    line.append((f(u), g(u)))
                else:
                    u = stop  # stop looping of contour
                    # print "count %f"%count
            else:
                line.append((f(stop), g(stop)))
                # print count
                # print len(line)
                break
        # calculate sections
        sections = []
        for index, (x, y) in enumerate(line):
            if index > 1:
                sections.append((x, y, prev_x, prev_y))
            prev_x = x
            prev_y = y
        return line, sections

    def _calc_bound_box_ini_(self):
        """
        calculates bounding initial bounding box
        """
        (x_0, y_0) = self.v_lines[0][0]
        x_left = x_0
        y_top = max(self.u_func(np.array(self.params['u_values'])))
        x_right = x_0
        y_bottom = min(self.u_func(np.array(self.params['u_values'])))
        for line in self.v_lines:
            for x, y in line:
                if x < x_left:
                    x_left = x
                if x > x_right:
                    x_right = x
                if y < y_bottom:
                    y_bottom = y
                if y > y_top:
                    y_top = y
                    # print "y_top %f"%y_top
        # print x_left,x_right,y_bottom,y_top
        if self.params['manual_x_scale'] == True:
            self.x_left_ini = self.params['x_min']
            self.x_right_ini = self.params['x_max']
        else:
            self.x_left_ini = x_left
            self.x_right_ini = x_right
        self.y_top_ini = y_top
        self.y_bottom_ini = y_bottom
        # self.BB_width_ini=x_right-x_left
        self.BB_width_ini = abs(self.x_left_ini - self.x_right_ini)
        self.BB_height_ini = y_top - y_bottom
        return x_left, x_right, y_bottom, y_top

    #    def _build_box_(self):
    #        """
    #        box around structure
    #        """
    #        pass
    #
    #    def _build_diagonal_line(self):
    #        """
    #        diagonal line to make 90 degree angle
    #        """
    #        pass

    def _draw_debug_ini_(self, filename='nomo_grid_test_debug.pdf'):
        """
        draws lines for debugging purposes, initial figure
        """
        cc = pyx.canvas.canvas()
        x00, y00 = self.u_lines[0][0]
        line = pyx.path.path(pyx.path.moveto(x00, y00))
        for u_line in self.u_lines:
            x0, y0 = u_line[0]
            line.append(pyx.path.moveto(x0, y0))
            for x, y in u_line:
                line.append(pyx.path.lineto(x, y))
        for v_line in self.v_lines:
            x0, y0 = v_line[0]
            line.append(pyx.path.moveto(x0, y0))
            for x, y in v_line:
                line.append(pyx.path.lineto(x, y))

        cc.stroke(line, [pyx.style.linewidth.normal])
        cc.writePDFfile(filename)


if __name__ == '__main__':
    def f1(x, u):
        return np.log(x / (x - u / 100.0)) / np.log(1 + u / 100.0)

    params = {'width': 10.0,
              'height': 10.0,
              'u_func': lambda u: u,
              'v_func': f1,
              'u_values': [10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0],
              'v_values': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
              'v_tick_side': 'left',
              }
    tic = time.time()
    test = Nomo_Grid_Box(params=params)
    toc = time.time()
    # print toc - tic, ' has elapsed'

    manual_axis_data = {1.0: 'first',
                        2.0: 'second',
                        3.0: 'third',
                        3.1415: r'$\pi$',
                        4.0: 'fourth',
                        5.0: 'fifth',
                        6.0: 'sixth',
                        7.0: 'seventh',
                        8.0: 'eigth',
                        9.0: 'nineth',
                        10.0: 'tenth'}
