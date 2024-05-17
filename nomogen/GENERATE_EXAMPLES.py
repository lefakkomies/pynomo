#!/usr/bin/env python3

"""
    GENERATE_EXAMPLES.py

    Generates example nomographs. Used for testing that software package works.

    Copyright (C) 2024  Leif Roschier

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import re
import time
import sys
import subprocess

sys.path.append('../pynomo')
sys.path.append('../pynomo/pynomo')

# from nomo_wrapper import *

for root, dirs, files in os.walk('.'):
    if root == '.':
        filelist = files

filelist.remove('GENERATE_EXAMPLES.py')
filelist.remove('axestest.py')
filelist.remove('nomogen.py')

tic_orig = time.time()
for filename in filelist:
    if filename.endswith( ".py" ):
        print("************************************")
        text = open(filename).read()
        if 'Nomographer' in text and not 'dual' in text:
            print("executing %s" % filename)
            code = compile(text, filename, 'exec')
            tic = time.time()
            exec(code)
            toc = time.time()
            print('Took %3.1f s for %s to execute.' % (toc - tic, filename))
            # execfile(filename)
            pdffilename = filename.replace("py", "pdf" )

            import platform
            if not True:
                pass
            elif platform.system() == 'Darwin':       # macOS
                subprocess.call(('open', pdffilename))
            elif platform.system() == 'Windows':    # Windows
                os.startfile(pdffilename)
            else:                                   # linux variants
                subprocess.call(('xdg-open', pdffilename))
        else:
            print( 'file {} is not a nomogram file'.format(filename) )
        print("------------------------------------")
toc_orig = time.time()
print('%3.1f s has elapsed overall' % (toc_orig - tic_orig))
