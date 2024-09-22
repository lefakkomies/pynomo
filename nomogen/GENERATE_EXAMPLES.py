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
import time
import sys
import subprocess

showPdf = False
for a in sys.argv[1:]:
    #print( "arg is ", a )
    if a == '-d':
        showPdf = True


sys.path.append('../pynomo')
sys.path.append('../pynomo/pynomo')

# from nomo_wrapper import *

for root, dirs, files in os.walk('.'):
    if root == '.':
        filelist = files

if 'GENERATE_EXAMPLES.py' in filelist: filelist.remove('GENERATE_EXAMPLES.py')
if 'nomogen.py' in filelist:  filelist.remove('nomogen.py')

nr_fails = 0
tic_orig = time.time()

for filename in filelist:
    if filename.endswith( ".py" ):
        print("\n************************************")
        #print( filename )
        text = open(filename).read()
        if 'Nomographer' in text:
            print("executing %s" % filename)
            code = compile(text, filename, 'exec')
            tic = time.time()
            # recover if this test fails
            try:
                exec(code)
            except BaseException as e:
                print( "test", filename, "failed -", repr(e) )
                nr_fails = nr_fails + 1
            toc = time.time()
            print('Took %3.1f s for %s to execute.' % (toc - tic, filename))
            # execfile(filename)
            pdffilename = filename.replace("py", "pdf" )

            if showPdf:
                import platform
                if platform.system() == 'Darwin':       # macOS
                    subprocess.call(('open', pdffilename))
                elif platform.system() == 'Windows':    # Windows
                    os.startfile(pdffilename)
                else:                                   # linux variants
                    subprocess.call(('xdg-open', pdffilename))
        else:
            print( 'file {} is not a nomogram file'.format(filename) )


toc_orig = time.time()
print( "\nall tests passed" if nr_fails == 0 else
       "1 failed test" if nr_fails == 1 else
       "{} failed tests".format(nr_fails) )
print('%3.1f s has elapsed overall' % (toc_orig - tic_orig))

