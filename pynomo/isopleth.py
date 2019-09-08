# -*- encoding: utf-8 -*-
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
import copy, re
from scipy.optimize import *
from scipy import arange
import warnings


class Isopleth_Wrapper(object):
    """
    class to hold all isopleths and control everything related to them
    """

    def __init__(self, params):
        self.isopleth_list = []  # list of isopleth objects
        self.solutions = []  # list of dictionaries (solutions)
        self.ref_tag_number = 1  # to separate type 3 ref scales
        self.nomographer_params = params['isopleth_params']  # main params

    def add_isopleth_block(self, block, block_para):
        """
        Add block of type derived from Isopleth_Block
        """
        # type 1
        if block_para['block_type'] == 'type_1':
            iso_block = Isopleth_Block_Type_1(block.atom_stack, block_para)
            self.isopleth_list.append(iso_block)
        # type 2
        if block_para['block_type'] == 'type_2':
            iso_block = Isopleth_Block_Type_2(block.atom_stack, block_para)
            self.isopleth_list.append(iso_block)
        # type 7
        if block_para['block_type'] == 'type_7':
            iso_block = Isopleth_Block_Type_7(block.atom_stack, block_para)
            self.isopleth_list.append(iso_block)
        # type 8
        if block_para['block_type'] == 'type_8':
            iso_block = Isopleth_Block_Type_8(block.atom_stack, block_para)
            self.isopleth_list.append(iso_block)
        # type 9
        if block_para['block_type'] == 'type_9':
            iso_block = Isopleth_Block_Type_9(block.atom_stack, block_para)
            self.isopleth_list.append(iso_block)
        # type 10
        if block_para['block_type'] == 'type_10':
            iso_block = Isopleth_Block_Type_10(block.atom_stack, block_para)
            self.isopleth_list.append(iso_block)
        # type 6
        if block_para['block_type'] == 'type_6':
            iso_block = Isopleth_Block_Type_6(block.atom_stack, block_para)
            self.isopleth_list.append(iso_block)
        # type 3
        if block_para['block_type'] == 'type_3':
            # handle type 3 as multiple type 1
            N = block.N
            ref_N = N - 3
            ref_atoms = block.atom_stack[N:(N + ref_N)]
            # set ref axes
            for idx, ref_atom in enumerate(ref_atoms):
                ref_atom.params['tag'] = 'ref' + repr(idx) + repr(self.ref_tag_number)
            self.ref_tag_number += 1
            atoms = block.atom_stack[:N]
            atom_stack_start = [atoms[0], atoms[1], ref_atoms[0]]
            atom_stack_stop = [ref_atoms[-1], atoms[-2], atoms[-1]]
            center_atom_stack = []
            for idx in range(2, N - 2):
                center_atom_stack.append([ref_atoms[idx - 2], atoms[idx], ref_atoms[idx - 1]])
            # make block params
            # start
            block_para_start = copy.deepcopy(block_para)
            block_para_start['isopleth_values'] = []
            for idx, isopleth_values in enumerate(block_para['isopleth_values']):
                block_para_start['isopleth_values'].append([block_para['isopleth_values'][idx][0],
                                                            block_para['isopleth_values'][idx][1], 'x'])
            # stop
            block_para_stop = copy.deepcopy(block_para)
            block_para_stop['isopleth_values'] = []
            for idx, isopleth_values in enumerate(block_para['isopleth_values']):
                block_para_stop['isopleth_values'].append(['x', block_para['isopleth_values'][idx][-2],
                                                           block_para['isopleth_values'][idx][-1]])
            # middle
            block_para_middles = []
            for idx in range(3, N - 1):
                block_para_middles.append(copy.deepcopy(block_para))
                block_para_middles[-1]['isopleth_values'] = []
                for idx1, isopleth_values in enumerate(block_para['isopleth_values']):
                    block_para_middles[-1]['isopleth_values'].append(
                        ['x', block_para['isopleth_values'][idx1][idx - 1], 'x'])
            # do the list
            self.isopleth_list.append(Isopleth_Block_Type_1(atom_stack_start, block_para_start))
            for idx, atom_stack in enumerate(center_atom_stack):
                self.isopleth_list.append(Isopleth_Block_Type_1(atom_stack, block_para_middles[idx]))
            self.isopleth_list.append(Isopleth_Block_Type_1(atom_stack_stop, block_para_stop))

        # type 4
        if block_para['block_type'] == 'type_4':
            atoms = block.atom_stack
            atom_stack_12 = [atoms[0], atoms[1], atoms[4]]  # 4 = ref line
            atom_stack_34 = [atoms[2], atoms[3], atoms[4]]
            # tag the reference line
            atoms[4].params['tag'] = 'ref_type4' + repr(self.ref_tag_number)
            self.ref_tag_number += 1
            # make blocks
            block_para_12 = copy.deepcopy(block_para)
            block_para_12['isopleth_values'] = []
            for idx, isopleth_values in enumerate(block_para['isopleth_values']):
                block_para_12['isopleth_values'].append([block_para['isopleth_values'][idx][0],
                                                         block_para['isopleth_values'][idx][1], 'x'])
            block_para_34 = copy.deepcopy(block_para)
            block_para_34['isopleth_values'] = []
            for idx, isopleth_values in enumerate(block_para['isopleth_values']):
                block_para_34['isopleth_values'].append([block_para['isopleth_values'][idx][2],
                                                         block_para['isopleth_values'][idx][3], 'x'])
            self.isopleth_list.append(Isopleth_Block_Type_1(atom_stack_12, block_para_12))
            self.isopleth_list.append(Isopleth_Block_Type_1(atom_stack_34, block_para_34))

        # type 5 (contour)
        if block_para['block_type'] == 'type_5':
            iso_block = Isopleth_Block_Type_5(block.atom_stack, block_para, block)
            self.isopleth_list.append(iso_block)

    def draw(self, canvas):
        """
        solves isopleths and draws them
        """
        for isopleth in self.isopleth_list:
            isopleth.calc_atoms()
        self._solve_()
        for idx, isopleth in enumerate(self.isopleth_list):
            p = self.nomographer_params
            isopleth.draw(canvas, p)

    def _solve_(self):
        """
        solves unknown values
        """
        solutions_updated = True
        while solutions_updated:
            for idx, isopleth in enumerate(self.isopleth_list):
                isopleth.solve(self.solutions)
                # take initial values (they are most correct)
                isopleth.find_initial_solutions(self.solutions)
            # updates solutions
            solutions_updated = False
            for idx, isopleth in enumerate(self.isopleth_list):
                update = isopleth.update_solutions(self.solutions)
                if update:
                    solutions_updated = True
        # check for error
        for idx, isopleth in enumerate(self.isopleth_list):
            isopleth.check_if_all_solutions_found(self.solutions)


class Isopleth_Block(object):
    """
    parent class for isopleth generation for blocks.
    Isopleths should be instanced once Atoms have final transformations
    """

    def __init__(self, atom_stack, params):
        """
        params is for example:
        {
        'isopleth_values':[['x',0.1,0.2]],
        }
        if x is found outside this implementation, 'x' is replaced
        by tuple (x,y) of the coordinate pair
        """
        self.params = params
        # self.block=block
        self.isopleth_values = params['isopleth_values']
        self.atom_stack = atom_stack
        self.draw_coordinates = []  # coordinates [[x1,y1,x2,y2,x3,y3],...] to be drawn
        self.other_points = []  # list of list of additional solution coordinates

    def calc_atoms(self):
        """
        calculates coordinates for atoms
        """
        for atom in self.atom_stack:
            # calculates lines (list of coordinates)
            atom.calc_line_and_sections()

        #    def _replace_found_values_(self,found_dict={}):
        #        """
        #        replaces found variables with the coordinates
        #        found_dict is of form (for example)
        #        {
        #        'x1':(1.0,2.0),
        #        'y2':(3.4,2.1)
        #        }
        #        """
        #        for key in found_dict.keys():
        #            if self.params['points'].count(key)>0:
        #                idx=self.params['points'].index(key)
        #                self.params['points'][idx]=found_dict[key]

    @staticmethod
    def _calc_distance_(x0, y0, x1, y1, x2, y2):
        """
        Calculates distance of point (x0,y0) from line passing
        through points (x1,y1), (x2,y2)
        """
        return abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1)) / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def _calc_distance_points_(x1, y1, x2, y2):
        """
        calcs distance between two points
        """
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def _find_closest_point_old_(self, line, x1, y1, x2, y2):
        """
        finds closest point(S) of isopleth and axis (scale)
        """
        x = line[0][0]
        y = line[0][1]
        distances = []
        smallest_distance = self._calc_distance_(x, y, x1, y1, x2, y2)
        distances.append(smallest_distance)
        smallest_idx = 0
        for idx, (x, y) in enumerate(line):
            distance = self._calc_distance_(x, y, x1, y1, x2, y2)
            distances.append(distance)
            if distance < smallest_distance:
                smallest_distance = distance
                smallest_idx = idx
        if smallest_idx == 0:
            idx2 = 1
        if smallest_idx == len(line):
            idx2 = len(line) - 1
        if 0 < smallest_idx < len(line):
            if distances[smallest_idx - 1] < distances[smallest_idx + 1]:
                idx2 = smallest_idx - 1
            else:
                idx2 = smallest_idx + 1

            #        sum_distance=distances[smallest_idx]+distances[idx2]
            #        middle_x=distances[smallest_idx]/sum_distance*line[smallest_idx][0]+\
            #                 distances[idx2]/sum_distance*line[idx2][0]
            #        middle_y=distances[smallest_idx]/sum_distance*line[smallest_idx][1]+\
            #                 distances[idx2]/sum_distance*line[idx2][1]
        # a better
        middle_x, middle_y = self._two_line_intersection_(line[smallest_idx][0], line[smallest_idx][1],
                                                          line[idx2][0], line[idx2][1],
                                                          x1, y1, x2, y2)
        return middle_x, middle_y

    def _find_closest_point_(self, sections, x1, y1, x2, y2):
        """
        finds closest point(S) of isopleth and axis (scale)
        """
        f1 = 1.0 - 1e-12
        f2 = 1.0 + 1e-12
        interps = []
        for idx, (x1s, y1s, x2s, y2s) in enumerate(sections):
            x_inter, y_inter = self._two_line_intersection_(x1s, y1s, x2s, y2s, x1, y1, x2, y2)
            # check if instersection
            # if (f1*min(x1s,x2s)<=x_inter<=f2*max(x1s,x2s)) and (f1*min(y1s,y2s)<=y_inter<=f2*max(y1s,y2s)):
            if self._between_(x1s, y1s, x2s, y2s, x_inter, y_inter):
                interps.append((x_inter, y_inter))
        if len(interps) < 1:
            interps.append((-10, -10))  # dummy point
        return interps[0][0], interps[0][1]

    @staticmethod
    def _between_(x1s, y1s, x2s, y2s, x, y):
        """
        checks if (x,y) in rectangle of (x1s,y1s)-(x2s,y2s)
        """
        f1 = 1.0 - 1e-12
        f2 = 1.0 + 1e-12
        f3 = 1e-6
        xs_min = min(x1s, x2s)
        if xs_min > 0:
            xs_min *= f1
        else:
            xs_min *= f2
        xs_max = max(x1s, x2s)
        if xs_max > 0:
            xs_max *= f2
        else:
            xs_max *= f1
        ys_min = min(y1s, y2s)
        if ys_min > 0:
            ys_min *= f1
        else:
            ys_min *= f2
        ys_max = max(y1s, y2s)
        if ys_max > 0:
            ys_max *= f2
        else:
            ys_max *= f1
        # trick to make little little over zero
        if xs_min == 0:
            xs_min = -xs_max * f3
        if xs_max == 0:
            xs_max = -xs_min * f3
        if ys_min == 0:
            ys_min = -ys_max * f3
        if ys_max == 0:
            ys_max = -ys_min * f3
        if xs_min <= x <= xs_max and ys_min <= y <= ys_max:
            return True
        else:
            return False

    def _find_closest_other_points_(self, sections, x1, y1, x2, y2, x_found, y_found):
        """
        finds closest point(S) of isopleth and axis (scale)
        x_found, y_found are found already before
        """
        f = 1 - 1e-12  # factor to reduce double hits
        interps = []
        for idx, (x1s, y1s, x2s, y2s) in enumerate(sections):
            x_inter, y_inter = self._two_line_intersection_(x1s, y1s, x2s * f, y2s * f, x1, y1, x2, y2)
            # check if instersection
            if (min(x1s, x2s * f) <= x_inter <= max(x1s, x2 * f)) and (
                    min(y1s, y2s * f) <= y_inter <= max(y1s, y2s * f)):
                if not x_found == x_inter and not y_found == y_inter:
                    interps.append((x_inter, y_inter))
        return interps

    @staticmethod
    def collinear(x1, y1, x2, y2, x3, y3):
        determinant = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
        if abs(determinant) < 1e-3:
            return True
        else:
            return False

    def find_farthest_pair_extra(self, x1, y1, x2, y2, x3, y3, idx):
        """
        finds farthest pair including extra points
        """
        xf1, yf1, xf2, yf2 = self.find_farthest_pair(x1, y1, x2, y2, x3, y3)
        for points in self.other_points[idx]:
            for (x, y) in points:
                xf1, yf1, xf2, yf2 = self.find_farthest_pair(xf1, yf1, xf2, yf2, x, y)
        return xf1, yf1, xf2, yf2

    def find_farthest_pair(self, x1, y1, x2, y2, x3, y3):
        """
        finds farthest two points of three
        """
        dist_12 = self._calc_distance_points_(x1, y1, x2, y2)
        dist_13 = self._calc_distance_points_(x1, y1, x3, y3)
        dist_23 = self._calc_distance_points_(x2, y2, x3, y3)
        if dist_12 >= dist_13 and dist_12 >= dist_23:
            return x1, y1, x2, y2
        if dist_13 >= dist_23 and dist_13 >= dist_12:
            return x1, y1, x3, y3
        if dist_23 >= dist_13 and dist_23 >= dist_12:
            return x2, y2, x3, y3

    def draw(self, canvas, draw_params=[{}]):
        """
        draws the isopleth
        """
        for idx, (x1, y1, x2, y2, x3, y3) in enumerate(self.draw_coordinates):
            xx1, yy1, xx2, yy2 = self.find_farthest_pair_extra(x1, y1, x2, y2, x3, y3, idx)
            # print xx1,yy1,xx2,yy2
            # check for collinearity
            #            if not self.collinear(x1, y1, x2, y2, x3, y3):
            #                print "found points not collinear in isopleth..."
            if len(draw_params) > idx:
                p = draw_params[idx]
            else:
                p = draw_params[len(draw_params) - 1]
            draw_params_list = self.parse_isopleth_params(p)
            color_param = draw_params_list[0]
            #            canvas.stroke(pyx.path.line(xx1,yy1,xx2,yy2),[pyx.color.cmyk.Black,
            #                                                    pyx.style.linewidth.thick,
            #                                                    pyx.style.linestyle.dashed])
            canvas.stroke(pyx.path.line(xx1, yy1, xx2, yy2), draw_params_list)
            circle_radius = self.parse_circle_size(p)
            self._draw_circle_(canvas, x1, y1, circle_radius, color_param)
            self._draw_circle_(canvas, x2, y2, circle_radius, color_param)
            self._draw_circle_(canvas, x3, y3, circle_radius, color_param)
        for idx, line_points in enumerate(self.other_points):
            if len(draw_params) > idx:
                p = draw_params[idx]
            else:
                p = draw_params[len(draw_params) - 1]
            circle_radius = self.parse_circle_size(p)
            draw_params_list = self.parse_isopleth_params(p)
            color_param = draw_params_list[0]
            for points in line_points:
                for (x, y) in points:
                    self._draw_circle_(canvas, x, y, circle_radius, color_param)

    def _draw_circle_(self, canvas, x, y, r, circle_color=pyx.color.cmyk.Black):
        """
        draws marker circle
        """
        canvas.fill(pyx.path.circle(x, y, r), [pyx.color.rgb.white])
        canvas.stroke(pyx.path.circle(x, y, r), [circle_color])

    def solve(self, solutions):
        """
        parent class to be overriden, solves coordinates
        """
        pass

    def check_if_all_solutions_found(self, solutions):
        """
        this has right now no function
        """
        all_found = True
        """
        for atom_idx,atom in enumerate(self.atom_stack):
            for idx,dummy in enumerate(solutions):
                if not isinstance(self.isopleth_values[idx][atom_idx],(int,float,tuple)):
                    pass
                    #print "not all isopleths solved yet..."
                    """

    def find_initial_solutions(self, solutions):
        """
        Finds initial solutions
        """
        for atom_idx, atom in enumerate(self.atom_stack):
            if not atom.params['tag'] == 'none':
                for idx, dummy in enumerate(solutions):
                    # store only true (x,y) tuples
                    if isinstance(self.isopleth_values[idx][atom_idx], (tuple)):
                        solutions[idx][atom.params['tag']] = self.isopleth_values[idx][atom_idx]
                    if isinstance(self.isopleth_values[idx][atom_idx], (int, float)):
                        value = self.isopleth_values[idx][atom_idx]
                        x = atom.give_x(value) - atom.params['align_x_offset']
                        y = atom.give_y(value) - atom.params['align_y_offset']
                        solutions[idx][atom.params['tag']] = (x, y)
            else:
                if not atom.params['dtag'] == 'none':
                    for idx, dummy in enumerate(solutions):
                        # store only true (x,y) tuples
                        if isinstance(self.isopleth_values[idx][atom_idx], (tuple)):
                            solutions[idx][atom.params['dtag']] = self.isopleth_values[idx][atom_idx]
                        if isinstance(self.isopleth_values[idx][atom_idx], (int, float)):
                            value = self.isopleth_values[idx][atom_idx]
                            x = atom.give_x(value) - atom.params['align_x_offset']
                            y = atom.give_y(value) - atom.params['align_y_offset']
                            solutions[idx][atom.params['dtag']] = (x, y)

    def update_solutions(self, solutions):
        """
        Updates solutions
        """
        solutions_updated = False
        for idx, solution in enumerate(solutions):
            for key in solution.keys():
                for atom_idx, atom in enumerate(self.atom_stack):
                    if atom.params['tag'] == key or atom.params['dtag'] == key:
                        if isinstance(self.isopleth_values[idx][atom_idx], str):
                            self.isopleth_values[idx][atom_idx] = solution[key]
                            solutions_updated = True
        return solutions_updated

    def _check_if_enough_params_(self, idx):
        """
        parent class to be overriden, checks if enough params to solve
        """
        pass

    def _two_line_intersection_(self, x1, y1, x2, y2, x3, y3, x4, y4):
        """
        intersection of lines (x1,y1)-(x2,y2) and (x3,y3)-(x4,y4)
        """
        # here we catch divide-by-zero and set value to inf
        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                x = self._det_(self._det_(x1, y1, x2, y2), (x1 - x2), self._det_(x3, y3, x4, y4), (x3 - x4)) / \
                    self._det_(x1 - x2, y1 - y2, x3 - x4, y3 - y4)
            except:
                # print("ValueError on L488 %g" % (self._det_(x1 - x2, y1 - y2, x3 - x4, y3 - y4)))
                x = float('Inf')
            try:
                y = self._det_(self._det_(x1, y1, x2, y2), (y1 - y2), self._det_(x3, y3, x4, y4), (y3 - y4)) / \
                    self._det_(x1 - x2, y1 - y2, x3 - x4, y3 - y4)
            except:
                # print("ValueError on L499 %g" % (self._det_(x1 - x2, y1 - y2, x3 - x4, y3 - y4)))
                y = float('Inf')
        return x, y

    def _det_(self, a, b, c, d):
        return a * d - c * b

    def interp_xy(self, x, y, atom):
        """
        given a point in u-axis, corresponding value is interpolated
        """
        f = 1.0
        interps = []
        min_distance = None
        for idx, (x1s, y1s, x2s, y2s) in enumerate(atom.sections):
            distance_1 = self._calc_distance_points_(x1s, y1s, x, y)
            distance_2 = self._calc_distance_points_(x2s, y2s, x, y)
            distance = min(distance_1, distance_2)
            if min_distance is None:
                min_distance = distance
                closest_value = atom.section_values[idx][0]
            else:
                if distance < min_distance:
                    min_distance = distance
                    value_0 = atom.section_values[idx][0]
                    value_1 = atom.section_values[idx][1]
                    closest_value = self.interpolate(x1s, y1s, x2s, y2s, x, y, value_0, value_1)
                    closest_value_0 = value_0
                    closest_value_1 = value_1
        # print closest_value,closest_value_0,closest_value_1
        return closest_value

    def interpolate(self, x1, y1, x2, y2, x3, y3, value_1, value_2):
        """
        value 1 = x1,y1
        value 2 = x2,y2
        point = x3,y3
        Interpolates linearly what is the value of point in line (x1,y1)-(x2,y2)
        """
        distance_1 = self._calc_distance_points_(x1, y1, x3, y3)
        distance_2 = self._calc_distance_points_(x2, y2, x3, y3)
        value = value_1 + (value_2 - value_1) * distance_1 / (distance_1 + distance_2)
        return value

    def parse_linestyle(self, line_style):
        """
        parses linestyle
        """
        if not re.search("solid", line_style, re.IGNORECASE) is None:
            return pyx.style.linestyle.solid
        if not re.search("dashed", line_style, re.IGNORECASE) is None:
            return pyx.style.linestyle.dashed
        if not re.search("dotted", line_style, re.IGNORECASE) is None:
            return pyx.style.linestyle.dotted
        if not re.search("dashdotted", line_style, re.IGNORECASE) is None:
            return pyx.style.linestyle.dashdotted
        # no match return default
        print("unknown linestyle: %s" % line_style)
        return pyx.style.linestyle.dashed

    def parse_linewidth(self, line_width):
        """
        parses linewidth
        """
        if not re.search("THIN", line_width) is None:
            return pyx.style.linewidth.THIN
        if not re.search("THIn", line_width) is None:
            return pyx.style.linewidth.THIn
        if not re.search("THin", line_width) is None:
            return pyx.style.linewidth.THin
        if not re.search("Thin", line_width) is None:
            return pyx.style.linewidth.Thin
        if not re.search("thin", line_width) is None:
            return pyx.style.linewidth.thin
        if not re.search("thick", line_width) is None:
            return pyx.style.linewidth.thick
        if not re.search("Thick", line_width) is None:
            return pyx.style.linewidth.Thick
        if not re.search("THick", line_width) is None:
            return pyx.style.linewidth.THick
        if not re.search("THIck", line_width) is None:
            return pyx.style.linewidth.THIck
        if not re.search("THICk", line_width) is None:
            return pyx.style.linewidth.THICk
        if not re.search("THICK", line_width) is None:
            return pyx.style.linewidth.THICK
        if not re.search("normal", line_width, re.IGNORECASE) is None:
            return pyx.style.linewidth.normal
        # no match return default
        print("unknown linewidth: %s" % line_width)
        return pyx.style.linewidth.normal

    def parse_color(self, color_str):
        """
        parses color
        """
        if re.match("GreenYellow", color_str, re.IGNORECASE):
            return pyx.color.cmyk.GreenYellow
        if re.match("Yellow", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Yellow
        if re.match("Goldenrod", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Goldenrod
        if re.match("Dandelion", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Dandelion
        if re.match("Apricot", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Apricot
        if re.match("Peach", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Peach
        if re.match("Melon", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Melon
        if re.match("YellowOrange", color_str, re.IGNORECASE):
            return pyx.color.cmyk.YellowOrange
        if re.match("Orange", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Orange
        if re.match("BurntOrange", color_str, re.IGNORECASE):
            return pyx.color.cmyk.BurntOrange
        if re.match("Bittersweet", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Bittersweet
        if re.match("RedOrange", color_str, re.IGNORECASE):
            return pyx.color.cmyk.RedOrange
        if re.match("Mahogany", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Mahogany
        if re.match("Maroon", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Maroon
        if re.match("BrickRed", color_str, re.IGNORECASE):
            return pyx.color.cmyk.BrickRed
        if re.match("Red", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Red
        if re.match("OrangeRed", color_str, re.IGNORECASE):
            return pyx.color.cmyk.OrangeRed
        if re.match("RubineRed", color_str, re.IGNORECASE):
            return pyx.color.cmyk.RubineRed
        if re.match("WildStrawberry", color_str, re.IGNORECASE):
            return pyx.color.cmyk.WildStrawberry
        if re.match("Salmon", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Salmon
        if re.match("CarnationPink", color_str, re.IGNORECASE):
            return pyx.color.cmyk.CarnationPink
        if re.match("Magenta", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Magenta
        if re.match("VioletRed", color_str, re.IGNORECASE):
            return pyx.color.cmyk.VioletRed
        if re.match("Rhodamine", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Rhodamine
        if re.match("Mulberry", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Mulberry
        if re.match("RedViolet", color_str, re.IGNORECASE):
            return pyx.color.cmyk.RedViolet
        if re.match("Fuchsia", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Fuchsia
        if re.match("Lavender", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Lavender
        if re.match("Thistle", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Thistle
        if re.match("Orchid", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Orchid
        if re.match("DarkOrchid", color_str, re.IGNORECASE):
            return pyx.color.cmyk.DarkOrchid
        if re.match("Purple", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Purple
        if re.match("Plum", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Plum
        if re.match("Violet", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Violet
        if re.match("RoyalPurple", color_str, re.IGNORECASE):
            return pyx.color.cmyk.RoyalPurple
        if re.match("BlueViolet", color_str, re.IGNORECASE):
            return pyx.color.cmyk.BlueViolet
        if re.match("Periwinkle", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Periwinkle
        if re.match("CadetBlue", color_str, re.IGNORECASE):
            return pyx.color.cmyk.CadetBlue
        if re.match("CornFlowerBlue", color_str, re.IGNORECASE):
            return pyx.color.cmyk.CornFlowerBlue
        if re.match("MidnightBlue", color_str, re.IGNORECASE):
            return pyx.color.cmyk.MidnightBlue
        if re.match("NavyBlue", color_str, re.IGNORECASE):
            return pyx.color.cmyk.NavyBlue
        if re.match("RoyalBlue", color_str, re.IGNORECASE):
            return pyx.color.cmyk.RoyalBlue
        if re.match("Blue", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Blue
        if re.match("Cerulean", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Cerulean
        if re.match("Cyan", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Cyan
        if re.match("ProcessBlue", color_str, re.IGNORECASE):
            return pyx.color.cmyk.ProcessBlue
        if re.match("SkyBlue", color_str, re.IGNORECASE):
            return pyx.color.cmyk.SkyBlue
        if re.match("Turquoise", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Turquoise
        if re.match("TealBlue", color_str, re.IGNORECASE):
            return pyx.color.cmyk.TealBlue
        if re.match("AquaMarine", color_str, re.IGNORECASE):
            return pyx.color.cmyk.AquaMarine
        if re.match("BlueGreen", color_str, re.IGNORECASE):
            return pyx.color.cmyk.BlueGreen
        if re.match("Emerald", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Emerald
        if re.match("JungleGreen", color_str, re.IGNORECASE):
            return pyx.color.cmyk.JungleGreen
        if re.match("SeaGreen", color_str, re.IGNORECASE):
            return pyx.color.cmyk.SeaGreen
        if re.match("Green", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Green
        if re.match("ForestGreen", color_str, re.IGNORECASE):
            return pyx.color.cmyk.ForestGreen
        if re.match("PineGreen", color_str, re.IGNORECASE):
            return pyx.color.cmyk.PineGreen
        if re.match("LimeGreen", color_str, re.IGNORECASE):
            return pyx.color.cmyk.LimeGreen
        if re.match("YellowGreen", color_str, re.IGNORECASE):
            return pyx.color.cmyk.YellowGreen
        if re.match("SpringGreen", color_str, re.IGNORECASE):
            return pyx.color.cmyk.SpringGreen
        if re.match("OliveGreen", color_str, re.IGNORECASE):
            return pyx.color.cmyk.OliveGreen
        if re.match("RawSienna", color_str, re.IGNORECASE):
            return pyx.color.cmyk.RawSienna
        if re.match("Sepia", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Sepia
        if re.match("Brown", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Brown
        if re.match("Tan", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Tan
        if re.match("Gray", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Gray
        if re.match("Black", color_str, re.IGNORECASE):
            return pyx.color.cmyk.Black
        if re.match("White", color_str, re.IGNORECASE):
            return pyx.color.cmyk.White
        # default
        print("unknown color: %s" % color)
        return pyx.color.cmyk.Black

    def parse_isopleth_params(self, params):
        """
        parses single definition. Definition is for example:
          'isopleth_params':[{'color':'Black',
                              'linestyle':'Dashed',
                              'lineweight':'THick',
                              'circle_size':0.05}]
        """
        # color
        if 'color' in params:
            color_param = self.parse_color(params['color'])
        else:
            color_param = self.parse_color('black')

        # color rgb
        if 'color_rgb' in params:
            r = params['color_rgb'][0]
            g = params['color_rgb'][1]
            b = params['color_rgb'][2]
            color_param = pyx.color.rgb(r, g, b)
        # color cmyk
        if 'color_cmyk' in params:
            c = params['color_cmyk'][0]
            m = params['color_cmyk'][1]
            y = params['color_cmyk'][2]
            k = params['color_cmyk'][3]
            color_param = pyx.color.cmyk(c, m, y, k)
        # transparent
        transparent = False
        if 'transparency' in params:
            color_param_transparency = pyx.color.transparency(params['transparency'])
            transparent = True
        # linestyle
        if 'linestyle' in params:
            linestyle_param = self.parse_linestyle(params['linestyle'])
        else:
            linestyle_param = self.parse_linestyle('dashed')
        # linewidth
        if 'linewidth' in params:
            linewidth_param = self.parse_linewidth(params['linewidth'])
        else:
            linewidth_param = self.parse_linewidth('thick')
        if transparent:
            return [color_param, linestyle_param, linewidth_param, color_param_transparency]
        else:
            return [color_param, linestyle_param, linewidth_param]

    def parse_circle_size(self, params):
        #
        # circle radius
        if 'circle_size' in params:
            return params['circle_size']
        else:
            return 0.05


class Isopleth_Block_Type_1(Isopleth_Block):
    """
    type F1+F2+F3=0 isopleth
    atom stack is the stack of scales
    solution_dict is a dictionary of found solutions
    """

    def __init__(self, atom_stack, params):
        super(Isopleth_Block_Type_1, self).__init__(atom_stack, params)

    def _check_if_enough_params_(self, idx):
        """
        checks if enough numbers given to find solution
        """
        numbers = self.isopleth_values[idx]
        given = 0
        for number in numbers:
            if isinstance(number, (int, float, tuple, list)):
                given += 1
        if given < 2:
            return False  # isopleth not solvable (right now)
        else:
            return True  # isopleth solvable

    def solve(self, solutions):
        """
        solves coordinates
        solutions is list of dicts of found solutions
        """
        for idx, isopleth_values_single in enumerate(self.isopleth_values):
            if len(self.draw_coordinates) < (idx + 1):
                self.draw_coordinates.append([])  # dummy expansion of matrix
            if len(solutions) < (idx + 1):
                solutions.append({})
            if len(self.other_points) < (idx + 1):
                self.other_points.append([])
            if self._check_if_enough_params_(idx):
                x0, y0, x1, y1, x2, y2 = self.solve_single(solutions[idx],
                                                           isopleth_values_single, idx)
                self.draw_coordinates[idx] = [x0, y0, x1, y1, x2, y2]

    def solve_single(self, solution, isopleth_values, idx):
        """
        solves single isopleth
        solution = dict with values of found solutions
        isopleth_values = list of values and coordinates
        idx = # of isopleth line
        """
        atom_stack = self.atom_stack
        f1_known = False
        f2_known = False
        f3_known = False
        # f1 known
        if isinstance(isopleth_values[0], (int, float)):
            x0 = atom_stack[0].give_x(isopleth_values[0])
            y0 = atom_stack[0].give_y(isopleth_values[0])
            f1_known = True
        if isinstance(isopleth_values[0], tuple):
            x0 = isopleth_values[0][0]
            y0 = isopleth_values[0][1]
            f1_known = True
        if isinstance(isopleth_values[0], list):  # = this is grid
            x0 = atom_stack[0].give_x_grid(isopleth_values[0][0], isopleth_values[0][1])
            y0 = atom_stack[0].give_y_grid(isopleth_values[0][0], isopleth_values[0][1])
            f1_known = True
        # f2 known
        if isinstance(isopleth_values[1], (int, float)):
            x1 = atom_stack[1].give_x(isopleth_values[1])
            y1 = atom_stack[1].give_y(isopleth_values[1])
            f2_known = True
        if isinstance(isopleth_values[1], tuple):
            x1 = isopleth_values[1][0]
            y1 = isopleth_values[1][1]
            f2_known = True
        if isinstance(isopleth_values[1], list):  # = this is grid
            x1 = atom_stack[1].give_x_grid(isopleth_values[1][0], isopleth_values[1][1])
            y1 = atom_stack[1].give_y_grid(isopleth_values[1][0], isopleth_values[1][1])
            f2_known = True
        # f3 known
        if isinstance(isopleth_values[2], (int, float)):
            x2 = atom_stack[2].give_x(isopleth_values[2])
            y2 = atom_stack[2].give_y(isopleth_values[2])
            f3_known = True
        if isinstance(isopleth_values[2], tuple):
            x2 = isopleth_values[2][0]
            y2 = isopleth_values[2][1]
            f3_known = True
        if isinstance(isopleth_values[2], list):  # = this is grid
            x2 = atom_stack[2].give_x_grid(isopleth_values[2][0], isopleth_values[2][1])
            y2 = atom_stack[2].give_y_grid(isopleth_values[2][0], isopleth_values[2][1])
            f3_known = True
        if not f1_known:
            # line=self.atom_stack[0].line
            x0, y0 = self._find_closest_point_(self.atom_stack[0].sections, x1, y1, x2, y2)
            other_points = self._find_closest_other_points_(self.atom_stack[0].sections, x1, y1, x2, y2, x0, y0)
            # solution[isopleth_values[0]]=(x0,y0)
            if not self.atom_stack[0].params['tag'] == 'none':
                solution[self.atom_stack[0].params['tag']] = (x0, y0)
            isopleth_values[0] = (x0, y0)
            self.other_points[idx].append(other_points)
        if not f2_known:
            # line=self.atom_stack[1].line
            x1, y1 = self._find_closest_point_(self.atom_stack[1].sections, x0, y0, x2, y2)
            other_points = self._find_closest_other_points_(self.atom_stack[1].sections, x0, y0, x2, y2, x1, y1)
            # solution[isopleth_values[1]]=(x1,y1)
            if not self.atom_stack[1].params['tag'] == 'none':
                solution[self.atom_stack[1].params['tag']] = (x1, y1)
            isopleth_values[1] = (x1, y1)
            self.other_points[idx].append(other_points)
        if not f3_known:
            # line=self.atom_stack[2].line
            x2, y2 = self._find_closest_point_(self.atom_stack[2].sections, x0, y0, x1, y1)
            other_points = self._find_closest_other_points_(self.atom_stack[2].sections, x0, y0, x1, y1, x2, y2)
            # solution[isopleth_values[2]]=(x2,y2)
            if not self.atom_stack[2].params['tag'] == 'none':
                solution[self.atom_stack[2].params['tag']] = (x2, y2)
            isopleth_values[2] = (x2, y2)
            self.other_points[idx].append(other_points)
        return x0, y0, x1, y1, x2, y2


class Isopleth_Block_Type_2(Isopleth_Block_Type_1):
    """
    type F1=F2*F3 isopleth
    atom stack is the stack of scales
    solution_dict is a dictionary of found solutions
    """

    def __init__(self, atom_stack, params):
        super(Isopleth_Block_Type_2, self).__init__(atom_stack, params)


class Isopleth_Block_Type_5(Isopleth_Block):
    """
    type 5 = contour, nomo_block = block of class Nomo_Block_Type_5
    """

    def __init__(self, atom_stack, params, nomo_block):
        super(Isopleth_Block_Type_5, self).__init__(atom_stack, params)
        self.nomo_block = nomo_block

    def _check_if_enough_params_(self, idx):
        """
        checks if enough numbers given to find solution
        """
        numbers = self.isopleth_values[idx]
        given = 0
        for number in numbers:
            if isinstance(number, (int, float, tuple)):
                given = given + 1
        if given < 2:
            return False  # isopleth not solvable (right now)
        else:
            return True  # isopleth solvable

    def draw(self, canvas, draw_params=[{}]):
        """
        draws the isopleth
        """
        for idx, (x1, y1, x2, y2, x3, y3) in enumerate(self.draw_coordinates):
            if len(draw_params) > idx:
                p = draw_params[idx]
            else:
                p = draw_params[len(draw_params) - 1]
            draw_params_list = self.parse_isopleth_params(p)
            color_param = draw_params_list[0]
            circle_radius = self.parse_circle_size(p)
            canvas.stroke(pyx.path.line(x1, y1, x2, y2), draw_params_list)
            canvas.stroke(pyx.path.line(x2, y2, x3, y3), draw_params_list)
            self._draw_circle_(canvas, x1, y1, circle_radius, color_param)
            self._draw_circle_(canvas, x2, y2, circle_radius, color_param)
            self._draw_circle_(canvas, x3, y3, circle_radius, color_param)
        for idx, line_points in enumerate(self.other_points):
            if len(draw_params) > idx:
                p = draw_params[idx]
            else:
                p = draw_params[len(draw_params) - 1]
            draw_params_list = self.parse_isopleth_params(p)
            color_param = draw_params_list[0]
            circle_radius = self.parse_circle_size(p)
            for points in line_points:
                for (x, y) in points:
                    self._draw_circle_(canvas, x, y, circle_radius)

    def solve(self, solutions):
        """
        solves coordinates
        solutions is list of dicts of found solutions
        """
        for idx, isopleth_values_single in enumerate(self.isopleth_values):
            if len(self.draw_coordinates) < (idx + 1):
                self.draw_coordinates.append([])  # dummy expansion of matrix
            if len(solutions) < (idx + 1):
                solutions.append({})
            if len(self.other_points) < (idx + 1):
                self.other_points.append([])
            if self._check_if_enough_params_(idx):
                x_u, y_u, x_v, y_v, x_wd, y_wd = self.solve_single(solutions[idx],
                                                                   isopleth_values_single, idx)
                self.draw_coordinates[idx] = [x_u, y_u, x_v, y_v, x_wd, y_wd]

    def solve_single(self, solution, isopleth_values, idx):
        """
        solves the thing
        """
        atom_stack = self.atom_stack
        u_known = False
        v_known = False
        wd_known = False
        # initial values that are replaced (for debugging)
        x_u = -10
        y_u = -10
        x_wd = -10
        y_wd = -10
        x_v = -10
        x_v = -10
        # u known
        if isinstance(isopleth_values[0], (int, float)):
            x_u, x_u_ini, y_u_ini = self.x_u(isopleth_values[0])
            y_u, x_u_ini, y_u_ini = self.y_u(isopleth_values[0])
            u_known = True
        # u known as tuple
        if isinstance(isopleth_values[0], tuple):
            u_value = self.u_x_y_interp(isopleth_values[0][0], isopleth_values[0][1])
            x_u, x_u_ini, y_u_ini = self.x_u(u_value)
            y_u, x_u_ini, y_u_ini = self.y_u(u_value)
            u_known = True
        # wd known
        if isinstance(isopleth_values[2], (int, float)):
            x_wd, x_wd_ini, y_wd_ini = self.x_wd(isopleth_values[2])
            y_wd, x_wd_ini, y_wd_ini = self.y_wd(isopleth_values[2])
            wd_known = True
        # wd known as tuple
        if isinstance(isopleth_values[2], tuple):
            wd_value = self.wd_x_y_interp(isopleth_values[2][0], isopleth_values[2][1])
            x_wd, x_wd_ini, y_wd_ini = self.x_wd(wd_value)
            y_wd, x_wd_ini, y_wd_ini = self.y_wd(wd_value)
            wd_known = True
        # v known as tuple (possible?)
        if isinstance(isopleth_values[1], tuple):
            x_v, x_v_ini, y_v_ini = isopleth_values[1][0]
            y_v, x_v_ini, y_v_ini = isopleth_values[1][1]
            v_known = True
        # v and wd known as values
        if isinstance(isopleth_values[1], (int, float)) and isinstance(isopleth_values[2], (int, float)):
            x_v, x_v_ini, y_v_ini = self.x_v_wd(isopleth_values[1], isopleth_values[2])
            y_v, x_v_ini, y_v_ini = self.y_v_wd(isopleth_values[1], isopleth_values[2])
            v_known = True
        # v known as value and wd known as tuple (x,y)
        if isinstance(isopleth_values[1], (int, float)) and isinstance(isopleth_values[2], (tuple)):
            x_v, x_v_ini, y_v_ini = self.x_v_wd_tuple(isopleth_values[1], isopleth_values[2])
            y_v, x_v_ini, y_v_ini = self.y_v_wd_tuple(isopleth_values[1], isopleth_values[2])
            v_known = True
        # v and u known as values
        if isinstance(isopleth_values[1], (int, float)) and isinstance(isopleth_values[0], (int, float)):
            x_v, y_v, x_v_ini, y_v_ini = self.xy_v_u(isopleth_values[1], isopleth_values[0])
            v_known = True
        # v known as value and u known as tuple (x,y)
        if isinstance(isopleth_values[1], (int, float)) and isinstance(isopleth_values[0], (tuple)):
            x_v, y_v, x_v_ini, y_v_ini = self.xy_v_u_tuple(isopleth_values[1], isopleth_values[0])
            v_known = True
        # now, all needed coordinates known
        if not u_known and v_known and wd_known:
            x_u_ini = self.nomo_block.grid_box.params_u['F'](0)
            y_u_ini = y_v_ini
            x_u = self.nomo_block._give_trafo_x_(x_u_ini, y_u_ini)
            y_u = self.nomo_block._give_trafo_y_(x_u_ini, y_u_ini)
            if not self.nomo_block.grid_box.params_u['tag'] == 'none':
                solution[self.nomo_block.grid_box.params_u['tag']] = (x_u, y_u)
        if not v_known and u_known and wd_known:
            x_v_ini = x_wd_ini
            y_v_ini = y_u_ini
            x_v = self.nomo_block._give_trafo_x_(x_v_ini, y_v_ini)
            y_v = self.nomo_block._give_trafo_y_(x_v_ini, y_v_ini)
            if not self.nomo_block.grid_box.params_v['tag'] == 'none':
                solution[self.nomo_block.grid_box.params_v['tag']] = (x_v, y_v)
        if not wd_known and u_known and v_known:
            x_wd_ini = x_v_ini
            y_wd_ini = self.nomo_block.grid_box.params_wd['G'](0)
            x_wd = self.nomo_block._give_trafo_x_(x_wd_ini, y_wd_ini)
            y_wd = self.nomo_block._give_trafo_y_(x_wd_ini, y_wd_ini)
            if not self.nomo_block.grid_box.params_wd['tag'] == 'none':
                solution[self.nomo_block.grid_box.params_wd['tag']] = (x_wd, y_wd)
        return x_u, y_u, x_v, y_v, x_wd, y_wd

    def x_u(self, u):
        """
        give x(u)
        """
        x0 = self.nomo_block.grid_box.params_u['F'](u)
        y0 = self.nomo_block.grid_box.params_u['G'](u)
        return self.nomo_block._give_trafo_x_(x0, y0), x0, y0

    def y_u(self, u):
        """
        give y(u)
        """
        x0 = self.nomo_block.grid_box.params_u['F'](u)
        y0 = self.nomo_block.grid_box.params_u['G'](u)
        return self.nomo_block._give_trafo_y_(x0, y0), x0, y0

    def x_wd(self, wd):
        """
        give x(wd)
        """
        x0 = self.nomo_block.grid_box.params_wd['F'](wd)
        y0 = self.nomo_block.grid_box.params_wd['G'](wd)
        return self.nomo_block._give_trafo_x_(x0, y0), x0, y0

    def y_wd(self, wd):
        """
        give y(wd)
        """
        x0 = self.nomo_block.grid_box.params_wd['F'](wd)
        y0 = self.nomo_block.grid_box.params_wd['G'](wd)
        return self.nomo_block._give_trafo_y_(x0, y0), x0, y0

    def xy_v_u(self, v, u):
        """
        give x(v,u), y(v,u)
        """
        x_start = self.nomo_block.grid_box.x_left
        x_stop = self.nomo_block.grid_box.x_right
        if x_start > x_stop:  # should no be
            x_start, x_stop = x_stop, x_start
        # x_init=(x_start+x_stop)/2.0
        v_func = self.nomo_block.grid_box.v_func
        u_func = self.nomo_block.grid_box.u_func
        u_value = u_func(u)  # = y
        func_opt = lambda x: (v_func(x, v) - u_value) ** 2  # func to minimize
        # let's try to find good starting point for optimization
        x_range = arange(x_start, x_stop, (x_stop - x_start) / 30.0, dtype=complex)
        #        print "x_range:"
        #        print x_range
        # use complex numbers to filter results with complex part
        #values = func_opt(x_range.astype(complex))
        values = x_range
        values_list_complex = values.tolist()
        values_list = []
        for value in values_list_complex:
            if value.imag == 0:
                values_list.append(value.real)
            else:
                values_list.append(1e12)  # large number
            #        print "values_list:"
            #        print values_list
        min_x_idx = values_list.index(min(values_list))
        x_init = x_range[min_x_idx]
        #        print "x_start %g"%x_start
        #        print "x_stop %g"%x_stop
        #        print "x_init %g"%x_init
        # find x point where u meets v = optimization
        x_opt = fmin(func_opt, [x_init], disp=0, maxiter=1e5, maxfun=1e5, ftol=1e-8, xtol=1e-8)[0]
        x_transformed = self.nomo_block._give_trafo_x_(x_opt, u_value)
        y_transformed = self.nomo_block._give_trafo_y_(x_opt, u_value)
        return x_transformed, y_transformed, x_opt, u_value

    def xy_v_u_tuple(self, v, u):
        """
        give x(v,u), y(v,u) where u is tuple (x,y)
        """
        return self.xy_v_u(v, self.u_x_y_interp(u[0], u[1]))

    def x_v_wd(self, v, wd):
        """
        give x(v,wd)
        """
        x0 = self.nomo_block.grid_box.params_wd['F'](wd)
        y0 = self.nomo_block.grid_box.v_func(x0, v)
        return self.nomo_block._give_trafo_x_(x0, y0), x0, y0

    def y_v_wd(self, v, wd):
        """
        give y(v,wd)
        """
        x0 = self.nomo_block.grid_box.params_wd['F'](wd)
        y0 = self.nomo_block.grid_box.v_func(x0, v)
        return self.nomo_block._give_trafo_y_(x0, y0), x0, y0

    def x_v_wd_tuple(self, v, wd):
        """
        give x(v,wd) where wd is tuple of final coordinates
        """
        return self.x_v_wd(v, self.wd_x_y_interp(wd[0], wd[1]))

    def y_v_wd_tuple(self, v, wd):
        """
        give y(v,wd) where wd is tuple of final coordinates
        """
        return self.y_v_wd(v, self.wd_x_y_interp(wd[0], wd[1]))

    def wd_x_y_interp(self, x, y):
        """
        given a point in wd-axis, corresponding value is interpolated
        """
        f = 1.0
        interps = []
        min_distance = None
        for idx, (x1s, y1s, x2s, y2s) in enumerate(self.nomo_block.atom_wd.sections):
            distance_1 = self._calc_distance_points_(x1s, y1s, x, y)
            distance_2 = self._calc_distance_points_(x2s, y2s, x, y)
            distance = min(distance_1, distance_2)
            if min_distance == None:
                min_distance = distance
                closest_value = self.nomo_block.atom_wd.section_values[idx][0]
            else:
                if distance < min_distance:
                    min_distance = distance
                    value_0 = self.nomo_block.atom_wd.section_values[idx][0]
                    value_1 = self.nomo_block.atom_wd.section_values[idx][1]
                    closest_value = self.interpolate(x1s, y1s, x2s, y2s, x, y, value_0, value_1)
                    closest_value_0 = value_0
                    closest_value_1 = value_1
        # print closest_value,closest_value_0,closest_value_1
        return closest_value

    def u_x_y_interp(self, x, y):
        """
        given a point in u-axis, corresponding value is interpolated
        """
        f = 1.0
        interps = []
        min_distance = None
        for idx, (x1s, y1s, x2s, y2s) in enumerate(self.nomo_block.atom_u.sections):
            distance_1 = self._calc_distance_points_(x1s, y1s, x, y)
            distance_2 = self._calc_distance_points_(x2s, y2s, x, y)
            distance = min(distance_1, distance_2)
            if min_distance == None:
                min_distance = distance
                closest_value = self.nomo_block.atom_u.section_values[idx][0]
            else:
                if distance < min_distance:
                    min_distance = distance
                    value_0 = self.nomo_block.atom_u.section_values[idx][0]
                    value_1 = self.nomo_block.atom_u.section_values[idx][1]
                    closest_value = self.interpolate(x1s, y1s, x2s, y2s, x, y, value_0, value_1)
                    closest_value_0 = value_0
                    closest_value_1 = value_1
        # print closest_value,closest_value_0,closest_value_1
        return closest_value


class Isopleth_Block_Type_6(Isopleth_Block):
    """
    type single
    atom stack is the stack of scales
    solution_dict is a dictionary of found solutions
    """

    def __init__(self, atom_stack, params):
        super(Isopleth_Block_Type_6, self).__init__(atom_stack, params)

    def _check_if_enough_params_(self, idx):
        """
        checks if enough numbers given to find solution
        """
        numbers = self.isopleth_values[idx]
        given = 0
        for number in numbers:
            if isinstance(number, (int, float, tuple, list)):
                given = given + 1
        if given > 0:
            return True  # isopleth solvable (right now)
        else:
            return False  # isopleth not solvable

    def solve(self, solutions):
        """
        solves coordinates
        solutions is list of dicts of found solutions
        """
        for idx, isopleth_values_single in enumerate(self.isopleth_values):
            if len(self.draw_coordinates) < (idx + 1):
                self.draw_coordinates.append([])  # dummy expansion of matrix
            if len(solutions) < (idx + 1):
                solutions.append({})
            if len(self.other_points) < (idx + 1):
                self.other_points.append([])
            if self._check_if_enough_params_(idx):
                x1, y1, x2, y2 = self.solve_single(solutions[idx], isopleth_values_single, idx)
                self.draw_coordinates[idx] = [x1, y1, x2, y2]

    def solve_single(self, solution, isopleth_values, idx):
        """
        solves single isopleth
        solution = dict with values of found solutions
        isopleth_values = list of values and coordinates
        idx = # of isopleth line
        """
        atom_stack = self.atom_stack
        atom1 = atom_stack[0]
        atom2 = atom_stack[1]
        f1_known = False
        f2_known = False
        # f1 value known
        if isinstance(isopleth_values[0], (int, float)):
            x1 = atom_stack[0].give_x(isopleth_values[0])
            y1 = atom_stack[0].give_y(isopleth_values[0])
            f1_known = True
            value = self.interp_xy(x1, y1, atom1)
        if isinstance(isopleth_values[0], tuple):
            x1 = isopleth_values[0][0]
            y1 = isopleth_values[0][1]
            f1_known = True
            value = self.interp_xy(x1, y1, atom1)
        # f2 value known
        if isinstance(isopleth_values[1], (int, float)):
            x2 = atom_stack[1].give_x(isopleth_values[1])
            y2 = atom_stack[1].give_y(isopleth_values[1])
            f2_known = True
            value = self.interp_xy(x2, y2, atom2)
        if isinstance(isopleth_values[1], tuple):
            x2 = isopleth_values[1][0]
            y2 = isopleth_values[1][1]
            f2_known = True
            value = self.interp_xy(x2, y2, atom2)
        if not f1_known:
            x1 = atom1.give_x(value)
            y1 = atom1.give_y(value)
        if not f2_known:
            x2 = atom2.give_x(value)
            y2 = atom2.give_y(value)
        # let's save the result
        if not atom1.params['tag'] == 'none':
            solution[atom1.params['tag']] = (x1, y1)
        if not atom2.params['tag'] == 'none':
            solution[atom2.params['tag']] = (x2, y2)
        return x1, y1, x2, y2

    def draw(self, canvas, draw_params=[{}]):
        """
        draws the isopleth
        """
        for idx, (x1, y1, x2, y2) in enumerate(self.draw_coordinates):
            if len(draw_params) > idx:
                p = draw_params[idx]
            else:
                p = draw_params[len(draw_params) - 1]
            draw_params_list = self.parse_isopleth_params(p)
            color_param = draw_params_list[0]
            circle_radius = self.parse_circle_size(p)
            x_offset1 = self.atom_stack[0].params['align_x_offset']
            y_offset1 = self.atom_stack[0].params['align_y_offset']
            x_offset2 = self.atom_stack[1].params['align_x_offset']
            y_offset2 = self.atom_stack[1].params['align_y_offset']
            canvas.stroke(pyx.path.line(x1 - x_offset1, y1 - y_offset1, x2 - x_offset2, y2 - y_offset2),
                          draw_params_list)
            self._draw_circle_(canvas, x1, y1, circle_radius, color_param)
            self._draw_circle_(canvas, x2, y2, circle_radius, color_param)
        for idx, line_points in enumerate(self.other_points):
            if len(draw_params) > idx:
                p = draw_params[idx]
            else:
                p = draw_params[len(draw_params) - 1]
            draw_params_list = self.parse_isopleth_params(p)
            color_param = draw_params_list[0]
            circle_radius = self.parse_circle_size(p)
            for points in line_points:
                for (x, y) in points:
                    self._draw_circle_(canvas, x, y, circle_radius, color_param)


class Isopleth_Block_Type_7(Isopleth_Block_Type_1):
    """
    type 1/F1+1/F2=1/F3 isopleth
    atom stack is the stack of scales
    solution_dict is a dictionary of found solutions
    """

    def __init__(self, atom_stack, params):
        super(Isopleth_Block_Type_7, self).__init__(atom_stack, params)


class Isopleth_Block_Type_8(Isopleth_Block):
    """
    type single
    atom stack is the stack of scales
    solution_dict is a dictionary of found solutions
    """

    def __init__(self, atom_stack, params):
        super(Isopleth_Block_Type_8, self).__init__(atom_stack, params)

    def _check_if_enough_params_(self, idx):
        """
        checks if enough numbers given to find solution
        """
        numbers = self.isopleth_values[idx]
        given = 0
        for number in numbers:
            if isinstance(number, (int, float, tuple, list)):
                given = given + 1
        if given > 0:
            return True  # isopleth solvable (right now)
        else:
            return False  # isopleth not solvable

    def solve(self, solutions):
        """
        solves coordinates
        solutions is list of dicts of found solutions
        """
        for idx, isopleth_values_single in enumerate(self.isopleth_values):
            if len(self.draw_coordinates) < (idx + 1):
                self.draw_coordinates.append([])  # dummy expansion of matrix
            if len(solutions) < (idx + 1):
                solutions.append({})
            if len(self.other_points) < (idx + 1):
                self.other_points.append([])
            if self._check_if_enough_params_(idx):
                x0, y0 = self.solve_single(solutions[idx], isopleth_values_single, idx)
                self.draw_coordinates[idx] = [x0, y0]

    def solve_single(self, solution, isopleth_values, idx):
        """
        solves single isopleth
        solution = dict with values of found solutions
        isopleth_values = list of values and coordinates
        idx = # of isopleth line
        """
        atom_stack = self.atom_stack
        # value known
        if isinstance(isopleth_values[0], (int, float)):
            x0 = atom_stack[0].give_x(isopleth_values[0])
            y0 = atom_stack[0].give_y(isopleth_values[0])
        if isinstance(isopleth_values[0], tuple):
            x0 = isopleth_values[0][0]
            y0 = isopleth_values[0][1]
        if not self.atom_stack[0].params['tag'] == 'none':
            solution[self.atom_stack[0].params['tag']] = (x0, y0)
        return x0, y0

    def draw(self, canvas, draw_params=[{}]):
        """
        draws the isopleth
        """
        for idx, (x1, y1) in enumerate(self.draw_coordinates):
            if len(draw_params) > idx:
                p = draw_params[idx]
            else:
                p = draw_params[len(draw_params) - 1]
            draw_params_list = self.parse_isopleth_params(p)
            color_param = draw_params_list[0]
            circle_radius = self.parse_circle_size(p)
            x_offset = self.atom_stack[0].params['align_x_offset']
            y_offset = self.atom_stack[0].params['align_y_offset']
            if x_offset != 0 or y_offset != 0:
                canvas.stroke(pyx.path.line(x1, y1, x1 - x_offset, y1 - y_offset), draw_params_list)
            self._draw_circle_(canvas, x1, y1, circle_radius, color_param)
        for idx, line_points in enumerate(self.other_points):
            if len(draw_params) > idx:
                p = draw_params[idx]
            else:
                p = draw_params[len(draw_params) - 1]
            draw_params_list = self.parse_isopleth_params(p)
            color_param = draw_params_list[0]
            circle_radius = self.parse_circle_size(p)
            for points in line_points:
                for (x, y) in points:
                    self._draw_circle_(canvas, x, y, circle_radius, color_param)


class Isopleth_Block_Type_9(Isopleth_Block_Type_1):
    """
    type general determinant isopleth
    note, that parameters for grid should be given, they are not solved
    """

    def __init__(self, atom_stack, params):
        super(Isopleth_Block_Type_9, self).__init__(atom_stack, params)


class Isopleth_Block_Type_10(Isopleth_Block_Type_1):
    """
    type F1(u)+F2(v)*F3(w)+F4(w)=0
    atom stack is the stack of scales
    solution_dict is a dictionary of found solutions
    """

    def __init__(self, atom_stack, params):
        super(Isopleth_Block_Type_10, self).__init__(atom_stack, params)
