# -*- coding: utf-8 -*-
#    This file is part of PyNomo -
#    a program to create nomographs with Python (https://github.com/lefakkomies/pynomo)
#
#    Copyright (C) 2007-2019  Leif Roschier  <lefakkomies@users.sourceforge.net>
#
#    This file otherwise obsolete but used  in nomo_wrapper.py
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


import numpy as np


class Nomograph3(object):
    def __init__(self, f1, g1, h1, f2, g2, h2, f3, g3, h3,
                 vk=[['u', 0.5, 'x', -5],
                     ['u', 0.5, 'y', 0.0],
                     ['u', 1.0, 'x', -5],
                     ['u', 1.0, 'y', 15],
                     ['w', 1.0, 'x', 5],
                     ['w', 1.0, 'y', 0],
                     ['w', 0.5, 'x', 5],
                     ['w', 0.5, 'y', 15]]):
        """ arguments (f1,...,h3) are the functions in determinant
        vk is the structure to transform nomograph
        etc, generally the values set 4 points of axes
        """
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3
        self.g1 = g1
        self.g2 = g2
        self.g3 = g3
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.vk = vk
        self._make_transformation_matrix_()

    def _make_row_(self, variable='u', variable_value=0, coordinate='x', coord_value=10):
        """ makes a single row into matrix that transforms final nomographs such that
        value of variable (u,v or w) corresponds to the coordinate (x or y). See eq.37,a
        in Allcock. We take \alpha_1=1.
        """
        # to make expressions shorter
        vv = variable_value
        cv = coord_value
        f1 = self.f1
        f2 = self.f2
        f3 = self.f3
        g1 = self.g1
        g2 = self.g2
        g3 = self.g3
        h1 = self.h1
        h2 = self.h2
        h3 = self.h3
        if variable == 'u' and coordinate == 'x':
            row = np.array([g1(vv), h1(vv), 0, 0, 0, -cv * f1(vv), -cv * g1(vv), -cv * h1(vv)])
            value = np.array([f1(vv)])
        if variable == 'u' and coordinate == 'y':
            row = np.array([0, 0, f1(vv), g1(vv), h1(vv), -cv * f1(vv), -cv * g1(vv), -cv * h1(vv)])
            value = np.array([0])
        if variable == 'v' and coordinate == 'x':
            row = np.array([g2(vv), h2(vv), 0, 0, 0, -cv * f2(vv), -cv * g2(vv), -cv * h2(vv)])
            value = np.array([f2(vv)])
        if variable == 'v' and coordinate == 'y':
            row = np.array([0, 0, f2(vv), g2(vv), h2(vv), -cv * f2(vv), -cv * g2(vv), -cv * h2(vv)])
            value = np.array([0])
        if variable == 'w' and coordinate == 'x':
            row = np.array([g3(vv), h3(vv), 0, 0, 0, -cv * f3(vv), -cv * g3(vv), -cv * h3(vv)])
            value = np.array([f3(vv)])
        if variable == 'w' and coordinate == 'y':
            row = np.array([0, 0, f3(vv), g3(vv), h3(vv), -cv * f3(vv), -cv * g3(vv), -cv * h3(vv)])
            value = np.array([0])
        return row, value

    def _make_transformation_matrix_(self):
        vk = self.vk
        row1, const1 = self._make_row_(variable=vk[0][0], variable_value=vk[0][1], coordinate=vk[0][2],
                                       coord_value=vk[0][3])
        row2, const2 = self._make_row_(variable=vk[1][0], variable_value=vk[1][1], coordinate=vk[1][2],
                                       coord_value=vk[1][3])
        row3, const3 = self._make_row_(variable=vk[2][0], variable_value=vk[2][1], coordinate=vk[2][2],
                                       coord_value=vk[2][3])
        row4, const4 = self._make_row_(variable=vk[3][0], variable_value=vk[3][1], coordinate=vk[3][2],
                                       coord_value=vk[3][3])
        row5, const5 = self._make_row_(variable=vk[4][0], variable_value=vk[4][1], coordinate=vk[4][2],
                                       coord_value=vk[4][3])
        row6, const6 = self._make_row_(variable=vk[5][0], variable_value=vk[5][1], coordinate=vk[5][2],
                                       coord_value=vk[5][3])
        row7, const7 = self._make_row_(variable=vk[6][0], variable_value=vk[6][1], coordinate=vk[6][2],
                                       coord_value=vk[6][3])
        row8, const8 = self._make_row_(variable=vk[7][0], variable_value=vk[7][1], coordinate=vk[7][2],
                                       coord_value=vk[7][3])
        matrix = np.array([row1, row2, row3, row4, row5, row6, row7, row8])
        b = np.array([const1, const2, const3, const4, const5, const6, const7, const8])
        coeff_vector = np.linalg.solve(matrix, b)
        self.alpha1 = -1
        self.beta1 = coeff_vector[0]
        self.gamma1 = coeff_vector[1]
        self.alpha2 = coeff_vector[2]
        self.beta2 = coeff_vector[3]
        self.gamma2 = coeff_vector[4]
        self.alpha3 = coeff_vector[5]
        self.beta3 = coeff_vector[6]
        self.gamma3 = coeff_vector[7]
        return coeff_vector

    # following methods give the actual coordinates on canvas with a given function value
    def give_x1(self, u):
        value = (self.alpha1 * self.f1(u) + self.beta1 * self.g1(u) + self.gamma1 * self.h1(u)) / (
        self.alpha3 * self.f1(u) + self.beta3 * self.g1(u) + self.gamma3 * self.h1(u))
        return value[0]

    def give_y1(self, u):
        value = (self.alpha2 * self.f1(u) + self.beta2 * self.g1(u) + self.gamma2 * self.h1(u)) / (
        self.alpha3 * self.f1(u) + self.beta3 * self.g1(u) + self.gamma3 * self.h1(u))
        return value[0]

    def give_x2(self, v):
        value = (self.alpha1 * self.f2(v) + self.beta1 * self.g2(v) + self.gamma1 * self.h2(v)) / (
        self.alpha3 * self.f2(v) + self.beta3 * self.g2(v) + self.gamma3 * self.h2(v))
        return value[0]

    def give_y2(self, v):
        value = (self.alpha2 * self.f2(v) + self.beta2 * self.g2(v) + self.gamma2 * self.h2(v)) / (
        self.alpha3 * self.f2(v) + self.beta3 * self.g2(v) + self.gamma3 * self.h2(v))
        return value[0]

    def give_x3(self, w):
        value = (self.alpha1 * self.f3(w) + self.beta1 * self.g3(w) + self.gamma1 * self.h3(w)) / (
        self.alpha3 * self.f3(w) + self.beta3 * self.g3(w) + self.gamma3 * self.h3(w))
        return value[0]

    def give_y3(self, w):
        value = (self.alpha2 * self.f3(w) + self.beta2 * self.g3(w) + self.gamma2 * self.h3(w)) / (
        self.alpha3 * self.f3(w) + self.beta3 * self.g3(w) + self.gamma3 * self.h3(w))
        return value[0]

    def give_general_x_grid_fn(self, f, g, h):
        """
        gives transformed 2-dimensional (grid) x function
        f(u,v), g(u,v), h(u,v)
        """
        return lambda u, v: (self.alpha1 * f(u, v) + self.beta1[0] * g(u, v) + self.gamma1[0] * h(u, v)) / \
                            (self.alpha3[0] * f(u, v) + self.beta3[0] * g(u, v) + self.gamma3[0] * h(u, v))

    def give_general_y_grid_fn(self, f, g, h):
        """
        gives transformed 2-dimensional (grid) y function
        f(u,v), g(u,v), h(u,v)
        """
        return lambda u, v: (self.alpha2[0] * f(u, v) + self.beta2[0] * g(u, v) + self.gamma2[0] * h(u, v)) / \
                            (self.alpha3[0] * f(u, v) + self.beta3[0] * g(u, v) + self.gamma3[0] * h(u, v))


## Testing
if __name__ == '__main__':
    def main():
        def f1(u):
            return 2 * (u * u - 1)

        def g1(u):
            return 3 * u * (u + 1)

        def h1(u):
            return -u * (u - 1)

        def f2(v):
            return 2 * (2 * v + 1)

        def g2(v):
            return 3 * (v + 1)

        def h2(v):
            return -(v + 1) * (2 * v + 1)

        def f3(w):
            return w

        def g3(w):
            return 1

        def h3(w):
            return -w * w

        nomograph = Nomograph3(f1=f1, f2=f2, f3=f3, g1=g1, g2=g2, g3=g3, h1=h1, h2=h2, h3=h3)
        # aa,bb= nomograph._make_row_(variable='u',variable_value=0.5,coordinate='x',coord_value=-1)
        ##    print 'aa'+`aa`
        ##    print 'bb'+`bb`
        ##    cc=np.array([bb,bb,bb])
        ##    print 'cc'+`cc`
        ##    print 5*nomograph._make_transformation_matrix_()
        print(nomograph.give_x1(0.5))
        print(nomograph.give_x1(1.0))
        print(nomograph.give_y1(0.5))
        print(nomograph.give_y1(1.0))
        print(nomograph.give_x3(0.5))
        print(nomograph.give_x3(1.0))
        print(nomograph.give_y3(0.5))
        print(nomograph.give_y3(1.0))


    main()
