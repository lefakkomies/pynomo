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
import numpy as np
from scipy import linalg
#import scipy


class FourPoint(object):
    """
    class to transform four points to four points.
    """

    def __init__(self, x1, y1, x2, y2, x3, y3, x4, y4, x1d, y1d, x2d, y2d, x3d, y3d, x4d, y4d):
        """
        assumes:
           (x1,y1)     (x3,y3)          (x1d,y1d)      (x3d,y3d)
               |  polygon  |      ---->      |   polygon  |
            (x2,y2)     (x4,y4)          (x2d,y2d)      (x4d,y4d)
        """
        trafo_1 = self.find_trafo_to_unity_rectangle(x1, y1, x2, y2, x3, y3, x4, y4)
        trafo_2 = self.find_trafo_to_unity_rectangle(x1d, y1d, x2d, y2d, x3d, y3d, x4d, y4d)
        #        test1=np.array([[x1,y1,1.0],
        #                     [x2,y2,1.0],
        #                     [x3,y3,1.0]])
        #        test2=np.array([[x1,y1,1.0],
        #                     [x2,y2,1.0],
        #                     [x4,y4,1.0]])
        #        test1d=np.array([[x1d,y1d,1.0],
        #                     [x2d,y2d,1.0],
        #                     [x3d,y3d,1.0]])
        #        test2d=np.array([[x1d,y1d,1.0],
        #                     [x2d,y2d,1.0],
        #                     [x4d,y4d,1.0]])
        #        test1f=np.dot(test1,trafo_1)
        #        test2f=np.dot(test2,trafo_1)
        #        test1fd=np.dot(test1d,trafo_2)
        #        test2fd=np.dot(test2d,trafo_2)
        #        print test1f
        #        print test2f
        #        print test1fd
        #        print test2fd
        #        print "goal"
        #        print x1d,y1d,x2d,y2d,x3d,y3d,x4d,y4d
        self.trafo = np.dot(trafo_1, linalg.inv(trafo_2))
        #        print "result"
        #        print np.dot(test1,self.trafo)
        #        print np.dot(test2,self.trafo)
        """
        o1,o2,o3,p1,p2,p3,q1,q2,q3=self.find_three_points_to_transform(x1,y1,x2,y2,x3,y3,x4,y4)
        self.transformation=self.find_transformation_points_to_rectangle(o1,o2,o3,p1,p2,p3,q1,q2,q3)
        initial=np.array([[x1,y1,1.0],
                       [x2,y2,1.0],
                       [x3,y3,1.0]])
        initial2=np.array([[x1,y1,1.0],
                       [x2,y2,1.0],
                       [x4,y4,1.0]])
        inter=np.dot(initial,self.transformation)
        xi1=inter[0][0]/inter[0][2]
        yi1=inter[0][1]/inter[0][2]
        xi2=inter[1][0]/inter[1][2]
        yi2=inter[1][1]/inter[1][2]
        xi3=inter[2][0]/inter[2][2]
        yi3=inter[2][1]/inter[2][2]
        print xi1,yi1,xi2,yi2,xi3,yi3

        self.transformation1=self.affine_trafo_3_points(xi1,yi1,xi2,yi2,xi3,yi3,
                                                        0.0,0.0,0.0,1.0,1.0,0.0)
        self.total_trafo=np.dot(self.transformation,self.transformation1)
        final2=np.dot(initial2,self.transformation)
        final1a=np.dot(initial,self.total_trafo)
        print np.dot(np.array([2,2,1]),self.transformation)
        print np.dot(np.array([2,4,1]),self.transformation)
        print "initial"
        print initial
        print "inter"
        print inter
        print "final2"
        print final2
        print "transformation"
        print self.transformation
        print "final1a"
        print final1a
        """

    def give_trafo_mat(self):
        """
        gives transformation matrix
        """
        mat = self.trafo
        return mat[0][0], mat[1][0], mat[2][0], \
               mat[0][1], mat[1][1], mat[2][1], \
               mat[0][2], mat[1][2], mat[2][2]

    def find_trafo_to_unity_rectangle(self, x1, y1, x2, y2, x3, y3, x4, y4):
        """
        transforms 4 points to unity rectangle
        point 1 -> (0,0)
        point 2 -> (0,1)
        point 3 -> (1,0)
        point 4 -> (1,1)
        """
        # permute if quadilateral not in correct order
        x1p, y1p, x2p, y2p, x3p, y3p, x4p, y4p = self.check_order(x1, y1, x2, y2, x3, y3, x4, y4)
        # find 3 points out of 4 points to transform
        o1, o2, o3, p1, p2, p3, q1, q2, q3 = self.find_three_points_to_transform(x1p, y1p, x2p, y2p, x3p, y3p, x4p, y4p)
        transformation_1 = self.find_transformation_points_to_rectangle(o1, o2, o3, p1, p2, p3, q1, q2, q3)
        # three points to make correct order with affine transformation
        initial = np.array([[x1, y1, 1.0],
                         [x2, y2, 1.0],
                         [x3, y3, 1.0]])
        # intermediate points
        inter = np.dot(initial, transformation_1)
        xi1 = inter[0][0] / inter[0][2]
        yi1 = inter[0][1] / inter[0][2]
        xi2 = inter[1][0] / inter[1][2]
        yi2 = inter[1][1] / inter[1][2]
        xi3 = inter[2][0] / inter[2][2]
        yi3 = inter[2][1] / inter[2][2]
        transformation_2 = self.affine_trafo_3_points(xi1, yi1, xi2, yi2, xi3, yi3,
                                                      0.0, 0.0, 0.0, 1.0, 1.0, 0.0)
        total_trafo = np.dot(transformation_1, transformation_2)
        return total_trafo

    def calc_distance_points(self, x1, y1, x2, y2):
        """
        calcs distance between two points
        """
        return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def check_order(self, x1, y1, x2, y2, x3, y3, x4, y4):
        """
        makes sure that quadrilateral has order 1-2-4-3
        calculates angles around
        """

        def angle(v1, v2):
            v1_l = np.sqrt(v1[0] ** 2 + v1[1] ** 2)
            v2_l = np.sqrt(v2[0] ** 2 + v2[1] ** 2)
            return math.acos(np.dot(v1, v2) / (v1_l * v2_l))

        v21 = np.array([x2 - x1, y2 - y1])
        v42 = np.array([x4 - x2, y4 - y2])
        v34 = np.array([x3 - x4, y3 - y4])
        v13 = np.array([x1 - x3, y1 - y3])
        angle_1 = angle(v21, -v42)
        angle_2 = angle(v42, -v34)
        angle_3 = angle(v34, -v13)
        angle_4 = angle(v13, -v21)
        #print (angle_1 + angle_2 + angle_3 + angle_4)
        if abs((angle_1 + angle_2 + angle_3 + angle_4) - 2 * math.pi) < 1e-9:
            return x1, y1, x2, y2, x3, y3, x4, y4
        else:
            return x1, y1, x2, y2, x4, y4, x3, y3

    def check_if_both_lines_collinear(self, x1, y1, x2, y2, x3, y3, x4, y4):
        """
        checks if both opposite edeges collinear
        """
        if self.collinear(x1, y1, x2, y2, x3, y3, x4, y4) and \
                self.collinear(x1, y1, x3, y3, x2, y2, x4, y4):
            return True
        else:
            return False

    def collinear(self, x1, y1, x2, y2, x3, y3, x4, y4):
        """
        checks if lines (x1,y1)-(x2,y2) and (x3,y3)-(x4,y4) collinear
        """

        def det(a, b, c, d):
            return a * d - c * b

        determinant = det(x1 - x2, y1 - y2, x3 - x4, y3 - y4)
        # print "determinant"
        # print determinant
        if abs(determinant) < 1e-9:
            return True
        else:
            return False

    def two_line_intersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
        """
        intersection of lines (x1,y1)-(x2,y2) and (x3,y3)-(x4,y4)
        """

        def det(a, b, c, d):
            return a * d - c * b

        x = det(det(x1, y1, x2, y2), (x1 - x2), det(x3, y3, x4, y4), (x3 - x4)) / \
            det(x1 - x2, y1 - y2, x3 - x4, y3 - y4)
        y = det(det(x1, y1, x2, y2), (y1 - y2), det(x3, y3, x4, y4), (y3 - y4)) / \
            det(x1 - x2, y1 - y2, x3 - x4, y3 - y4)
        return x, y

    def infinity_point(self, x1, y1, x2, y2):
        """
        finds point of line (of two parallel lines) end at infinity
        """
        x = x2 - x1
        y = y2 - y1
        d = 0.0  # inifinity
        return x, y, d

    def find_three_points_to_transform(self, x1, y1, x2, y2, x3, y3, x4, y4):
        """
        ...of points(x1,y1),(x2,y2),(x3,y3),(x4,y4)
        Three points are (o1,o2,o3),(p1,p2,p3),(q1,q2,q3)
        """
        # o
        # o1,o2,o3=x1,y1,1.0
        # P
        # check if lines (x1,y1)-(x2,y2) and (x3,y3)-(x4,y4) collinear
        if self.collinear(x1, y1, x2, y2, x3, y3, x4, y4):
            p1, p2, p3 = self.infinity_point(x1, y1, x2, y2)
            potential_points_1 = [1, 3]
        else:
            # lines 1-2, 3-4
            p1, p2 = self.two_line_intersection(x1, y1, x2, y2, x3, y3, x4, y4)
            p3 = 1.0  # divider of x1,y1
            if self.calc_distance_points(p1, p2, x1, y1) < self.calc_distance_points(p1, p2, x2, y2):
                potential_points_1 = [2, 4]
            else:
                potential_points_1 = [1, 3]
        # Q
        # check if lines (x1,y1)-(x3,y3) and (x2,y2)-(x4,y4) collinear
        if self.collinear(x1, y1, x3, y3, x2, y2, x4, y4):
            q1, q2, q3 = self.infinity_point(x1, y1, x3, y3)
            potential_points_2 = [1, 2]
        else:
            # lines 1-3, 2-4
            q1, q2 = self.two_line_intersection(x1, y1, x3, y3, x2, y2, x4, y4)
            q3 = 1.0  # divider of x1,y1
            if self.calc_distance_points(q1, q2, x1, y1) < self.calc_distance_points(q1, q2, x3, y3):
                potential_points_2 = [3, 4]
            else:
                potential_points_2 = [1, 2]

        if potential_points_1.count(1) == 1 and potential_points_2.count(1) == 1:
            o1, o2, o3 = x1, y1, 1.0
        if potential_points_1.count(2) == 1 and potential_points_2.count(2) == 1:
            o1, o2, o3 = x2, y2, 1.0
        if potential_points_1.count(3) == 1 and potential_points_2.count(3) == 1:
            o1, o2, o3 = x3, y3, 1.0
        if potential_points_1.count(4) == 1 and potential_points_2.count(4) == 1:
            o1, o2, o3 = x4, y4, 1.0
        return o1, o2, o3, p1, p2, p3, q1, q2, q3

    def find_transformation_points_to_rectangle(self, o1, o2, o3, p1, p2, p3, q1, q2, q3):
        """
        finds transformation that transforms points o,p,q to
        orthogonal rectangle. See Otto: p.40
        """
        trafo_mat_inv = np.array([[p1, p2, p3],
                               [q1, q2, q3],
                               [o1, o2, o3]])
        # print "trafo_mat_inv"
        # print trafo_mat_inv
        trafo_mat = linalg.inv(trafo_mat_inv)
        return trafo_mat

    def affine_trafo_3_points(self, x1, y1, x2, y2, x3, y3, x1d, y1d, x2d, y2d, x3d, y3d):
        """
        transforms three points to three points via affine transformation
        """
        # points to be transformed
        p = np.array([[x1, y1, 1.0],
                   [x2, y2, 1.0],
                   [x3, y3, 1.0]])
        # destination
        d = np.array([[x1d, y1d, 1.0],
                   [x2d, y2d, 1.0],
                   [x3d, y3d, 1.0]])
        # transformation
        t = np.dot(linalg.inv(p), d)
        return t


if __name__ == '__main__':
    """
    testing
    """
    print("#### TEST 1 ######")
    FourPoint(1, 3, 2, 2, 2, 4, 4, 3, 1, 3, 2, 2, 4, 3, 2, 4)
    print("#### TEST 2 ######")
    FourPoint(1, 3, 1, 1, 2, 2, 2, 1, 1, 3, 2, 2, 4, 3, 2, 4)
    print("#### TEST 3######")
    FourPoint(1, 4, 1, 2, 2, 2, 2, 1, 1, 3, 2, 2, 4, 3, 2, 4)
    print("#### TEST 4######")
    FourPoint(1, 4, 1, 2, 2, 1, 2, 2, 1, 3, 2, 2, 4, 3, 2, 4)
    print(FourPoint(1, 4, 1, 2, 2, 1, 2, 2, 1, 3, 2, 2, 4, 3, 2, 4).calc_distance_points(1, 1, 2, 2))
    #print(FourPoint.calc_distance_points(1, 1, 2, 2))
