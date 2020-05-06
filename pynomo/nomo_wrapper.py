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

from .nomo_axis import Nomo_Axis
from .nomo_axis_func import Axis_Wrapper, Axes_Wrapper
from .nomo_grid_box import Nomo_Grid_Box
from .nomo_grid import Nomo_Grid
from .nomograph3 import Nomograph3
from .nomo_axis import find_linear_ticks, find_log_ticks
from .nomo_axis import find_tick_directions, find_linear_ticks_smart
from .math_utilities import FourPoint

import math
import numpy as np
import scipy
import pyx

import copy
import re
import pprint
import random


class Nomo_Wrapper:
    """
    class for building nomographs consisting of many blocks (pieces connected by
    a line)
    """

    def __init__(self, params={}, paper_width=10.0, paper_height=10.0, filename='dummy.pdf'):
        # default parameters
        self.params_default = {
            'title_str': '',
            'title_x': paper_width / 2.0,
            'title_y': paper_height,
            'title_color': pyx.color.rgb.black,
            'title_box_width': paper_width / 2.2,
            'extra_texts': []}
        self.params = self.params_default
        self.params.update(params)
        self.block_stack = []
        self.filename = filename
        self.paper_width = paper_width
        self.paper_height = paper_height
        # self._build_axes_wrapper_()

    def add_block(self, nomo_block):
        """
        adds nomograph (Nomo_Block) to the wrapper
        """
        self.block_stack.append(nomo_block)
        # TODO: calculate transformation according to tag

    def _return_initial_shift_(self):
        """
        shifts (tanslates) axes off from zero
        """
        epsilon = 1e-3
        alpha1 = 1.0
        beta1 = 0.0
        gamma1 = epsilon
        alpha2 = 0.0
        beta2 = 1.0
        gamma2 = epsilon
        alpha3 = 0.0
        beta3 = 0.0
        gamma3 = 1.0
        return alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3

    def _calc_trafo_(self, x1, y1, x2, y2, x3, y3, x1d, y1d, x2d, y2d, x3d, y3d):
        """
        transforms three points to three points via rotation and scaling
        and transformation
        xd = alpha1*x+beta1*y+gamma1
        yd = alpha2*x+beta2*y+gamma2
        alpha3=0, beta3=0, gamma3=1.0
        """
        matt = np.array([[x1, y1, 1.0, 0.0, 0.0, 0.0],
                         [0, 0, 0, x1, y1, 1],
                         [x2, y2, 1, 0, 0, 0],
                         [0, 0, 0, x2, y2, 1],
                         [x3, y3, 1, 0, 0, 0],
                         [0, 0, 0, x3, y3, 1]])
        # print rank(mat)
        inverse = np.linalg.inv(matt)
        # vec=dot(inverse,[[x1d,y1d,x2d,y2d,x3d,y3d]])
        dest = np.array([x1d, y1d, x2d, y2d, x3d, y3d])
        vec = np.linalg.solve(matt, dest)
        alpha1 = vec[0]
        beta1 = vec[1]
        gamma1 = vec[2]
        alpha2 = vec[3]
        beta2 = vec[4]
        gamma2 = vec[5]
        alpha3 = 0.0
        beta3 = 0.0
        gamma3 = 1.0
        return alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3

    def _update_trafo_(self):
        """
        updates transformation to self.alpha1,...
        updates blocks
        """
        # self.axes_wrapper.fit_to_paper()
        # self.axes_wrapper._print_result_pdf_("dummy1.pdf")
        self.alpha1, self.beta1, self.gamma1, \
            self.alpha2, self.beta2, self.gamma2, \
            self.alpha3, self.beta3, self.gamma3 = self.axes_wrapper.give_trafo()
        # update last block trafos, note that trafo to align blocks should not be
        # changed
        for block in self.block_stack:
            block.change_last_transformation(alpha1=self.alpha1, beta1=self.beta1, gamma1=self.gamma1,
                                             alpha2=self.alpha2, beta2=self.beta2, gamma2=self.gamma2,
                                             alpha3=self.alpha3, beta3=self.beta3, gamma3=self.gamma3)

        #    def _update_block_trafos_(self):
        #        """
        #        updates (adds) transformation to blocks
        #        """
        #        for block in self.block_stack:
        #            block.add_transformation(alpha1=self.alpha1,beta1=self.beta1,gamma1=self.gamma1,
        #                           alpha2=self.alpha2,beta2=self.beta2,gamma2=self.gamma2,
        #                           alpha3=self.alpha3,beta3=self.beta3,gamma3=self.gamma3)

    def build_axes_wrapper(self):
        """
        builds full instance of class Axes_Wrapper to find
        transformation
        """
        self.axes_wrapper = Axes_Wrapper(paper_width=self.paper_width,
                                         paper_height=self.paper_height)
        for block in self.block_stack:
            for atom in block.atom_stack:
                if not atom.params['reference'] == True:
                    if atom.params['grid'] == True:
                        v0 = atom.params['v_start']
                        v1 = atom.params['v_stop']
                        u0 = atom.params['u_start']
                        u1 = atom.params['u_stop']
                        # first line of grid
                        self.axes_wrapper.add_axis(Axis_Wrapper(lambda u: atom.give_x_grid(u, v0),
                                                                lambda u: atom.give_y_grid(
                                                                    u, v0),
                                                                u0, u1))
                        # second line of grid
                        self.axes_wrapper.add_axis(Axis_Wrapper(lambda u: atom.give_x_grid(u, v1),
                                                                lambda u: atom.give_y_grid(
                                                                    u, v1),
                                                                u0, u1))
                        # third line of grid
                        self.axes_wrapper.add_axis(Axis_Wrapper(lambda v: atom.give_x_grid(u0, v),
                                                                lambda v: atom.give_y_grid(
                                                                    u0, v),
                                                                v0, v1))
                        # fourth line of grid
                        self.axes_wrapper.add_axis(Axis_Wrapper(lambda v: atom.give_x_grid(u1, v),
                                                                lambda v: atom.give_y_grid(
                                                                    u1, v),
                                                                v0, v1))
                    else:
                        self.axes_wrapper.add_axis(Axis_Wrapper(atom.give_x, atom.give_y,
                                                                atom.params['u_min'],
                                                                atom.params['u_max']))
                        # add extra axes to the list to find correct transformation
                        for extra_axis in atom.params['extra_params']:
                            self.axes_wrapper.add_axis(Axis_Wrapper(atom.give_x, atom.give_y,
                                                                    extra_axis['u_min'],
                                                                    extra_axis['u_max']))

                else:  # this atom is reference axis
                    self.axes_wrapper.add_axis(Axis_Wrapper(atom.give_x_ref, atom.give_y_ref,
                                                            atom.u_min_ref,
                                                            atom.u_max_ref))

    def do_transformation(self, method='scale paper', params=None):
        """
        main function to find and update transformation up to atoms
        """
        try:
            {'scale paper': self._do_scale_to_canvas_trafo_,
             'optimize': self._do_optimize_trafo_,
             'polygon': self._do_polygon_trafo_,
             'rotate': self._do_rotate_trafo_,
             'matrix': self._do_explicite_matrix_}[method](params)
        except KeyError:
            print("Wrong transformation identifier")

        # self.alpha1,self.beta1,self.gamma1,\
        # self.alpha2,self.beta2,self.gamma2,\
        # self.alpha3,self.beta3,self.gamma3 = self.axes_wrapper.give_trafo()
        self._update_trafo_()

    def _do_scale_to_canvas_trafo_(self, params):
        """
        Finds transformation to scale to pyx.canvas
        """
        self.axes_wrapper.fit_to_paper()
        # self.axes_wrapper._print_result_pdf_("dummy1_paper.pdf")

    def _do_optimize_trafo_(self, params):
        """
        Finds "optimal" transformation
        """
        self.axes_wrapper.optimize_transformation()
        # self.axes_wrapper._print_result_pdf_("dummy1_optimize.pdf")

    def _do_polygon_trafo_(self, params):
        """
        Finds "polygon" transformation
        """
        self.axes_wrapper.make_polygon_trafo()
        # self.axes_wrapper._print_result_pdf_("dummy1_polygon.pdf")

    def _do_rotate_trafo_(self, params):
        """
        Finds transformation to scale to pyx.canvas
        """
        self.axes_wrapper.rotate_canvas(params)
        # self.axes_wrapper._print_result_pdf_("dummy1_rotate.pdf")

    def _do_explicite_matrix_(self, params):
        """
        Does explicite matrix transformation
        """
        self.axes_wrapper.matrix_trafo(params)

    def draw_nomogram(self, canvas, post_func=None):
        """
        draws the nomogram = draws blocks, titles, etc.
        post_func is a function(canvas) to be draws after all
        """
        for block in self.block_stack:
            block.draw(canvas)
        self._draw_title_(canvas)
        self._draw_extra_texts_(canvas)
        if post_func is not None:
            post_func(canvas)
        if isinstance(self.filename, list):
            for filename_this in self.filename:
                if not re.compile(".eps$").search(filename_this, 1) is None:
                    canvas.writeEPSfile(filename_this)
                else:
                    if not re.compile(".svg$").search(filename_this, 1) is None:
                        canvas.writeSVGfile(filename_this)
                    else:
                        canvas.writePDFfile(filename_this)
        else:
            if not re.compile(".eps$").search(self.filename, 1) is None:
                canvas.writeEPSfile(self.filename)
            else:
                if not re.compile(".svg$").search(self.filename, 1) is None:
                    canvas.writeSVGfile(self.filename)
                else:
                    canvas.writePDFfile(self.filename)

    def _draw_title_(self, c):
        """
        draws title
        """
        # print self.params
        c.text(self.params['title_x'], self.params['title_y'],
               self.params['title_str'],
               [pyx.text.parbox(self.params['title_box_width']),
                pyx.text.halign.boxcenter, pyx.text.halign.flushcenter,
                self.params['title_color']])

    def _draw_extra_texts_(self, c):
        """
        draws extra texts
        """
        text_default = {'x': 0.0,
                        'y': 0.0,
                        'text': 'no text defined...',
                        'width': 5,
                        'pyx_extra_defs': []
                        }
        if len(self.params['extra_texts']) > 0:
            for texts in self.params['extra_texts']:
                for key in text_default:
                    if not key in texts:
                        texts[key] = text_default[key]
                x = texts['x']
                y = texts['y']
                text_str = texts['text']
                width = texts['width']
                pyx_extra_defs = texts['pyx_extra_defs']
                c.text(x, y, text_str, [
                       pyx.text.parbox(width)] + pyx_extra_defs)

    def align_blocks_old(self):
        """
        aligns blocks w.r.t. each other according to 'tag' fields
        in Atom params dictionary
        """
        #        # translate all blocks initially
        #        for block in self.block_stack:
        #            alpha1,beta1,gamma1,alpha2,beta2,gamma2,alpha3,beta3,gamma3=\
        #            self._return_initial_shift_()
        #            block.add_transformation(alpha1,beta1,gamma1,
        #                                     alpha2,beta2,gamma2,
        #                                     alpha3,beta3,gamma3)

        for idx1, block1 in enumerate(self.block_stack):
            for idx2, block2 in enumerate(self.block_stack):
                if idx2 > idx1:
                    for atom1 in block1.atom_stack:
                        for atom2 in block2.atom_stack:
                            if atom1.params['tag'] == atom2.params['tag'] \
                                    and not atom1.params['tag'] == 'none' \
                                    and not atom2.params['aligned']:  # align only once
                                # let's see if need for double align
                                double_aligned = False
                                for atom1d in block1.atom_stack:
                                    for atom2d in block2.atom_stack:
                                        if atom1d.params['dtag'] == atom2d.params['dtag'] \
                                                and not atom1d.params['dtag'] == 'none':
                                            # and not atom1d.params['tag']==atom1.params['tag']:
                                            # and not atom2d.params['aligned']: # align only once
                                            # do first pre-alignment
                                            #                                            alpha1,beta1,gamma1,alpha2,beta2,gamma2,alpha3,beta3,gamma3=\
                                            #                                            self._find_trafo_2_atoms_(atom1,atom2)
                                            #                                            block2.add_transformation(alpha1,beta1,gamma1,
                                            #                                                                      alpha2,beta2,gamma2,
                                            #                                                                      alpha3,beta3,gamma3)
                                            # double alignment
                                            # print "double aligning with tags %s %s" % (
                                            # atom1.params['tag'], atom1d.params['dtag'])
                                            #                                            alpha1,beta1,gamma1,alpha2,beta2,gamma2,alpha3,beta3,gamma3=\
                                            #                                            self._find_trafo_4_atoms_3_points_(atom1,atom1d,atom2,atom2d)
                                            #                                            block2.add_transformation(alpha1,beta1,gamma1,
                                            #                                                                      alpha2,beta2,gamma2,
                                            #                                                                      alpha3,beta3,gamma3)
                                            alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3 = \
                                                self._find_trafo_4_atoms_(
                                                    atom1, atom1d, atom2, atom2d)
                                            block2.add_transformation(alpha1, beta1, gamma1,
                                                                      alpha2, beta2, gamma2,
                                                                      alpha3, beta3, gamma3)
                                            double_aligned = True
                                        #                                            # DEBUG
                                        #                                            u_start_1=min(atom1.params['u_min'],atom1.params['u_max'])
                                        #                                            u_stop_1=max(atom1.params['u_min'],atom1.params['u_max'])
                                        #                                            u_start_1d=min(atom1d.params['u_min'],atom2.params['u_max'])
                                        #                                            u_stop_1d=max(atom1d.params['u_min'],atom2.params['u_max'])
                                        #                                            print "test if same:"
                                        #                                            print atom1.give_x(u_start_1)
                                        #                                            print atom1d.give_x(u_start_1d)
                                        #                                            print atom1.give_y(u_start_1)
                                        #                                            print atom1d.give_y(u_start_1d)
                                        #                                            print atom2.give_x(u_start_1)
                                        #                                            print atom2d.give_x(u_start_1d)
                                        #                                            print atom2.give_y(u_start_1)
                                        #                                            print atom2d.give_y(u_start_1d)
                                # print idx2
                                # print idx2
                                if not double_aligned:
                                    # print "Aligning with tag %s" % atom1.params['tag']
                                    alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3 = \
                                        self._find_trafo_2_atoms_(atom1, atom2)
                                    block2.add_transformation(alpha1, beta1, gamma1,
                                                              alpha2, beta2, gamma2,
                                                              alpha3, beta3, gamma3)
                                # align only once
                                atom2.params['aligned'] = True
        # let's make identity matrix that will be changed when optimized
        for block in self.block_stack:
            block.add_transformation()

    def align_blocks(self):
        """
        aligns blocks w.r.t. each other according to 'tag' fields
        in Atom params dictionary
        """
        #        # translate all blocks initially
        #        for block in self.block_stack:
        #            alpha1,beta1,gamma1,alpha2,beta2,gamma2,alpha3,beta3,gamma3=\
        #            self._return_initial_shift_()
        #            block.add_transformation(alpha1,beta1,gamma1,
        #                                     alpha2,beta2,gamma2,
        #                                     alpha3,beta3,gamma3)

        for idx1, block1 in enumerate(self.block_stack):
            for idx2, block2 in enumerate(self.block_stack):
                if idx2 > idx1:
                    for atom1 in block1.atom_stack:
                        for atom2 in block2.atom_stack:
                            if atom1.params['tag'] == atom2.params['tag'] \
                                    and not atom1.params['tag'] == 'none' \
                                    and block2.aligned == False:  # align only once
                                # let's see if need for double align
                                double_aligned = False
                                for atom2d in block2.atom_stack:
                                    for idx3, dblock3 in enumerate(
                                            self.block_stack):  # other blocks with potential dtags
                                        for atom3d in dblock3.atom_stack:
                                            if atom3d.params['dtag'] == atom2d.params['dtag'] \
                                                    and not atom3d.params['dtag'] == 'none' \
                                                    and idx3 <= idx1 \
                                                    and not idx3 == idx2 \
                                                    and double_aligned == False:  # make sure not block1 or block2 are checked agains block1 dtag
                                                # and not atom1d.params['tag']==atom1.params['tag']:
                                                # and not atom2d.params['aligned']: # align only once
                                                # do first pre-alignment
                                                #                                            alpha1,beta1,gamma1,alpha2,beta2,gamma2,alpha3,beta3,gamma3=\
                                                #                                            self._find_trafo_2_atoms_(atom1,atom2)
                                                #                                            block2.add_transformation(alpha1,beta1,gamma1,
                                                #                                                                      alpha2,beta2,gamma2,
                                                #                                                                      alpha3,beta3,gamma3)
                                                # double alignment
                                                # print "Double aligning with tags %s %s" % (
                                                # atom1.params['tag'], atom3d.params['dtag'])
                                                #                                            alpha1,beta1,gamma1,alpha2,beta2,gamma2,alpha3,beta3,gamma3=\
                                                #                                            self._find_trafo_4_atoms_3_points_(atom1,atom1d,atom2,atom2d)
                                                #                                            block2.add_transformation(alpha1,beta1,gamma1,
                                                #                                                                      alpha2,beta2,gamma2,
                                                #                                                                      alpha3,beta3,gamma3)
                                                alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3 = \
                                                    self._find_trafo_4_atoms_(
                                                        atom1, atom3d, atom2, atom2d)
                                                block2.add_transformation(alpha1, beta1, gamma1,
                                                                          alpha2, beta2, gamma2,
                                                                          alpha3, beta3, gamma3)
                                                double_aligned = True
                                                block2.aligned = True
                                                #                                            # DEBUG
                                                #                                            u_start_1=min(atom1.params['u_min'],atom1.params['u_max'])
                                                #                                            u_stop_1=max(atom1.params['u_min'],atom1.params['u_max'])
                                                #                                            u_start_1d=min(atom1d.params['u_min'],atom2.params['u_max'])
                                                #                                            u_stop_1d=max(atom1d.params['u_min'],atom2.params['u_max'])
                                                #                                            print "test if same:"
                                                #                                            print atom1.give_x(u_start_1)
                                                #                                            print atom1d.give_x(u_start_1d)
                                                #                                            print atom1.give_y(u_start_1)
                                                #                                            print atom1d.give_y(u_start_1d)
                                                #                                            print atom2.give_x(u_start_1)
                                                #                                            print atom2d.give_x(u_start_1d)
                                                #                                            print atom2.give_y(u_start_1)
                                                #                                            print atom2d.give_y(u_start_1d)
                                                # print idx2
                                                # print idx2
                                if not double_aligned:
                                    # print "Aligning with tag %s" % atom1.params['tag']
                                    alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3 = \
                                        self._find_trafo_2_atoms_(atom1, atom2)
                                    block2.add_transformation(alpha1, beta1, gamma1,
                                                              alpha2, beta2, gamma2,
                                                              alpha3, beta3, gamma3)
                                # atom2.params['aligned']=True # align only once
                                block2.aligned = True  # align only once
        # let's make identity matrix that will be changed when optimized
        for block in self.block_stack:
            block.add_transformation()

    def _find_trafo_4_atoms_3_points_(self, atom1a, atom1b, atom2a, atom2b):
        """
        transforms two points from one atom (scale) and one point from other atom (scale)
        into each other
        """

        def find_coords(atom1, atom2):
            # taking points from atom1
            u_start = min(atom1.params['u_min'], atom1.params['u_max'])
            u_stop = max(atom1.params['u_min'], atom1.params['u_max'])
            diff = u_stop - u_start
            u_start = u_start + 0.001 * diff
            u_stop = u_stop - 0.001 * diff
            # print "u_start: %g"%u_start
            # print "u_stop: %g"%u_stop
            x1_atom_2 = atom2.give_x(u_start)
            y1_atom_2 = atom2.give_y(u_start)
            x2_atom_2 = atom2.give_x(u_stop)
            y2_atom_2 = atom2.give_y(u_stop)

            x1_atom_1 = atom1.give_x(atom2.params['align_func'](u_start)) \
                + atom2.params['align_x_offset']
            y1_atom_1 = atom1.give_y(atom2.params['align_func'](u_start)) \
                + atom2.params['align_y_offset']
            x2_atom_1 = atom1.give_x(atom2.params['align_func'](u_stop)) \
                + atom2.params['align_x_offset']
            y2_atom_1 = atom1.give_y(atom2.params['align_func'](u_stop)) \
                + atom2.params['align_y_offset']
            return x1_atom_1, y1_atom_1, x2_atom_1, y2_atom_1, x1_atom_2, y1_atom_2, x2_atom_2, y2_atom_2

        # end find coords
        x1, y1, x2, y2, x1d, y1d, x2d, y2d = find_coords(atom2a, atom1a)
        # x3,y3,x4,y4,x3d,y3d,x4d,y4d=find_coords(atom1b,atom2b)
        x4, y4, x3, y3, x4d, y4d, x3d, y3d = find_coords(atom2b, atom1b)
        alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3 = \
            self._calc_trafo_(x1, y1, x2, y2, x3, y3,
                              x1d, y1d, x2d, y2d, x3d, y3d)
        # print (alpha1,beta1,gamma1,alpha2,beta2,gamma2,alpha3,beta3,gamma3)
        return alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3

    def _find_trafo_4_atoms_(self, atom1a, atom1b, atom2a, atom2b):
        """
        finds transformation that aligns two atoms in one block to
        two  atoms in second block, double alignment
        atom1a to atom2a
        atom1b to atom2b
        """

        def find_coords(atom1, atom2):
            # taking points from atom1
            u_start = min(atom1.params['u_min'], atom1.params['u_max'])
            u_stop = max(atom1.params['u_min'], atom1.params['u_max'])
            diff = u_stop - u_start
            # u_start=u_start+0.001*diff
            # u_stop=u_stop-0.001*diff
            # print "u_start: %g"%u_start
            # print "u_stop: %g"%u_stop
            x1_atom_2 = atom2.give_x(u_start)
            y1_atom_2 = atom2.give_y(u_start)
            x2_atom_2 = atom2.give_x(u_stop)
            y2_atom_2 = atom2.give_y(u_stop)

            x1_atom_1 = atom1.give_x(atom2.params['align_func'](u_start)) \
                + atom2.params['align_x_offset']
            y1_atom_1 = atom1.give_y(atom2.params['align_func'](u_start)) \
                + atom2.params['align_y_offset']
            x2_atom_1 = atom1.give_x(atom2.params['align_func'](u_stop)) \
                + atom2.params['align_x_offset']
            y2_atom_1 = atom1.give_y(atom2.params['align_func'](u_stop)) \
                + atom2.params['align_y_offset']
            return x1_atom_1, y1_atom_1, x2_atom_1, y2_atom_1, x1_atom_2, y1_atom_2, x2_atom_2, y2_atom_2

        # end find coords
        x1, y1, x2, y2, x1d, y1d, x2d, y2d = find_coords(atom2a, atom1a)
        # x3,y3,x4,y4,x3d,y3d,x4d,y4d=find_coords(atom1b,atom2b)
        x3, y3, x4, y4, x3d, y3d, x4d, y4d = find_coords(atom2b, atom1b)
        # DEBUG
        if False:
            # print "x1: %f y1: %f x2: %f y2: %f x1d: %f y1d: %f x2d: %f y2d: %f" % (x1, y1, x2, y2, x1d, y1d, x2d, y2d)
            # print "x3: %f y3: %f x4: %f y4: %f x3d: %f y3d: %f x4d: %f y4d: %f" % (x3, y3, x4, y4, x3d, y3d, x4d, y4d)
            c = pyx.canvas.canvas()
            c.fill(pyx.path.circle(x1, y1, 0.02))
            c.text(x1, y1, '1')
            c.fill(pyx.path.circle(x2, y2, 0.03))
            c.text(x2, y2, '2')
            c.fill(pyx.path.circle(x3, y3, 0.04))
            c.text(x3, y3, '3')
            c.fill(pyx.path.circle(x4, y4, 0.05))
            c.text(x4, y4, '4')
            c.fill(pyx.path.circle(x1d, y1d, 0.02))
            c.text(x1d, y1d, '1d')
            c.fill(pyx.path.circle(x2d, y2d, 0.03))
            c.text(x2d, y2d, '2d')
            c.fill(pyx.path.circle(x3d, y3d, 0.04))
            c.text(x3d, y3d, '3d')
            c.fill(pyx.path.circle(x4d, y4d, 0.05))
            c.text(x4d, y4d, '4d')
            c.writePDFfile('double_debug.pdf')

        #        alpha1,beta1,gamma1,alpha2,beta2,gamma2,alpha3,beta3,gamma3=\
        #        self._calc_transformation_matrix_(x1,y1,x2,y2,x3,y3,x4,y4,\
        #                                                 x1d,y1d,x2d,y2d,x3d,y3d,x4d,y4d)
        alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3 = \
            FourPoint(x1, y1, x2, y2, x3, y3, x4, y4,
                      x1d, y1d, x2d, y2d, x3d, y3d, x4d, y4d).give_trafo_mat()
        # print (alpha1,beta1,gamma1,alpha2,beta2,gamma2,alpha3,beta3,gamma3)
        return alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3

    def _calc_transformation_matrix_(self, x1, y1, x2, y2, x3, y3, x4, y4,
                                     x1d, y1d, x2d, y2d, x3d, y3d, x4d, y4d):
        """
        copied from nomo_axis_func.py
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

        def _make_row_(coordinate='x', x=1.0, y=1.0, coord_value=1.0):
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

        row1, const1 = _make_row_(coordinate='x', coord_value=x2d, x=x2, y=y2)
        row2, const2 = _make_row_(coordinate='y', coord_value=y2d, x=x2, y=y2)
        row3, const3 = _make_row_(coordinate='x', coord_value=x1d, x=x1, y=y1)
        row4, const4 = _make_row_(coordinate='y', coord_value=y1d, x=x1, y=y1)
        row5, const5 = _make_row_(coordinate='x', coord_value=x4d, x=x4, y=y4)
        row6, const6 = _make_row_(coordinate='y', coord_value=y4d, x=x4, y=y4)
        row7, const7 = _make_row_(coordinate='x', coord_value=x3d, x=x3, y=y3)
        row8, const8 = _make_row_(coordinate='y', coord_value=y3d, x=x3, y=y3)

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

    def _find_trafo_2_atoms_(self, atom1, atom2):
        """
        finds transformation that aligns atom2 to atom1
        In practice takes 0.3 from endpoints and a third point in 90 degree
        to form a triangle for both atoms to be aligned
        """
        # taking points from atom1
        u_start = min(atom2.params['u_min'], atom2.params['u_max'])
        u_stop = max(atom2.params['u_min'], atom2.params['u_max'])
        diff = u_stop - u_start
        u_start = u_start + 0.3 * diff
        u_stop = u_stop - 0.3 * diff
        # print "u_start: %g"%u_start
        # print "u_stop: %g"%u_stop
        x1_atom_2 = atom2.give_x(u_start)
        y1_atom_2 = atom2.give_y(u_start)
        x2_atom_2 = atom2.give_x(u_stop)
        y2_atom_2 = atom2.give_y(u_stop)

        x1_atom_1 = atom1.give_x(atom2.params['align_func'](u_start)) \
            + atom2.params['align_x_offset']
        y1_atom_1 = atom1.give_y(atom2.params['align_func'](u_start)) \
            + atom2.params['align_y_offset']
        x2_atom_1 = atom1.give_x(atom2.params['align_func'](u_stop)) \
            + atom2.params['align_x_offset']
        y2_atom_1 = atom1.give_y(atom2.params['align_func'](u_stop)) \
            + atom2.params['align_y_offset']

        x3_atom_1 = x1_atom_1 + (y2_atom_1 - y1_atom_1) * 0.01
        y3_atom_1 = y1_atom_1 - (x2_atom_1 - x1_atom_1) * 0.01

        x3_atom_2 = x1_atom_2 + (y2_atom_2 - y1_atom_2) * 0.01
        y3_atom_2 = y1_atom_2 - (x2_atom_2 - x1_atom_2) * 0.01
        alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3 = \
            self._calc_trafo_(x1_atom_2, y1_atom_2, x2_atom_2, y2_atom_2, x3_atom_2, y3_atom_2,
                              x1_atom_1, y1_atom_1, x2_atom_1, y2_atom_1, x3_atom_1, y3_atom_1)
        return alpha1, beta1, gamma1, alpha2, beta2, gamma2, alpha3, beta3, gamma3


class Nomo_Block(object):
    """
    class to hold separate nomograph blocks connected by a single line in
    order to build the whole nomograph consisting of multiple blocks
    """

    def __init__(self, mirror_x=False, mirror_y=False):
        """
        if mirror=True the transformation wrt to other blocks is mirrored
        """
        # self.super.__init__()
        if mirror_x == True:  # if make mirror w.r.t x-axis
            self.x_mirror = -1.0
        else:
            self.x_mirror = 1.0
        if mirror_y == True:  # if make mirror w.r.t x-axis
            self.y_mirror = -1.0
        else:
            self.y_mirror = 1.0
        """
        Idea is that block has one own tranformation that aligns it with respect to other
        blocks and one overall transformation that optimizes axes w.r.t. paper size.
        Overall transformation is calculated using class Axis_Wrapper in nomo_axis_func.py
        in wrapper class Nomo_Wrapper.
        """
        # initial transformation
        self.atom_stack = []  # atoms
        self.trafo_stack = []  # stack for transformation matrices for block
        self.axis_wrapper_stack = []  # stack of Axis_Wrapper objects in order to calculate
        # general block parameters like highest point, etc.
        self.ref_block_texts = []  # handle for additional texts in block
        self.ref_block_lines = []  # handle for additional lines in block
        self.ref_block_params = {}  # handle for params that define the block
        self.add_transformation()  # adds initial unit transformation
        self.aligned = False  # block is not aligned, and should be aligned only once

    def add_atom(self, atom):
        """
        adds atom to the block
        """
        self.atom_stack.append(atom)

    def add_transformation(self, alpha1=1.0, beta1=0.0, gamma1=0.0,
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
        self._calculate_total_trafo_mat_()  # update coeffs (also in atoms)

    def change_last_transformation(self, alpha1=1.0, beta1=0.0, gamma1=0.0,
                                   alpha2=0.0, beta2=1.0, gamma2=0.0,
                                   alpha3=0.0, beta3=0.0, gamma3=1.0):
        """
        adds transformation to be applied as a basis.
        all transformation matrices are multiplied together
        """
        trafo_mat = np.array([[alpha1, beta1, gamma1],
                              [alpha2, beta2, gamma2],
                              [alpha3, beta3, gamma3]])
        self.trafo_stack.pop()  # last away
        self.trafo_stack.append(trafo_mat)
        self._calculate_total_trafo_mat_()  # update coeffs (also in atoms)

    def _give_trafo_x_(self, x, y):
        """
        transformed x-coordinate
        """
        return ((self.alpha1 * x + self.beta1 * y + self.gamma1)
                / (self.alpha3 * x + self.beta3 * y + self.gamma3))

    def _give_trafo_y_(self, x, y):
        """
        transformed y-coordinate
        """
        return ((self.alpha2 * x + self.beta2 * y + self.gamma2)
                / (self.alpha3 * x + self.beta3 * y + self.gamma3))

    def _calculate_total_trafo_mat_(self):
        """
        calculates total transformation matrix and
        master coeffs self.alpha1,self.beta1,...
        """
        stack_copy = copy.copy(self.trafo_stack)
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
        self._set_trafo_to_atoms()

    def _set_trafo_to_atoms(self):
        """
        sets overall transformation to all atoms
        """
        for atom in self.atom_stack:
            atom.set_trafo(alpha1=self.alpha1, beta1=self.beta1, gamma1=self.gamma1,
                           alpha2=self.alpha2, beta2=self.beta2, gamma2=self.gamma2,
                           alpha3=self.alpha3, beta3=self.beta3, gamma3=self.gamma3)

    def draw(self, canvas):
        """
        draws the Atoms of block
        """
        for atom in self.atom_stack:
            # print "atom"
            atom.draw(canvas)

    def _calc_y_limits_original_(self):
        """
        calculates min y and max y coordinates using axis_wrapper_stack
        that contains original coordinates without further transformations.
        This function is intended mainly for reference axis-calculations
        """
        min_y = 1.0e120  # large number
        max_y = -1.0e120  # large number
        for axis in self.axis_wrapper_stack:
            dummy, min_value = axis.calc_lowest_point()
            if min_value < min_y:
                min_y = min_value
            dummy, max_value = axis.calc_highest_point()
            if max_value > max_y:
                max_y = max_value
        return min_y, max_y

    def set_reference_axes(self):
        """
        Axes that are set to be reference axes (pivot lines)
        are tuned w.r.t. to
        other "real" axes that have values.
        """
        min_y, max_y = self._calc_y_limits_original_()
        # print "min_y,max_y"
        # print min_y,max_y
        y_range = max_y - min_y
        for atom in self.atom_stack:
            if atom.params['reference'] == True:
                y_addition = y_range * atom.params['reference_padding']
                # print "y_addition"
                # print y_addition
                atom.f_ref = atom.f
                atom.g_ref = lambda u: u
                atom.u_min_ref = min_y - y_addition
                atom.u_max_ref = max_y + y_addition
                atom.params['tick_levels'] = 5
                atom.params['tick_text_levels'] = 5

    def _build_axes_wrapper_block_(self):
        """
        builds full instance of class Axes_Wrapper to find
        transformation for block
        to be called after set_block function
        """
        self.axes_wrapper = Axes_Wrapper(paper_width=self.width,
                                         paper_height=self.height)
        for atom in self.atom_stack:
            if not atom.params['reference'] == True:
                self.axes_wrapper.add_axis(Axis_Wrapper(atom.give_x, atom.give_y,
                                                        atom.params['u_min'],
                                                        atom.params['u_max']))
            else:  # this atom is reference axis = pivot line
                self.axes_wrapper.add_axis(Axis_Wrapper(atom.give_x_ref, atom.give_y_ref,
                                                        atom.u_min_ref,
                                                        atom.u_max_ref))

    def _scale_to_box_(self):
        """
        adds transformation to scale to box. To be used to scale to paper
        """
        self.axes_wrapper.fit_to_paper()
        alpha1, beta1, gamma1, \
            alpha2, beta2, gamma2, \
            alpha3, beta3, gamma3 = self.axes_wrapper.give_trafo()
        self.add_transformation(alpha1=alpha1, beta1=beta1, gamma1=gamma1,
                                alpha2=alpha2, beta2=beta2, gamma2=gamma2,
                                alpha3=alpha3, beta3=beta3, gamma3=gamma3)


class Nomo_Block_Type_1(Nomo_Block):
    """
    type F1+F2+F3=0
    """

    def __init__(self, mirror_x=False, mirror_y=False):
        super(Nomo_Block_Type_1, self).__init__(
            mirror_x=mirror_x, mirror_y=mirror_y)

    def define_F1(self, params):
        """
        defines function F1
        """
        params['F'] = lambda u: -1.0 * self.x_mirror
        params['G'] = lambda u: params['function'](u) * self.y_mirror
        self.atom_F1 = Nomo_Atom(params)
        self.add_atom(self.atom_F1)
        # for inital axis calculations
        self.F1_axis_ini = Axis_Wrapper(f=params['F'], g=params['G'],
                                        start=params['u_min'], stop=params['u_max'])
        # self.axis_wrapper_stack.append(self.F1_axis)

    def define_F2(self, params):
        """
        defines function F2
        """
        params['F'] = lambda u: 0.0
        params['G'] = lambda u: -0.5 * params['function'](u) * self.y_mirror
        self.atom_F2 = Nomo_Atom(params)
        self.add_atom(self.atom_F2)
        # for axis calculations
        self.F2_axis_ini = Axis_Wrapper(f=params['F'], g=params['G'],
                                        start=params['u_min'], stop=params['u_max'])
        # self.axis_wrapper_stack.append(self.F2_axis)

    def define_F3(self, params):
        """
        defines function F3
        """
        params['F'] = lambda u: 1.0 * self.x_mirror
        params['G'] = lambda u: 1.0 * params['function'](u) * self.y_mirror
        self.atom_F3 = Nomo_Atom(params)
        self.add_atom(self.atom_F3)
        # for axis calculations original parameters
        self.F3_axis_ini = Axis_Wrapper(f=params['F'], g=params['G'],
                                        start=params['u_min'], stop=params['u_max'])
        # self.axis_wrapper_stack.append(self.F3_axis)

    def set_block(self, width=10.0, height=10.0, proportion=1.0):
        """
        sets original width, height and x-distance proportion for the nomogram before
        transformations
        """
        self.width = width
        self.height = height
        p = proportion
        delta_1 = proportion * width / (1 + proportion)
        delta_3 = width / (proportion + 1)
        # print delta_1
        # print delta_3
        if True:
            x_dummy, f1_max = self.F1_axis_ini.calc_highest_point()
            x_dummy, f1_min = self.F1_axis_ini.calc_lowest_point()
            f1_mean = (f1_max + f1_min) / 2.0
            x_dummy, f2_max = self.F2_axis_ini.calc_highest_point()
            x_dummy, f2_min = self.F2_axis_ini.calc_lowest_point()
            f2_mean = (f2_max + f2_min) / 2.0
            x_dummy, f3_max = self.F3_axis_ini.calc_highest_point()
            x_dummy, f3_min = self.F3_axis_ini.calc_lowest_point()
            f3_mean = (f3_max + f3_min) / 2.0
            # this tries to align lines w.r.t each other
            diff_1 = f1_mean - f2_mean
            diff_3 = f3_mean - f2_mean
            corr = diff_1 + diff_3
            self.F1_axis_ini.g = lambda u: self.atom_F1.params['G'](
                u) - diff_1 + corr / 2.0
            self.F3_axis_ini.g = lambda u: self.atom_F3.params['G'](
                u) - diff_3 + corr / 2.0
            # print "diff_1: %g"%diff_1
            # print "diff_3: %g"%diff_3
            # print "corr: %g"%corr
        # again
        x_dummy, f1_max = self.F1_axis_ini.calc_highest_point()
        x_dummy, f1_min = self.F1_axis_ini.calc_lowest_point()
        x_dummy, f2_max = self.F2_axis_ini.calc_highest_point()
        x_dummy, f2_min = self.F2_axis_ini.calc_lowest_point()
        x_dummy, f3_max = self.F3_axis_ini.calc_highest_point()
        x_dummy, f3_min = self.F3_axis_ini.calc_lowest_point()
        # assume mu_3=1, mu_1 = proportion for a moment
        max_y = max(1.0 * p * f1_max, p / (1.0 + p) * f2_max, 1.0 * f3_max)
        min_y = min(p * f1_max, p / (1 + p) * f2_max, f3_max)
        y_distance = max_y - min_y
        multiplier = height / y_distance
        mu_1 = p * multiplier
        mu_3 = multiplier
        # redefine scaled functions
        self.atom_F1.f = lambda u: self.F1_axis_ini.f(u) * delta_1
        self.atom_F1.g = lambda u: self.F1_axis_ini.g(u) * mu_1
        self.atom_F2.f = lambda u: self.F2_axis_ini.f(u)
        self.atom_F2.g = lambda u: self.F2_axis_ini.g(
            u) * 2 * (mu_1 * mu_3) / (mu_1 + mu_3)
        self.atom_F3.f = lambda u: self.F3_axis_ini.f(u) * delta_3
        self.atom_F3.g = lambda u: self.F3_axis_ini.g(u) * mu_3

        self.F1_axis = Axis_Wrapper(f=self.atom_F1.f, g=self.atom_F1.g,
                                    start=self.atom_F1.params['u_min'],
                                    stop=self.atom_F1.params['u_max'])
        self.axis_wrapper_stack.append(self.F1_axis)
        self.F2_axis = Axis_Wrapper(f=self.atom_F2.f, g=self.atom_F2.g,
                                    start=self.atom_F2.params['u_min'],
                                    stop=self.atom_F2.params['u_max'])
        self.axis_wrapper_stack.append(self.F2_axis)

        self.F3_axis = Axis_Wrapper(f=self.atom_F3.f, g=self.atom_F3.g,
                                    start=self.atom_F3.params['u_min'],
                                    stop=self.atom_F3.params['u_max'])
        self.axis_wrapper_stack.append(self.F3_axis)
        self.set_reference_axes()


class Nomo_Block_Type_2(Nomo_Block):
    """
    type F1=F2*F3
    """

    def __init__(self, mirror_x=False, mirror_y=False):
        super(Nomo_Block_Type_2, self).__init__(
            mirror_x=mirror_x, mirror_y=mirror_y)

    def define_F1(self, params):
        """
        defines function F1
        """
        self.F1 = params['function']
        self.params_F1 = params

    def define_F2(self, params):
        """
        defines function F2
        """
        self.F2 = params['function']
        self.params_F2 = params

    def define_F3(self, params):
        """
        defines function F3
        """
        self.F3 = params['function']
        self.params_F3 = params

    def set_block(self, height=10.0, width=10.0):
        """
        sets the N-nomogram of the block using geometrical approach from Levens
        f1 and f3 scales are set to equal length by using multipliers c1 and c2
        """
        self.width = width
        self.height = height
        length_f1_ini = max(self.F1(self.params_F1['u_min']), self.F1(self.params_F1['u_max'])) - \
            min(self.F1(self.params_F1['u_min']),
                self.F1(self.params_F1['u_max']))
        length_f3_ini = max(self.F3(self.params_F3['u_min']), self.F3(self.params_F3['u_max'])) - \
            min(self.F3(self.params_F3['u_min']),
                self.F3(self.params_F3['u_max']))
        K1 = width
        #    length_f1=length_f3
        m1 = height / length_f1_ini
        m3 = height / length_f3_ini
        f1_min = m1 * \
            min(self.F1(self.params_F1['u_min']),
                self.F1(self.params_F1['u_max']))
        f3_max = m3 * \
            max(self.F3(self.params_F3['u_min']),
                self.F3(self.params_F3['u_max']))
        y_offset_1_3 = f1_min - (height - f3_max)

        K = np.sqrt(height ** 2 + width ** 2)
        self.params_F1['F'] = lambda u: 0.0
        self.params_F1['G'] = lambda u: ((self.F1(u)) * m1) * self.y_mirror
        self.atom_F1 = Nomo_Atom(self.params_F1)
        self.add_atom(self.atom_F1)
        def x_func(u): return (width - K * m3 /
                               (m1 * self.F2(u) + m3) * width / K)
        self.params_F2['F'] = lambda u: (
            width - K * m3 / (m1 * self.F2(u) + m3) * width / K) * self.x_mirror
        self.params_F2['G'] = lambda u: (height - K * m3 / (m1 * self.F2(u) + m3) * height / K + x_func(
            u) / width * y_offset_1_3) * self.y_mirror
        self.atom_F2 = Nomo_Atom(self.params_F2)
        self.add_atom(self.atom_F2)
        self.params_F3['F'] = lambda u: (width) * self.x_mirror
        self.params_F3['G'] = lambda u: (
            (height - (self.F3(u)) * m3) + y_offset_1_3) * self.y_mirror
        self.atom_F3 = Nomo_Atom(self.params_F3)
        self.add_atom(self.atom_F3)

        self.F1_axis = Axis_Wrapper(f=self.params_F1['F'], g=self.params_F1['G'],
                                    start=self.params_F1['u_min'], stop=self.params_F1['u_max'])
        self.axis_wrapper_stack.append(self.F1_axis)

        self.F2_axis = Axis_Wrapper(f=self.params_F2['F'], g=self.params_F2['G'],
                                    start=self.params_F2['u_min'], stop=self.params_F2['u_max'])
        self.axis_wrapper_stack.append(self.F2_axis)

        self.F3_axis = Axis_Wrapper(f=self.params_F3['F'], g=self.params_F3['G'],
                                    start=self.params_F3['u_min'], stop=self.params_F3['u_max'])
        self.axis_wrapper_stack.append(self.F3_axis)
        self.set_reference_axes()

    def set_block_old(self, height=10.0, width=10.0):
        """
        sets the N-nomogram of the block using geometrical approach from Levens
        f1 and f3 scales are set to equal length by using multipliers c1 and c2
        """
        self.width = width
        self.height = height
        length_f1_ini = max(
            self.F1(self.params_F1['u_min']), self.F1(self.params_F1['u_max']))
        length_f3_ini = max(
            self.F3(self.params_F3['u_min']), self.F3(self.params_F3['u_max']))
        c1 = length_f3_ini / length_f1_ini
        c2 = c1
        length_f1 = max(
            c1 * self.F1(self.params_F1['u_min']), c1 * self.F1(self.params_F1['u_max']))
        length_f3 = max(self.F3(self.params_F3['u_min']), self.F3(
            self.params_F3['u_max']))
        #    length_f1=length_f3
        m1 = height / length_f1
        m3 = height / length_f3
        K = np.sqrt(height ** 2 + width ** 2)
        self.params_F1['F'] = lambda u: 0.0
        self.params_F1['G'] = lambda u: (c1 * self.F1(u) * m1) * self.y_mirror
        self.atom_F1 = Nomo_Atom(self.params_F1)
        self.add_atom(self.atom_F1)
        self.params_F2['F'] = lambda u: (
            width - K * m3 / (m1 * c2 * self.F2(u) + m3) * width / K) * self.x_mirror
        self.params_F2['G'] = lambda u: (
            height - K * m3 / (m1 * c2 * self.F2(u) + m3) * height / K) * self.y_mirror
        self.atom_F2 = Nomo_Atom(self.params_F2)
        self.add_atom(self.atom_F2)
        self.params_F3['F'] = lambda u: (width) * self.x_mirror
        self.params_F3['G'] = lambda u: (
            height - self.F3(u) * m1) * self.y_mirror
        self.atom_F3 = Nomo_Atom(self.params_F3)
        self.add_atom(self.atom_F3)

        self.F1_axis = Axis_Wrapper(f=self.params_F1['F'], g=self.params_F1['G'],
                                    start=self.params_F1['u_min'], stop=self.params_F1['u_max'])
        self.axis_wrapper_stack.append(self.F1_axis)

        self.F2_axis = Axis_Wrapper(f=self.params_F2['F'], g=self.params_F2['G'],
                                    start=self.params_F2['u_min'], stop=self.params_F2['u_max'])
        self.axis_wrapper_stack.append(self.F2_axis)

        self.F3_axis = Axis_Wrapper(f=self.params_F3['F'], g=self.params_F3['G'],
                                    start=self.params_F3['u_min'], stop=self.params_F3['u_max'])
        self.axis_wrapper_stack.append(self.F3_axis)
        self.set_reference_axes()


class Nomo_Block_Type_3(Nomo_Block):
    """
    type F1+F2+...+FN=0 parallel line nomogram
    """

    def __init__(self, mirror_x=False, mirror_y=False):
        super(Nomo_Block_Type_3, self).__init__(
            mirror_x=mirror_x, mirror_y=mirror_y)
        self.F_stack = []  # stack of function definitions
        self.shift_stack = []
        self.N = 0  # number of lines
        axes_wrapper_N = Axes_Wrapper()  # to calculate bounding box

    def add_F(self, params):
        """
        appends function F
        """
        self.F_stack.append(params)
        self.N = self.N + 1
        self.shift_stack.append(0)  # initial correction 0

    def set_block(self, height=10.0, width=10.0, reference_padding=0.2,
                  reference_titles=[], reference_color=pyx.color.rgb.black):
        """
        sets up equations in block after definitions are given
        """
        # builds self.x_func,self.y_func,
        # self.xR_func and self.yR_func
        self.width = width
        self.height = height
        self.reference_padding = reference_padding
        self.reference_titles = reference_titles
        self.reference_color = reference_color
        self._make_definitions_()
        self._calculate_shifts_()
        for idx in range(1, self.N + 1, 1):
            params = self.F_stack[idx - 1]  # original parameters
            params['F'] = self._give_x_func_(idx)
            params['G'] = self._give_y_func_(idx)
            temp_atom = Nomo_Atom(params)
            self.add_atom(temp_atom)
            temp_axis = Axis_Wrapper(f=temp_atom.f, g=temp_atom.g,
                                     start=temp_atom.params['u_min'],
                                     stop=temp_atom.params['u_max'])
            self.axis_wrapper_stack.append(temp_axis)
        # let's make reference axis atoms
        for ref_para in self.ref_params:
            self.add_atom(Nomo_Atom(ref_para))
        # build reference axes
        self.set_reference_axes()
        # scale to fit the paper
        self._build_axes_wrapper_block_()
        self._scale_to_box_()

    def _give_x_func_(self, idx):
        """
        copied trick to solve function defitions inside loop
        (I could not figure out how to use lambda...)
        this is quite stupid code, but can't help ?
        """

        def f(u): return self.x_func[idx](u)

        return f

    def _give_y_func_(self, idx):
        """
        copied trick to solve function defitions inside loop
        (I could not figure out how to use lambda...)
        this is quite stupid code, but can't help ?
        """

        def f(u): return self.y_func[idx](u)

        return f

    def _calculate_shifts_(self):
        """
        calculates line positions (in y-direction) in order to
        make line center points as concentric as possible by
        using shifts that are additions to the functions
        """
        mean_values = []
        self.shifts = []
        # calculate means
        for idx in range(1, self.N + 1, 1):
            params = self.F_stack[idx - 1]
            min_value = self._makeDoY_(idx)(params['u_min'])
            max_value = self._makeDoY_(idx)(params['u_max'])
            if idx == 1 or idx == self.N:
                min_value = min_value * 2
                max_value = max_value * 2
            if max_value < min_value:
                min_value, max_value = max_value, min_value
            mean_values.append((min_value + max_value) / 2.0)
        mean_value = np.mean(mean_values)
        # calculate needed additions to funcs = shifts
        shift_sum = 0
        for idx in range(1, self.N + 1, 1):
            difference = mean_values[idx - 1] - mean_value
            shift = difference / self._calc_shift_(idx)
            if idx == 1 or idx == self.N:
                shift = difference / self._calc_shift_(idx) * 0.5
            self.shifts.append(shift)
            shift_sum = shift_sum + shift
        # let's divide shift sum to all shifts = correction
        correction = shift_sum / (self.N - 1)  # ends get factor 0.5
        for idx in range(1, self.N + 1, 1):
            self.shift_stack[idx - 1] = -(self.shifts[idx - 1] - correction)
        self.shift_stack[0] = -(self.shifts[0] - correction / 2)
        self.shift_stack[self.N - 1] = - \
            (self.shifts[self.N - 1] - correction / 2)

    def _make_definitions_(self):
        """
        defines functions. Copied originally from nomograp_N_lin.py
        """
        N = self.N
        self.x_func = {}  # x coordinate to map points into pyx.canvas
        self.y_func = {}  # y coordinate to map points into pyx.canvas
        self.xR_func = {}  # turning-point axis
        self.yR_func = {}
        fn2x_table = {}  # mapping from function fn to x-coord
        r_table = {}
        # how many x values are needed including turning axes
        x_max = (N - 4) + N
        self.x_scaling = self.width / x_max  # to make correct width
        fn2x_table[1] = 0.0
        fn2x_table[2] = 1.0
        fn2x_table[N] = x_max * 1.0
        fn2x_table[N - 1] = x_max - 1.0
        # function numbers between reflection axes
        f_mid = range(3, (N - 1), 1)
        x_mid = [(f - 3) * 2.0 + 3.0 for f in f_mid]
        for idx, x in enumerate(x_mid):
            fn2x_table[f_mid[idx]] = x * 1.0
            r_table[idx + 1] = x - 1.0
        r_table[N - 3] = x_max - 2.0
        """
        fn2x_table: table of x-coordinates of functions
        r_table: table of x-coordinates of functions
        """
        # print "fn2x_table "
        # print fn2x_table
        # make fn functions
        for idx in range(2, N, 1):
            self.x_func[idx] = self._makeDoX_(fn2x_table[idx])
            self.y_func[idx] = self._makeDoY_(idx)
        self.x_func[1] = lambda x: fn2x_table[1] * 1.0 * self.x_mirror
        self.x_func[N] = lambda x: fn2x_table[N] * 1.0 * self.x_mirror
        # self.y_func[1]=lambda u:self.functions['f1'](u)
        self.y_func[1] = lambda u: (self.F_stack[0]['function'](u)
                                    + self.shift_stack[0]) * self.y_mirror
        # self.y_func[N]=lambda u:(-1)**(N+1)*self.functions['f%i'%N](u)
        self.y_func[N] = lambda u: (-1) ** (N + 1) * (self.F_stack[N - 1]['function'](u)
                                                      + self.shift_stack[N - 1]) * self.y_mirror
        # make reflection axes
        self.ref_params = []
        ref_para_ini = {  # this is for reference
            'u_min': 0.0,
            'u_max': 1.0,
            'function': lambda u: u,
            'title': 'R',
            'reference': True
        }
        for idx in range(1, N - 2):
            ref_para = copy.copy(ref_para_ini)
            ref_para['F'] = self._makeDoX_(r_table[idx])
            ref_para['G'] = lambda y: y
            ref_para['reference_padding'] = self.reference_padding
            ref_para['title_color'] = self.reference_color
            ref_para['text_color'] = self.reference_color
            ref_para['axis_color'] = self.reference_color
            if len(self.reference_titles) >= idx:
                ref_para['title'] = self.reference_titles[idx - 1]
            else:
                ref_para['title'] = 'R$_' + repr(idx) + '$'
            self.ref_params.append(ref_para)

    def _makeDoX_(self, value):
        """
        copied trick to solve function defitions inside loop
        (I could not figure out how to use lambda...)
        """

        def f(dummy): return value * self.x_mirror

        return f

    def _makeDoY_(self, idx):
        """
        copied trick to solve function definitions inside loop
        (I could not figure out how to use lambda...)
        """

        # def ff(u): return (-1)**(idx+1)*0.5*self.functions['f%i'%idx](u)
        def ff(u): return (-1) ** (idx + 1) * 0.5 * (self.F_stack[idx - 1]['function'](u)
                                                     + self.shift_stack[idx - 1]) * self.y_mirror

        return ff

    def _calc_shift_(self, idx):
        """
        copied trick to solve function definitions inside loop
        (I could not figure out how to use lambda...)
        calculates how much additional constant shifts the curve
        """
        return (-1) ** (idx + 1) * 0.5 * 1 * self.y_mirror


class Nomo_Block_Type_4(Nomo_Block):
    """
    type F1/F2=F3/F4
    """

    def __init__(self, mirror_x=False, mirror_y=False):
        super(Nomo_Block_Type_4, self).__init__(
            mirror_x=mirror_x, mirror_y=mirror_y)

    def define_F1(self, params):
        """
        defines function F1
        """
        self.params_F1 = params
        params['F'] = lambda u: 0.0
        params['G'] = lambda u: params['function'](u)
        self.F1_axis_ini = Axis_Wrapper(f=params['F'], g=params['G'],
                                        start=params['u_min'], stop=params['u_max'])

    def define_F2(self, params):
        """
        defines function F2
        """
        self.params_F2 = params
        params['F'] = lambda u: 0.0
        params['G'] = lambda u: params['function'](u)
        self.F2_axis_ini = Axis_Wrapper(f=params['F'], g=params['G'],
                                        start=params['u_min'], stop=params['u_max'])

    def define_F3(self, params):
        """
        defines function F3
        """
        self.params_F3 = params
        params['F'] = lambda u: 0.0
        params['G'] = lambda u: params['function'](u)
        self.F3_axis_ini = Axis_Wrapper(f=params['F'], g=params['G'],
                                        start=params['u_min'], stop=params['u_max'])

    def define_F4(self, params):
        """
        defines function F4
        """
        self.params_F4 = params
        params['F'] = lambda u: 0.0
        params['G'] = lambda u: params['function'](u)
        self.F4_axis_ini = Axis_Wrapper(f=params['F'], g=params['G'],
                                        start=params['u_min'], stop=params['u_max'])

    def set_block(self, height=10.0, width=10.0, float_axis='F1 or F2', padding=0.9,
                  reference_color=pyx.color.rgb.black):
        """
        sets up equations in block after definitions are given
        float_axis is the axis that's scaling is set by other's scaling
        padding is how much axis extend w.r.t. width/height
        """
        self.width = width
        self.height = height
        self.reference_color = reference_color
        x_dummy, f1_max = self.F1_axis_ini.calc_highest_point()
        # x_dummy,f1_min=self.F1_axis_ini.calc_lowest_point()
        x_dummy, f2_max = self.F2_axis_ini.calc_highest_point()
        # x_dummy,f2_min=self.F2_axis_ini.calc_lowest_point()
        x_dummy, f3_max = self.F3_axis_ini.calc_highest_point()
        # x_dummy,f3_min=self.F3_axis_ini.calc_lowest_point()
        x_dummy, f4_max = self.F4_axis_ini.calc_highest_point()
        # x_dummy,f4_min=self.F4_axis_ini.calc_lowest_point()
        # scaling factor.
        # print f1_max,f2_max,f3_max,f4_max

        m1 = height / f1_max * padding
        m2 = height / f2_max * padding
        m3 = width / f3_max * padding
        m4 = width / f4_max * padding
        # one has to be scaling according to others
        if float_axis == 'F1 or F2':
            if (m1 / m2) > (m3 / m4):
                m1 = m3 / m4 * m2
            if (m1 / m2) <= (m3 / m4):
                m2 = m4 / m3 * m1
        else:
            if (m3 / m4) > (m1 / m2):
                m3 = m1 / m2 * m4
            if (m3 / m4) <= (m1 / m2):
                m4 = m2 / m1 * m3

        self.params_F1['F'] = lambda u: 0.0 * self.x_mirror
        self.params_F1['G'] = lambda u: m1 * \
            self.params_F1['function'](u) * self.y_mirror
        self.atom_F1 = Nomo_Atom(self.params_F1)
        self.add_atom(self.atom_F1)

        self.params_F2['F'] = lambda u: width * self.x_mirror
        self.params_F2['G'] = lambda u: (
            height - m2 * self.params_F2['function'](u)) * self.y_mirror
        self.atom_F2 = Nomo_Atom(self.params_F2)
        self.add_atom(self.atom_F2)

        self.params_F3['F'] = lambda u: m3 * \
            self.params_F3['function'](u) * self.x_mirror
        self.params_F3['G'] = lambda u: 0.0 * self.y_mirror
        self.atom_F3 = Nomo_Atom(self.params_F3)
        self.add_atom(self.atom_F3)

        self.params_F4['F'] = lambda u: (
            width - m4 * self.params_F4['function'](u)) * self.x_mirror
        self.params_F4['G'] = lambda u: height * self.y_mirror
        self.atom_F4 = Nomo_Atom(self.params_F4)
        self.add_atom(self.atom_F4)
        # set side of text in axes
        #        if self.x_mirror<0:
        #                self.atom_F1.params['tick_side']='right'
        #                self.atom_F2.params['tick_side']='left'
        #        else:
        #                self.atom_F1.params['tick_side']='left'
        #                self.atom_F2.params['tick_side']='right'
        #        if self.y_mirror<0:
        #                self.atom_F3.params['tick_side']='right'
        #                self.atom_F4.params['tick_side']='left'
        #        else:
        #                self.atom_F3.params['tick_side']='left'
        #                self.atom_F4.params['tick_side']='right'

        # let's make centerline
        center_line_para = {
            'u_min': 0.0,
            'u_max': 1.0,
            'function': lambda u: u,
            'F': lambda u: u * width * self.x_mirror,
            'G': lambda u: u * height * self.y_mirror,
            'title': '',
            'tick_levels': 0.0,
            'tick_text_levels': 0.0,
            'axis_color': self.reference_color
        }
        self.add_atom(Nomo_Atom(center_line_para))


class Nomo_Block_Type_5(Nomo_Block):
    """
             v
       --------------------
       |   \    \         |           y
     u |----\----\--------| w         |           Diagonal "line_func" missing in pic.
       |-----\----\-------|           |           Pic. without mirrorings.
       |      \    \      |           |-----> x
       --------------------
              wd
    u,v relate to coordinates x,y in rectangle as
    func_u(u)=y
    func_v(x,v)=y
    w,wd relate to coordinates x,y in right and bottom axes of rectangle:
    func_wd(wd)=x
    line_func(x)=y=func_w(w)

    x,y are same in all Eqs. above

    Constructing this needs paper and pencil...
    """

    def __init__(self, mirror_x=False, mirror_y=False):
        super(Nomo_Block_Type_5, self).__init__(
            mirror_x=mirror_x, mirror_y=mirror_y)

    def define_block(self, params):
        """
        defines the block. Dict params has all the definitions
        """
        self.params = params
        self.grid_box = Nomo_Grid_Box(params=params)

    def set_block(self):
        """
        sets block up
        """
        self._build_u_axis_()
        self._build_w_axis_()
        self._build_wd_axis_()
        # build additional v-scale. Put isopleths off in main params, otherwise error
        if self.grid_box.params['allow_additional_v_scale']:
            self._build_v_axis_()
        self.set_reference_axes()

    def draw(self, canvas):
        """
        overrides the parent draw function
        draws also contours
        """
        self._draw_horizontal_guides_(canvas)
        self._draw_vertical_guides_(canvas)
        self._draw_box_around_(canvas)
        # sets u-axis to correct side
        self._set_u_axis_side_()
        # super(Nomo_Block_Type_5,self).draw(canvas=canvas)
        # draws the inner contour lines
        x00, y00 = self.grid_box.u_lines[0][0]
        x00t = self._give_trafo_x_(x00, y00)
        y00t = self._give_trafo_y_(x00, y00)
        u_line_list = pyx.path.path(pyx.path.moveto(x00t, y00t))
        for u_line in self.grid_box.u_lines:
            x0, y0 = u_line[0]
            x0t = self._give_trafo_x_(x0, y0)
            y0t = self._give_trafo_y_(x0, y0)
            u_line_list.append(pyx.path.moveto(x0t, y0t))
            for x, y in u_line:
                xt = self._give_trafo_x_(x, y)
                yt = self._give_trafo_y_(x, y)
                u_line_list.append(pyx.path.lineto(xt, yt))
        # for v-title positioning
        x00, y00 = self.grid_box.v_lines[0][0]
        x00t = self._give_trafo_x_(x00, y00)
        y00t = self._give_trafo_y_(x00, y00)
        v_line_list = pyx.path.path(pyx.path.moveto(x00t, y00t))
        median_v = len(self.grid_box.v_lines) / 2
        if median_v == 0:
            median_v = 1
        for index, v_line in enumerate(self.grid_box.v_lines):
            x0, y0 = v_line[0]
            x0t = self._give_trafo_x_(x0, y0)
            y0t = self._give_trafo_y_(x0, y0)
            v_line_list.append(pyx.path.moveto(x0t, y0t))
            for x, y in v_line:
                xt = self._give_trafo_x_(x, y)
                yt = self._give_trafo_y_(x, y)
                v_line_list.append(pyx.path.lineto(xt, yt))
            # make texts
            x_start, y_start = v_line[0]
            x_stop, y_stop = v_line[-1]
            xt_start = self._give_trafo_x_(x_start, y_start)
            xt_stop = self._give_trafo_x_(x_stop, y_stop)
            yt_start = self._give_trafo_y_(x_start, y_start)
            yt_stop = self._give_trafo_y_(x_stop, y_stop)
            # extra params for v-lines
            x_corr = 0.0
            y_corr = 0.0
            draw_line = False
            # if manual axis data given
            if self.grid_box.params['v_manual_axis_data'] != None:
                if isinstance(self.grid_box.params['v_manual_axis_data'][self.params['v_values'][index]], str):
                    title_raw = self.grid_box.params['v_manual_axis_data'][self.params['v_values'][index]]
                else:
                    dummy = len(
                        self.grid_box.params['v_manual_axis_data'][self.params['v_values'][index]])
                    if isinstance(self.grid_box.params['v_manual_axis_data'][self.params['v_values'][index]], list):
                        title_raw = self.grid_box.params['v_manual_axis_data'][self.params['v_values'][index]][0]
                        ex_params = self.grid_box.params['v_manual_axis_data'][self.params['v_values'][index]][1]
                        if 'x_corr' in ex_params:
                            x_corr = ex_params['x_corr']
                        if 'y_corr' in ex_params:
                            y_corr = ex_params['y_corr']
                        if 'draw_line' in ex_params:
                            draw_line = ex_params['draw_line']
            else:
                title_raw = self.params['v_values'][index]
            if index == median_v:
                # title=self.grid_box.params_v['title']+'='+self.grid_box.params_v['text_format']%title_raw
                title_title = self.grid_box.params_v['title']
            else:
                # title=self.grid_box.params_v['text_format']%title_raw
                title_title = ''
            if self.grid_box.params['v_manual_axis_data'] != None:
                title = title_raw
            else:
                title = self.grid_box.params_v['text_format'] % title_raw
            if (y_start > y_stop and self.params['mirror_y'] == False) or \
                    (y_start < y_stop and self.params['mirror_y'] == True):
                x_1, y_1 = v_line[2]  # two first points are identical
                xt_1 = self._give_trafo_x_(x_1, y_1)
                yt_1 = self._give_trafo_y_(x_1, y_1)
                xt, yt = xt_start, yt_start
            else:
                x_1, y_1 = v_line[-2]
                xt_1 = self._give_trafo_x_(x_1, y_1)
                yt_1 = self._give_trafo_y_(x_1, y_1)
                xt, yt = xt_stop, yt_stop
            dx = xt_1 - xt
            dy = yt_1 - yt
            if self.grid_box.params['allow_additional_v_scale'] == False:
                self._draw_v_text_(xt, yt, dx, dy, canvas, title,
                                   title_title, x_corr, y_corr, draw_line)
        canvas.stroke(u_line_list, [
                      pyx.style.linewidth.normal, self.grid_box.params['u_axis_color']])
        canvas.stroke(v_line_list, [
                      pyx.style.linewidth.normal, self.grid_box.params['v_axis_color']])
        # take handle
        self.ref_block_lines.append(u_line_list)
        self.ref_block_lines.append(v_line_list)
        super(Nomo_Block_Type_5, self).draw(canvas=canvas)
        # self._draw_horizontal_guides_(canvas)
        # self._draw_vertical_guides_(canvas)
        # self._draw_box_around_(canvas)

    def _draw_v_text_(self, x, y, dx, dy, canvas, title, title_title='', x_corr=0.0, y_corr=0.0,
                      draw_line=False):
        """"
        draws titles to v-contours
        """
        para_v = self.grid_box.params_v
        if np.sqrt(dx ** 2 + dy ** 2) == 0:
            dx_unit = 0
            dy_unit = 0
        else:
            dx_unit = dx / np.sqrt(dx ** 2 + dy ** 2)
            dy_unit = dy / np.sqrt(dx ** 2 + dy ** 2)
        if dy_unit != 0:
            angle = -math.atan(dx_unit / dy_unit) * 180 / np.pi
        else:
            angle = 0
        text_distance = 0.5
        if dy >= 0.0:
            if (angle - 90.0) <= -90.0:
                angle = angle + 180.0
            if dx_unit > 0.0:
                text_attr = [pyx.text.valign.middle, pyx.text.halign.right, pyx.text.size.small,
                             pyx.trafo.rotate(angle - 90), para_v['text_color']]
                title_text = title_title + ' ' + title
            if dx_unit <= 0.0:
                text_attr = [pyx.text.valign.middle, pyx.text.halign.left, pyx.text.size.small,
                             pyx.trafo.rotate(angle - 90), para_v['text_color']]
                title_text = title + ' ' + title_title
        else:
            if (angle + 90.0) >= 90.0:
                angle = angle - 180.0
            if dx_unit > 0.0:
                text_attr = [pyx.text.valign.middle, pyx.text.halign.right, pyx.text.size.small,
                             pyx.trafo.rotate(angle + 90), para_v['text_color']]
                title_text = title_title + ' ' + title
            if dx_unit <= 0.0:
                text_attr = [pyx.text.valign.middle, pyx.text.halign.left, pyx.text.size.small,
                             pyx.trafo.rotate(angle + 90), para_v['text_color']]
                title_text = title + ' ' + title_title
        text_distance = self.grid_box.params['v_text_distance']
        canvas.text(x - text_distance * dx_unit + x_corr,
                    y - text_distance * dy_unit + y_corr,
                    title_text, text_attr)
        # take handle
        self.ref_block_texts.append([title_text, x - text_distance * dx_unit + x_corr,
                                     y - text_distance * dy_unit + y_corr,
                                     text_attr])
        # draw line if needed
        if draw_line:
            canvas.stroke(
                pyx.path.line(x, y, x - text_distance * dx_unit +
                              x_corr, y - text_distance * dy_unit + y_corr),
                [pyx.style.linewidth.normal, para_v['axis_color']])
        # take handle
        line_handle = pyx.path.path()
        line_handle.append(pyx.path.moveto(x, y))
        line_handle.append(pyx.path.lineto(
            x - text_distance * dx_unit + x_corr, y - text_distance * dy_unit + y_corr))
        self.ref_block_lines.append(line_handle)

    def _draw_box_around_(self, canvas):
        """
        draws box around
        """
        xt1 = self._give_trafo_x_(self.grid_box.x_left, self.grid_box.y_top)
        yt1 = self._give_trafo_y_(self.grid_box.x_left, self.grid_box.y_top)
        xt2 = self._give_trafo_x_(self.grid_box.x_right, self.grid_box.y_top)
        yt2 = self._give_trafo_y_(self.grid_box.x_right, self.grid_box.y_top)
        xt3 = self._give_trafo_x_(self.grid_box.x_left, self.grid_box.y_bottom)
        yt3 = self._give_trafo_y_(self.grid_box.x_left, self.grid_box.y_bottom)
        xt4 = self._give_trafo_x_(
            self.grid_box.x_right, self.grid_box.y_bottom)
        yt4 = self._give_trafo_y_(
            self.grid_box.x_right, self.grid_box.y_bottom)
        line = pyx.path.path()
        line.append(pyx.path.moveto(xt1, yt1))
        line.append(pyx.path.lineto(xt2, yt2))
        line.append(pyx.path.lineto(xt4, yt4))
        line.append(pyx.path.lineto(xt3, yt3))
        line.append(pyx.path.lineto(xt1, yt1))
        # pyx.canvas.stroke(line, [pyx.style.linewidth.thick])
        canvas.stroke(line)
        # take handle
        self.ref_block_lines.append(line)

    def _draw_horizontal_guides_(self, canvas, axis_color=pyx.color.cmyk.Gray):
        """
        draws horizontal guides
        """
        p = self.grid_box.params
        if p['horizontal_guides']:
            line = pyx.path.path()
            nr = p['horizontal_guide_nr']
            for y in scipy.linspace(self.grid_box.y_top, self.grid_box.y_bottom, nr):
                xt1 = self._give_trafo_x_(self.grid_box.x_left, y)
                yt1 = self._give_trafo_y_(self.grid_box.x_left, y)
                xt2 = self._give_trafo_x_(self.grid_box.x_right, y)
                yt2 = self._give_trafo_y_(self.grid_box.x_right, y)
                line.append(pyx.path.moveto(xt1, yt1))
                line.append(pyx.path.lineto(xt2, yt2))
            canvas.stroke(line, [pyx.style.linewidth.normal, pyx.style.linestyle.dotted,
                                 p['u_axis_color']])
            self.ref_block_lines.append(line)

    def _draw_vertical_guides_(self, canvas, axis_color=pyx.color.cmyk.Gray):
        """
        draws vertical guides
        """
        p = self.grid_box.params
        if p['vertical_guides']:
            line = pyx.path.path()
            nr = p['vertical_guide_nr']
            for x in scipy.linspace(self.grid_box.x_left, self.grid_box.x_right, nr):
                xt1 = self._give_trafo_x_(x, self.grid_box.y_top)
                yt1 = self._give_trafo_y_(x, self.grid_box.y_top)
                xt2 = self._give_trafo_x_(x, self.grid_box.y_bottom)
                yt2 = self._give_trafo_y_(x, self.grid_box.y_bottom)
                line.append(pyx.path.moveto(xt1, yt1))
                line.append(pyx.path.lineto(xt2, yt2))
            canvas.stroke(line, [pyx.style.linewidth.normal, pyx.style.linestyle.dotted,
                                 p['wd_axis_color']])
            # take handle
            self.ref_block_lines.append(line)

    def _build_u_axis_(self):
        """
        builds u_axis
        """
        para_u = self.grid_box.params_u
        self.atom_u = Nomo_Atom(para_u)
        self.add_atom(self.atom_u)
        self.u_axis = Axis_Wrapper(f=para_u['F'], g=para_u['G'],
                                   start=para_u['u_min'], stop=para_u['u_max'])
        self.axis_wrapper_stack.append(self.u_axis)

    def _set_u_axis_side_(self):
        """
        sets side of u-axis to correct
        """
        if self.atom_u.params['tick_side'] == None:
            # let's find out tick side from first u_line
            x1, y1 = self.grid_box.u_lines[0][0]
            x2, y2 = self.grid_box.u_lines[0][2]
            x3, y3 = self.grid_box.u_lines[1][0]
            x1t = self._give_trafo_x_(x1, y1)
            x2t = self._give_trafo_x_(x2, y2)
            x3t = self._give_trafo_x_(x3, y3)
            y1t = self._give_trafo_y_(x1, y1)
            y2t = self._give_trafo_y_(x2, y2)
            y3t = self._give_trafo_y_(x3, y3)
            vx_A = x2t - x1t
            vy_A = y2t - y1t
            vx_B = x3t - x1t
            vy_B = y3t - y1t
            test1 = (vx_A * vy_B + vy_A * (-vx_B))
            test2 = (vy_B * vx_A * (vx_A * vy_B + vy_A * (-vx_B)))
            # if (vy_B*vx_A*(vx_A*vy_B+vy_A*(-vx_B)))>0:
            if vx_A > 0:
                self.atom_u.params['tick_side'] = 'left'
            else:
                self.atom_u.params['tick_side'] = 'right'
            if self.grid_box.params['u_scale_opposite'] and vx_A > 0:
                self.atom_u.params['tick_side'] = 'right'
            else:
                self.atom_u.params['tick_side'] = 'left'

    def _build_v_axis_(self):
        """
        builds v_axis
        """
        para_v = self.grid_box.params_v
        self.atom_v = Nomo_Atom(para_v)
        self.add_atom(self.atom_v)
        self.v_axis = Axis_Wrapper(f=para_v['F'], g=para_v['G'],
                                   start=para_v['u_min'], stop=para_v['u_max'])
        self.axis_wrapper_stack.append(self.v_axis)

    def _build_w_axis_(self):
        """
        builds w_axis
        """
        para_w = self.grid_box.params_w
        self.atom_w = Nomo_Atom(para_w)
        self.add_atom(self.atom_w)
        self.w_axis = Axis_Wrapper(f=para_w['F'], g=para_w['G'],
                                   start=para_w['u_min'], stop=para_w['u_max'])
        self.axis_wrapper_stack.append(self.w_axis)

    def _build_wd_axis_(self):
        """
        builds wd_axis
        """
        para_wd = self.grid_box.params_wd
        self.atom_wd = Nomo_Atom(para_wd)
        self.add_atom(self.atom_wd)
        self.wd_axis = Axis_Wrapper(f=para_wd['F'], g=para_wd['G'],
                                    start=para_wd['u_min'], stop=para_wd['u_max'])
        self.axis_wrapper_stack.append(self.wd_axis)


class Nomo_Block_Type_6(Nomo_Block):
    """
    type F1 <-> F2 Ladder
    """

    def __init__(self, mirror_x=False, mirror_y=False):
        super(Nomo_Block_Type_6, self).__init__(
            mirror_x=mirror_x, mirror_y=mirror_y)

    def define(self, params1, params2):
        """
        defines straight scales
        """
        params1['F'] = lambda u: 0.0
        params1['G'] = lambda u: params1['function'](u)
        self.atom_F1 = Nomo_Atom(params1)
        self.add_atom(self.atom_F1)
        # for initial axis calculations
        self.F1_axis_ini = Axis_Wrapper(f=params1['F'], g=params1['G'],
                                        start=params1['u_min'], stop=params1['u_max'])

        params2['F'] = lambda u: 1.0
        params2['G'] = lambda u: params2['function'](u)
        self.atom_F2 = Nomo_Atom(params2)
        self.add_atom(self.atom_F2)
        # for inital axis calculations
        self.F2_axis_ini = Axis_Wrapper(f=params2['F'], g=params2['G'],
                                        start=params2['u_min'], stop=params2['u_max'])

    def set_block(self, width=10.0, height=10.0, type='parallel', x_empty=0.2, y_empty=0.2,
                  curve_const=0.5, ladder_color=pyx.color.rgb.black):
        """
        sets original width, height and x-distance proportion for the nomogram before
        transformations
        type = 'parallel' or 'orthogonal'
        x_empty is proportial distance from virtual axis crossing
        y_empty is proportial distance from virtual axis crossing
        in orthogonal F1 is for vertical (y) and F2 for horizontal (x)
        """
        self.width = width
        self.height = height
        self.curve_const = curve_const
        self.ladder_color = ladder_color
        # p=proportion
        # delta_1=proportion*width/(1+proportion)
        # delta_3=width/(proportion+1)
        # print delta_1
        # print delta_3
        x_dummy, f1_max = self.F1_axis_ini.calc_highest_point()
        x_dummy, f1_min = self.F1_axis_ini.calc_lowest_point()
        f1_length = f1_max - f1_min
        x_dummy, f2_max = self.F2_axis_ini.calc_highest_point()
        x_dummy, f2_min = self.F2_axis_ini.calc_lowest_point()
        f2_length = f2_max - f2_min
        if type == 'parallel':
            # redefine scaled functions to be width x height
            self.atom_F1.f = lambda u: (self.F1_axis_ini.f(u)) * self.x_mirror
            self.atom_F1.g = lambda u: (
                (self.F1_axis_ini.g(u) - f1_min) / f1_length * height) * self.y_mirror
            self.atom_F2.f = lambda u: (
                self.F2_axis_ini.f(u) * width) * self.x_mirror
            self.atom_F2.g = lambda u: (
                (self.F2_axis_ini.g(u) - f2_min) / f2_length * height) * self.y_mirror

        if type == 'orthogonal':
            # redefine scaled functions to be orthogonal width x height
            ax1_length = height / (1 + y_empty)
            ax1_empty = height * y_empty
            ax2_length = width / (1 + x_empty)
            ax2_empty = width * y_empty
            self.atom_F1.f = lambda u: (self.F1_axis_ini.f(u)) * self.x_mirror
            self.atom_F1.g = lambda u: ((self.F1_axis_ini.g(u) - f1_min) / f1_length * ax1_length + ax1_empty) \
                * self.y_mirror
            self.atom_F2.f = lambda u: ((self.F2_axis_ini.g(u) - f2_min) / f2_length * ax2_length + ax2_empty) \
                * self.x_mirror
            self.atom_F2.g = lambda u: (0.0) * self.y_mirror

        self.F1_axis = Axis_Wrapper(f=self.atom_F1.f, g=self.atom_F1.g,
                                    start=self.atom_F1.params['u_min'],
                                    stop=self.atom_F1.params['u_max'])
        self.axis_wrapper_stack.append(self.F1_axis)
        self.F2_axis = Axis_Wrapper(f=self.atom_F2.f, g=self.atom_F2.g,
                                    start=self.atom_F2.params['u_min'],
                                    stop=self.atom_F2.params['u_max'])
        self.axis_wrapper_stack.append(self.F2_axis)
        self.set_reference_axes()

    def draw(self, canvas):
        """
        overrides the parent draw function
        draws also ladders
        """
        super(Nomo_Block_Type_6, self).draw(canvas=canvas)
        self._do_ladder_lines_(canvas)

    def _do_ladder_lines_(self, canvas_given):
        """
        finds points and derivatives for ladder
        1. find points (according to F1 or given)
        -linear
        -log
        -given (manual axis)
        2. find derivatives at points
        - delta_x and delta_y unit vector
        """
        f1 = self.atom_F1.give_x
        g1 = self.atom_F1.give_y
        f2 = self.atom_F2.give_x
        g2 = self.atom_F2.give_y
        start = self.atom_F1.params['u_min']
        stop = self.atom_F1.params['u_max']
        side1 = self.atom_F1.params['tick_side']
        side2 = self.atom_F2.params['tick_side']

        # Linear
        if self.atom_F1.params['scale_type'] == 'linear':
            tick_0_list, tick_1_list, tick_2_list, tick_3_list, tick_4_list, start_ax, stop_ax = \
                find_linear_ticks(start, stop)

            dx_units_0_1, dy_units_0_1, angles_0_1 = \
                find_tick_directions(tick_0_list, f1, g1, side1, start, stop)

            dx_units_0_2, dy_units_0_2, angles_0_2 = \
                find_tick_directions(tick_0_list, f2, g2, side2, start, stop)

            dx_units_1_1, dy_units_1_1, angles_1_1 = \
                find_tick_directions(tick_1_list, f1, g1, side1, start, stop)

            dx_units_1_2, dy_units_1_2, angles_1_2 = \
                find_tick_directions(tick_1_list, f2, g2, side2, start, stop)

            self._draw_ladder_lines_(dx_units_0_1, dy_units_0_1, dx_units_0_2, dy_units_0_2,
                                     tick_0_list, f1, g1, f2, g2, canvas_given, pyx.style.linestyle.solid)
            self._draw_ladder_lines_(dx_units_1_1, dy_units_1_1, dx_units_1_2, dy_units_1_2,
                                     tick_1_list, f1, g1, f2, g2, canvas_given, pyx.style.linestyle.dotted)

        # Linear smart
        if self.atom_F1.params['scale_type'] == 'linear smart':
            tick_0_list, tick_1_list, tick_2_list, tick_3_list, tick_4_list = \
                find_linear_ticks_smart(start, stop, f1, g1, turn=1,
                                        base_start=self.atom_F1.params['base_start'],
                                        base_stop=self.atom_F1.params['base_stop'],
                                        scale_max_0=self.atom_F1.params['scale_max'],
                                        distance_limit=self.atom_F1.params['tick_distance_smart'])

            #            tick_0_list,tick_1_list,tick_2_list,tick_3_list,tick_4_list,start_ax,stop_ax=\
            #            find_linear_ticks(start,stop)

            dx_units_0_1, dy_units_0_1, angles_0_1 = find_tick_directions(tick_0_list, f1, g1, side1, start, stop,
                                                                          full_angle=self.atom_F1.params['full_angle'],
                                                                          extra_angle=self.atom_F1.params[
                                                                              'extra_angle'],
                                                                          turn_relative=self.atom_F1.params[
                                                                              'turn_relative'])
            #            dx_units_0_1,dy_units_0_1,angles_0_1=\
            #            find_tick_directions(tick_0_list,f1,g1,side1,start,stop)

            dx_units_0_2, dy_units_0_2, angles_0_2 = find_tick_directions(tick_0_list, f2, g2, side2, start, stop,
                                                                          full_angle=self.atom_F2.params['full_angle'],
                                                                          extra_angle=self.atom_F2.params[
                                                                              'extra_angle'],
                                                                          turn_relative=self.atom_F2.params[
                                                                              'turn_relative'])
            #            dx_units_0_2,dy_units_0_2,angles_0_2=\
            #            find_tick_directions(tick_0_list,f2,g2,side2,start,stop)
            #
            dx_units_1_1, dy_units_1_1, angles_1_1 = find_tick_directions(tick_1_list, f1, g1, side1, start, stop,
                                                                          full_angle=self.atom_F1.params['full_angle'],
                                                                          extra_angle=self.atom_F1.params[
                                                                              'extra_angle'],
                                                                          turn_relative=self.atom_F1.params[
                                                                              'turn_relative'])

            #            dx_units_1_1,dy_units_1_1,angles_1_1=\
            #            find_tick_directions(tick_1_list,f1,g1,side1,start,stop)
            #
            dx_units_1_2, dy_units_1_2, angles_1_2 = find_tick_directions(tick_1_list, f2, g2, side2, start, stop,
                                                                          full_angle=self.atom_F2.params['full_angle'],
                                                                          extra_angle=self.atom_F2.params[
                                                                              'extra_angle'],
                                                                          turn_relative=self.atom_F2.params[
                                                                              'turn_relative'])
            #            dx_units_1_2,dy_units_1_2,angles_1_2=\
            #            find_tick_directions(tick_1_list,f2,g2,side2,start,stop)

            self._draw_ladder_lines_(dx_units_0_1, dy_units_0_1, dx_units_0_2, dy_units_0_2,
                                     tick_0_list, f1, g1, f2, g2, canvas_given, pyx.style.linestyle.solid)
            self._draw_ladder_lines_(dx_units_1_1, dy_units_1_1, dx_units_1_2, dy_units_1_2,
                                     tick_1_list, f1, g1, f2, g2, canvas_given, pyx.style.linestyle.dotted)

        # np.log smart
        if self.atom_F1.params['scale_type'] == 'log smart':
            c = pyx.canvas.canvas()
            dummy_axis = Nomo_Axis(f1, g1, start, stop, turn=1, title='', canvas=c, type='log smart',
                                   text_style='normal', title_x_shift=0, title_y_shift=0.25,
                                   tick_levels=4, tick_text_levels=3,
                                   text_color=pyx.color.rgb.black, axis_color=pyx.color.rgb.black,
                                   manual_axis_data={},
                                   axis_appear=self.atom_F1.params, side=self.atom_F1.params['tick_side'],
                                   base_start=self.atom_F1.params['base_start'],
                                   base_stop=self.atom_F1.params['base_stop'])
            tick_0_list = dummy_axis.tick_0_list
            tick_1_list = dummy_axis.tick_1_list
            tick_2_list = dummy_axis.tick_2_list
            tick_3_list = dummy_axis.tick_3_list
            tick_4_list = dummy_axis.tick_4_list
            find_linear_ticks_smart(start, stop, f1, g1, turn=1,
                                    base_start=self.atom_F1.params['base_start'],
                                    base_stop=self.atom_F1.params['base_stop'],
                                    scale_max_0=self.atom_F1.params['scale_max'],
                                    distance_limit=self.atom_F1.params['tick_distance_smart'])

            #            tick_0_list,tick_1_list,tick_2_list,tick_3_list,tick_4_list,start_ax,stop_ax=\
            #            find_linear_ticks(start,stop)

            dx_units_0_1, dy_units_0_1, angles_0_1 = find_tick_directions(tick_0_list, f1, g1, side1, start, stop,
                                                                          full_angle=self.atom_F1.params['full_angle'],
                                                                          extra_angle=self.atom_F1.params[
                                                                              'extra_angle'],
                                                                          turn_relative=self.atom_F1.params[
                                                                              'turn_relative'])
            #            dx_units_0_1,dy_units_0_1,angles_0_1=\
            #            find_tick_directions(tick_0_list,f1,g1,side1,start,stop)

            dx_units_0_2, dy_units_0_2, angles_0_2 = find_tick_directions(tick_0_list, f2, g2, side2, start, stop,
                                                                          full_angle=self.atom_F2.params['full_angle'],
                                                                          extra_angle=self.atom_F2.params[
                                                                              'extra_angle'],
                                                                          turn_relative=self.atom_F2.params[
                                                                              'turn_relative'])
            #            dx_units_0_2,dy_units_0_2,angles_0_2=\
            #            find_tick_directions(tick_0_list,f2,g2,side2,start,stop)
            #
            dx_units_1_1, dy_units_1_1, angles_1_1 = find_tick_directions(tick_1_list, f1, g1, side1, start, stop,
                                                                          full_angle=self.atom_F1.params['full_angle'],
                                                                          extra_angle=self.atom_F1.params[
                                                                              'extra_angle'],
                                                                          turn_relative=self.atom_F1.params[
                                                                              'turn_relative'])

            #            dx_units_1_1,dy_units_1_1,angles_1_1=\
            #            find_tick_directions(tick_1_list,f1,g1,side1,start,stop)
            #
            dx_units_1_2, dy_units_1_2, angles_1_2 = find_tick_directions(tick_1_list, f2, g2, side2, start, stop,
                                                                          full_angle=self.atom_F2.params['full_angle'],
                                                                          extra_angle=self.atom_F2.params[
                                                                              'extra_angle'],
                                                                          turn_relative=self.atom_F2.params[
                                                                              'turn_relative'])
            #            dx_units_1_2,dy_units_1_2,angles_1_2=\
            #            find_tick_directions(tick_1_list,f2,g2,side2,start,stop)

            self._draw_ladder_lines_(dx_units_0_1, dy_units_0_1, dx_units_0_2, dy_units_0_2,
                                     tick_0_list, f1, g1, f2, g2, canvas_given, pyx.style.linestyle.solid)
            self._draw_ladder_lines_(dx_units_1_1, dy_units_1_1, dx_units_1_2, dy_units_1_2,
                                     tick_1_list, f1, g1, f2, g2, canvas_given, pyx.style.linestyle.dotted)

        # np.log
        if self.atom_F1.params['scale_type'] == 'log':
            tick_0_list, tick_1_list, tick_2_list, start_ax, stop_ax = \
                find_log_ticks(start, stop)

            dx_units_0_1, dy_units_0_1, angles_0_1 = \
                find_tick_directions(tick_0_list, f1, g1, side1, start, stop)

            dx_units_0_2, dy_units_0_2, angles_0_2 = \
                find_tick_directions(tick_0_list, f2, g2, side2, start, stop)

            dx_units_1_1, dy_units_1_1, angles_1_1 = \
                find_tick_directions(tick_1_list, f1, g1, side1, start, stop)

            dx_units_1_2, dy_units_1_2, angles_1_2 = \
                find_tick_directions(tick_1_list, f2, g2, side2, start, stop)
            self._draw_ladder_lines_(dx_units_0_1, dy_units_0_1, dx_units_0_2, dy_units_0_2,
                                     tick_0_list, f1, g1, f2, g2, canvas_given, pyx.style.linestyle.solid)
            self._draw_ladder_lines_(dx_units_1_1, dy_units_1_1, dx_units_1_2, dy_units_1_2,
                                     tick_1_list, f1, g1, f2, g2, canvas_given, pyx.style.linestyle.dotted)

        # manual point or manual arrow
        if self.atom_F1.params['scale_type'] == 'manual point' or \
                self.atom_F1.params['scale_type'] == 'manual arrow':
            tick_0_list = self.atom_F1.params['manual_axis_data'].keys()
            tick_0_list.sort()

            dx_units_0_1, dy_units_0_1, angles_0_1 = \
                find_tick_directions(tick_0_list, f1, g1, side1, start, stop)

            dx_units_0_2, dy_units_0_2, angles_0_2 = \
                find_tick_directions(tick_0_list, f2, g2, side2, start, stop)

            self._draw_ladder_lines_(dx_units_0_1, dy_units_0_1, dx_units_0_2, dy_units_0_2,
                                     tick_0_list, f1, g1, f2, g2, canvas_given, pyx.style.linestyle.solid)

        # manual line
        if self.atom_F1.params['scale_type'] == 'manual line':
            tick_0_list = self.atom_F1.params['manual_axis_data'].keys()
            tick_0_list.sort()

            dx_units_0_1, dy_units_0_1, angles_0_1 = \
                find_tick_directions(tick_0_list, f1, g1, side1, start, stop)

            dx_units_0_2, dy_units_0_2, angles_0_2 = \
                find_tick_directions(tick_0_list, f2, g2, side2, start, stop)

            self._draw_ladder_lines_(dx_units_0_1, dy_units_0_1, dx_units_0_2, dy_units_0_2,
                                     tick_0_list, f1, g1, f2, g2, canvas_given, pyx.style.linestyle.solid)

    def _draw_ladder_lines_(self, dx_units_1, dy_units_1, dx_units_2, dy_units_2,
                            tick_list, f1, g1, f2, g2, canvas, line_style):
        """
        draws the lines
        """
        line = pyx.path.path(pyx.path.moveto(
            f1(tick_list[0]), g1(tick_list[0])))
        curves = []
        for idx, u in enumerate(tick_list):
            # line.append(pyx.path.moveto(f1(u), g1(u)))
            # line.append(pyx.path.lineto(f2(u), g2(u)))
            pyx.path_length = np.sqrt(
                (f1(u) - f2(u)) ** 2 + (g1(u) - g2(u)) ** 2)
            factor = self.curve_const * pyx.path_length
            x1, y1 = f1(u), g1(u)
            x2, y2 = f1(u) - dy_units_1[idx] * \
                factor, g1(u) + dx_units_1[idx] * factor
            x3, y3 = f2(u) - dy_units_2[idx] * \
                factor, g2(u) + dx_units_2[idx] * factor
            x4, y4 = f2(u), g2(u)
            curves.append(pyx.path.curve(x1, y1, x2, y2, x3, y3, x4, y4))
        for curve in curves:
            canvas.stroke(
                curve, [pyx.style.linewidth.normal, line_style, self.ladder_color])
        canvas.stroke(line, [pyx.style.linewidth.normal,
                             line_style, self.ladder_color])


class Nomo_Block_Type_7(Nomo_Block):
    """
    type 1/f1+1/f2=1/f3 angle nomogram
    """

    def __init__(self, mirror_x=False, mirror_y=False):
        super(Nomo_Block_Type_7, self).__init__(
            mirror_x=mirror_x, mirror_y=mirror_y)

    def define_F1(self, params):
        """
        defines function F1
        """
        params['F'] = lambda u: 0.0
        params['G'] = lambda u: params['function'](u)
        self.F1 = params['function']
        self.params_F1 = params
        self.F1_axis_ini = Axis_Wrapper(f=params['F'], g=params['G'],
                                        start=params['u_min'], stop=params['u_max'])

    def define_F2(self, params):
        """
        defines function F2
        """
        params['F'] = lambda u: 0.0
        params['G'] = lambda u: params['function'](u)
        self.F2 = params['function']
        self.params_F2 = params
        self.F2_axis_ini = Axis_Wrapper(f=params['F'], g=params['G'],
                                        start=params['u_min'], stop=params['u_max'])

    def define_F3(self, params):
        """
        defines function F3
        """
        params['F'] = lambda u: 0.0
        params['G'] = lambda u: params['function'](u)
        self.F3 = params['function']
        self.params_F3 = params
        self.F3_axis_ini = Axis_Wrapper(f=params['F'], g=params['G'],
                                        start=params['u_min'], stop=params['u_max'])

    def set_block(self, width_1=10.0, angle_u=60.0, angle_v=60.0):
        """
        sets the angle-nomogram of the block
        """
        angle_u_rad = angle_u * np.pi / 180.0
        angle_v_rad = angle_v * np.pi / 180.0

        x_dummy, f1_max = self.F1_axis_ini.calc_highest_point()
        x_dummy, f1_min = self.F1_axis_ini.calc_lowest_point()
        axis_1_length = abs(f1_max - f1_min)
        k1 = width_1 / axis_1_length
        k2 = k1 * np.sin(angle_u_rad) / np.sin(angle_v_rad)
        k3 = k1 * np.sin(angle_u_rad + angle_v_rad) / np.sin(angle_v_rad)

        factor_3_x = np.cos(angle_u_rad)
        factor_3_y = np.sin(angle_u_rad)
        factor_2_x = np.cos(angle_u_rad + angle_v_rad)
        factor_2_y = np.sin(angle_u_rad + angle_v_rad)

        self.params_F1['F'] = lambda u: (k1 * self.F1(u)) * self.x_mirror
        self.params_F1['G'] = lambda u: 0.0
        self.atom_F1 = Nomo_Atom(self.params_F1)
        self.add_atom(self.atom_F1)
        self.params_F2['F'] = lambda u: factor_2_x * \
            (k2 * self.F2(u)) * self.x_mirror
        self.params_F2['G'] = lambda u: factor_2_y * \
            (k2 * self.F2(u)) * self.y_mirror
        self.atom_F2 = Nomo_Atom(self.params_F2)
        self.add_atom(self.atom_F2)
        self.params_F3['F'] = lambda u: factor_3_x * \
            (k3 * self.F3(u)) * self.x_mirror
        self.params_F3['G'] = lambda u: factor_3_y * \
            (k3 * self.F3(u)) * self.y_mirror
        self.atom_F3 = Nomo_Atom(self.params_F3)
        self.add_atom(self.atom_F3)

        self.F1_axis = Axis_Wrapper(f=self.params_F1['F'], g=self.params_F1['G'],
                                    start=self.params_F1['u_min'], stop=self.params_F1['u_max'])
        self.axis_wrapper_stack.append(self.F1_axis)

        self.F2_axis = Axis_Wrapper(f=self.params_F2['F'], g=self.params_F2['G'],
                                    start=self.params_F2['u_min'], stop=self.params_F2['u_max'])
        self.axis_wrapper_stack.append(self.F2_axis)

        self.F3_axis = Axis_Wrapper(f=self.params_F3['F'], g=self.params_F3['G'],
                                    start=self.params_F3['u_min'], stop=self.params_F3['u_max'])
        self.axis_wrapper_stack.append(self.F3_axis)
        self.set_reference_axes()


class Nomo_Block_Type_8(Nomo_Block):
    """
    type F single
    """

    def __init__(self, mirror_x=False, mirror_y=False):
        super(Nomo_Block_Type_8, self).__init__(
            mirror_x=mirror_x, mirror_y=mirror_y)

    def define_F(self, params):
        """
        defines function F1
        """
        if 'function_y' in params:
            params['function'] = params['function_y']
        if 'function_x' not in params:
            params['function_x'] = lambda u: 1.0
        params['F'] = lambda u: params['function_x'](u) * self.x_mirror
        params['G'] = lambda u: params['function'](u) * self.y_mirror
        self.atom_F = Nomo_Atom(params)
        self.add_atom(self.atom_F)
        self.params_F = params
        self.F = params['function']
        # for inital axis calculations
        self.F_axis_ini = Axis_Wrapper(f=params['F'], g=params['G'],
                                       start=params['u_min'], stop=params['u_max'])

    def set_block(self, length=10.0):
        x_dummy, f_max = self.F_axis_ini.calc_highest_point()
        x_dummy, f_min = self.F_axis_ini.calc_lowest_point()
        def y_func(u): return length / abs(f_max - f_min) * self.F(u)
        self.F_axis = Axis_Wrapper(f=self.params_F['F'], g=y_func,
                                   start=self.params_F['u_min'], stop=self.params_F['u_max'])
        self.axis_wrapper_stack.append(self.F_axis)
        self.set_reference_axes()


class Nomo_Block_Type_9_old(Nomo_Block):
    """
    type determinant and 3 line axes (no grid)
    """

    def __init__(self, mirror_x=False, mirror_y=False):
        super(Nomo_Block_Type_9_old, self).__init__(
            mirror_x=mirror_x, mirror_y=mirror_y)

    def define_determinant(self, params1, params2, params3, transform_ini=False):
        """
        defines scales as determinant form. If transform_ini=True, scales
        are transformed initially such that scale 1 and 3 ends hit corners
        of rectangle size 10x10 (to be scales later). This is due to the
        fact that sometimes term h=0 in determinant that divides f and g
        in actual coordinates. This divergency can be put away by transforming
        matrix before starting to use only x, and y coordinates
        u : 1
        v : 2
        w : 3
        """
        p1 = params1
        p2 = params2
        p3 = params3
        f1, g1, h1 = p1['f'], p1['g'], p1['h']
        f2, g2, h2 = p2['f'], p2['g'], p2['h']
        f3, g3, h3 = p3['f'], p3['g'], p3['h']
        if transform_ini:
            vk = [['u', p1['u_min'], 'x', 0.0],
                  ['u', p1['u_min'], 'y', 0.0],
                  ['u', p1['u_max'], 'x', 0.0],
                  ['u', p1['u_max'], 'y', 10.0],
                  ['w', p3['u_min'], 'x', 10.0],
                  ['w', p3['u_min'], 'y', 0.0],
                  ['w', p3['u_max'], 'x', 10.0],
                  ['w', p3['u_max'], 'y', 10.0]]
            nomo = Nomograph3(f1, g1, h1, f2, g2, h2, f3, g3, h3, vk)
            # F1
            params1['F'] = lambda u: nomo.give_x1(u) * self.x_mirror
            params1['G'] = lambda u: nomo.give_y1(u) * self.y_mirror
            # F2
            params2['F'] = lambda u: nomo.give_x2(u) * self.x_mirror
            params2['G'] = lambda u: nomo.give_y2(u) * self.y_mirror
            # F3
            params3['F'] = lambda u: nomo.give_x3(u) * self.x_mirror
            params3['G'] = lambda u: nomo.give_y3(u) * self.y_mirror
        else:
            # F1
            params1['F'] = lambda u: p1['f'](u) / p1['h'](u) * self.x_mirror
            params1['G'] = lambda u: p1['g'](u) / p1['h'](u) * self.y_mirror
            # F2
            params2['F'] = lambda u: p2['f'](u) / p2['h'](u) * self.x_mirror
            params2['G'] = lambda u: p2['f'](u) / p2['h'](u) * self.y_mirror
            # F3
            params3['F'] = lambda u: p3['f'](u) / p3['h'](u) * self.x_mirror
            params3['G'] = lambda u: p3['f'](u) / p3['h'](u) * self.y_mirror

        self.atom_F1 = Nomo_Atom(params1)
        self.add_atom(self.atom_F1)
        # for inital axis calculations
        self.F1_axis_ini = Axis_Wrapper(f=params1['F'], g=params1['G'],
                                        start=params1['u_min'], stop=params1['u_max'])

        self.atom_F2 = Nomo_Atom(params2)
        self.add_atom(self.atom_F2)
        # for inital axis calculations
        self.F2_axis_ini = Axis_Wrapper(f=params2['F'], g=params2['G'],
                                        start=params2['u_min'], stop=params2['u_max'])

        self.atom_F3 = Nomo_Atom(params3)
        self.add_atom(self.atom_F3)
        # for inital axis calculations
        self.F3_axis_ini = Axis_Wrapper(f=params3['F'], g=params3['G'],
                                        start=params3['u_min'], stop=params3['u_max'])

    #    def define_F1(self,params):
    #        """
    #        defines function F1
    #        """
    #        params['F']=lambda u:params['f'](u)*self.x_mirror
    #        params['G']=lambda u:params['g'](u)*self.y_mirror
    #        self.atom_F1=Nomo_Atom(params)
    #        self.add_atom(self.atom_F1)
    #        # for inital axis calculations
    #        self.F1_axis_ini=Axis_Wrapper(f=params['F'],g=params['G'],
    #                             start=params['u_min'],stop=params['u_max'])
    #
    #    def define_F2(self,params):
    #        """
    #        defines function F2
    #        """
    #        params['F']=lambda u:params['f'](u)*self.x_mirror
    #        params['G']=lambda u:params['g'](u)*self.y_mirror
    #        self.atom_F2=Nomo_Atom(params)
    #        self.add_atom(self.atom_F2)
    #        # for inital axis calculations
    #        self.F2_axis_ini=Axis_Wrapper(f=params['F'],g=params['G'],
    #                             start=params['u_min'],stop=params['u_max'])
    #
    #    def define_F3(self,params):
    #        """
    #        defines function F3
    #        """
    #        params['F']=lambda u:params['f'](u)*self.x_mirror
    #        params['G']=lambda u:params['g'](u)*self.y_mirror
    #        self.atom_F3=Nomo_Atom(params)
    #        self.add_atom(self.atom_F3)
    #        # for inital axis calculations
    #        self.F3_axis_ini=Axis_Wrapper(f=params['F'],g=params['G'],
    #                             start=params['u_min'],stop=params['u_max'])

    def set_block(self, width=10.0, height=10.0):
        """
        sets original width, height
        """
        self.width = width
        self.height = height
        f1_max_x, f1_max_y = self.F1_axis_ini.calc_highest_point()
        f1_min_x, f1_min_y = self.F1_axis_ini.calc_lowest_point()
        f2_max_x, f2_max_y = self.F2_axis_ini.calc_highest_point()
        f2_min_x, f2_min_y = self.F2_axis_ini.calc_lowest_point()
        f3_max_x, f3_max_y = self.F3_axis_ini.calc_highest_point()
        f3_min_x, f3_min_y = self.F3_axis_ini.calc_lowest_point()
        max_x = max(f1_max_x, f2_max_x, f3_max_x)
        min_x = min(f1_min_x, f2_min_x, f3_min_x)
        max_y = max(f1_max_y, f2_max_y, f3_max_y)
        min_y = min(f1_min_y, f2_min_y, f3_min_y)
        width_orig = abs(max_x - min_x)
        height_orig = abs(max_y - min_y)
        x_factor = width / width_orig
        y_factor = height / height_orig
        # redefine scaled functions
        self.atom_F1.f = lambda u: self.F1_axis_ini.f(u) * x_factor
        self.atom_F1.g = lambda u: self.F1_axis_ini.g(u) * y_factor
        self.atom_F2.f = lambda u: self.F2_axis_ini.f(u) * x_factor
        self.atom_F2.g = lambda u: self.F2_axis_ini.g(u) * y_factor
        self.atom_F3.f = lambda u: self.F3_axis_ini.f(u) * x_factor
        self.atom_F3.g = lambda u: self.F3_axis_ini.g(u) * y_factor
        # save axes for reference calculations
        self.F1_axis = Axis_Wrapper(f=self.atom_F1.f, g=self.atom_F1.g,
                                    start=self.atom_F1.params['u_min'],
                                    stop=self.atom_F1.params['u_max'])
        self.axis_wrapper_stack.append(self.F1_axis)
        self.F2_axis = Axis_Wrapper(f=self.atom_F2.f, g=self.atom_F2.g,
                                    start=self.atom_F2.params['u_min'],
                                    stop=self.atom_F2.params['u_max'])
        self.axis_wrapper_stack.append(self.F2_axis)

        self.F3_axis = Axis_Wrapper(f=self.atom_F3.f, g=self.atom_F3.g,
                                    start=self.atom_F3.params['u_min'],
                                    stop=self.atom_F3.params['u_max'])
        self.axis_wrapper_stack.append(self.F3_axis)
        self.set_reference_axes()


class Nomo_Block_Type_9(Nomo_Block):
    """
    type determinant and 3 line axes or grids
    to override type 9
    """

    def __init__(self, mirror_x=False, mirror_y=False):
        super(Nomo_Block_Type_9, self).__init__(
            mirror_x=mirror_x, mirror_y=mirror_y)

    def define_determinant(self, params1, params2, params3, transform_ini=False):
        """
        defines scales as determinant form. If transform_ini=True, scales
        are transformed initially such that scale 1 and 3 ends hit corners
        of rectangle size 10x10 (to be scales later). This is due to the
        fact that sometimes term h=0 in determinant that divides f and g
        in actual coordinates. This divergency can be put away by transforming
        matrix before starting to use only x, and y coordinates
        u : 1
        v : 2
        w : 3
        """
        p1 = params1
        p2 = params2
        p3 = params3
        # F1
        if p1['grid']:
            v0 = p1['v_start']
            def f1(u): return p1['f_grid'](u, v0)
            def g1(u): return p1['g_grid'](u, v0)
            def h1(u): return p1['h_grid'](u, v0)
        else:
            f1, g1, h1 = p1['f'], p1['g'], p1['h']
        # F2
        if p2['grid']:
            v0 = p2['v_start']
            def f2(u): return p2['f_grid'](u, v0)
            def g2(u): return p2['g_grid'](u, v0)
            def h2(u): return p2['h_grid'](u, v0)
        else:
            f2, g2, h2 = p2['f'], p2['g'], p2['h']
        # F3
        if p3['grid']:
            v0 = p3['v_start']
            def f3(u): return p3['f_grid'](u, v0)
            def g3(u): return p3['g_grid'](u, v0)
            def h3(u): return p3['h_grid'](u, v0)
        else:
            f3, g3, h3 = p3['f'], p3['g'], p3['h']
        if transform_ini:  # do initial transformation
            vk = [['u', p1['u_min_trafo'], 'x', 0.0],
                  ['u', p1['u_min_trafo'], 'y', 0.0],
                  ['u', p1['u_max_trafo'], 'x', 0.0],
                  ['u', p1['u_max_trafo'], 'y', 10.0],
                  ['w', p3['u_min_trafo'], 'x', 10.0],
                  ['w', p3['u_min_trafo'], 'y', 0.0],
                  ['w', p3['u_max_trafo'], 'x', 10.0],
                  ['w', p3['u_max_trafo'], 'y', 10.0]]
            nomo = Nomograph3(f1, g1, h1, f2, g2, h2, f3, g3, h3, vk)
            # F1
            if p1['grid']:
                params1['F_grid'] = lambda u, v: nomo.give_general_x_grid_fn(p1['f_grid'], p1['g_grid'], p1['h_grid'])(
                    u, v) * self.x_mirror
                params1['G_grid'] = lambda u, v: nomo.give_general_y_grid_fn(p1['f_grid'], p1['g_grid'], p1['h_grid'])(
                    u, v) * self.y_mirror
            else:
                params1['F'] = lambda u: nomo.give_x1(u) * self.x_mirror
                params1['G'] = lambda u: nomo.give_y1(u) * self.y_mirror
            # F2
            if p2['grid']:
                params2['F_grid'] = lambda u, v: nomo.give_general_x_grid_fn(p2['f_grid'], p2['g_grid'], p2['h_grid'])(
                    u, v) * self.x_mirror
                params2['G_grid'] = lambda u, v: nomo.give_general_y_grid_fn(p2['f_grid'], p2['g_grid'], p2['h_grid'])(
                    u, v) * self.y_mirror
            else:
                params2['F'] = lambda u: nomo.give_x2(u) * self.x_mirror
                params2['G'] = lambda u: nomo.give_y2(u) * self.y_mirror
            # F3
            if p3['grid']:
                params3['F_grid'] = lambda u, v: nomo.give_general_x_grid_fn(p3['f_grid'], p3['g_grid'], p3['h_grid'])(
                    u, v) * self.x_mirror
                params3['G_grid'] = lambda u, v: nomo.give_general_y_grid_fn(p3['f_grid'], p3['g_grid'], p3['h_grid'])(
                    u, v) * self.y_mirror
            else:
                params3['F'] = lambda u: nomo.give_x3(u) * self.x_mirror
                params3['G'] = lambda u: nomo.give_y3(u) * self.y_mirror
        else:  # no initial transformation
            # F1
            if p1['grid']:
                params1['F_grid'] = lambda u, v: p1['f_grid'](
                    u, v) / p1['h_grid'](u, v) * self.x_mirror
                params1['G_grid'] = lambda u, v: p1['g_grid'](
                    u, v) / p1['h_grid'](u, v) * self.y_mirror
            else:
                params1['F'] = lambda u: p1['f'](
                    u) / p1['h'](u) * self.x_mirror
                params1['G'] = lambda u: p1['g'](
                    u) / p1['h'](u) * self.y_mirror
            # F2
            if p2['grid']:
                params2['F_grid'] = lambda u, v: p2['f_grid'](
                    u, v) / p2['h_grid'](u, v) * self.x_mirror
                params2['G_grid'] = lambda u, v: p2['g_grid'](
                    u, v) / p2['h_grid'](u, v) * self.y_mirror
            else:
                params2['F'] = lambda u: p2['f'](
                    u) / p2['h'](u) * self.x_mirror
                params2['G'] = lambda u: p2['g'](
                    u) / p2['h'](u) * self.y_mirror
            # F3
            if p3['grid']:
                params3['F_grid'] = lambda u, v: p3['f_grid'](
                    u, v) / p3['h_grid'](u, v) * self.x_mirror
                params3['G_grid'] = lambda u, v: p3['g_grid'](
                    u, v) / p3['h_grid'](u, v) * self.y_mirror
            else:
                params3['F'] = lambda u: p3['f'](
                    u) / p3['h'](u) * self.x_mirror
                params3['G'] = lambda u: p3['g'](
                    u) / p3['h'](u) * self.y_mirror
        # build atoms
        # F1
        if p1['grid']:
            self.atom_F1 = Nomo_Atom_Grid(params1)
            self.add_atom(self.atom_F1)
        else:
            self.atom_F1 = Nomo_Atom(params1)
            self.add_atom(self.atom_F1)
        # F2
        if p2['grid']:
            self.atom_F2 = Nomo_Atom_Grid(params2)
            self.add_atom(self.atom_F2)
        else:
            self.atom_F2 = Nomo_Atom(params2)
            self.add_atom(self.atom_F2)
        # F3
        if p3['grid']:
            self.atom_F3 = Nomo_Atom_Grid(params3)
            self.add_atom(self.atom_F3)
        else:
            self.atom_F3 = Nomo_Atom(params3)
            self.add_atom(self.atom_F3)

        # for inital axis calculations
        # F1
        self.axis_ini_stack = []
        if p1['grid']:
            v0 = p1['v_start']
            v1 = p1['v_stop']
            u0 = p1['u_start']
            u1 = p1['u_stop']
            # first line of grid
            self.axis_ini_stack.append(Axis_Wrapper(lambda u: params1['F_grid'](u, v0),
                                                    lambda u: params1['G_grid'](
                                                        u, v0),
                                                    u0, u1))
            # second line of grid
            self.axis_ini_stack.append(Axis_Wrapper(lambda u: params1['F_grid'](u, v1),
                                                    lambda u: params1['G_grid'](
                                                        u, v1),
                                                    u0, u1))
            # third line of grid
            self.axis_ini_stack.append(Axis_Wrapper(lambda v: params1['F_grid'](u0, v),
                                                    lambda v: params1['G_grid'](
                                                        u0, v),
                                                    v0, v1))
            # fourth line of grid
            self.axis_ini_stack.append(Axis_Wrapper(lambda v: params1['F_grid'](u1, v),
                                                    lambda v: params1['G_grid'](
                                                        u1, v),
                                                    v0, v1))
        else:
            self.axis_ini_stack.append(Axis_Wrapper(f=params1['F'], g=params1['G'],
                                                    start=params1['u_min'], stop=params1['u_max']))
        # F2
        if p2['grid']:
            v0 = p2['v_start']
            v1 = p2['v_stop']
            u0 = p2['u_start']
            u1 = p2['u_stop']
            # first line of grid
            self.axis_ini_stack.append(Axis_Wrapper(lambda u: params2['F_grid'](u, v0),
                                                    lambda u: params2['G_grid'](
                                                        u, v0),
                                                    u0, u1))
            # second line of grid
            self.axis_ini_stack.append(Axis_Wrapper(lambda u: params2['F_grid'](u, v1),
                                                    lambda u: params2['G_grid'](
                                                        u, v1),
                                                    u0, u1))
            # third line of grid
            self.axis_ini_stack.append(Axis_Wrapper(lambda v: params2['F_grid'](u0, v),
                                                    lambda v: params2['G_grid'](
                                                        u0, v),
                                                    v0, v1))
            # fourth line of grid
            self.axis_ini_stack.append(Axis_Wrapper(lambda v: params2['F_grid'](u1, v),
                                                    lambda v: params2['G_grid'](
                                                        u1, v),
                                                    v0, v1))
        else:
            self.axis_ini_stack.append(Axis_Wrapper(f=params2['F'], g=params2['G'],
                                                    start=params2['u_min'], stop=params2['u_max']))
        # F3
        if p3['grid']:
            v0 = p3['v_start']
            v1 = p3['v_stop']
            u0 = p3['u_start']
            u1 = p3['u_stop']
            # first line of grid
            self.axis_ini_stack.append(Axis_Wrapper(lambda u: params3['F_grid'](u, v0),
                                                    lambda u: params3['G_grid'](
                                                        u, v0),
                                                    u0, u1))
            # second line of grid
            self.axis_ini_stack.append(Axis_Wrapper(lambda u: params3['F_grid'](u, v1),
                                                    lambda u: params3['G_grid'](
                                                        u, v1),
                                                    u0, u1))
            # third line of grid
            self.axis_ini_stack.append(Axis_Wrapper(lambda v: params3['F_grid'](u0, v),
                                                    lambda v: params3['G_grid'](
                                                        u0, v),
                                                    v0, v1))
            # fourth line of grid
            self.axis_ini_stack.append(Axis_Wrapper(lambda v: params3['F_grid'](u1, v),
                                                    lambda v: params3['G_grid'](
                                                        u1, v),
                                                    v0, v1))
        else:
            self.axis_ini_stack.append(Axis_Wrapper(f=params3['F'], g=params3['G'],
                                                    start=params3['u_min'], stop=params3['u_max']))
        # save for later
        self.params1 = params1
        self.params2 = params2
        self.params3 = params3

    def set_block(self, width=10.0, height=10.0, ignore_transforms=False):
        """
        sets original width, height
        """
        self.width = width
        self.height = height
        min_x, max_x, min_y, max_y = self.axis_ini_stack[0].calc_bound_box()
        for axis in self.axis_ini_stack:
            x_left, x_right, y_bottom, y_top = axis.calc_bound_box()
            if x_left < min_x:
                min_x = x_left
            if x_right > max_x:
                max_x = x_right
            if y_bottom < min_y:
                min_y = y_bottom
            if y_top > max_y:
                max_y = y_top
        width_orig = abs(max_x - min_x)
        height_orig = abs(max_y - min_y)
        x_factor = width / width_orig
        y_factor = height / height_orig
        # if ignoring transforms
        if ignore_transforms == True:
            x_factor = 1.0
            y_factor = 1.0
        # redefine scaled functions
        # F1
        if self.params1['grid']:
            self.atom_F1.f = lambda u, v: self.params1['F_grid'](
                u, v) * x_factor
            self.atom_F1.g = lambda u, v: self.params1['G_grid'](
                u, v) * y_factor
        else:
            self.atom_F1.f = lambda u: self.params1['F'](u) * x_factor
            self.atom_F1.g = lambda u: self.params1['G'](u) * y_factor
        # F2
        if self.params2['grid']:
            self.atom_F2.f = lambda u, v: self.params2['F_grid'](
                u, v) * x_factor
            self.atom_F2.g = lambda u, v: self.params2['G_grid'](
                u, v) * y_factor
        else:
            self.atom_F2.f = lambda u: self.params2['F'](u) * x_factor
            self.atom_F2.g = lambda u: self.params2['G'](u) * y_factor
        # F3
        if self.params3['grid']:
            self.atom_F3.f = lambda u, v: self.params3['F_grid'](
                u, v) * x_factor
            self.atom_F3.g = lambda u, v: self.params3['G_grid'](
                u, v) * y_factor
        else:
            self.atom_F3.f = lambda u: self.params3['F'](u) * x_factor
            self.atom_F3.g = lambda u: self.params3['G'](u) * y_factor
        # save axes for reference calculations
        # only axes (not grid are used as reference)
        if self.params1['grid'] == False:
            self.F1_axis = Axis_Wrapper(f=self.atom_F1.f, g=self.atom_F1.g,
                                        start=self.atom_F1.params['u_min'],
                                        stop=self.atom_F1.params['u_max'])
            self.axis_wrapper_stack.append(self.F1_axis)
        if self.params2['grid'] == False:
            self.F2_axis = Axis_Wrapper(f=self.atom_F2.f, g=self.atom_F2.g,
                                        start=self.atom_F2.params['u_min'],
                                        stop=self.atom_F2.params['u_max'])
            self.axis_wrapper_stack.append(self.F2_axis)
        if self.params3['grid'] == False:
            self.F3_axis = Axis_Wrapper(f=self.atom_F3.f, g=self.atom_F3.g,
                                        start=self.atom_F3.params['u_min'],
                                        stop=self.atom_F3.params['u_max'])
            self.axis_wrapper_stack.append(self.F3_axis)
        self.set_reference_axes()


class Nomo_Block_Type_10(Nomo_Block):
    """
    type F1(u)+F2(v)*F3(w)+F4(w)=0
    Levens: Chapter 10
    """

    def __init__(self, mirror_x=False, mirror_y=False):
        super(Nomo_Block_Type_10, self).__init__(
            mirror_x=mirror_x, mirror_y=mirror_y)

    def define_F1(self, params):
        """
        defines function F1
        """
        self.F1 = params['function']
        self.params_F1 = params

    def define_F2(self, params):
        """
        defines function F2
        """
        self.F2 = params['function']
        self.params_F2 = params

    def define_F3(self, params):
        """
        defines function F3
        """
        self.F3_3 = params['function_3']
        self.F3_4 = params['function_4']
        self.params_F3 = params

    def set_block(self, height=10.0, width=10.0):
        """
        sets the N-nomogram of the block using geometrical approach from Levens
        f1 and f3 scales are set to equal length by using multipliers c1 and c2
        """
        self.width = width
        self.height = height
        length_f1_ini = max(self.F1(self.params_F1['u_min']), self.F1(self.params_F1['u_max'])) - \
            min(self.F1(self.params_F1['u_min']),
                self.F1(self.params_F1['u_max']))
        length_f2_ini = max(self.F2(self.params_F2['u_min']), self.F2(self.params_F2['u_max'])) - \
            min(self.F2(self.params_F2['u_min']),
                self.F2(self.params_F2['u_max']))
        # c1=length_f2_ini/length_f1_ini
        # c2=c1
        # length_f1=max(c1*self.F1(self.params_F1['u_min']),c1*self.F1(self.params_F1['u_max']))
        # length_f3=max(self.F3(self.params_F3['u_min']),self.F3(self.params_F3['u_max']))
        #    length_f1=length_f3
        m1 = height / length_f1_ini
        m2 = height / length_f2_ini
        K = width
        # 1
        y_offset_1 = m1 * \
            min(self.F1(self.params_F1['u_min']),
                self.F1(self.params_F1['u_max']))
        y_offset_2 = m2 * \
            min(self.F2(self.params_F2['u_min']),
                self.F2(self.params_F2['u_max']))
        offset_2_1 = y_offset_2 - y_offset_1
        self.params_F1['F'] = lambda u: 0.0
        self.params_F1['G'] = lambda u: (self.F1(u) * m1) * self.y_mirror
        self.atom_F1 = Nomo_Atom(self.params_F1)
        self.add_atom(self.atom_F1)
        # 2
        self.params_F2['F'] = lambda u: (width) * self.x_mirror
        self.params_F2['G'] = lambda u: (
            self.F2(u) * m2 - offset_2_1) * self.y_mirror
        self.atom_F2 = Nomo_Atom(self.params_F2)
        self.add_atom(self.atom_F2)
        # 3
        def x_func(u): return (
            K * m1 * self.F3_3(u) / (m1 * self.F3_3(u) + m2))
        self.params_F3['F'] = lambda u: (
            K * m1 * self.F3_3(u) / (m1 * self.F3_3(u) + m2)) * self.x_mirror
        self.params_F3['G'] = lambda u: (-m1 * m2 * self.F3_4(u) / (m1 * self.F3_3(u) + m2) - x_func(
            u) / width * offset_2_1) * self.y_mirror
        self.atom_F3 = Nomo_Atom(self.params_F3)
        self.add_atom(self.atom_F3)

        self.F1_axis = Axis_Wrapper(f=self.params_F1['F'], g=self.params_F1['G'],
                                    start=self.params_F1['u_min'], stop=self.params_F1['u_max'])
        self.axis_wrapper_stack.append(self.F1_axis)

        self.F2_axis = Axis_Wrapper(f=self.params_F2['F'], g=self.params_F2['G'],
                                    start=self.params_F2['u_min'], stop=self.params_F2['u_max'])
        self.axis_wrapper_stack.append(self.F2_axis)

        self.F3_axis = Axis_Wrapper(f=self.params_F3['F'], g=self.params_F3['G'],
                                    start=self.params_F3['u_min'], stop=self.params_F3['u_max'])
        self.axis_wrapper_stack.append(self.F3_axis)
        self.set_reference_axes()


class Nomo_Atom:
    """
    class for single axis or equivalent.
    """

    def __init__(self, params):
        # default parameters
        self.params_default = {
            'ID': 'none',  # to identify the axis
            'tag': 'none',  # for aligning block wrt others
            'dtag': 'none',  # double alignment
            'u_min': 0.1,
            'u_max': 1.0,
            'F': lambda u: u,  # x-coordinate
            'G': lambda u: u,  # y-coordinate
            'title': 'no title given',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'scale_type': 'linear',  # 'linear' 'log' 'manual point' 'manual line'
            'tick_levels': 10,
            'tick_text_levels': 10,
            'tick_side': 'right',
            'reference': False,
            'grid': False,
            'reference_padding': 0.20,  # fraction of reference line over other lines
            'manual_axis_data': {},
            'title_distance_center': 0.5,
            'title_opposite_tick': True,
            'align_func': lambda u: u,  # function to align different scalings
            'align_x_offset': 0.0,
            'align_y_offset': 0.0,
            'aligned': False,
            'base_start': None,
            'base_stop': None,
            'scale_max': None,
            'extra_params': [],  # additional axis params
            'debug': False,  # print dictionary
            'tick_distance_smart': 0.05,
            'full_angle': False,
            'extra_angle': 0.0,
            'turn_relative': False,
        }
        self.params = self.params_default
        self.params.update(params)
        # let's make default values for extra params
        for idx, iter_params in enumerate(self.params['extra_params']):
            for key in self.params_default:
                if not key in iter_params:
                    self.params['extra_params'][idx][key] = self.params_default[key]
        self.set_trafo()  # initialize
        self.f = self.params['F']  # x-coord func
        self.g = self.params['G']  # y-coord func
        self.f_ref = self.params['F']  # x-coord func for reflection axis
        self.g_ref = self.params['G']  # y-coord func for reflection axis

    def calc_line_and_sections(self):
        """
        calculates line and sections
        """
        self.line = []
        self.value_list = []  # list of values corresponding to points
        if self.params['reference'] == False:
            start = self.params['u_min']
            stop = self.params['u_max']
            f = self.give_x
            g = self.give_y
        else:
            start = self.u_min_ref
            stop = self.u_max_ref
            f = self.give_x_ref
            g = self.give_y_ref
        if start > stop:
            start, stop = stop, start
        du = math.fabs(stop - start) * 1e-6
        # approximate line length is found
        line_length_straigth = math.sqrt(
            (f(start) - f(stop)) ** 2 + (g(start) - g(stop)) ** 2)
        random.seed(0.0)  # so that mistakes always the same
        for dummy in range(100):  # for case if start = stop
            first = random.uniform(start, stop)
            second = random.uniform(start, stop)
            temp = math.sqrt((f(first) - f(second)) ** 2 +
                             (g(first) - g(second)) ** 2)
            if temp > line_length_straigth:
                line_length_straigth = temp
                # print "length: %f"%line_length_straigth
        sections = 1000.0  # about number of sections
        section_length = line_length_straigth / sections
        u = start
        laskuri = 1
        self.line.append((f(start), g(start)))
        self.value_list.append(start)
        # print "start: %g"%(start)
        # print "stop: %g"%(stop)
        # print "du: %g"%(du)
        while True:
            if u < stop:
                self.line.append((f(u), g(u)))
                self.value_list.append(u)
                dx = (f(u + du) - f(u))
                dy = (g(u + du) - g(u))
                dl = math.sqrt(dx ** 2 + dy ** 2)
                if dl > 0:
                    delta_u = du * section_length / dl
                else:
                    delta_u = du
                # in order to avoid too slow derivatives
                if math.fabs(stop - start) < (delta_u * 100.0):
                    delta_u = math.fabs(stop - start) / 500.0
                u += delta_u

            else:
                self.line.append((f(stop), g(stop)))
                self.value_list.append(stop)
                break
        # calculate sections
        sections = []
        section_values = []
        for index, (x, y) in enumerate(self.line):
            if index > 0:
                sections.append((x, y, prev_x, prev_y))
                section_values.append([self.value_list[index],
                                       self.value_list[index - 1]])
            prev_x = x
            prev_y = y
        self.sections = sections
        self.section_values = section_values

    def set_trafo(self, alpha1=1.0, beta1=0.0, gamma1=0.0,
                  alpha2=0.0, beta2=1.0, gamma2=0.0,
                  alpha3=0.0, beta3=0.0, gamma3=1.0):
        """
        sets the transformation for x,y points to be applied
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

    def give_x(self, u):
        """
        x-function
        """
        value = (self.alpha1 * self.f(u) + self.beta1 * self.g(u) + self.gamma1) / \
                (self.alpha3 * self.f(u) + self.beta3 * self.g(u) + self.gamma3)
        return value

    def give_y(self, u):
        """
        y-function
        """
        value = (self.alpha2 * self.f(u) + self.beta2 * self.g(u) + self.gamma2) / \
                (self.alpha3 * self.f(u) + self.beta3 * self.g(u) + self.gamma3)
        return value

    def give_x_ref(self, u):
        """
        x-function for reflection axis
        """
        value = (self.alpha1 * self.f_ref(u) + self.beta1 * self.g_ref(u) + self.gamma1) / \
                (self.alpha3 * self.f_ref(u) +
                 self.beta3 * self.g_ref(u) + self.gamma3)
        return value

    def give_y_ref(self, u):
        """
        y-function for reflection axis
        """
        value = (self.alpha2 * self.f_ref(u) + self.beta2 * self.g_ref(u) + self.gamma2) / \
                (self.alpha3 * self.f_ref(u) +
                 self.beta3 * self.g_ref(u) + self.gamma3)
        return value

    def draw(self, canvas):
        """
        draws the axis
        """
        p = self.params
        # print p['title']
        # print p['tick_levels']
        # print p['tick_text_levels']
        """
        base start is from initial dict
        """
        if not p['reference'] == True:
            if p['base_start'] is None:
                base_start = p['u_min']
            else:
                base_start = p['base_start']
            if p['base_stop'] is None:
                base_stop = p['u_max']
            else:
                base_stop = p['base_stop']
            self.nomo_axis_ref = Nomo_Axis(func_f=self.give_x, func_g=self.give_y,
                                           start=p['u_min'], stop=p['u_max'],
                                           turn=-1, title=p['title'], canvas=canvas, type=p['scale_type'],
                                           tick_levels=p['tick_levels'], tick_text_levels=p['tick_text_levels'],
                                           side=p['tick_side'], manual_axis_data=p['manual_axis_data'],
                                           title_x_shift=p['title_x_shift'], title_y_shift=p['title_y_shift'],
                                           axis_appear=p, base_start=base_start, base_stop=base_stop)
            for pp in p['extra_params']:
                if pp['base_start'] is None:
                    base_start_pp = base_start
                else:
                    base_start_pp = pp['base_start']
                if pp['base_stop'] is None:
                    base_stop_pp = base_stop
                else:
                    base_stop_pp = pp['base_stop']
                Nomo_Axis(func_f=self.give_x, func_g=self.give_y,
                          start=pp['u_min'], stop=pp['u_max'],
                          turn=-1, title='', canvas=canvas, type=pp['scale_type'],
                          tick_levels=pp['tick_levels'], tick_text_levels=pp['tick_text_levels'],
                          side=pp['tick_side'], manual_axis_data=pp['manual_axis_data'],
                          title_x_shift=pp['title_x_shift'], title_y_shift=pp['title_y_shift'],
                          axis_appear=pp, base_start=base_start_pp, base_stop=base_stop_pp)
        else:  # reference axis
            # print "u_min_ref"
            # print self.u_min_ref
            # print "u_max_ref"
            # print self.u_max_ref
            Nomo_Axis(func_f=self.give_x_ref, func_g=self.give_y_ref,
                      start=self.u_min_ref, stop=self.u_max_ref,
                      turn=-1, title=p['title'], canvas=canvas, type=p['scale_type'],
                      tick_levels=0, tick_text_levels=0,
                      side=p['tick_side'], axis_appear=p)
        if p['debug']:
            print("##### SINGLE AXIS PARAMS #######")
            pprint.pprint(p)


class Nomo_Atom_Grid(Nomo_Atom):
    """
    Grid type Atom
    """

    def __init__(self, params):
        # default parameters
        self.params_default = {
            'ID': 'none',  # to identify the axis
            'tag': 'none',  # for aligning block wrt others
            'dtag': 'none',  # double alignment
            'title': 'no title given',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'title_distance_center': 0.5,
            'title_opposite_tick': True,
            'u_min': None,  # for alignment
            'u_max': None,  # for alignment
            'F_grid': None,
            'G_grid': None,
            'u_start': 0.0,
            'u_stop': 1.0,
            'v_start': 0.0,
            'v_stop': 1.0,
            'u_values': [0.0, 0.25, 0.5, 0.75, 1.0],
            'v_values': [0.0, 0.25, 0.5, 0.75, 1.0],
            'reference': False,
            'grid': True,
            'v_texts_u_start': False,
            'v_texts_u_stop': True,
            'u_texts_v_start': False,
            'u_texts_v_stop': True,
            'u_line_color': pyx.color.rgb.black,
            'v_line_color': pyx.color.rgb.black,
            'u_text_color': pyx.color.rgb.black,
            'v_text_color': pyx.color.rgb.black,
            'extra_params': [],
            'debug': False,  # print dictionary
        }
        self.params = self.params_default
        self.params.update(params)
        self.params['u_min'] = self.params['u_start']
        self.params['u_max'] = self.params['u_stop']
        for idx, iter_params in enumerate(self.params['extra_params']):
            for key in self.params_default:
                if not key in iter_params:
                    self.params['extra_params'][idx][key] = self.params_default[key]
        self.set_trafo()  # initialize
        self.f = self.params['F_grid']
        self.g = self.params['G_grid']

    def calc_line_and_sections(self):
        """
        calculates line and sections... TBD
        """
        pass

    def give_x(self, u):
        """
        gives first line x. This x is used if grid is to be aligned
        with an axis.
        """
        v0 = self.params['v_start']  # value for reference line
        value = (self.alpha1 * self.f(u, v0) + self.beta1 * self.g(u, v0) + self.gamma1) / \
                (self.alpha3 * self.f(u, v0) +
                 self.beta3 * self.g(u, v0) + self.gamma3)
        return value

    def give_y(self, u):
        """
        gives first line y. This y is used if grid is to be aligned
        with an axis.
        """
        v0 = self.params['v_start']  # value for reference line
        value = (self.alpha2 * self.f(u, v0) + self.beta2 * self.g(u, v0) + self.gamma2) / \
                (self.alpha3 * self.f(u, v0) +
                 self.beta3 * self.g(u, v0) + self.gamma3)
        return value

    def give_x_grid(self, u, v):
        """
        gives x of grid.
        """
        value = (self.alpha1 * self.f(u, v) + self.beta1 * self.g(u, v) + self.gamma1) / \
                (self.alpha3 * self.f(u, v) +
                 self.beta3 * self.g(u, v) + self.gamma3)
        return value

    def give_y_grid(self, u, v):
        """
        gives y of grid.
        """
        value = (self.alpha2 * self.f(u, v) + self.beta2 * self.g(u, v) + self.gamma2) / \
                (self.alpha3 * self.f(u, v) +
                 self.beta3 * self.g(u, v) + self.gamma3)
        return value

    def draw(self, canvas):
        """
        draws the grid
        """
        for pp in self.params['extra_params']:
            Nomo_Grid(func_f=self.give_x_grid, func_g=self.give_y_grid,
                      canvas=canvas, data=pp)
        # main nomogram
        self.grid_ref = Nomo_Grid(func_f=self.give_x_grid, func_g=self.give_y_grid,
                                  canvas=canvas, data=self.params)
        if self.params['debug']:
            print("##### SINGLE AXIS PARAMS #######")
            pprint.pprint(self.params)


if __name__ == '__main__':
    """
    testing
    """
    test = Nomo_Wrapper()
    # print test._calc_trafo_(1,0,1,1,2,0,1,0,1,1,2,0)
    # print test._calc_trafo_(1,0,1,1,2,0,4,1,4,2,5,1)
    """
    0. build definitions of atoms
    1. build block1
    2. build block2
    3. build nomowrapper
    4. add block1 and block2
    5. optimize transformation
    6. draw nomogram in nomowrapper
    """
    do_test_1 = False
    # do_test_1=True
    do_test_2 = False
    # do_test_2=True
    # do_test_3=False
    do_test_3 = False
    do_test_4 = False
    # do_test_4=True
    do_test_5 = False
    # do_test_5=True
    do_test_6 = False
    # do_test_6=True
    do_test_7 = False
    # do_test_7=True
    do_test_8 = False
    # do_test_8=True
    do_test_9 = False
    do_test_9 = True
    # do_test_10=False
    do_test_10 = True
    if do_test_1:
        # build atoms
        block1_atom1_para = {
            'u_min': 3.0,
            'u_max': 10.0,
            'F': lambda u: 0,
            'G': lambda u: u,
            'title': 'b1 a1',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'scale_type': 'linear',
            'tick_levels': 10,
            'tick_text_levels': 10,
            'tick_side': 'right',
            'tag': 'none'}
        b1_atom1 = Nomo_Atom(params=block1_atom1_para)

        block1_atom2_para = {
            'u_min': 3.0,
            'u_max': 10.0,
            'F': lambda u: 1.0,
            'G': lambda u: u,
            'title': 'b1 a2',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'scale_type': 'linear',
            'tick_levels': 10,
            'tick_text_levels': 10,
            'tick_side': 'right',
            'tag': 'none'}
        b1_atom2 = Nomo_Atom(params=block1_atom2_para)

        block1_atom3_para = {
            'u_min': 0.0,
            'u_max': 10.0,
            'F': lambda u: 2.0,
            'G': lambda u: u,
            'title': 'b1 a3',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'scale_type': 'linear',
            'tick_levels': 10,
            'tick_text_levels': 10,
            'tick_side': 'right',
            'tag': 'A'}

        b1_atom3 = Nomo_Atom(params=block1_atom3_para)

        # block 2
        block2_atom1_para = {
            'u_min': 0.0,
            'u_max': 10.0,
            'F': lambda u: u,
            'G': lambda u: 0.0 + 0.1 * u,
            'title': 'b2 a1',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'scale_type': 'linear',
            'tick_levels': 10,
            'tick_text_levels': 10,
            'tick_side': 'right',
            'tag': 'B'}
        b2_atom1 = Nomo_Atom(params=block2_atom1_para)

        block2_atom2_para = {
            'u_min': 0.0,
            'u_max': 10.0,
            'F': lambda u: u,
            'G': lambda u: 1.0 + 0.1 * u,
            'title': 'b2 a2',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'scale_type': 'linear',
            'tick_levels': 10,
            'tick_text_levels': 10,
            'tick_side': 'right',
            'tag': 'none'}
        b2_atom2 = Nomo_Atom(params=block2_atom2_para)

        block2_atom3_para = {
            'u_min': 1.0,
            'u_max': 10.0,
            'F': lambda u: u,
            'G': lambda u: 2.0 + 0.1 * u,
            'title': 'b2 a3',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'scale_type': 'linear',
            'tick_levels': 10,
            'tick_text_levels': 10,
            'tick_side': 'left',
            'tag': 'A'}

        b2_atom3 = Nomo_Atom(params=block2_atom3_para)

        # block 3
        block3_atom1_para = {
            'u_min': 0.0,
            'u_max': 10.0,
            'F': lambda u: u,
            'G': lambda u: 0.0 + 0.5 * u,
            'title': 'b3 a1',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'scale_type': 'linear',
            'tick_levels': 10,
            'tick_text_levels': 10,
            'tick_side': 'right',
            'tag': 'none'}
        b3_atom1 = Nomo_Atom(params=block3_atom1_para)

        block3_atom2_para = {
            'u_min': 0.0,
            'u_max': 10.0,
            'F': lambda u: 0.1 * u ** 2,
            'G': lambda u: 1.0 + 0.5 * u,
            'title': 'b3 a2',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'scale_type': 'linear',
            'tick_levels': 10,
            'tick_text_levels': 10,
            'tick_side': 'right',
            'tag': 'none'}
        b3_atom2 = Nomo_Atom(params=block3_atom2_para)

        block3_atom3_para = {
            'u_min': 1.0,
            'u_max': 10.0,
            'F': lambda u: u,
            'G': lambda u: 2.0 + 0.5 * u,
            'title': 'b3 a3',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'scale_type': 'linear',
            'tick_levels': 10,
            'tick_text_levels': 10,
            'tick_side': 'left',
            'tag': 'B'}

        b3_atom3 = Nomo_Atom(params=block3_atom3_para)

        block4_f1_para = {
            'u_min': -3.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'f1'
        }

        block4_f2_para = {
            'u_min': 2.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'f2'
        }
        block4_f3_para = {
            'u_min': 0.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'f3',
            'tag': 'C',
            'reference': True
        }

        block5_f1_para = {
            'u_min': 1.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'f1 b',
            'tag': 'C',
            'tick_side': 'left'
        }

        block5_f2_para = {
            'u_min': 2.0,
            'u_max': 11.0,
            'function': lambda u: u,
            'title': 'f2 b',
            'reference': True
        }
        block5_f3_para = {
            'u_min': 0.0,
            'u_max': 11.0,
            'function': lambda u: u,
            'title': 'f3 b',
            'tag': 'D',
            'tick_side': 'left'
        }

        block6_f1_para = {
            'u_min': 1.0,
            'u_max': 12.0,
            'function': lambda u: u,
            'title': 'f1 c',
            'tag': 'D',
            'tick_side': 'right'
        }

        block6_f2_para = {
            'u_min': 0.1,
            'u_max': 4.0,
            'function': lambda u: u,
            'title': 'f2 c'
        }
        block6_f3_para = {
            'u_min': 0.0,
            'u_max': 12.0,
            'function': lambda u: u,
            'title': 'f3 c',
            'reference': False
        }

        block7_f1_para = {
            'u_min': -12.0,
            'u_max': 12.0,
            'function': lambda u: u,
            'title': 'N1',
            'tag': 'none',
            'tick_side': 'right'
        }
        block7_f2_para = {
            'u_min': -12.0,
            'u_max': 12.0,
            'function': lambda u: u,
            'title': 'N2',
            'tag': 'none',
            'tick_side': 'right'
        }
        block7_f3_para = {
            'u_min': -12.0,
            'u_max': 12.0,
            'function': lambda u: u,
            'title': 'N3',
            'tag': 'none',
            'tick_side': 'right'
        }
        block7_f4_para = {
            'u_min': -12.0,
            'u_max': 12.0,
            'function': lambda u: u,
            'title': 'N4',
            'tag': 'none',
            'tick_side': 'right'
        }

        block7_f5_para = {
            'u_min': -12.0,
            'u_max': 12.0,
            'function': lambda u: u,
            'title': 'N5',
            'tag': 'none',
            'tick_side': 'right'
        }

        block1 = Nomo_Block()
        block1.add_atom(b1_atom1)
        block1.add_atom(b1_atom2)
        block1.add_atom(b1_atom3)

        block2 = Nomo_Block()
        block2.add_atom(b2_atom1)
        block2.add_atom(b2_atom2)
        block2.add_atom(b2_atom3)

        block3 = Nomo_Block()
        block3.add_atom(b3_atom1)
        block3.add_atom(b3_atom2)
        block3.add_atom(b3_atom3)

        block4 = Nomo_Block_Type_1()
        block4.define_F1(block4_f1_para)
        block4.define_F2(block4_f2_para)
        block4.define_F3(block4_f3_para)
        block4.set_block(width=5.0, height=25.0, proportion=1.2)

        block5 = Nomo_Block_Type_1(mirror_x=True)
        block5.define_F1(block5_f1_para)
        block5.define_F2(block5_f2_para)
        block5.define_F3(block5_f3_para)
        block5.set_block(width=5.0, height=25.0, proportion=1.2)

        block6 = Nomo_Block_Type_2(mirror_x=True)
        block6.define_F1(block6_f1_para)
        block6.define_F2(block6_f2_para)
        block6.define_F3(block6_f3_para)
        block6.set_block(height=10.0, width=3.0)

        block7 = Nomo_Block_Type_3(mirror_x=True)
        block7.add_F(block7_f1_para)
        block7.add_F(block7_f2_para)
        block7.add_F(block7_f3_para)
        block7.add_F(block7_f4_para)
        block7.add_F(block7_f5_para)
        block7.set_block()

        wrapper = Nomo_Wrapper(paper_width=2 * 40.0, paper_height=2 * 60.0)
        # wrapper.add_block(block1)
        # wrapper.add_block(block2)
        # wrapper.add_block(block3)
        wrapper.add_block(block4)
        wrapper.add_block(block5)
        wrapper.add_block(block6)
        wrapper.add_block(block7)
        wrapper.align_blocks()
        wrapper.build_axes_wrapper()  # build structure for optimization
        # wrapper.do_transformation(method='scale paper')
        # wrapper.do_transformation(method='rotate',params=10.0)
        # wrapper.do_transformation(method='rotate',params=30.0)
        # wrapper.do_transformation(method='rotate',params=20.0)
        # wrapper.do_transformation(method='rotate',params=90.0)
        wrapper.do_transformation(method='polygon')
        # wrapper.do_transformation(method='optimize')
        wrapper.do_transformation(method='scale paper')
        c = pyx.canvas.canvas()
        wrapper.draw_nomogram(c)
    # end of test1

    if do_test_2:
        block8_f1_para = {
            'u_min': 1.0,
            'u_max': 12.0,
            'function': lambda u: u,
            'title': 'F1',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2
        }

        block8_f2_para = {
            'u_min': 1.0,
            'u_max': 18.0,
            'function': lambda u: u,
            'title': 'F2',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2,
            'tag': 'A'
        }

        block8_f3_para = {
            'u_min': 1.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'F3',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2
        }

        block8_f4_para = {
            'u_min': 1.0,
            'u_max': 14.0,
            'function': lambda u: u,
            'title': 'F4',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2,
            'tag': 'B'
        }
        block9_f1_para = {
            'u_min': 1.0,
            'u_max': 12.0,
            'function': lambda u: u,
            'title': 'F1',
            'tag': 'none',
            'tick_side': 'left',
            'tick_levels': 2,
            'tick_text_levels': 2,
            'tag': 'A'
        }

        block9_f2_para = {
            'u_min': 0.1,
            'u_max': 2.0,
            'function': lambda u: u,
            'title': 'F2',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 1,
            'tick_text_levels': 1
        }

        block9_f3_para = {
            'u_min': 1.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'F3',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2
        }

        block10_f1_para = {
            'u_min': 1.0,
            'u_max': 12.0,
            'function': lambda u: u - 7,
            'title': 'F1',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2,
            'tag': 'B'
        }

        block10_f2_para = {
            'u_min': 1.0,
            'u_max': 18.0,
            'function': lambda u: u + 7,
            'title': 'F2',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2
        }

        block10_f3_para = {
            'u_min': -10,
            'u_max': 0.0,
            'function': lambda u: u,
            'title': 'F3',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2
        }

        block10_f4_para = {
            'u_min': 1.0,
            'u_max': 14.0,
            'function': lambda u: u + 7,
            'title': 'F4',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2
        }

        block10_f5_para = {
            'u_min': 1.0,
            'u_max': 14.0,
            'function': lambda u: u - 7,
            'title': 'F5',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2
        }

        block8 = Nomo_Block_Type_4(mirror_x=False)
        block8.define_F1(block8_f1_para)
        block8.define_F2(block8_f2_para)
        block8.define_F3(block8_f3_para)
        block8.define_F4(block8_f4_para)
        block8.set_block()
        block8.set_reference_axes()
        block9 = Nomo_Block_Type_2(mirror_x=True)
        block9.define_F1(block9_f1_para)
        block9.define_F2(block9_f2_para)
        block9.define_F3(block9_f3_para)
        block9.set_block()

        block10 = Nomo_Block_Type_3(mirror_x=False)
        block10.add_F(block10_f1_para)
        block10.add_F(block10_f2_para)
        block10.add_F(block10_f3_para)
        block10.add_F(block10_f4_para)
        block10.add_F(block10_f5_para)
        block10.set_block(width=10.0, height=10.0)
        # block10.set_reference_axes()

        wrapper1 = Nomo_Wrapper(
            paper_width=20.0, paper_height=20.0, filename='type4.pdf')
        wrapper1.add_block(block8)
        wrapper1.add_block(block9)
        wrapper1.add_block(block10)
        wrapper1.align_blocks()
        wrapper1.build_axes_wrapper()  # build structure for optimization
        # wrapper1.do_transformation(method='scale paper')
        wrapper1.do_transformation(method='rotate', params=10.0)
        # wrapper1.do_transformation(method='rotate',params=30.0)
        # wrapper1.do_transformation(method='rotate',params=20.0)
        # wrapper1.do_transformation(method='rotate',params=90.0)
        # wrapper1.do_transformation(method='polygon')
        # wrapper1.do_transformation(method='optimize')
        wrapper1.do_transformation(method='scale paper')
        cc = pyx.canvas.canvas()
        wrapper1.draw_nomogram(cc)
    # end of test_2
    if do_test_3:
        def f1(x, u):
            # return np.log(np.log(x/(x-u/100.0))/log(1+u/100.0))
            return np.log(np.log(x / (x - u / (100.0 * 12.0))) / np.log(1 + u / (100.0 * 12.0)))

        params = {'width': 10.0,
                  'height': 10.0,
                  # 'u_func':lambda u:log(u),
                  'u_func': lambda u: np.log(u * 12.0),
                  'v_func': f1,
                  'u_values': [10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0],
                  'v_values': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
                  'v_tick_side': 'left',
                  'u_title': 'years',
                  'v_title': r'interest rate \%',
                  'u_reference': False,  # manual labels
                  'v_reference': False,
                  'w_reference': False,
                  'wd_reference': False,
                  'wd_tick_levels': 0,
                  'wd_tick_text_levels': 0,
                  'wd_tag': 'A',
                  'w_tick_levels': 0,
                  'w_tick_text_levels': 0,
                  'horizontal_guides': False,
                  }
        block11 = Nomo_Block_Type_5(mirror_x=False)
        block11.define_block(params)
        block11.set_block()

        block12_f3_para = {
            # 'u_min':0.03,
            'u_min': block11.grid_box.params_wd['u_min'],
            # 'u_max':0.16,
            'u_max': block11.grid_box.params_wd['u_max'],
            'function': lambda u: u,
            'title': '',
            'tag': 'A',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2,
            'tag': 'A',
            'reference': False,
            'tick_levels': 0,
            'tick_text_levels': 0,
            'title_draw_center': True
        }
        block12_f2_para = {
            'u_min': 30.0,
            'u_max': 1000.0,
            'function': lambda u: u,
            'title': 'Loan',
            'tag': 'none',
            'tick_side': 'left',
            'tick_levels': 3,
            'tick_text_levels': 2,
            'title_draw_center': True
        }
        block12_f1_para = {
            'u_min': 0.2,
            'u_max': 3.0,
            # 'function':lambda u:u*12.0,
            'function': lambda u: u,
            'title': 'monthly payment',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 3,
            'tick_text_levels': 2,
            'title_draw_center': True
        }

        block12 = Nomo_Block_Type_2(mirror_x=False)
        block12.define_F1(block12_f1_para)
        block12.define_F2(block12_f2_para)
        block12.define_F3(block12_f3_para)
        block12.set_block(height=10.0, width=5.0)

        wrapper2 = Nomo_Wrapper(params={
            'title_str': r'Amortized loan calculator    \copyright    Leif Roschier  2008',
            'title_x': 17,
            'title_y': 21,
            'title_box_width': 5,
            'mirror_y': False},
            paper_width=20.0, paper_height=20.0, filename='type5.pdf')
        wrapper2.add_block(block11)
        wrapper2.add_block(block12)
        wrapper2.align_blocks()
        wrapper2.build_axes_wrapper()  # build structure for optimization
        # wrapper2.do_transformation(method='scale paper')
        wrapper2.do_transformation(method='rotate', params=0.01)
        # wrapper2.do_transformation(method='rotate',params=30.0)
        # wrapper2.do_transformation(method='rotate',params=20.0)
        # wrapper2.do_transformation(method='rotate',params=90.0)
        # wrapper2.do_transformation(method='polygon')
        # wrapper2.do_transformation(method='optimize')
        wrapper2.do_transformation(method='scale paper')
        ccc = pyx.canvas.canvas()
        wrapper2.draw_nomogram(ccc)
        # end of test3
    if do_test_4:
        block20_f1_para = {
            'u_min': 0.0,
            'u_max': 12.0,
            'function': lambda u: u,
            'title': 'F1',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2,
            'tag': 'B'
        }
        block20_f2_para = {
            'u_min': 0.0,
            'u_max': 18.0,
            'function': lambda u: u,
            'title': 'F2',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2
        }
        block20_f3_para = {
            'u_min': 0.0,
            'u_max': 20.0,
            'function': lambda u: -u,
            'title': 'F3',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2
        }

        block20_f4_para = {
            'u_min': 0.0,
            'u_max': 14.0,
            'function': lambda u: u,
            'title': 'F4',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2
        }
        block20_f5_para = {
            'u_min': 0.0,
            'u_max': 34.0,
            'function': lambda u: u,
            'title': 'F5',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2
        }
        block20 = Nomo_Block_Type_3(mirror_x=False)
        block20.add_F(block20_f1_para)
        block20.add_F(block20_f2_para)
        block20.add_F(block20_f3_para)
        block20.add_F(block20_f4_para)
        block20.add_F(block20_f5_para)
        block20.set_block(width=10.0, height=10.0)
        wrapper4 = Nomo_Wrapper(
            paper_width=20.0, paper_height=20.0, filename='type3a.pdf')
        wrapper4.add_block(block20)
        wrapper4.align_blocks()
        wrapper4.build_axes_wrapper()  # build structure for optimization
        # wrapper1.do_transformation(method='scale paper')
        # wrapper4.do_transformation(method='rotate',params=10.0)
        # wrapper1.do_transformation(method='rotate',params=30.0)
        # wrapper1.do_transformation(method='rotate',params=20.0)
        # wrapper1.do_transformation(method='rotate',params=90.0)
        # wrapper4.do_transformation(method='polygon')
        # wrapper1.do_transformation(method='optimize')
        wrapper4.do_transformation(method='scale paper')
        cc4 = pyx.canvas.canvas()
        wrapper4.draw_nomogram(cc4)

    if do_test_5:
        # build atoms
        block30_f1_para = {
            'u_min': 1.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'F1',
            'tag': 'none',
            'tick_side': 'left',
            'tick_levels': 2,
            'scale_type': 'linear',
            'tick_text_levels': 2
        }

        block30_f1_para_a = {
            'u_min': 1.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'F1',
            'tag': 'none',
            'tick_side': 'left',
            'tick_levels': 2,
            'scale_type': 'manual point',
            'manual_axis_data': {
                1: '1',
                3.14: r'$\pi$',
                5: '5',
                10: '10'},
            'tick_text_levels': 2
        }

        block30_f2_para = {
            'u_min': 1.0,
            'u_max': 10.0,
            'function': lambda u: np.log(u),
            'title': 'F2',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 2
        }
        block30 = Nomo_Block_Type_6(mirror_x=False, mirror_y=False)
        block30.define(params1=block30_f1_para, params2=block30_f2_para)
        block30.set_block(width=5.0, height=25.0, type='orthogonal')
        wrapper5 = Nomo_Wrapper(
            paper_width=20.0, paper_height=20.0, filename='type6.pdf')
        wrapper5.add_block(block30)
        wrapper5.align_blocks()
        wrapper5.build_axes_wrapper()  # build structure for optimization
        # wrapper1.do_transformation(method='scale paper')
        wrapper5.do_transformation(method='rotate', params=0.01)
        # wrapper1.do_transformation(method='rotate',params=30.0)
        # wrapper1.do_transformation(method='rotate',params=20.0)
        # wrapper1.do_transformation(method='rotate',params=90.0)
        # wrapper4.do_transformation(method='polygon')
        # wrapper1.do_transformation(method='optimize')
        wrapper5.do_transformation(method='scale paper')
        cc5 = pyx.canvas.canvas()
        wrapper5.draw_nomogram(cc5)

    if do_test_6:
        block60_f1_para = {
            'u_min': 1.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'F1',
            'tag': 'none',
            'tick_side': 'left',
            'tick_levels': 3,
            'tick_text_levels': 2,
            'title_draw_center': True
        }
        block60_f2_para = {
            'u_min': 1.0,
            'u_max': 10.0,
            'function': lambda u: u,
            'title': 'F2',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 3,
            'tick_text_levels': 2,
            'title_draw_center': True
        }
        block60_f3_para = {
            'u_min': 1.0,
            'u_max': 10.0,
            # 'function':lambda u:u*12.0,
            'function': lambda u: u,
            'title': 'F3',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 3,
            'tick_text_levels': 2,
            'title_draw_center': True
        }
        block60 = Nomo_Block_Type_7(mirror_x=False)
        block60.define_F1(block60_f1_para)
        block60.define_F2(block60_f2_para)
        block60.define_F3(block60_f3_para)
        block60.set_block(width_1=10.0, angle_u=20.0, angle_v=60.0)
        wrapper60 = Nomo_Wrapper(
            paper_width=20.0, paper_height=20.0, filename='type7.pdf')
        wrapper60.add_block(block60)
        wrapper60.align_blocks()
        wrapper60.build_axes_wrapper()  # build structure for optimization
        # wrapper1.do_transformation(method='scale paper')
        wrapper60.do_transformation(method='rotate', params=0.01)
        # wrapper1.do_transformation(method='rotate',params=30.0)
        # wrapper1.do_transformation(method='rotate',params=20.0)
        # wrapper1.do_transformation(method='rotate',params=90.0)
        # wrapper4.do_transformation(method='polygon')
        # wrapper1.do_transformation(method='optimize')
        wrapper60.do_transformation(method='scale paper')
        cc60 = pyx.canvas.canvas()
        wrapper60.draw_nomogram(cc60)

    if do_test_7:
        block70_f_para = {
            'u_min': 0.0,
            'u_max': 20.0,
            'function': lambda u: u,
            'title': 'F1',
            'tag': 'A',
            'tick_side': 'left',
            'tick_levels': 3,
            'tick_text_levels': 2
        }
        block71_f_para = {
            'u_min': 1.0,
            'u_max': 4.0,
            'function': lambda u: u ** 2,
            'title': 'F2',
            'tag': 'A',
            'tick_side': 'right',
            'tick_levels': 3,
            'tick_text_levels': 2,
            'align_func': lambda u: u ** 2
        }
        block70 = Nomo_Block_Type_8(mirror_x=False)
        block70.define_F(block70_f_para)
        block70.set_block(length=12)
        block71 = Nomo_Block_Type_8(mirror_x=False)
        block71.define_F(block71_f_para)
        block71.set_block(length=12)
        wrapper70 = Nomo_Wrapper(
            paper_width=20.0, paper_height=20.0, filename='type8.pdf')
        wrapper70.add_block(block70)
        wrapper70.add_block(block71)
        wrapper70.align_blocks()
        wrapper70.build_axes_wrapper()  # build structure for optimization
        # wrapper1.do_transformation(method='scale paper')
        wrapper70.do_transformation(method='rotate', params=0.01)
        # wrapper1.do_transformation(method='rotate',params=30.0)
        # wrapper1.do_transformation(method='rotate',params=20.0)
        # wrapper1.do_transformation(method='rotate',params=90.0)
        # wrapper4.do_transformation(method='polygon')
        # wrapper1.do_transformation(method='optimize')
        # wrapper70.do_transformation(method='scale paper')
        cc70 = pyx.canvas.canvas()
        wrapper70.draw_nomogram(cc70)

    if do_test_8:
        # determinant nomograph
        block80_f1_para = {
            'u_min': 0.5,
            'u_max': 1.0,
            'f': lambda u: 2 * (u * u - 1.0),
            'g': lambda u: 3 * u * (u + 1.0),
            'h': lambda u: (-u * (u - 1.0)),
            'title': 'p',
            'tick_side': 'left',
            'tick_levels': 4,
            'tick_text_levels': 2,
            'grid': False
        }
        block80_f2_para = {
            'u_min': 1.0,
            'u_max': 0.75,
            'f': lambda v: v,
            'g': lambda v: 1.0,
            'h': lambda v: (-v * v),
            'title': 'h',
            'tick_side': 'right',
            'tick_levels': 3,
            'tick_text_levels': 2,
            'grid': False
        }
        block80_f3_para = {
            'u_min': 1.0,
            'u_max': 0.5,
            'f': lambda w: 2.0 * (2.0 * w + 1.0),
            'g': lambda w: 3.0 * (w + 1.0),
            'h': lambda w: (-(w + 1.0) * (2.0 * w + 1.0)),
            'title': 'L',
            'tick_side': 'left',
            'tick_levels': 4,
            'tick_text_levels': 2,
            'grid': False
        }

        block80 = Nomo_Block_Type_9()
        # block80.define_F1(block80_f1_para)
        # block80.define_F2(block80_f2_para)
        # block80.define_F3(block80_f3_para)
        block80.define_determinant(block80_f1_para, block80_f2_para,
                                   block80_f3_para, transform_ini=True)
        block80.set_block(width=12.0, height=15.0)

        wrapper80 = Nomo_Wrapper(
            paper_width=10.0, paper_height=10.0, filename='type9.pdf')
        wrapper80.add_block(block80)
        wrapper80.align_blocks()
        wrapper80.build_axes_wrapper()  # build structure for optimization
        # wrapper1.do_transformation(method='scale paper')
        wrapper80.do_transformation(method='rotate', params=0.01)
        # wrapper1.do_transformation(method='rotate',params=30.0)
        # wrapper1.do_transformation(method='rotate',params=20.0)
        # wrapper1.do_transformation(method='rotate',params=90.0)
        # wrapper80.do_transformation(method='polygon')
        # wrapper1.do_transformation(method='optimize')
        wrapper80.do_transformation(method='scale paper')
        cc80 = pyx.canvas.canvas()
        wrapper80.draw_nomogram(cc80)

    if do_test_9:
        """
        0. build definitions of atoms
        1. build block1
        2. build block2
        3. build nomowrapper
        4. add block1 and block2
        5. optimize transformation
        6. draw nomogram in nomowrapper
        """
        # build atoms
        block_atom1_para_9 = {
            'u_min': 3.0,
            'u_max': 10.0,
            'F': lambda u: 0,
            'G': lambda u: u,
            'title': 'A',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'scale_type': 'linear',
            'tick_levels': 3,
            'tick_text_levels': 2,
            'tick_side': 'right',
            'tag': 'none',
            'grid': False}
        b_atom1_9 = Nomo_Atom(params=block_atom1_para_9)

        block_atom2_para_9 = {
            'u_min': 3.0,
            'u_max': 10.0,
            'F': lambda u: 4.0,
            'G': lambda u: u,
            'title': 'B',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'scale_type': 'linear',
            'tick_levels': 3,
            'tick_text_levels': 2,
            'tick_side': 'right',
            'tag': 'none',
            'grid': False}
        b_atom2_9 = Nomo_Atom(params=block_atom2_para_9)

        block_atom3_para_9 = {
            'ID': 'none',  # to identify the axis
            'tag': 'none',  # for aligning block wrt others
            'title': 'Grid',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'title_distance_center': 0.5,
            'title_opposite_tick': True,
            'u_min': 0.0,  # for alignment
            'u_max': 1.0,  # for alignment
            'F_grid': lambda u, v: u + 2.0,
            'G_grid': lambda u, v: 2 * v,
            'u_start': 0.0,
            'u_stop': 1.0,
            'v_start': 0.0,
            'v_stop': 1.0,
            'u_values': [0.0, 0.25, 0.5, 0.75, 1.0],
            'v_values': [0.0, 0.25, 0.5, 0.75, 1.0],
            'grid': True
        }
        #        b_atom3_9=Nomo_Atom_Grid(params=block_atom3_para_9)
        #        block_1_9=Nomo_Block()
        #        block_1_9.add_atom(b_atom1_9)
        #        block_1_9.add_atom(b_atom2_9)
        #        block_1_9.add_atom(b_atom3_9)
        #
        #        wrapper80=Nomo_Wrapper(paper_width=10.0,paper_height=10.0,filename='typegrid.pdf')
        #        wrapper80.add_block(block_1_9)
        #        wrapper80.align_blocks()
        #        wrapper80.build_axes_wrapper() # build structure for optimization
        #        #wrapper1.do_transformation(method='scale paper')
        #        wrapper80.do_transformation(method='rotate',params=0.001)
        #        #wrapper80.do_transformation(method='rotate',params=-30.0)
        #        #wrapper1.do_transformation(method='rotate',params=30.0)
        #        #wrapper1.do_transformation(method='rotate',params=20.0)
        #        #wrapper1.do_transformation(method='rotate',params=90.0)
        #        #wrapper4.do_transformation(method='polygon')
        #        #wrapper1.do_transformation(method='optimize')
        #        wrapper80.do_transformation(method='scale paper')
        #        cc90=canvas.canvas()
        #        wrapper80.draw_nomogram(cc90)
        block_atom1_para_9a = {
            'u_min': 3.0,
            'u_max': 10.0,
            'f': lambda u: 0,
            'g': lambda u: u,
            'h': lambda u: 1.0,
            'title': 'A',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'title_color': pyx.color.rgb.red,
            'scale_type': 'linear',
            'tick_levels': 3,
            'tick_text_levels': 2,
            'tick_side': 'right',
            'tag': 'none',
            'grid': False}

        block_atom2_para_9a = {
            'u_min': 3.0,
            'u_max': 10.0,
            'f': lambda u: 4.0,
            'g': lambda u: u,
            'h': lambda u: 1.0,
            'title': 'B',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'title_color': pyx.color.rgb.red,
            'scale_type': 'linear',
            'tick_levels': 3,
            'tick_text_levels': 2,
            'tick_side': 'right',
            'tag': 'none',
            'grid': False}

        block_atom3_para_9a = {
            'ID': 'none',  # to identify the axis
            'tag': 'none',  # for aligning block wrt others
            'title': 'Grid',
            'title_x_shift': 0.0,
            'title_y_shift': 0.25,
            'title_distance_center': 0.5,
            'title_opposite_tick': True,
            'title_color': pyx.color.rgb.red,
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
        # more abstract way
        block_1_9a = Nomo_Block_Type_9()
        block_1_9a.define_determinant(
            block_atom1_para_9a, block_atom2_para_9a, block_atom3_para_9a)
        block_1_9a.set_block()

        wrapper80a = Nomo_Wrapper(
            paper_width=10.0, paper_height=10.0, filename='typegrid_a.pdf')
        wrapper80a.add_block(block_1_9a)
        wrapper80a.align_blocks()
        wrapper80a.build_axes_wrapper()  # build structure for optimization
        # wrapper1.do_transformation(method='scale paper')
        wrapper80a.do_transformation(method='rotate', params=0.001)
        # wrapper80.do_transformation(method='rotate',params=-30.0)
        # wrapper1.do_transformation(method='rotate',params=30.0)
        # wrapper1.do_transformation(method='rotate',params=20.0)
        # wrapper1.do_transformation(method='rotate',params=90.0)
        # wrapper4.do_transformation(method='polygon')
        # wrapper1.do_transformation(method='optimize')
        wrapper80a.do_transformation(method='scale paper')
        cc90a = pyx.canvas.canvas()
        wrapper80a.draw_nomogram(cc90a)

    if do_test_10:
        block_atom_10_1 = {
            'u_min': -25.0,
            'u_max': 0.0,
            'function': lambda u: u,
            'title': 'F1',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 1
        }
        block_atom_10_2 = {
            'u_min': -5.0,
            'u_max': 0.0,
            'function': lambda u: u,
            'title': 'F2',
            'tag': 'none',
            'tick_side': 'right',
            'tick_levels': 2,
            'tick_text_levels': 1
        }
        block_atom_10_3 = {
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
        block_1_10 = Nomo_Block_Type_10()
        block_1_10.define_F1(block_atom_10_1)
        block_1_10.define_F2(block_atom_10_2)
        block_1_10.define_F3(block_atom_10_3)
        block_1_10.set_block()

        wrapper10 = Nomo_Wrapper(
            paper_width=10.0, paper_height=10.0, filename='type_10.pdf')
        wrapper10.add_block(block_1_10)
        wrapper10.align_blocks()
        wrapper10.build_axes_wrapper()  # build structure for optimization
        # wrapper1.do_transformation(method='scale paper')
        wrapper10.do_transformation(method='rotate', params=0.001)
        # wrapper80.do_transformation(method='rotate',params=-30.0)
        # wrapper1.do_transformation(method='rotate',params=30.0)
        # wrapper1.do_transformation(method='rotate',params=20.0)
        # wrapper1.do_transformation(method='rotate',params=90.0)
        # wrapper4.do_transformation(method='polygon')
        # wrapper1.do_transformation(method='optimize')
        wrapper10.do_transformation(method='scale paper')
        cc10 = pyx.canvas.canvas()
        wrapper10.draw_nomogram(cc10)
