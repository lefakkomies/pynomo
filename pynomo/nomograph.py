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
from nomo_axis import *
from nomograph3 import *
from math import *


class Nomograph:
    """
    Main module for easy building of nomographs.

    Types of nomographs:
    ====================
        Simple
        ------
          - F2(v)=F1(u)+F3(w)
          - F2(v)=F1(u)*F3(w)
        General
        -------
          - An equation in determinant form::
              -------------------------
              | f1(u) | g1(u) | h1(u) |
              -------------------------
              | f2(v) | g2(v) | h2(v) | = 0
              -------------------------
              | f3(w) | g3(w) | h3(w) |
              -------------------------
    Axis
    ====
      Axes may be chosen to be linear or logarithmic

    """

    def __init__(self, nomo_type, functions, nomo_height=15.0, nomo_width=10.0,
                 manual_coord_points=False):
        """
        @param nomo_type: This values describes the type of nomogram.
            allowed values are:
                - 'F2(v)=F1(u)+F3(w)'
                - 'F2(v)=F3(w)/F1(u)'
                - 'general3', a general eq in determinant form::
                        -------------------------
                        | f1(u) | g1(u) | h1(u) |
                        -------------------------
                        | f2(v) | g2(v) | h2(v) | = 0
                        -------------------------
                        | f3(w) | g3(w) | h3(w) |
                        -------------------------

        @type nomo_type: string
        @param functions: dictionary with corresponding functions.
            for examples if we plan to plot z=x*x+2*y, then we have::
                functions={ 'filename':'nomogram1.pdf',
                            'F1':lambda z:z,
                            'u_start':1.0,
                            'u_stop':5.0,
                            'u_title':'z',
                            'F2':lambda x:x*x,
                            'v_start':1.0,
                            'v_stop':3.0,
                            'v_title','x'
                            'F3':lambda y:2*y,
                            'w_start':0.0,
                            'w_stop':3.0
                            'w_title','y'}

        """
        # default parameters
        self.functions_default = {
            'title_str': '',
            'title_x': nomo_width / 2.0,
            'title_y': nomo_height,
            'title_box_width': nomo_width / 2.2,
            'u_title': 'f(u)',
            'u_title_x_shift': 0.0,
            'u_title_y_shift': 0.25,
            'u_scale_type': 'linear',
            'u_tick_levels': 10,
            'u_tick_text_levels': 10,
            'u_tick_dir': -1,
            'u_start_x_coord': 0.0,
            'u_start_y_coord': 0.0,
            'u_stop_x_coord': 0.0,
            'u_stop_y_coord': nomo_height,
            'v_title': 'f(v)',
            'v_title_x_shift': 0.0,
            'v_title_y_shift': 0.25,
            'v_scale_type': 'linear',
            'v_tick_levels': 10,
            'v_tick_text_levels': 10,
            'v_tick_dir': 1,
            'w_title': 'f(w)',
            'w_title_x_shift': 0.0,
            'w_title_y_shift': 0.25,
            'w_scale_type': 'linear',
            'w_tick_levels': 10,
            'w_tick_text_levels': 10,
            'w_tick_dir': -1,
            'w_start_x_coord': nomo_width,
            'w_start_y_coord': 0.0,
            'w_stop_x_coord': nomo_width,
            'w_stop_y_coord': nomo_height}
        self.functions = self.functions_default
        self.functions.update(functions)
        self.nomo_height = nomo_height
        self.nomo_width = nomo_width
        try:
            {'F2(v)=F1(u)+F3(w)': self.init_sum_three,
             'F2(v)=F3(w)/F1(u)': self.init_product_three,
             'general3': self.init_general}[nomo_type]()
        except KeyError:
            print("nomo_type not valid")
        # This structure sets the limits
        vk = [['u', self.functions['u_start'], 'x', self.functions['u_start_x_coord']],
              ['u', self.functions['u_start'], 'y', self.functions['u_start_y_coord']],
              ['u', self.functions['u_stop'], 'x', self.functions['u_stop_x_coord']],
              ['u', self.functions['u_stop'], 'y', self.functions['u_stop_y_coord']],
              ['w', self.functions['w_start'], 'x', self.functions['w_start_x_coord']],
              ['w', self.functions['w_start'], 'y', self.functions['w_start_y_coord']],
              ['w', self.functions['w_stop'], 'x', self.functions['w_stop_x_coord']],
              ['w', self.functions['w_stop'], 'y', self.functions['w_stop_y_coord']]]
        nomo = Nomograph3(f1=self.f1, f2=self.f2, f3=self.f3,
                          g1=self.g1, g2=self.g2, g3=self.g3,
                          h1=self.h1, h2=self.h2, h3=self.h3,
                          vk=vk)
        c = canvas.canvas()
        u_axis = Nomo_Axis(func_f=nomo.give_x1, func_g=nomo.give_y1,
                           start=self.functions['u_start'], stop=self.functions['u_stop'],
                           turn=self.functions['u_tick_dir'], title=self.functions['u_title'],
                           canvas=c, type=self.functions['u_scale_type'],
                           title_x_shift=self.functions['u_title_x_shift'],
                           title_y_shift=self.functions['u_title_y_shift'],
                           tick_levels=self.functions['u_tick_levels'],
                           tick_text_levels=self.functions['u_tick_text_levels'])
        v_axis = Nomo_Axis(func_f=nomo.give_x2, func_g=nomo.give_y2,
                           start=self.functions['v_start'], stop=self.functions['v_stop'],
                           turn=self.functions['v_tick_dir'], title=self.functions['v_title'],
                           canvas=c, type=self.functions['v_scale_type'],
                           title_x_shift=self.functions['v_title_x_shift'],
                           title_y_shift=self.functions['v_title_y_shift'],
                           tick_levels=self.functions['v_tick_levels'],
                           tick_text_levels=self.functions['v_tick_text_levels'])
        w_axis = Nomo_Axis(func_f=nomo.give_x3, func_g=nomo.give_y3,
                           start=self.functions['w_start'], stop=self.functions['w_stop'],
                           turn=self.functions['w_tick_dir'], title=self.functions['w_title'],
                           canvas=c, type=self.functions['w_scale_type'],
                           title_x_shift=self.functions['w_title_x_shift'],
                           title_y_shift=self.functions['w_title_y_shift'],
                           tick_levels=self.functions['w_tick_levels'],
                           tick_text_levels=self.functions['w_tick_text_levels'])
        self.canvas = c
        self.nomo = nomo
        # let's draw title
        c.text(self.functions['title_x'], self.functions['title_y'],
               self.functions['title_str'],
               [text.parbox(self.functions['title_box_width']),
                text.halign.boxcenter, text.halign.flushcenter])
        c.writePDFfile(self.functions['filename'])

    def init_sum_three(self):
        """
        Make initializations for nomogram F2(v)=F1(u)+F3(w)
        """
        self.f1 = lambda u: 0.0
        self.g1 = lambda u: self.functions['F1'](u)
        self.h1 = lambda u: 1.0
        self.f2 = lambda v: 0.5
        self.g2 = lambda v: 0.5 * self.functions['F2'](v)
        self.h2 = lambda v: 1.0
        self.f3 = lambda w: 1.0
        self.g3 = lambda w: self.functions['F3'](w)
        self.h3 = lambda w: 1.0

    def init_product_three(self):
        """
        Make initializations for nomogram F2(v)=F3(w)/F1(u)::
                        ------------------------------------
                        |      1         | -F1(u)  | 1     |
                        ------------------------------------
                        | F2(v)/(F2(v)+1)|   0     | 1     | = 0
                        ------------------------------------
                        |      0         |  F3(w)  | 1     |
                        ------------------------------------
        """
        # u and w scales have to go in opposite directions in this nomograph
        u_start = self.functions['u_start']
        u_stop = self.functions['u_stop']
        u_start_fn_value = self.functions['F1'](u_start)
        u_stop_fn_value = self.functions['F1'](u_stop)
        w_start = self.functions['w_start']
        w_stop = self.functions['w_stop']
        w_start_fn_value = self.functions['F3'](w_start)
        w_stop_fn_value = self.functions['F3'](w_stop)
        if ((u_start_fn_value - u_stop_fn_value) *
                (w_start_fn_value - w_stop_fn_value) > 0.0):
            self.functions['w_start'], self.functions['w_stop'] = \
                self.functions['w_stop'], self.functions['w_start']

        self.f1 = lambda u: 1.0
        self.g1 = lambda u: -self.functions['F1'](u)
        self.h1 = lambda u: 1.0
        self.f2 = lambda v: self.functions['F2'](v) / (self.functions['F2'](v) + 1.0)
        self.g2 = lambda v: 0.0
        self.h2 = lambda v: 1.0
        self.f3 = lambda w: 0.0
        self.g3 = lambda w: self.functions['F3'](w)
        self.h3 = lambda w: 1.0

    def init_general(self):
        """
        Make initializations for nomogram in determinant form::
                        -------------------------
                        | f1(u) | g1(u) | h1(u) |
                        -------------------------
                        | f2(v) | g2(v) | h2(v) | = 0
                        -------------------------
                        | f3(w) | g3(w) | h3(w) |
                        -------------------------
        """
        self.f1 = lambda u: self.functions['f1'](u)
        self.g1 = lambda u: self.functions['g1'](u)
        self.h1 = lambda u: self.functions['h1'](u)
        self.f2 = lambda v: self.functions['f2'](v)
        self.g2 = lambda v: self.functions['g2'](v)
        self.h2 = lambda v: self.functions['h2'](v)
        self.f3 = lambda w: self.functions['f3'](w)
        self.g3 = lambda w: self.functions['g3'](w)
        self.h3 = lambda w: self.functions['h3'](w)


if __name__ == '__main__':
    """
    Example nomograph z=x*x+2*y
    """
    nomo_type = 'F2(v)=F1(u)+F3(w)'
    functions = {'filename': 'nomogram1.pdf',
                 'F2': lambda z: z,
                 'v_start': 1.0,
                 'v_stop': 15.0,
                 'v_title': 'z',
                 'v_scale_type': 'linear',
                 'F1': lambda x: x * x,
                 'u_start': 1.0,
                 'u_stop': 3.0,
                 'u_title': 'x',
                 'u_scale_type': 'linear',
                 'F3': lambda y: 2 * y,
                 'w_start': 0.0,
                 'w_stop': 3.0,
                 'w_title': 'y',
                 'w_scale_type': 'linear', }
    Nomograph(nomo_type=nomo_type, functions=functions)

    """
    Example nomograph z=y/x or y=x*z
    """
    nomo_type = 'F2(v)=F3(w)/F1(u)'
    functions1 = {'filename': 'nomogram2.pdf',
                  'F2': lambda z: z,
                  'v_start': 2.0,
                  'v_stop': 0.5,
                  'v_title': 'z',
                  'v_scale_type': 'linear',
                  'F1': lambda x: x,
                  'u_start': 1.0,
                  'u_stop': 5.0,
                  'u_title': 'x',
                  'u_scale_type': 'linear',
                  'F3': lambda y: y,
                  'w_start': 5.0,
                  'w_stop': 1.0,
                  'w_title': 'y',
                  'w_scale_type': 'linear', }
    Nomograph(nomo_type=nomo_type, functions=functions1)
    """
    Example nomograph of equation T=((1+p/100)^N-1)*100
    N = years
    p = interest rate as percentage
    N = total interest after N years
    equation in suitable form is
    log(T/100+1)=N*log(1+p/100)
    """
    nomo_type = 'F2(v)=F3(w)/F1(u)'
    functions1 = {'filename': 'nomogram_interest.pdf',
                  'F2': lambda T: log(T / 100.0 + 1.0),
                  'v_start': 20.0,
                  'v_stop': 900.0,
                  'v_title': r'Total interest \% (T)',
                  'v_title_x_shift': 1.0,
                  'v_title_y_shift': 0.5,
                  'v_scale_type': 'log',
                  'F1': lambda N: 1 / N,
                  'u_start': 3.0,
                  'u_stop': 20.0,
                  'u_title': 'N (years)',
                  'u_scale_type': 'linear',
                  'F3': lambda p: log(1.0 + p / 100.0),
                  'w_start': 0.2,
                  'w_stop': 20.0,
                  'w_title': r'p \%',
                  'w_title_x_shift': 0.0,
                  'w_title_y_shift': 0.25,
                  'w_scale_type': 'linear',
                  'title_str': r"$T=((1+p/100)^{N-1}) 100$",
                  'title_box_width': 10}
    Nomograph(nomo_type=nomo_type, functions=functions1)
    """
    Example nomograph of body-mass index BMI = weight (kg)/(height^2(m^2))
    BMI = W/H^2
    """
    nomo_type = 'F2(v)=F3(w)/F1(u)'
    functions1 = {'filename': 'BMI.pdf',
                  'F2': lambda BMI: BMI,
                  'v_start': 15.0,
                  'v_stop': 45.0,
                  'v_title': r'BMI',
                  'v_scale_type': 'linear',
                  'v_title_x_shift': -3.0,
                  'v_title_y_shift': 0.5,
                  'v_tick_text_levels': 3,  # not really used here, only for demonstration
                  'v_tick_levels': 4,  # of syntax
                  'F1': lambda H: H ** 2,
                  'u_start': 1.4,
                  'u_stop': 2.2,
                  'u_title': 'Height (m)',
                  'u_scale_type': 'linear',
                  'u_tick_dir': 1,
                  'F3': lambda W: W,
                  'w_start': 200,
                  'w_stop': 30.0,
                  'w_title': r'Weight (kg)',
                  'w_scale_type': 'linear',
                  'title_str': r"Body mass index $BMI=W($kg$)/H($m$)^2$"
                  }
    nomo_bmi = Nomograph(nomo_type=nomo_type, functions=functions1)


    # lets add additional scales for demonstration
    def feet2meter(feet):
        return feet * 0.3048


    def pound2kg(pound):
        return pound * 0.45359237


    Nomo_Axis(func_f=(lambda h: nomo_bmi.nomo.give_x1(feet2meter(h)) - 0),
              func_g=(lambda h: nomo_bmi.nomo.give_y1(feet2meter(h))),
              start=4.6, stop=7.2, turn=-1, title='Height (ft)',
              title_x_shift=-2,
              canvas=nomo_bmi.canvas, type='linear')
    Nomo_Axis(func_f=(lambda h: nomo_bmi.nomo.give_x3(pound2kg(h)) + 0),
              func_g=(lambda h: nomo_bmi.nomo.give_y3(pound2kg(h))),
              start=70.0, stop=440.0, turn=1, title='Weight (lb)',
              title_x_shift=-2,
              canvas=nomo_bmi.canvas, type='linear')

    # nomo_bmi.canvas.text(5, 15, r"Body mass index $BMI=W/H^2$",
    #   [text.parbox(3), text.halign.boxcenter, text.halign.flushcenter])

    nomo_bmi.canvas.writePDFfile('BMI1.pdf')

    """
    Retaining wall example nomograph from Allcock's book. Also found in O'Cagne:
    Traite de Nomographie (1899).
    Eq: (1+L)h^2-L*h*(1+p)-1/3*(1-L)*(1+2*p)=0
    in determinant form::
              -----------------------------------------
              | 2*(u*u-1) | 3*u*(u+1) | -u*(u-1.0)    |
              -----------------------------------------
              |      v    |     1     |    -v*v       | = 0
              -----------------------------------------
              | 2*(2*w+1) | 3*(w+1)   |-(w+1)*(2*w+1) |
              -----------------------------------------

    """
    nomo_type = 'general3'
    functions2 = {'filename': 'nomogram3.pdf',
                  'f1': lambda u: 2 * (u * u - 1.0),
                  'g1': lambda u: 3 * u * (u + 1.0),
                  'h1': lambda u: -u * (u - 1.0),
                  'f2': lambda v: v,
                  'g2': lambda v: 1.0,
                  'h2': lambda v: -v * v,
                  'f3': lambda w: 2.0 * (2.0 * w + 1.0),
                  'g3': lambda w: 3.0 * (w + 1.0),
                  'h3': lambda w: -(w + 1.0) * (2.0 * w + 1.0),
                  'u_start': 0.5,
                  'u_stop': 1.0,
                  'u_title': 'p',
                  'v_start': 1.0,
                  'v_stop': 0.75,
                  'v_title': 'h',
                  'w_start': 1.0,
                  'w_stop': 0.5,
                  'w_title': 'L',
                  'title_y': 2,
                  'title_box_width': 10,
                  'title_str': r'Solution to retaining wall equation:  $(1+L)h^2-Lh(1+p)-1/3(1-L)(1+2p)=0$'}
    Nomograph(nomo_type=nomo_type, functions=functions2)
    """
    Clock tuning example (linear extrapolation).
    Measure error e1.
    Turn knob once around.
    Measure error e2.
    To make error=0, turn knob T turns from its current position.
    Problem in determinant form::
              -----------------------------------------
              |     1     |     -e1     |     0       |
              -----------------------------------------
              |     0     |     -e2     |     1       | = 0
              -----------------------------------------
              |   -T+1    |     0       |     T       |
              -----------------------------------------

    """
    # Needs tuning -> make axis start and stop to be free x,y points
    # """
    nomo_type = 'general3'
    functions_clock = {'filename': 'clock.pdf',
                       'f1': lambda u: 1.0,
                       'g1': lambda u: -u,
                       'h1': lambda u: 0.0,
                       'f2': lambda v: 0.0,
                       'g2': lambda v: -v,
                       'h2': lambda v: 1.0,
                       'f3': lambda w: -w + 1,
                       'g3': lambda w: 0.0,
                       'h3': lambda w: w,
                       'u_start': -10.0,
                       'u_stop': 10.0,
                       'u_start_x_coord': 1.0,
                       'u_start_y_coord': -10.0,
                       'u_stop_x_coord': 1.0,
                       'u_stop_y_coord': 10.0,
                       'u_title': r'$\epsilon_1$',
                       'u_tick_dir': -1,
                       'v_start': 10.0,
                       'v_stop': -10.0,
                       'v_title': r'$\epsilon_2$',
                       'v_tick_dir': 1,
                       'w_start': -10.0,
                       'w_stop': 10.0,
                       'w_start_x_coord': -10.0,
                       'w_start_y_coord': -5.0,
                       'w_stop_x_coord': 10.0,
                       'w_stop_y_coord': 5.0,
                       'w_title': r'Turns',
                       'title_y': 5,
                       'title_x': -4,
                       'title_box_width': 10,
                       'title_str': r'Clock tuning problem'}
    Nomograph(nomo_type=nomo_type, functions=functions_clock)
    # """
