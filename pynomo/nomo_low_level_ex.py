#
#    This file is part of PyNomo -
#    a program to create nomographs with Python (http://pynomo.sourceforge.net/)
#
#    Copyright (C) 2007  Leif Roschier  <lefakkomies@users.sourceforge.net>
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
"""
This is example how to use lower level functions to build a nomograph.
Also Latex is used with oldstyle fonts that should be installed.
"""

from nomo_axis import *
from nomograph3 import *
import pyx

def f1(u):
    return 2 * (u * u - 1)


def g1(u):
    return 3 * u * (u + 1)


def h1(u):
    return -u * (u - 1)


def f3(v):
    return 2 * (2 * v + 1)


def g3(v):
    return 3 * (v + 1)


def h3(v):
    return -(v + 1) * (2 * v + 1)


def f2(w):
    return w


def g2(w):
    return 1


def h2(w):
    return -w * w


def f4(x):
    return 1


def g4(x):
    return 4 * math.log10(x)


pyx.text.set(mode="latex")
pyx.text.set(mode="latex", texmessagesdocclass=[pyx.text.texmessage.ignore])
nomograph = Nomograph3(f1=f1, f2=f2, f3=f3, g1=g1, g2=g2, g3=g3, h1=h1, h2=h2, h3=h3,
                       vk=[['u', 0.5, 'x', -5.0],
                           ['u', 0.5, 'y', 0.0],
                           ['u', 1.0, 'x', -5.0],
                           ['u', 1.0, 'y', 20.0],
                           ['w', 1.0, 'x', 5.0],
                           ['w', 1.0, 'y', 0.0],
                           ['w', 0.5, 'x', 5.0],
                           ['w', 0.5, 'y', 20.0]])
# nomograph._make_transformation_matrix_()
# \usepackage[T1]{fontenc}
# \usepackage[math]{anttor}
pyx.text.set(mode="latex")
# text.preamble(r"\usepackage[T1]{fontenc}")
# text.preamble(r"\usepackage[math]{anttor}")
# text.preamble(r"\oldstyle")

ccc = pyx.canvas.canvas()
gg3 = Nomo_Axis(func_f=nomograph.give_x3, func_g=nomograph.give_y3, start=1.0, stop=0.5,
                turn=-1, title='L', canvas=ccc, text_style='oldstyle')
gg1 = Nomo_Axis(func_f=nomograph.give_x1, func_g=nomograph.give_y1, start=0.5, stop=1.0,
                turn=-1, title='p', canvas=ccc, text_style='oldstyle')
gg1 = Nomo_Axis(func_f=nomograph.give_x2, func_g=nomograph.give_y2, start=1.0, stop=0.75,
                turn=1, title='h', canvas=ccc, text_style='oldstyle')
# gg2=Nomo_Axis(func_f=f4,func_g=g4,start=0.00001,stop=3,turn=1,title='log',canvas=ccc,type='log')
ccc.writePDFfile("nomotest_font5")
# SVN test 6
