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


import math
import pyx
import numpy as np
import random
from copy import copy


class Axis_Wrapper:
    """
    class to wrap axis functionalities. Grid_wrapper and other classes
    will be derived from this.
    """

    def __init__(self, f, g, start, stop, sections=350):
        self.sections = sections  # how many sections are used for calculations
        self.f = f
        self.g = g
        self.start = start
        self.stop = stop
        # initial transformation coeffs
        self.set_transformation()
        self._calculate_points_()
        self.calc_length()
        self.calc_bound_box()

    def _calculate_points_(self):
        """
        calculates points and segments of the line
        """
        f = self.f
        g = self.g
        start = self.start
        stop = self.stop
        # du=math.fabs(start-stop)*1e-8
        du = math.fabs(start - stop) * 1e-12
        # approximate line length is found
        line_length_straigth = math.sqrt(
            (f(start) - f(stop)) ** 2 + (g(start) - g(stop)) ** 2)
        random.seed(0.1)  # so that mistakes always the same
        for dummy in range(100):
            first = random.uniform(start, stop)
            second = random.uniform(start, stop)
            temp = math.sqrt((f(first) - f(second)) ** 2 +
                             (g(first) - g(second)) ** 2)
            if temp > line_length_straigth:
                line_length_straigth = temp
                # print "length: %f"%line_length_straigth
        sections = self.sections  # about number of sections
        section_length = line_length_straigth / sections
        line = [(f(start), g(start))]
        line.append((f(start), g(start)))
        u = start
        count = 1
        while True:
            if u < stop:
                dx = (f(u + du) - f(u))
                dy = (g(u + du) - g(u))
                dl = math.sqrt(dx ** 2 + dy ** 2)
                if dl > 0:
                    delta_u = du * section_length / dl
                else:
                    delta_u = du  # dummy constant?
                # let's calculate actual length
                # and iterate until length is in factor 2 from target
                """
                while True:
                    delta_x=f(u+delta_u)-f(u)
                    delta_y=g(u+delta_u)-g(u)
                    delta_l=math.sqrt(delta_x**2+delta_y**2)

                    if delta_l>2.0*section_length:
                        delta_u=delta_u*0.999
                        #print "delta_u math.pienenee:%f"%delta_u
                    else:
                        if delta_l<section_length/2.0:
                            delta_u=delta_u*1.001
                            #print "delta_u kasvaa:%f"%delta_u
                    if delta_l<=2*section_length and delta_l>=0.5*section_length:
                        break
                """
                u += delta_u
                # print u,stop
                count = count + 1
                if u < stop:
                    line.append((f(u), g(u)))
            else:
                line.append((f(stop), g(stop)))
                # print count
                # print line
                break
        self.line = line
        # calculate sections
        sections = []
        for index, (x, y) in enumerate(line):
            if index > 1:
                sections.append((x, y, prev_x, prev_y))
            prev_x = x
            prev_y = y
        self.sections = sections

    def give_trafo_x(self, x, y):
        """
        transformed x-coordinate
        """
        return ((self.alpha1 * x + self.beta1 * y + self.gamma1)
                / (self.alpha3 * x + self.beta3 * y + self.gamma3))

    def give_trafo_y(self, x, y):
        """
        transformed y-coordinate
        """
        return ((self.alpha2 * x + self.beta2 * y + self.gamma2)
                / (self.alpha3 * x + self.beta3 * y + self.gamma3))

    def set_transformation(self, alpha1=1.0, beta1=0.0, gamma1=0.0,
                           alpha2=0.0, beta2=1.0, gamma2=0.0,
                           alpha3=0.0, beta3=0.0, gamma3=1.0):
        """
        sets the transformation for x,y points to be applied
        see funcs give_trafo_x and give_trafo_y for details
        """
        self.alpha1 = alpha1
        self.beta1 = beta1
        self.gamma1 = gamma1
        self.alpha2 = alpha2
        self.beta2 = beta2
        self.gamma2 = gamma2
        self.alpha3 = alpha3
        self.beta3 = beta3
        self.gamma3 = gamma3

    def calc_length(self):
        """
        calculates length of the basic line
        """
        length = 0
        for x1, y1, x2, y2 in self.sections:
            x1t = self.give_trafo_x(x1, y1)
            y1t = self.give_trafo_y(x1, y1)
            x2t = self.give_trafo_x(x2, y2)
            y2t = self.give_trafo_y(x2, y2)
            section = math.sqrt((x1t - x2t) ** 2 + (y1t - y2t) ** 2)
            length = length + section
        # print length
        self.length = length
        return length

    def plot_axis(self, c):
        """
        plots axis to pyx.canvas
        """
        x00, y00 = self.line[0]
        x0 = self.give_trafo_x(x00, y00)
        y0 = self.give_trafo_y(x00, y00)
        # print x0,y0
        line = pyx.path.path(pyx.path.moveto(x0, y0))
        for x, y in self.line:
            xt = self.give_trafo_x(x, y)
            yt = self.give_trafo_y(x, y)
            line.append(pyx.path.lineto(xt, yt))
        c.stroke(line, [pyx.style.linewidth.normal])

    def calc_bound_box(self):
        """
        calculates bounding box for axis
        """
        line = self.line
        (x_0, y_0) = line[0]
        x_left = self.give_trafo_x(x_0, y_0)
        y_top = self.give_trafo_y(x_0, y_0)
        x_right = self.give_trafo_x(x_0, y_0)
        y_bottom = self.give_trafo_y(x_0, y_0)
        for x, y in line:
            x_trafo = self.give_trafo_x(x, y)
            y_trafo = self.give_trafo_y(x, y)
            if x_trafo < x_left:
                x_left = x_trafo
            if x_trafo > x_right:
                x_right = x_trafo
            if y_trafo < y_bottom:
                y_bottom = y_trafo
            if y_trafo > y_top:
                y_top = y_trafo
        # print x_left,x_right,y_bottom,y_top
        # in case there is no area inside box, let's make
        # small in order to avoid math.singularities. These are
        # specifically for dual-axis stationary scales
        if x_left == x_right:
            x_left = x_right - 1e-2 * abs(y_top - y_bottom)
        if y_top == y_bottom:
            y_top = y_bottom + 1e-2 * abs(x_left - x_right)
        self.x_left = x_left
        self.x_right = x_right
        self.y_top = y_top
        self.y_bottom = y_bottom
        # print x_left,x_right,y_bottom,y_top
        return x_left, x_right, y_bottom, y_top

    def calc_highest_point(self):
        """
        calculates point with heighest y_value
        """
        line = self.line
        (x_0, y_0) = line[0]
        x_best = self.give_trafo_x(x_0, y_0)
        y_best = self.give_trafo_y(x_0, y_0)
        for x, y in line:
            x_trafo = self.give_trafo_x(x, y)
            y_trafo = self.give_trafo_y(x, y)
            if y_trafo > y_best:
                y_best = y_trafo
                x_best = x_trafo
        return x_best, y_best

    def calc_lowest_point(self):
        """
        calculates point with lowest y-value
        """
        line = self.line
        (x_0, y_0) = line[0]
        x_best = self.give_trafo_x(x_0, y_0)
        y_best = self.give_trafo_y(x_0, y_0)
        for x, y in line:
            x_trafo = self.give_trafo_x(x, y)
            y_trafo = self.give_trafo_y(x, y)
            if y_trafo < y_best:
                y_best = y_trafo
                x_best = x_trafo
        return x_best, y_best

    def calc_min_slope(self, x_ref, y_ref):
        """
        calculates minimum absolute slope of any point in axis and
        given point (x_ref,y_ref)
        """
        line = self.line
        (x_0, y_0) = line[0]
        x_best = self.give_trafo_x(x_0, y_0)
        y_best = self.give_trafo_y(x_0, y_0)
        slope_best = self._calc_slope_(x_best, y_best, x_ref, y_ref)
        for x, y in line:
            x_trafo = self.give_trafo_x(x, y)
            y_trafo = self.give_trafo_y(x, y)
            slope = self._calc_slope_(x_trafo, y_trafo, x_ref, y_ref)
            if slope < slope_best:
                y_best = y_trafo
                x_best = x_trafo
                slope_best = slope
        return x_best, y_best, slope_best

    def _calc_slope_(self, x1, y1, x2, y2):
        """
        calculates absolute value of slope between points (x1,y1) and (x2,y2)
        slope = dy/dx
        """
        dx = abs(x2 - x1)
        dy = abs(y1 - y2)
        if dx > 1e-9:  # close to zero
            return dy / dx
        else:
            return 1e120  # = big number


class Axes_Wrapper:
    """
    class to wrap axes group functionalities. For optimization of
    axes w.r.t. to paper
    """

    def __init__(self, paper_width=10.0, paper_height=10.0):
        self.paper_width = paper_width
        self.paper_height = paper_height
        self.paper_prop = paper_width / paper_height
        self.set_transformation()
        self.trafo_stack = []  # stack for transformation matrices
        self._add_transformation_()
        self.axes_list = []

    def add_axis(self, axis):
        """
        adds axis to the list
        """
        self.axes_list.append(axis)
        # if same instance of Axis_Wrapper is used in many Axes Wrapper
        # instances, let's reset
        self._set_transformation_to_all_axis_()

    def define_paper_size(self, paper_width=10.0, paper_height=10.0):
        """
        sets proportion of the paper
        """
        self.paper_width = paper_width
        self.paper_height = paper_height
        self.paper_prop = paper_width / paper_height

    def set_transformation(self, alpha1=1.0, beta1=0.0, gamma1=0.0,
                           alpha2=0.0, beta2=1.0, gamma2=0.0,
                           alpha3=0.0, beta3=0.0, gamma3=1.0):
        """
        sets the transformation for x,y points to be applied
        see funcs give_trafo_x and give_trafo_y for details
        """
        self.alpha1 = alpha1
        self.beta1 = beta1
        self.gamma1 = gamma1
        self.alpha2 = alpha2
        self.beta2 = beta2
        self.gamma2 = gamma2
        self.alpha3 = alpha3
        self.beta3 = beta3
        self.gamma3 = gamma3

    def _set_transformation_to_all_axis_(self):
        """
        sets current transformation to all axes
        """
        for axis in self.axes_list:
            axis.set_transformation(alpha1=self.alpha1, beta1=self.beta1, gamma1=self.gamma1,
                                    alpha2=self.alpha2, beta2=self.beta2, gamma2=self.gamma2,
                                    alpha3=self.alpha3, beta3=self.beta3, gamma3=self.gamma3)

    def _calc_bounding_box_(self):
        """
        calculates bounding box for the axes
        """
        x_left, x_right, y_bottom, y_top = self.axes_list[0].calc_bound_box()
        for axis in self.axes_list:
            x_left0, x_right0, y_bottom0, y_top0 = axis.calc_bound_box()
            if x_left0 < x_left:
                x_left = x_left0
            if x_right0 > x_right:
                x_right = x_right0
            if y_bottom0 < y_bottom:
                y_bottom = y_bottom0
            if y_top0 > y_top:
                y_top = y_top0
        self.x_left = x_left
        self.x_right = x_right
        self.y_top = y_top
        self.y_bottom = y_bottom
        self.Wt = self.x_right - self.x_left
        self.Ht = self.y_top - self.y_bottom
        return x_left, x_right, y_bottom, y_top

    def _calc_paper_area_(self):
        """
        calculates paper area needed to fit axes to
        given paper proportions
        """
        proportion = self.Wt / self.Ht
        if proportion >= self.paper_prop:
            W = self.Wt
            H = self.Wt / self.paper_prop
        else:  # proportion<self.paper_prop
            W = self.Ht * self.paper_prop
            H = self.Ht
        # self.multiplier_x=self.paper_width/self.Wt
        # self.multiplier_y=self.paper_height/self.Ht
        self.H = H
        self.W = W
        self.paper_area = W * H

    def _trafo_to_paper_(self):
        """
        transforms nomogram to paper proportions
        """
        self._calc_bounding_box_()
        """
        multiplier_x=self.paper_width/self.Wt
        multiplier_y=self.paper_height/self.Ht
        """
        x1 = self.x_left
        y1 = self.y_top
        x2 = self.x_left
        y2 = self.y_bottom
        x3 = self.x_right
        y3 = self.y_top
        x4 = self.x_right
        y4 = self.y_bottom
        x1d = 0.0
        y1d = self.paper_height
        x2d = 0.0
        y2d = 0.0
        x3d = self.paper_width
        y3d = self.paper_height
        x4d = self.paper_width
        y4d = 0.0

        alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3 = \
            self._calc_transformation_matrix_(x1, y1, x2, y2, x3, y3, x4, y4,
                                              x1d, y1d, x2d, y2d, x3d, y3d, x4d, y4d)
        """
        alpha1=multiplier_x
        beta1=0.0
        gamma1=0.0
        alpha2=0.0
        beta2=multiplier_y
        gamma2=0.0
        alpha3=0.0
        beta3=0.0
        gamma3=1.0
        """
        self._add_transformation_(alpha1=alpha1, beta1=beta1, gamma1=gamma1,
                                  alpha2=alpha2, beta2=beta2, gamma2=gamma2,
                                  alpha3=alpha3, beta3=beta3, gamma3=gamma3)
        self._set_transformation_to_all_axis_()

    def _calc_axes_length_sq_sum_(self):
        """
        calculates sum of axes squared lengths
        """
        length_sum_sq = 0.0
        for axis in self.axes_list:
            length_sum_sq = length_sum_sq + (axis.calc_length()) ** 2
        self.length_sum_sq = length_sum_sq
        return length_sum_sq

    def _calc_min_func_(self, params):
        """
        function to be minimized
        """
        # print params
        # print "."
        self._change_params_to_last_trafo_mat_(
            params)  # sets tranformation parameters
        self._set_transformation_to_all_axis_()  # applies trafo to every axis
        bb = self._calc_bounding_box_()
        self._calc_paper_area_()
        self._calc_axes_length_sq_sum_()
        opt_value = self.paper_area / self.length_sum_sq
        max_bb = max(bb)
        min_bb = min(bb)
        max_bb = max(max_bb, -min_bb)
        if max_bb > 1000.0:
            opt_value = max_bb
        return opt_value

    def optimize_transformation(self):
        """
        returns optimal transformation
        """
        x0 = [1.0, 0, 0, 0, 1.0, 0, 0, 0, 1.0]
        self._add_params_trafo_stack_(x0)
        print("starts optimizing...")
        np.fmin(self._calc_min_func_, x0, full_output=1, maxiter=2000)
        # self.alpha1=self.multiplier_x*self.alpha1
        # self.beta1=self.multiplier_x*self.beta1
        # self.gamma1=self.multiplier_x*self.gamma1
        # self.alpha2=self.multiplier_y*self.alpha2
        # self.beta2=self.multiplier_y*self.beta2
        # self.gamma2=self.multiplier_y*self.gamma2
        self._set_transformation_to_all_axis_()
        # self._calc_bounding_box_()
        # self._trafo_to_paper_()

    def fit_to_paper(self):
        """
        makes tranformation to fit to paper
        """
        self._trafo_to_paper_()

    def matrix_trafo(self, given_matrix):
        """
        adds explicite matrix transformation
        """
        gm = given_matrix
        self._add_transformation_(alpha1=gm[0][0], beta1=gm[0][1], gamma1=gm[0][2],
                                  alpha2=gm[1][0], beta2=gm[1][1], gamma2=gm[1][2],
                                  alpha3=gm[2][0], beta3=gm[2][1], gamma3=gm[2][2])
        self._set_transformation_to_all_axis_()

    def _plot_axes_(self, c):
        """
        prints axes for debugging purposes
        """
        for axis in self.axes_list:
            axis.plot_axis(c)

    def _print_result_pdf_(self, filename="axis_func_test.pdf"):
        """
        prints result pdf for debugging purposes
        """
        c = pyx.canvas.canvas()
        self._plot_axes_(c)
        c.writePDFfile(filename)
        # print original
        # print transformed

    def _calc_transformation_matrix_(self, x1, y1, x2, y2, x3, y3, x4, y4,
                                     x1d, y1d, x2d, y2d, x3d, y3d, x4d, y4d):
        """
        calculates transformation from orig_points (4 x-y pairs) to
        dest_points (4 x-y pairs):

            (x1,y1)     (x3,y3)          (x1d,y1d)      (x3d,y3d)
               |  polygon  |      ---->      |   polygon  |
            (x2,y2)     (x4,y4)          (x2d,y2d)      (x4d,y4d)
        """
        """
        o=orig_points
        x1,y1,x2,y2=o['x1'],o['y1'],o['x2'],o['y2']
        x3,y3,x4,y4=o['x3'],o['y3'],o['x4'],o['y4']
        d=dest_points
        x1d,y1d,x2d,y2d=d['x1'],d['y1'],d['x2'],d['y2']
        x3d,y3d,x4d,y4d=d['x3'],d['y3'],d['x4'],d['y4']
        """
        row1, const1 = self._make_row_(
            coordinate='x', coord_value=x2d, x=x2, y=y2)
        row2, const2 = self._make_row_(
            coordinate='y', coord_value=y2d, x=x2, y=y2)
        row3, const3 = self._make_row_(
            coordinate='x', coord_value=x1d, x=x1, y=y1)
        row4, const4 = self._make_row_(
            coordinate='y', coord_value=y1d, x=x1, y=y1)
        row5, const5 = self._make_row_(
            coordinate='x', coord_value=x4d, x=x4, y=y4)
        row6, const6 = self._make_row_(
            coordinate='y', coord_value=y4d, x=x4, y=y4)
        row7, const7 = self._make_row_(
            coordinate='x', coord_value=x3d, x=x3, y=y3)
        row8, const8 = self._make_row_(
            coordinate='y', coord_value=y3d, x=x3, y=y3)

        matrix = np.array([row1, row2, row3, row4, row5, row6, row7, row8])
        # print matrix
        b = np.array([const1, const2, const3, const4,
                      const5, const6, const7, const8])
        coeff_vector = np.linalg.solve(matrix, b)
        alpha1 = -1.0  # fixed
        beta1 = coeff_vector[0][0]
        gamma1 = coeff_vector[1][0]
        alpha2 = coeff_vector[2][0]
        beta2 = coeff_vector[3][0]
        gamma2 = coeff_vector[4][0]
        alpha3 = coeff_vector[5][0]
        beta3 = coeff_vector[6][0]
        gamma3 = coeff_vector[7][0]
        return alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3

    def give_trafo(self):
        return self.alpha1, self.beta1, self.gamma1, \
            self.alpha2, self.beta2, self.gamma2, \
            self.alpha3, self.beta3, self.gamma3

    def _make_row_(self, coordinate='x', x=1.0, y=1.0, coord_value=1.0):
        """ Utility to find transformation matrix. See eq.37,a
        in Allcock. We take \alpha_1=1. h=1.
        """
        # to make expressions shorter
        cv = coord_value
        if coordinate == 'x':
            row = np.array([y, 1, 0, 0, 0, -cv * x, -cv * y, -cv * 1])
            value = np.array([x])
        if coordinate == 'y':
            row = np.array([0, 0, x, y, 1, -cv * x, -cv * y, -cv * 1])
            value = np.array([0])
        return row, value

    def _find_polygon_horizontal_(self):
        """
        finds intersection of horizontal line "dropmath.ping" until it
        hit the highest point (1) of axes. Then line tilts to minimum angle
        by another point (2).
        Same for bottom points (3) and (4) with vice versa.
        """
        # let's find the point with largest y-value
        y_high = -1e120  # big negative number
        for idx, axis in enumerate(self.axes_list):
            x, y = axis.calc_highest_point()
            if y > y_high:
                y_high = y
                x_high = x
                high_idx = idx
        # let's find the point with smallest y-value
        y_low = 1e120  # big number
        for idx, axis in enumerate(self.axes_list):
            x, y = axis.calc_lowest_point()
            if y < y_low:
                y_low = y
                x_low = x
                low_idx = idx
        # let's find the top-line with minimum slope
        slope_high = 1e120  # big number
        for idx, axis in enumerate(self.axes_list):
            x, y, slope = axis.calc_min_slope(x_high, y_high)
            if slope < slope_high and not idx == high_idx:
                y_slope_high = y
                x_slope_high = x
                slope_high = slope
        # let's find the bottom-lne with minimum slope
        slope_low = 1e120  # big number
        for idx, axis in enumerate(self.axes_list):
            x, y, slope = axis.calc_min_slope(x_low, y_low)
            if slope < slope_low and not idx == low_idx:
                y_slope_low = y
                x_slope_low = x
                slope_low = slope
        """ let's set the points to a ractangle form (not self-intersecting)
            (x1,y1)   -  (x3,y3)
               |  polygon  |
            (x2,y2)   -  (x4,y4)
        """
        x1, y1, x2, y2 = x_high, y_high, x_low, y_low
        x3, y3, x4, y4 = x_slope_high, y_slope_high, x_slope_low, y_slope_low
        # print x_high, y_high, x_low, y_low, x_slope_high, y_slope_high, x_slope_low, y_slope_low
        if (x1 - x3) * (x2 - x4) < 0:
            x1, y1, x3, y3 = x3, y3, x1, y1
        if x3 < x1:
            x1, y1, x2, y2, x3, y3, x4, y4 = x3, y3, x4, y4, x1, y1, x2, y2
        return x1, y1, x2, y2, x3, y3, x4, y4

    def make_polygon_trafo(self):
        """
        transforms polygon according to:

        finds intersection of horizontal line "dropmath.ping" until it
        hit the highest point (1) of axes. Then line tilts to minimum angle
        by another point (2).
        Same for bottom points (3) and (4) with vice versa. This polygon will
        be transformed to the corners of the paper.

            (x1,y1)     (x3,y3)          (x1d,y1d)      (x3d,y3d)
               |  polygon  |      ---->      |   polygon  |
            (x2,y2)     (x4,y4)          (x2d,y2d)      (x4d,y4d)
        """
        # find the left polygon
        x1, y1, x2, y2, x3, y3, x4, y4 = self._find_polygon_horizontal_()
        # define right polygon
        x1d, y1d = x1, self.paper_height
        x2d, y2d = x2, 0.0
        x3d, y3d = x3, self.paper_height
        x4d, y4d = x4, 0.0

        c = pyx.canvas.canvas()
        self._plot_axes_(c)
        c.fill(pyx.path.circle(x1, y1, 0.02))
        c.text(x1 + 1, y1, '1')
        c.fill(pyx.path.circle(x2, y2, 0.03))
        c.text(x2 + 1, y2, '2')
        c.fill(pyx.path.circle(x3, y3, 0.04))
        c.text(x3 + 1, y3, '3')
        c.fill(pyx.path.circle(x4, y4, 0.05))
        c.text(x4 + 1, y4, '4')
        # c.writePDFfile('poly_debug.pdf')
        # print "polygon coords:"
        # print x1,y1,x2,y2,x3,y3,x4,y4
        # calculate transformation
        alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3 = \
            self._calc_transformation_matrix_(x1, y1, x2, y2, x3, y3, x4, y4,
                                              x1d, y1d, x2d, y2d, x3d, y3d, x4d, y4d)
        # apply transformation
        self._add_transformation_(alpha1, beta1, gamma1, alpha2, beta2, gamma2,
                                  alpha3, beta3, gamma3)
        self._set_transformation_to_all_axis_()  # update axis
        self._trafo_to_paper_()  # transforms to paper

    def _add_transformation_(self, alpha1=1.0, beta1=0.0, gamma1=0.0,
                             alpha2=0.0, beta2=1.0, gamma2=0.0,
                             alpha3=0.0, beta3=0.0, gamma3=1.0):
        """
        adds transformation to be applied as a basis.
        all transformation matrices are multiplied together
        """
        trafo_mat = np.array([[alpha1, beta1, gamma1],
                              [alpha2, beta2, gamma2],
                              [alpha3, beta3, gamma3]])
        self.trafo_stack.append(trafo_mat)
        self._calculate_total_trafo_mat_()  # update coeffs

    def _calculate_total_trafo_mat_(self):
        """
        calculates total transformation matrix and
        master coeffs self.alpha1,self.beta1,...
        """
        stack_copy = copy(self.trafo_stack)
        stack_copy.reverse()
        trafo_mat = stack_copy.pop()
        for matrix in stack_copy:
            trafo_mat = np.dot(trafo_mat, matrix)  # matrix multiplication
        self.alpha1 = trafo_mat[0][0]
        self.beta1 = trafo_mat[0][1]
        self.gamma1 = trafo_mat[0][2]
        self.alpha2 = trafo_mat[1][0]
        self.beta2 = trafo_mat[1][1]
        self.gamma2 = trafo_mat[1][2]
        self.alpha3 = trafo_mat[2][0]
        self.beta3 = trafo_mat[2][1]
        self.gamma3 = trafo_mat[2][2]

    def _change_params_to_last_trafo_mat_(self, params):
        """
        changes transformation coeffs from optimization params to
        last transformation matrix in stack
        """
        alpha1 = params[0]
        beta1 = params[1]
        gamma1 = params[2]
        alpha2 = params[3]
        beta2 = params[4]
        gamma2 = params[5]
        alpha3 = params[6]
        beta3 = params[7]
        gamma3 = params[8]
        self.trafo_stack.pop()
        self._add_transformation_(alpha1=alpha1, beta1=beta1, gamma1=gamma1,
                                  alpha2=alpha2, beta2=beta2, gamma2=gamma2,
                                  alpha3=alpha3, beta3=beta3, gamma3=gamma3)

    def _add_params_trafo_stack_(self, params):
        """
        appends transformation coeffs from (optimization) params to stack
        """
        alpha1 = params[0]
        beta1 = params[1]
        gamma1 = params[2]
        alpha2 = params[3]
        beta2 = params[4]
        gamma2 = params[5]
        alpha3 = params[6]
        beta3 = params[7]
        gamma3 = params[8]
        self._add_transformation_(alpha1=alpha1, beta1=beta1, gamma1=gamma1,
                                  alpha2=alpha2, beta2=beta2, gamma2=gamma2,
                                  alpha3=alpha3, beta3=beta3, gamma3=gamma3)

    def _calc_rotation_trafo_(self, angle):
        """
        returns rotation transformation. angle in degrees.
        """
        angle_r = angle / 180.0 * math.pi  # angle in radians
        alpha1 = math.cos(angle_r)
        beta1 = -math.sin(angle_r)
        gamma1 = 0.0
        alpha2 = math.sin(angle_r)
        beta2 = math.cos(angle_r)
        gamma2 = 0.0
        alpha3 = 0.0
        beta3 = 0.0
        gamma3 = 1.0
        return alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3

    def rotate_canvas(self, angle):
        """
        rotates pyx.canvas by angle degrees by adding a rotation matrix
        into trafo_stack
        """
        alpha1, beta1, gamma1, alpha2, \
            beta2, gamma2, alpha3, beta3, gamma3 = self._calc_rotation_trafo_(
                angle)
        self._add_transformation_(alpha1=alpha1, beta1=beta1, gamma1=gamma1,
                                  alpha2=alpha2, beta2=beta2, gamma2=gamma2,
                                  alpha3=alpha3, beta3=beta3, gamma3=gamma3)
        self._set_transformation_to_all_axis_()


if __name__ == '__main__':
    """
    testing
    """

    def f1(L):
        return (2 * (L * L - 8 * L - 5) / (3 * L * L + 2 * L + 7))

    def g1(L):
        return 10 * (8 * L * L + 12 * L - 8) / (3 * L * L + 2 * L + 7)

    def f2(L):
        return math.log10(L)

    def g2(L):
        return 10 ** (L)

    def f3(L):
        return -L

    def g3(L):
        return L - 1.0

    def f4(L):
        return 3.0

    def g4(L):
        return L

    def f5(L):
        return 6.0

    def g5(L):
        return L

    test1_ax = Axis_Wrapper(f1, g1, 0.5, 1.0)
    test2_ax = Axis_Wrapper(f2, g2, 0.5, 1.0)
    test3_ax = Axis_Wrapper(f3, g3, 0.0, 1.0)
    test4_ax = Axis_Wrapper(f4, g4, 0.0, 2.0)
    test5_ax = Axis_Wrapper(f5, g5, 0.0, 3.0)
    test3a_ax = Axis_Wrapper(f3, g3, 0.0, 1.0)
    test4a_ax = Axis_Wrapper(f4, g4, 0.0, 2.0)
    test5a_ax = Axis_Wrapper(f5, g5, 0.0, 3.0)
    test_wrap = Axes_Wrapper()
    # print test_wrap._calc_transformation_matrix_(1, 1, 1, 2, 1, 3, 1, 4, 3, 3, 3, 4, 3, 5, 3, 6)
    test_wrap.add_axis(test3_ax)
    test_wrap.add_axis(test4_ax)
    test_wrap.add_axis(test5_ax)
    # test_wrap._calc_min_func_([3.0,0,0,0,2,0,0,0,1])
    test_wrap._print_result_pdf_("original.pdf")
    # test_wrap.optimize_transformation()
    # test_wrap._print_result_pdf_("final.pdf")

    test_wrap1 = Axes_Wrapper()
    test_wrap1.add_axis(test3_ax)
    test_wrap1.add_axis(test4_ax)
    test_wrap1.add_axis(test5_ax)
    # test_wrap._calc_min_func_([3.0,0,0,0,2,0,0,0,1])
    test_wrap1.rotate_canvas(45.0)
    test_wrap1._print_result_pdf_("final_rot.pdf")

    test_wrap2 = Axes_Wrapper()
    test_wrap2.add_axis(test3a_ax)
    test_wrap2.add_axis(test4a_ax)
    test_wrap2.add_axis(test5a_ax)
    # test_wrap._calc_min_func_([3.0,0,0,0,2,0,0,0,1])
    test_wrap2.rotate_canvas(45.0)
    test_wrap2._print_result_pdf_("ini_poly.pdf")
    test_wrap2.make_polygon_trafo()
    test_wrap2._print_result_pdf_("final_poly.pdf")
