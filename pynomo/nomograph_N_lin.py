#    PyNomo - nomographs with Python
#    Copyright (C) 2007  Leif Roschier
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
from numpy import *
from pyx import *
from nomo_axis import *
from copy import *
from math import log


class Nomograph_N_lin:
    """
    Writes N parallel line nomographs
    """

    def __init__(self, functions, N, transform=True):
        self.functions = functions
        self.N = N
        # initial transformation = no transformation
        self.alpha1 = 1.0
        self.beta1 = 0.0
        self.gamma1 = 0.0
        self.alpha2 = 0.0
        self.beta2 = 1.0
        self.gamma2 = 0.0
        self.alpha3 = 0.0
        self.beta3 = 0.0
        self.gamma3 = 1.0
        try:
            {'4': self._make_4_,
             '5': self._make_5_}[`N`]()
        except KeyError:
            self._make_N_()
            # print "N=%i is not defined" % N
        self.R_padding = 0.3
        # self.x_multiplier=self.functions['nomo_width']/N
        # self.y_multiplier=self.functions['nomo_height']/(self._max_y_()-self._min_y_())/self.R_padding
        # self.Ry_min=self._min_y_()*self.R_padding*self.y_multiplier
        # self.Ry_max=self._max_y_()*self.R_padding*self.y_multiplier
        self.transform_bool = transform
        if transform == True:
            self._make_transformation_matrix_()
        self._find_reflection_axes_()

    def give_u_x(self, n):
        # n:th function
        # return lambda value:self.x_func[n](value)*self.x_multiplier
        return lambda value: ((self.alpha1 * self.x_func[n](value) + self.beta1 * self.y_func[n](value) + self.gamma1) \
                              / (self.alpha3 * self.x_func[n](value) + self.beta3 * self.y_func[n](
            value) + self.gamma3))  # [0]

    def give_u_y(self, n):
        # return lambda value:self.y_func[n](value)*self.y_multiplier
        return lambda value: ((self.alpha2 * self.x_func[n](value) + self.beta2 * self.y_func[n](value) + self.gamma2) \
                              / (self.alpha3 * self.x_func[n](value) + self.beta3 * self.y_func[n](
            value) + self.gamma3))  # [0]

    def give_R_x(self, n):
        # n:th function
        # return lambda value:self.xR_func[n](value)*self.x_multiplier
        return lambda value: ((self.alpha1 * self.xR_func[n](value) + self.beta1 * self.yR_func[n](value) + self.gamma1) \
                              / (self.alpha3 * self.xR_func[n](value) + self.beta3 * self.yR_func[n](
            value) + self.gamma3))  # [0]

    def give_R_y(self, n):
        # n:th function
        # return self._give_R_y_
        return lambda value: ((self.alpha2 * self.xR_func[n](value) + self.beta2 * self.yR_func[n](value) + self.gamma2) \
                              / (self.alpha3 * self.xR_func[n](value) + self.beta3 * self.yR_func[n](
            value) + self.gamma3))  # [0]

    def transform(self, x, y):
        xt = ((self.alpha1 * x + self.beta1 * y + self.gamma1) / (self.alpha3 * x + self.beta3 * y + self.gamma3))
        yt = ((self.alpha2 * x + self.beta2 * y + self.gamma2) / (self.alpha3 * x + self.beta3 * y + self.gamma3))
        return xt, yt

    def _make_4_(self):
        """ makes nomogram with 4 variables
        f1+f2+f3+f4=0
        Even when _make_N_ handles N=4 or N=5 these are left as an example
        what is happening
        """
        self.x_func = {}  # x coordinate to map points into canvas
        self.y_func = {}  # y coordinate to map points into canvas
        self.xR_func = {}  # turning-point axis
        self.yR_func = {}
        self.x_func[1] = lambda u1: 0
        self.x_func[2] = lambda u2: 1
        self.x_func[3] = lambda u3: 3
        self.x_func[4] = lambda u4: 4
        self.xR_func[1] = lambda uR1: 2
        self.y_func[1] = lambda u1: self.functions['f1'](u1)
        self.y_func[2] = lambda u2: -0.5 * self.functions['f2'](u2)
        self.y_func[3] = lambda u3: 0.5 * self.functions['f3'](u3)
        self.y_func[4] = lambda u4: -self.functions['f4'](u4)
        self.yR_func[1] = lambda uR1: uR1

    def _make_5_(self):
        """ makes nomogram with 5 variables
        f1+f2+f3+f4+f5=0
        Even when _make_N_ handles N=4 or N=5 these are left as an example
        what is happening
        """
        self.x_func = {}  # x coordinate to map points into canvas
        self.y_func = {}  # y coordinate to map points into canvas
        self.xR_func = {}  # turning-point axis
        self.yR_func = {}
        self.x_func[1] = lambda x1: 0
        self.x_func[2] = lambda x2: 1
        self.x_func[3] = lambda x3: 3
        self.x_func[4] = lambda x4: 5
        self.x_func[5] = lambda x5: 6
        self.xR_func[1] = lambda xR1: 2
        self.xR_func[2] = lambda xR2: 4
        self.y_func[1] = lambda u1: self.functions['f1'](u1)
        self.y_func[2] = lambda u2: -0.5 * self.functions['f2'](u2)
        self.y_func[3] = lambda u3: 0.5 * self.functions['f3'](u3)
        self.y_func[4] = lambda u4: -0.5 * self.functions['f4'](u4)
        self.y_func[5] = lambda u5: self.functions['f5'](u5)
        self.yR_func[1] = lambda yR1: yR1
        self.yR_func[2] = lambda yR2: yR2

    def _make_N_(self):
        """
        makes nomogram with N variables for Eq
        f1+f2+...+fN=0
        """
        N = self.N
        self.x_func = {}  # x coordinate to map points into canvas
        self.y_func = {}  # y coordinate to map points into canvas
        self.xR_func = {}  # turning-point axis
        self.yR_func = {}
        fn2x_table = {}  # mapping from function fn to x-coord
        r_table = {}
        x_max = (N - 4) + N  # how many x values are needed including turning axes
        fn2x_table[1] = 0.0
        fn2x_table[2] = 1.0
        fn2x_table[N] = x_max * 1.0
        fn2x_table[N - 1] = x_max - 1.0
        f_mid = range(3, (N - 1), 1)  # function numbers between reflection axes
        x_mid = [(f - 3) * 2.0 + 3.0 for f in f_mid]
        for idx, x in enumerate(x_mid):
            fn2x_table[f_mid[idx]] = x * 1.0
            r_table[idx + 1] = x - 1.0
        r_table[N - 3] = x_max - 2.0
        """
        fn2x_table: table of x-coordinates of functions
        r_table: table of x-coordinates of functions
        """
        # make fn functions
        for idx in range(2, N, 1):
            self.x_func[idx] = self._makeDoX_(fn2x_table[idx])
            self.y_func[idx] = self._makeDoY_(idx)
        self.x_func[1] = lambda x: fn2x_table[1] * 1.0
        self.x_func[N] = lambda x: fn2x_table[N] * 1.0
        self.y_func[1] = lambda u: self.functions['f1'](u)
        self.y_func[N] = lambda u: (-1) ** (N + 1) * self.functions['f%i' % N](u)
        # make reflection axes
        for idx in range(1, N - 2):
            self.xR_func[idx] = self._makeDoX_(r_table[idx])
            self.yR_func[idx] = lambda y: y

    def _makeDoX_(self, value):
        """
        copied trick to solve function defitions inside loop
        (I could not figure out how to use lambda...)
        """

        def f(dummy): return value

        return f

    def _makeDoY_(self, idx):
        """
        copied trick to solve function definitions inside loop
        (I could not figure out how to use lambda...)
        """

        def ff(u): return (-1) ** (idx + 1) * 0.5 * self.functions['f%i' % idx](u)

        return ff

    def _max_y_(self):
        """
        return maximum y value of all fn axes
        """
        Ns = range(self.N)
        max1 = max([self.y_func[n + 1](self.functions['u_max'][n]) for n in Ns])
        max2 = max([self.y_func[n + 1](self.functions['u_min'][n]) for n in Ns])
        return max(max1, max2)

    def _min_y_(self):
        """
        return minimum y value of all fn axes
        """
        Ns = range(self.N)
        min1 = min([self.y_func[n + 1](self.functions['u_max'][n]) for n in Ns])
        min2 = min([self.y_func[n + 1](self.functions['u_min'][n]) for n in Ns])
        return min(min1, min2)

    def _make_row_(self, coordinate='x', x=1.0, y=1.0, coord_value=1.0):
        """ Makes transformation matrix. See eq.37,a
        in Allcock. We take \alpha_1=1. h=1.
        """
        # to make expressions shorter
        cv = coord_value
        if coordinate == 'x':
            row = array([y, 1, 0, 0, 0, -cv * x, -cv * y, -cv * 1])
            value = array([x])
        if coordinate == 'y':
            row = array([0, 0, x, y, 1, -cv * x, -cv * y, -cv * 1])
            value = array([0])
        return row, value

    def _make_transformation_matrix_(self):
        """ Makes transformation from polygon (non-intersecting) to rectangle
            (x1,y1)     (x3,y3)          (x1t,y1t)      (x3t,y3t)       (0,height)    (width,height)
               |  polygon  |      ---->      |   rectangle  |       =
            (x2,y2)     (x4,y4)          (x2t,y2t)      (x4t,y4t)       (0,0)         (width,0)
        """
        x1, y1, x2, y2, x3, y3, x4, y4 = self._find_polygon_()
        self.polyg_x1 = x1
        self.polyg_y1 = y1
        self.polyg_x2 = x2
        self.polyg_y2 = y2
        self.polyg_x3 = x3
        self.polyg_y3 = y3
        self.polyg_x4 = x4
        self.polyg_y4 = y4
        max_x = self.x_func[self.N](self.functions['u_max'][self.N - 1])
        width = self.functions['nomo_width']
        height = self.functions['nomo_height']  # /self.R_padding
        row1, const1 = self._make_row_(coordinate='x', coord_value=x2 / max_x * width, x=x2, y=y2)
        row2, const2 = self._make_row_(coordinate='y', coord_value=0.0, x=x2, y=y2)
        row3, const3 = self._make_row_(coordinate='x', coord_value=x1 / max_x * width, x=x1, y=y1)
        row4, const4 = self._make_row_(coordinate='y', coord_value=height, x=x1, y=y1)
        row5, const5 = self._make_row_(coordinate='x', coord_value=x4 / max_x * width, x=x4, y=y4)
        row6, const6 = self._make_row_(coordinate='y', coord_value=0.0, x=x4, y=y4)
        row7, const7 = self._make_row_(coordinate='x', coord_value=x3 / max_x * width, x=x3, y=y3)
        row8, const8 = self._make_row_(coordinate='y', coord_value=height, x=x3, y=y3)

        matrix = array([row1, row2, row3, row4, row5, row6, row7, row8])
        b = array([const1, const2, const3, const4, const5, const6, const7, const8])
        coeff_vector = linalg.solve(matrix, b)
        self.alpha1 = -1.0
        self.beta1 = coeff_vector[0][0]
        self.gamma1 = coeff_vector[1][0]
        self.alpha2 = coeff_vector[2][0]
        self.beta2 = coeff_vector[3][0]
        self.gamma2 = coeff_vector[4][0]
        self.alpha3 = coeff_vector[5][0]
        self.beta3 = coeff_vector[6][0]
        self.gamma3 = coeff_vector[7][0]
        return coeff_vector

    def _find_polygon_(self):
        """
        finds limiting polygon for transformation
        """
        # let's find max and min y values
        list1 = [self.y_func[n + 1](self.functions['u_min'][n]) for n in range(self.N)]
        list2 = [self.y_func[n + 1](self.functions['u_max'][n]) for n in range(self.N)]
        min_val, min_idx = list1[0], 1
        max_val, max_idx = list1[0], 1
        for idx, value in enumerate(list1[1:]):
            if value < min_val:
                min_val, min_idx = value, idx + 2  # enumerate starts from idx=1
            if value > max_val:
                max_val, max_idx = value, idx + 2  # enumerate starts from idx=1
        for idx, value in enumerate(list2[0:]):
            if value < min_val:
                min_val, min_idx = value, idx + 1  # enumerate starts from idx=0
            if value > max_val:
                max_val, max_idx = value, idx + 1  # enumerate starts from idx=0
        x_min = self.x_func[min_idx](self.functions['u_min'][min_idx - 1])
        y_min = min_val
        x_max = self.x_func[max_idx](self.functions['u_min'][max_idx - 1])
        y_max = max_val
        # let's find min slopes for lower part
        list1_slope = [self._calc_slope_(n + 1, self.functions['u_min'][n], x_min, y_min) for n in range(self.N)]
        list2_slope = [self._calc_slope_(n + 1, self.functions['u_max'][n], x_min, y_min) for n in range(self.N)]
        min_slope_lower, min_slope_lower_idx = list1_slope[0], 1
        for idx, value in enumerate(list1_slope[1:]):
            if value < min_slope_lower:
                min_slope_lower, min_slope_lower_idx = value, idx + 2  # enumerate starts from idx=1
        for idx, value in enumerate(list2_slope[0:]):
            if value < min_slope_lower:
                min_slope_lower, min_slope_lower_idx = value, idx + 1  # enumerate starts from idx=0
        # print "min slope below between %i and %i" % (min_idx,min_slope_lower_idx)
        # let's find min slopes for upper part
        list1_slope = [self._calc_slope_(n + 1, self.functions['u_min'][n], x_max, y_max) for n in range(self.N)]
        list2_slope = [self._calc_slope_(n + 1, self.functions['u_max'][n], x_max, y_max) for n in range(self.N)]
        min_slope_upper, min_slope_upper_idx = list1_slope[0], 1
        for idx, value in enumerate(list1_slope[1:]):
            if value < min_slope_upper:
                min_slope_upper, min_slope_upper_idx = value, idx + 2  # enumerate starts from idx=1
        for idx, value in enumerate(list2_slope[0:]):
            if value < min_slope_upper:
                min_slope_upper, min_slope_upper_idx = value, idx + 1  # enumerate starts from idx=0
        # print "min slope upper between %i and %i" % (max_idx,min_slope_upper_idx)
        """ returns polygon (to be transformed)
            (x1,y1)     (x3,y3)
               |  polygon  |
            (x2,y2)     (x4,y4)
        """
        x1 = x_max
        y1 = y_max
        x2 = x_min
        y2 = y_min
        x3 = self.x_func[min_slope_upper_idx](self.functions['u_min'][min_slope_upper_idx - 1])
        y3 = max(self.y_func[min_slope_upper_idx](self.functions['u_min'][min_slope_upper_idx - 1]),
                 self.y_func[min_slope_upper_idx](self.functions['u_max'][min_slope_upper_idx - 1]))
        x4 = self.x_func[min_slope_lower_idx](self.functions['u_min'][min_slope_lower_idx - 1])
        y4 = min(self.y_func[min_slope_lower_idx](self.functions['u_min'][min_slope_lower_idx - 1]),
                 self.y_func[min_slope_lower_idx](self.functions['u_max'][min_slope_lower_idx - 1]))
        if (x1 - x3) * (x2 - x4) < 0:
            x1, y1, x3, y3 = x3, y3, x1, y1
        if x3 < x1:
            x1, y1, x2, y2, x3, y3, x4, y4 = x3, y3, x4, y4, x1, y1, x2, y2
        return x1 * 1.0, y1 * 1.0, x2 * 1.0, y2 * 1.0, x3 * 1.0, y3 * 1.0, x4 * 1.0, y4 * 1.0

    def _calc_slope_(self, index, value, x_ref, y_ref):
        """
        calculates absolute value of slope between axis(index(value1)) and axis(index2(value2))
        slope = dy/dx
        """
        x1 = x_ref
        x2 = self.x_func[index](value)
        y1 = y_ref
        y2 = self.y_func[index](value)
        dx = abs(x2 - x1)
        dy = abs(y1 - y2)
        if dx > 0:
            return dy / dx
        else:
            return 1e12  # = big number

    def _line_points_(self, x1, y1, x2, y2, c):
        """
        makes line between given points to canvas c
        """
        steps = 100.0
        step_x = (x2 - x1) / steps
        step_y = (y2 - y1) / steps
        xt, yt = self.transform(x1, y1)
        line = path.path(path.moveto(xt, yt))
        x = x1
        y = y1
        step = 1
        while True:
            x = x + step_x
            y = y + step_y
            xt, yt = nomo.transform(x, y)
            line.append(path.lineto(xt, yt))
            step += 1
            if step > steps:
                break
        c.stroke(line, [style.linewidth.normal])

    def _give_y_coord_(self, x1, y1, x2, y2, x):
        """
        gives y coordinate of point (x,y) at line passing through points (x1,y1) and (x2,y2)
        for given x
        """
        return (y1 - y2) / (x1 - x2) * (x - x1) + y1

    def _find_reflection_axes_(self):
        """
        finds limits of reflection axes (for drawing)
        """
        self.y_R_top = {}
        self.y_R_bottom = {}
        if self.transform_bool:
            for idx in [idx + 1 for idx in range(self.N - 3)]:
                y_top = self._give_y_coord_(self.polyg_x1, self.polyg_y1,
                                            self.polyg_x3, self.polyg_y3, self.xR_func[idx](0))
                y_bottom = self._give_y_coord_(self.polyg_x2, self.polyg_y2,
                                               self.polyg_x4, self.polyg_y4, self.xR_func[idx](0))
                self.y_R_top[idx] = y_top + (y_top - y_bottom) * self.R_padding
                self.y_R_bottom[idx] = y_bottom - (y_top - y_bottom) * self.R_padding
        else:
            for idx in [idx + 1 for idx in range(self.N - 3)]:
                (self._max_y_() - self._min_y_()) * self.R_padding
                self.y_R_top[idx] = self._max_y_() + (self._max_y_() - self._min_y_()) * self.R_padding
                self.y_R_bottom[idx] = self._min_y_() - (self._max_y_() - self._min_y_()) * self.R_padding


if __name__ == '__main__':
    # example 0
    # f1+f2+f3+f4+f5+f6=0
    functions = {'u_min': array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                 'u_max': array([10.0, 10.0, 10.0, 10.0, 10.0, 10.0]),
                 'f1': lambda u1: u1,
                 'f2': lambda u2: u2,
                 'f3': lambda u3: u3,
                 'f4': lambda u4: u4,
                 'f5': lambda u5: u5,
                 'f6': lambda u6: -u6,
                 'nomo_width': 30.0,
                 'nomo_height': 18.0}
    nomo6 = Nomograph_N_lin(functions, 6, transform=True)
    c = canvas.canvas()
    """
    print "give_u_x(1)=%f"%nomo6.give_u_x(1)(0.0)
    print "x_func[1](1)=%f"%nomo6.x_func[1](0.0)
    print "give_u_x(2)=%f"%nomo6.give_u_x(2)(0.0)
    print "x_func[2](1)=%f"%nomo6.x_func[2](0.0)
    print "give_u_x(3)=%f"%nomo6.give_u_x(3)(0.0)
    print "x_func[3](1)=%f"%nomo6.x_func[3](1.0)
    print "give_u_x(4)=%f"%nomo6.give_u_x(4)(1.0)
    print "x_func[4](1)=%f"%nomo6.x_func[4](1.0)
    print "give_u_x(5)=%f"%nomo6.give_u_x(5)(1.0)
    print "x_func[5](1)=%f"%nomo6.x_func[5](1.0)
    print "give_u_x(6)=%f"%nomo6.give_u_x(6)(1.0)
    print nomo6.x_func[6](1)
    """
    ax1 = Nomo_Axis(func_f=nomo6.give_u_x(1), func_g=nomo6.give_u_y(1),
                    start=functions['u_min'][0], stop=functions['u_max'][0],
                    turn=1, title='f1', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax2 = Nomo_Axis(func_f=nomo6.give_u_x(2), func_g=nomo6.give_u_y(2),
                    start=functions['u_min'][1], stop=functions['u_max'][1],
                    turn=-1, title='f2', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax3 = Nomo_Axis(func_f=nomo6.give_u_x(3), func_g=nomo6.give_u_y(3),
                    start=functions['u_min'][2], stop=functions['u_max'][2],
                    turn=-1, title='f3', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax4 = Nomo_Axis(func_f=nomo6.give_u_x(4), func_g=nomo6.give_u_y(4),
                    start=functions['u_min'][3], stop=functions['u_max'][3],
                    turn=1, title='f4', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax5 = Nomo_Axis(func_f=nomo6.give_u_x(5), func_g=nomo6.give_u_y(5),
                    start=functions['u_min'][4], stop=functions['u_max'][4],
                    turn=1, title='f5', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax6 = Nomo_Axis(func_f=nomo6.give_u_x(6), func_g=nomo6.give_u_y(6),
                    start=functions['u_min'][5], stop=functions['u_max'][5],
                    turn=1, title='f6', canvas=c, type='linear',
                    tick_levels=3, tick_text_levels=2)

    R1 = Nomo_Axis(func_f=nomo6.give_R_x(1), func_g=nomo6.give_R_y(1),
                   start=nomo6.y_R_bottom[1], stop=nomo6.y_R_top[1],
                   turn=-1, title='R1', canvas=c, type='linear',
                   tick_levels=0, tick_text_levels=0)
    R2 = Nomo_Axis(func_f=nomo6.give_R_x(2), func_g=nomo6.give_R_y(2),
                   start=nomo6.y_R_bottom[2], stop=nomo6.y_R_top[2],
                   turn=-1, title='R2', canvas=c, type='linear',
                   tick_levels=0, tick_text_levels=0)
    R3 = Nomo_Axis(func_f=nomo6.give_R_x(3), func_g=nomo6.give_R_y(3),
                   start=nomo6.y_R_bottom[3], stop=nomo6.y_R_top[3],
                   turn=-1, title='R3', canvas=c, type='linear',
                   tick_levels=0, tick_text_levels=0)
    c.writePDFfile("nomolin6")



    # example 1
    # f1+f2+f3=f4
    functions = {'u_min': array([0.0, 0.0, 0.0, 0.0]),
                 'u_max': array([10.0, 10.0, 10.0, 10.0]),
                 'f1': lambda u1: u1,
                 'f2': lambda u2: u2,
                 'f3': lambda u3: u3,
                 'f4': lambda u4: -u4,
                 'nomo_width': 20.0,
                 'nomo_height': 14.0}
    nomo = Nomograph_N_lin(functions, 4, transform=True)
    c = canvas.canvas()
    ax1 = Nomo_Axis(func_f=nomo.give_u_x(1), func_g=nomo.give_u_y(1),
                    start=functions['u_min'][0], stop=functions['u_max'][0],
                    turn=1, title='f1', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax2 = Nomo_Axis(func_f=nomo.give_u_x(2), func_g=nomo.give_u_y(2),
                    start=functions['u_min'][1], stop=functions['u_max'][1],
                    turn=-1, title='f2', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax3 = Nomo_Axis(func_f=nomo.give_u_x(3), func_g=nomo.give_u_y(3),
                    start=functions['u_min'][2], stop=functions['u_max'][2],
                    turn=-1, title='f3', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax4 = Nomo_Axis(func_f=nomo.give_u_x(4), func_g=nomo.give_u_y(4),
                    start=functions['u_min'][3], stop=functions['u_max'][3],
                    turn=-1, title='f4', canvas=c, type='linear',
                    tick_levels=3, tick_text_levels=2)
    R = Nomo_Axis(func_f=nomo.give_R_x(1), func_g=nomo.give_R_y(1),
                  start=nomo.y_R_bottom[1], stop=nomo.y_R_top[1],
                  turn=-1, title='R', canvas=c, type='linear',
                  tick_levels=0, tick_text_levels=0)
    c.writePDFfile("nomolin")

    # example 2
    # f1+f2+f3+f4=f5
    functions = {'u_min': array([0.0, 0.0, 0.0, 0.0, 0.0]),
                 'u_max': array([10.0, 10.0, 10.0, 10.0, 10.0]),
                 'f1': lambda u1: u1,
                 'f2': lambda u2: u2,
                 'f3': lambda u3: u3,
                 'f4': lambda u4: u4,
                 'f5': lambda u5: -u5,
                 'nomo_width': 20.0,
                 'nomo_height': 18.0}
    nomo = Nomograph_N_lin(functions, 5, transform=True)
    c = canvas.canvas()
    ax1 = Nomo_Axis(func_f=nomo.give_u_x(1), func_g=nomo.give_u_y(1),
                    start=functions['u_min'][0], stop=functions['u_max'][0],
                    turn=1, title='f1', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax2 = Nomo_Axis(func_f=nomo.give_u_x(2), func_g=nomo.give_u_y(2),
                    start=functions['u_min'][1], stop=functions['u_max'][1],
                    turn=-1, title='f2', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax3 = Nomo_Axis(func_f=nomo.give_u_x(3), func_g=nomo.give_u_y(3),
                    start=functions['u_min'][2], stop=functions['u_max'][2],
                    turn=-1, title='f3', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax4 = Nomo_Axis(func_f=nomo.give_u_x(4), func_g=nomo.give_u_y(4),
                    start=functions['u_min'][3], stop=functions['u_max'][3],
                    turn=1, title='f4', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax5 = Nomo_Axis(func_f=nomo.give_u_x(5), func_g=nomo.give_u_y(5),
                    start=functions['u_min'][4], stop=functions['u_max'][4],
                    turn=1, title='f5', canvas=c, type='linear',
                    tick_levels=3, tick_text_levels=2)

    R1 = Nomo_Axis(func_f=nomo.give_R_x(1), func_g=nomo.give_R_y(1),
                   start=nomo.y_R_bottom[1], stop=nomo.y_R_top[1],
                   turn=-1, title='R1', canvas=c, type='linear',
                   tick_levels=0, tick_text_levels=0)
    R2 = Nomo_Axis(func_f=nomo.give_R_x(2), func_g=nomo.give_R_y(2),
                   start=nomo.y_R_bottom[2], stop=nomo.y_R_top[2],
                   turn=-1, title='R2', canvas=c, type='linear',
                   tick_levels=0, tick_text_levels=0)

    nomo._line_points_(0.0, 1.0, 1.0, -0.5, c)
    nomo._line_points_(1.0, -0.5, 2.0, -2.0, c)
    nomo._line_points_(2.0, -2.0, 3.0, 0.5, c)
    nomo._line_points_(3.0, 0.5, 4.0, 3.0, c)
    nomo._line_points_(4.0, 3.0, 5.0, -0.5, c)
    nomo._line_points_(5.0, -0.5, 6.0, -4.0, c)

    c.writePDFfile("nomolin2")


    # example 4
    # f1+f2+f3+f4+f5+f6=0
    functions = {'u_min': array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                 'u_max': array([10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]),
                 'f1': lambda u1: u1,
                 'f2': lambda u2: u2,
                 'f3': lambda u3: u3,
                 'f4': lambda u4: u4,
                 'f5': lambda u5: u5,
                 'f6': lambda u6: u6,
                 'f7': lambda u7: u7,
                 'f8': lambda u8: u8,
                 'f9': lambda u9: u9,
                 'f10': lambda u10: u10,
                 'f11': lambda u11: -u11,
                 'nomo_width': 60.0,
                 'nomo_height': 18.0}
    nomo11 = Nomograph_N_lin(functions, 11, transform=True)
    c = canvas.canvas()
    ax1 = Nomo_Axis(func_f=nomo11.give_u_x(1), func_g=nomo11.give_u_y(1),
                    start=functions['u_min'][0], stop=functions['u_max'][0],
                    turn=1, title='f1', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax2 = Nomo_Axis(func_f=nomo11.give_u_x(2), func_g=nomo11.give_u_y(2),
                    start=functions['u_min'][1], stop=functions['u_max'][1],
                    turn=-1, title='f2', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax3 = Nomo_Axis(func_f=nomo11.give_u_x(3), func_g=nomo11.give_u_y(3),
                    start=functions['u_min'][2], stop=functions['u_max'][2],
                    turn=-1, title='f3', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax4 = Nomo_Axis(func_f=nomo11.give_u_x(4), func_g=nomo11.give_u_y(4),
                    start=functions['u_min'][3], stop=functions['u_max'][3],
                    turn=1, title='f4', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax5 = Nomo_Axis(func_f=nomo11.give_u_x(5), func_g=nomo11.give_u_y(5),
                    start=functions['u_min'][4], stop=functions['u_max'][4],
                    turn=1, title='f5', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax6 = Nomo_Axis(func_f=nomo11.give_u_x(6), func_g=nomo11.give_u_y(6),
                    start=functions['u_min'][5], stop=functions['u_max'][5],
                    turn=1, title='f6', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax7 = Nomo_Axis(func_f=nomo11.give_u_x(7), func_g=nomo11.give_u_y(7),
                    start=functions['u_min'][6], stop=functions['u_max'][6],
                    turn=-1, title='f7', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax8 = Nomo_Axis(func_f=nomo11.give_u_x(8), func_g=nomo11.give_u_y(8),
                    start=functions['u_min'][7], stop=functions['u_max'][7],
                    turn=-1, title='f8', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax9 = Nomo_Axis(func_f=nomo11.give_u_x(9), func_g=nomo11.give_u_y(9),
                    start=functions['u_min'][8], stop=functions['u_max'][8],
                    turn=1, title='f9', canvas=c, type='linear',
                    tick_levels=2, tick_text_levels=1)
    ax10 = Nomo_Axis(func_f=nomo11.give_u_x(10), func_g=nomo11.give_u_y(10),
                     start=functions['u_min'][9], stop=functions['u_max'][9],
                     turn=1, title='f10', canvas=c, type='linear',
                     tick_levels=2, tick_text_levels=1)
    ax11 = Nomo_Axis(func_f=nomo11.give_u_x(11), func_g=nomo11.give_u_y(11),
                     start=functions['u_min'][10], stop=functions['u_max'][10],
                     turn=1, title='f11', canvas=c, type='linear',
                     tick_levels=3, tick_text_levels=2)

    R1 = Nomo_Axis(func_f=nomo11.give_R_x(1), func_g=nomo11.give_R_y(1),
                   start=nomo11.y_R_bottom[1], stop=nomo11.y_R_top[1],
                   turn=-1, title='R1', canvas=c, type='linear',
                   tick_levels=0, tick_text_levels=0)
    R2 = Nomo_Axis(func_f=nomo11.give_R_x(2), func_g=nomo11.give_R_y(2),
                   start=nomo11.y_R_bottom[2], stop=nomo11.y_R_top[2],
                   turn=-1, title='R2', canvas=c, type='linear',
                   tick_levels=0, tick_text_levels=0)
    R3 = Nomo_Axis(func_f=nomo11.give_R_x(3), func_g=nomo11.give_R_y(3),
                   start=nomo11.y_R_bottom[3], stop=nomo11.y_R_top[3],
                   turn=-1, title='R3', canvas=c, type='linear',
                   tick_levels=0, tick_text_levels=0)
    R4 = Nomo_Axis(func_f=nomo11.give_R_x(4), func_g=nomo11.give_R_y(4),
                   start=nomo11.y_R_bottom[4], stop=nomo11.y_R_top[4],
                   turn=-1, title='R4', canvas=c, type='linear',
                   tick_levels=0, tick_text_levels=0)
    R5 = Nomo_Axis(func_f=nomo11.give_R_x(5), func_g=nomo11.give_R_y(5),
                   start=nomo11.y_R_bottom[5], stop=nomo11.y_R_top[5],
                   turn=-1, title='R5', canvas=c, type='linear',
                   tick_levels=0, tick_text_levels=0)
    R6 = Nomo_Axis(func_f=nomo11.give_R_x(6), func_g=nomo11.give_R_y(6),
                   start=nomo11.y_R_bottom[6], stop=nomo11.y_R_top[6],
                   turn=-1, title='R6', canvas=c, type='linear',
                   tick_levels=0, tick_text_levels=0)
    R7 = Nomo_Axis(func_f=nomo11.give_R_x(7), func_g=nomo11.give_R_y(7),
                   start=nomo11.y_R_bottom[7], stop=nomo11.y_R_top[7],
                   turn=-1, title='R6', canvas=c, type='linear',
                   tick_levels=0, tick_text_levels=0)
    R8 = Nomo_Axis(func_f=nomo11.give_R_x(8), func_g=nomo11.give_R_y(8),
                   start=nomo11.y_R_bottom[8], stop=nomo11.y_R_top[8],
                   turn=-1, title='R6', canvas=c, type='linear',
                   tick_levels=0, tick_text_levels=0)
    c.writePDFfile("nomolin11")

    # example 5
    # equivalent light nomogram in photography
    # log2(ISO/100)+log2(f**2)-log2(t)=EV
    functions = {'u_min': array([50.0, 1.0, 0.0, 1.0]),
                 'u_max': array([3200.0, 4000.0, 18.0, 64.0]),
                 'f1': lambda ISO: -log(ISO / 100.0, 2.0),
                 'f4': lambda f: log(f ** 2.0, 2.0),
                 'f2': lambda t: log(t, 2.0),
                 'f3': lambda EV: -EV,
                 'nomo_width': 20.0,
                 'nomo_height': 14.0}
    nomo = Nomograph_N_lin(functions, 4, transform=True)
    c = canvas.canvas()
    ax1 = Nomo_Axis(func_f=nomo.give_u_x(2), func_g=nomo.give_u_y(2),
                    start=functions['u_min'][1], stop=functions['u_max'][1],
                    turn=1, title='1/t', canvas=c, type='log',
                    tick_levels=3, tick_text_levels=3)
    manual_axis_ISO = {50: 'ISO 50',
                       100: 'ISO 100',
                       200: 'ISO 200',
                       400: r'ISO 400',
                       800: 'ISO 800',
                       1600: 'ISO 1600',
                       3200: 'ISO 3200'}

    ax2 = Nomo_Axis(func_f=nomo.give_u_x(1), func_g=nomo.give_u_y(1),
                    start=functions['u_min'][0], stop=functions['u_max'][0],
                    turn=-1, title='Film speed', canvas=c, type='manual point',
                    tick_levels=3, tick_text_levels=1,
                    manual_axis_data=manual_axis_ISO, side='right')

    manual_axis_f = {1.0: r'$f$/1.0',
                     1.4: r'$f$/1.4',
                     2.0: r'$f$/2.0',
                     2.8: r'$f$/2.8',
                     4.0: r'$f$/4.0',
                     5.6: r'$f$/5.6',
                     8.0: r'$f$/8.0',
                     11.0: r'$f$/11',
                     16.0: r'$f$/16',
                     22.0: r'$f$/22',
                     32.0: r'$f$/32',
                     45.0: r'$f$/45',
                     64.0: r'$f$/64'}

    ax3 = Nomo_Axis(func_f=nomo.give_u_x(4), func_g=nomo.give_u_y(4),
                    start=functions['u_min'][3], stop=functions['u_max'][3],
                    turn=-1, title=r'Aperture', canvas=c, type='manual point',
                    tick_levels=3, tick_text_levels=1,
                    manual_axis_data=manual_axis_f, side='left')

    light_value_data = {0.0: '0',
                        1.0: '1',
                        2.0: '2',
                        3.0: '3',
                        4.0: '4',
                        5.0: '5',
                        6.0: '6',
                        7.0: '7',
                        8.0: '8',
                        9.0: '9',
                        10.0: '10',
                        11.0: '11',
                        12.0: '12',
                        13.0: '13',
                        14.0: '14',
                        15.0: '15',
                        16.0: '16',
                        17.0: '17',
                        18.0: '18'}
    ax4 = Nomo_Axis(func_f=nomo.give_u_x(3), func_g=nomo.give_u_y(3),
                    start=functions['u_min'][2], stop=functions['u_max'][2],
                    turn=-1, title=r'Light value (EV$_{100}$)', canvas=c, type='manual line',
                    tick_levels=3, tick_text_levels=3,
                    manual_axis_data=light_value_data, side='right')
    R = Nomo_Axis(func_f=nomo.give_R_x(1), func_g=nomo.give_R_y(1),
                  start=nomo.y_R_bottom[1], stop=nomo.y_R_top[1],
                  turn=-1, title='R', canvas=c, type='linear',
                  tick_levels=0, tick_text_levels=0)
    c.writePDFfile("equivalent_light")
