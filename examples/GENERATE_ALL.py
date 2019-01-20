"""
    GENERATE_ALL.py

    Generates example nomographs. Used for testing that software package works.

    Copyright (C) 2007-2015  Leif Roschier

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

sys.path.append('../pynomo')
sys.path.append('../pynomo/pynomo')

# from nomo_wrapper import *

for root, dirs, files in os.walk('.'):
    if root == '.':
        filelist = files

filelist.remove('GENERATE_ALL.py')

tic_orig = time.time()
# print filelist
for filename in filelist:
    if re.compile(".py").search(filename, 1) is not None:
        tic = time.time()
        print("************************************")
        print("executing %s" % filename)
        with open(filename) as f:
            code = compile(f.read(), filename, 'exec')
            exec(code)
        # execfile(filename)
        toc = time.time()
        print('Took %3.1f s for %s to execute.' % (toc - tic, filename))
        print("------------------------------------")
toc_orig = time.time()
print('%3.1f s has elapsed overall' % (toc_orig - tic_orig))
