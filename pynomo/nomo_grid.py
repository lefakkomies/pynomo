#
#    This file is part of PyNomo -
#    a program to create nomographs with Python (http://pynomo.sourceforge.net/)
#
#    Copyright (C) 2015  Leif Roschier  <lefakkomies@users.sourceforge.net>
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

from .nomo_axis import Nomo_Axis
import math
import numpy as np
import pyx
import random
import sys


class Nomo_Grid:
    """
    class to make grids
    """

    def __init__(self, func_f, func_g, canvas, data={}):
        self.f = func_f
        self.g = func_g
        self.canvas = canvas
        data_default_values = {'u_start': 0.0,
                               'u_stop': 1.0,
                               'v_start': 0.0,
                               'v_stop': 1.0,
                               'u_values': [0.0, 1.0],
                               'v_values': [0.0, 1.0],
                               'v_texts_u_start': False,
                               'v_texts_u_stop': True,
                               'u_texts_v_start': False,
                               'u_texts_v_stop': True,
                               'u_line_color': pyx.color.rgb.black,
                               'v_line_color': pyx.color.rgb.black,
                               'u_text_color': pyx.color.rgb.black,
                               'v_text_color': pyx.color.rgb.black,
                               'u_line_width': pyx.style.linewidth.normal,
                               'v_line_width': pyx.style.linewidth.normal,
                               'text_distance': 0.25,
                               'circles': False,  # if marker circles
                               'text_prefix_u': '',  # for example r'$\alpha$='
                               'text_prefix_v': '',  # for example r'$\beta$='
                               'text_format_u': "$%4.4g$",
                               'text_format_v': "$%4.4g$",
                               'iterator_factor': 1.001,
                               }
        self.grid_data = data_default_values
        self.grid_data.update(data)
        # print self.grid_data
        self._draw_line_u_()
        self._draw_line_v_()

    def _draw_line_u_(self):
        """
        draws a math.single line from start to stop for variable u
        """
        start = self.grid_data['u_start']
        stop = self.grid_data['u_stop']
        # if text labels to start and/or stop
        start_texts = self.grid_data['u_texts_v_start']
        stop_texts = self.grid_data['u_texts_v_stop']
        line_color = self.grid_data['v_line_color']
        line_width = self.grid_data['v_line_width']
        for idx, v in enumerate(self.grid_data['v_values']):
            f_here, g_here = self._make_u_funcs_(v)
            if 'v_texts' not in self.grid_data:
                # print self.grid_data['text_prefix_v']
                self._draw_line_(f_here, g_here, start, stop,
                                 r"%s%s" % (self.grid_data['text_prefix_v'], self.grid_data['text_format_v']) % v,
                                 line_color,
                                 start_texts, stop_texts, self.grid_data['v_text_color'], line_width)
            else:
                self._draw_line_(f_here, g_here, start, stop,
                                 self.grid_data['v_texts'][idx], line_color,
                                 start_texts, stop_texts, self.grid_data['v_text_color'], line_width)
                # print "v=%f"%v

    def _draw_line_v_(self):
        """
        draws a math.single line from start to stop for variable v
        """
        start = self.grid_data['v_start']
        stop = self.grid_data['v_stop']
        # if text labels to start and/or stop
        start_texts = self.grid_data['v_texts_u_start']
        stop_texts = self.grid_data['v_texts_u_stop']
        line_color = self.grid_data['u_line_color']
        line_width = self.grid_data['u_line_width']
        for idx, u in enumerate(self.grid_data['u_values']):
            f_here, g_here = self._make_v_funcs_(u)
            if 'u_texts' not in self.grid_data:
                self._draw_line_(f_here, g_here, start, stop,
                                 r"%s%s" % (self.grid_data['text_prefix_u'], self.grid_data['text_format_u']) % u,
                                 line_color,
                                 start_texts, stop_texts, self.grid_data['u_text_color'], line_width)
            else:
                self._draw_line_(f_here, g_here, start, stop,
                                 self.grid_data['u_texts'][idx], line_color,
                                 start_texts, stop_texts, self.grid_data['u_text_color'], line_width)
                # print "u=%f"%u

    def _make_u_funcs_(self, v_value):
        """
        copied trick to solve function defitions inside loop
        (I could not figure out how to use lambda...)
        """

        def f(u): return self.f(u, v_value)

        def g(u): return self.g(u, v_value)

        return f, g

    def _make_v_funcs_(self, u_value):
        """
        copied trick to solve function defitions inside loop
        (I could not figure out how to use lambda...)
        """

        def f(v): return self.f(u_value, v)

        def g(v): return self.g(u_value, v)

        return f, g

    def _draw_line_(self, f, g, start, stop, title, axis_color=pyx.color.rgb.red,
                    start_texts=False, stop_texts=True, text_color=pyx.color.rgb.black,
                    line_width=pyx.style.linewidth.normal):
        if start > 0 and stop > 0:
            du = (max(start, stop) - min(start, stop)) * 1e-10  # was 1e-10
            # print "start:%g stop:%g"%(start,stop)
            # print "testing du = %g"%du
        else:
            du = np.fabs(start - stop) * 1e-5
        # approximate line length is found
        line_length_straigth = np.sqrt((f(start) - f(stop)) ** 2 + (g(start) - g(stop)) ** 2)
        random.seed(0.0)  # so that mistakes always the same
        for dummy in range(100):
            first = random.uniform(start, stop)
            second = random.uniform(start, stop)
            temp = np.sqrt((f(first) - f(second)) ** 2 + (g(first) - g(second)) ** 2)
            if temp > line_length_straigth:
                line_length_straigth = temp
                # print "length: %f"%line_length_straigth
        sections = 350.0  # about number of sections
        section_length = line_length_straigth / sections
        line = pyx.path.path(pyx.path.moveto(f(start), g(start)))
        line.append(pyx.path.lineto(f(start), g(start)))
        u = start
        laskuri = 1
        up_factor = self.grid_data['iterator_factor']
        down_factor = 1.0 / up_factor
        delta_u = du  # initial
        while True:
            if (u + delta_u) < stop:
                dx = (f(u + du) - f(u))
                dy = (g(u + du) - g(u))
                dl = np.sqrt(dx ** 2 + dy ** 2)
                delta_u = du * section_length / dl
                # let's calculate actual length
                # and iterate until length is in factor 2 from target
                while True:
                    # u_delta_step = min(stop,u+delta_u) # in order to avoid going over range
                    if (u + delta_u) >= stop:  # stop if out of range
                        break
                    delta_x = f(u + delta_u) - f(u)
                    delta_y = g(u + delta_u) - g(u)
                    delta_l = np.sqrt(delta_x ** 2 + delta_y ** 2)
                    if delta_l > 5.0 * section_length:
                        delta_u = delta_u * down_factor  # 0.999
                        # print "delta_u math.pienenee:%f"%delta_u
                    else:
                        if delta_l < section_length / 5.0:
                            delta_u = delta_u * up_factor  # 1.001
                            # print "delta_u kasvaa:%f"%delta_u
                            # print "u+delta_u:%g, stop:%g"%(u+delta_u,stop)
                    if delta_l <= 5.0 * section_length and delta_l >= 0.2 * section_length:
                        # print "u:%g:x=%g, y=%g"%(u,f(u),g(u))
                        break

                u += delta_u
                # print u,stop
                laskuri = laskuri + 1
                line.append(pyx.path.lineto(f(u), g(u)))
            else:
                line.append(pyx.path.lineto(f(stop), g(stop)))
                # print laskuri
                sys.stdout.write('.')
                break

        self.canvas.stroke(line, [line_width, axis_color])
        # start number
        if start_texts:  # set texts to to start
            self._set_text_to_grid_(f, g, start, du, title, axis_color, text_color)
        if stop_texts:  # set texts to stop
            self._set_text_to_grid_(f, g, stop, -du, title, axis_color, text_color)
        if self.grid_data['circles']:
            self.canvas.fill(pyx.path.circle(f(start), g(start), 0.03), [axis_color])
            self.canvas.fill(pyx.path.circle(f(stop), g(stop), 0.03), [axis_color])
            # print "line drawn"

    def _set_text_to_grid_(self, f, g, u, du, title, axis_color, text_color=pyx.color.rgb.black):
        """
        draws text to the end of gridline
        """
        dx = (f(u + du) - f(u))
        dy = (g(u + du) - g(u))
        if np.sqrt(dx ** 2 + dy ** 2) == 0:
            dx_unit = 0
            dy_unit = 0
        else:
            dx_unit = dx / np.sqrt(dx ** 2 + dy ** 2)
            dy_unit = dy / np.sqrt(dx ** 2 + dy ** 2)
        if dy_unit != 0:
            """
            print "du %g"%du
            print "dx %g"%dx
            print "dy %g"%dy
            print "dx_unit %g"%dx_unit
            print "dy_unit %g"%dy_unit
            """
            angle = -math.atan(dx_unit / dy_unit) * 180 / math.pi
        else:
            angle = 0
        text_distance = 0.5
        # if dy<=0:
        if dy >= 0.0:
            if (angle - 90.0) <= -90.0:
                angle = angle + 180.0
            if dx_unit > 0.0:
                text_attr = [pyx.text.valign.middle, pyx.text.halign.right, pyx.text.size.small,
                             pyx.trafo.rotate(angle - 90)]
            if dx_unit <= 0.0:
                text_attr = [pyx.text.valign.middle, pyx.text.halign.left, pyx.text.size.small,
                             pyx.trafo.rotate(angle - 90)]
        else:
            if (angle + 90.0) >= 90.0:
                angle = angle - 180.0
            if dx_unit > 0.0:
                text_attr = [pyx.text.valign.middle, pyx.text.halign.right, pyx.text.size.small,
                             pyx.trafo.rotate(angle + 90)]
            if dx_unit <= 0.0:
                text_attr = [pyx.text.valign.middle, pyx.text.halign.left, pyx.text.size.small,
                             pyx.trafo.rotate(angle + 90)]
        """
        copied from nomo_axis.py
        if dy_units[idx]<0:
            text_attr=[pyx.text.valign.middle,pyx.text.halign.right,text_size,pyx.trafo.rotate(angles[idx])]
        else:
            text_attr=[pyx.text.valign.middle,pyx.text.halign.left,text_size,pyx.trafo.rotate(angles[idx])]
        text_list.append((self._put_text_(u),f(u)+text_distance*dy_units[idx],
                          g(u)-text_distance*dx_units[idx],text_attr))
        """
        text_distance = self.grid_data['text_distance']
        text_attr = text_attr + [text_color]
        self.canvas.text(f(u) - text_distance * dx_unit,
                         g(u) - text_distance * dy_unit,
                         title, text_attr)
        # self.canvas.fill(pyx.path.circle(f(u), g(u), 0.03),[axis_color])


if __name__ == '__main__':
    # functions for solartime
    # taken from solareqns.pdf from
    # http://www.srrb.noaa.gov/highlights/sunrise/solareqns.PDF
    def gamma(day):
        return 2 * math.pi / 365.0 * (day - 1 + 0.5)


    def eq_time(day):
        gamma0 = gamma(day)
        return 229.18 * (0.000075 + 0.001868 * np.cos(gamma0) - 0.032077 * np.sin(gamma0)
                         - 0.014615 * np.cos(2 * gamma0) - 0.040849 * np.sin(2 * gamma0))


    # np.mean correction, with constant correction we make less than 1.5 minutes error
    # in time axis
    temp_a = np.arange(0, 2 * math.pi, 0.001)
    temp_b = eq_time(temp_a)
    correction = np.mean(temp_b)  # this is about four minutes


    def eq_declination(day):
        g0 = gamma(day)
        return 0.006918 - 0.399912 * np.cos(g0) + 0.070257 * math.sin(g0) - 0.006758 * np.cos(2 * g0) \
               + 0.000907 * math.sin(2 * g0) - 0.002697 * np.cos(3 * g0) + 0.00148 * math.sin(3 * g0)


    def tst(day, hour):
        return hour * 60.0 + eq_time(day)


    def ha(day, hour):
        return tst(day, hour) / 4.0 - 180.0


    multiplier_x = 20.0
    multiplier_y = 10.0


    def f(lat, day):
        dec = eq_declination(day)
        return multiplier_x * (np.cos(lat * math.pi / 180.0) * np.cos(dec)) / (
                    1.0 + (np.cos(lat * math.pi / 180.0) * np.cos(dec)))


    def g(lat, day):
        dec = eq_declination(day)  # in radians
        return multiplier_y * (np.sin(lat * math.pi / 180.0) * math.sin(dec)) / (
                    1.0 + (np.cos(lat * math.pi / 180.0) * np.cos(dec)))


    def f1(dummy):
        return 0.0


    def g1(fii):
        return multiplier_y * np.cos(fii * math.pi / 180.0)


    def f3(dummy):
        return multiplier_x


    def g3(h):
        hr = (h * 60.0 + correction) / 4.0 - 180.0
        return -multiplier_y * np.cos(hr * math.pi / 180.0)


    days_in_month = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    times1 = []
    for idx in range(0, 12):
        times1.append(sum(days_in_month[0:idx]) + 1)

    # times=linspace(0,350,10)
    times = np.arange(0.0, 360.0, 10.0, dtype=np.double).tolist()
    time_titles = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    # times.append(365)
    data = {'u_start': 20.0,  # latitude
            'u_stop': 80.0,
            'v_start': times1[0],  # day
            'v_stop': times1[-1],
            'u_values': [20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0],
            # 'v_values':[0.0,60.0,120.0,180.0,240.0,300.0,365.0]
            'v_values': times1,
            'v_texts': time_titles}

    c = pyx.canvas.canvas()
    gridi = Nomo_Grid(f, g, c, data=data)
    ax1 = Nomo_Axis(func_f=f1, func_g=g1,
                    start=0.0, stop=90.0,
                    title=r'Solar zenith angle $\phi$', canvas=c, type='linear',
                    turn=-1,
                    tick_levels=2, tick_text_levels=1,
                    side='left')

    ax2 = Nomo_Axis(func_f=f3, func_g=g3,
                    start=0.0, stop=23.0,
                    title=r'Hour (h)', canvas=c, type='linear',
                    turn=-1,
                    tick_levels=3, tick_text_levels=1,
                    side='right')

    c.writePDFfile("test_nomo_grid")
    # let's get
    test_h = 10.0
    test_day = 70.0
    test_lat = 60.0
    test_ha = test_h * 60.0 / 4.0 - 180.0
    test_dec = eq_declination(test_day)
    test_cos_phi = math.sin(test_lat * math.pi / 180.0) * math.sin(test_dec) + \
                   np.cos(test_lat * math.pi / 180.0) * np.cos(test_dec) * np.cos(test_ha * math.pi / 180.0)
    # print acos(test_cos_phi)*180/pi
