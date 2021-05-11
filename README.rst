Python nomographs (nomograms).
==============================

                            Autogenerate nomograms from a formula

This branch contains the nomogen program.
Currently, it's just a prototype.  Nothing fancy, no optimisation, just the
bare essentials.  It doesn't always work, but mostly it does.


Quick start:
------------
- Look at the example nomogram classes near the top of nomogen.py.
- Modify or copy one of these for your formula.
  The uscale is the left, the v scale is on the right, and the w scale is in
  the middle.
- set the upper and lower limits for each scale.  nomogen is very fussy
  about this.
- edit the line
                      testNomo = yrs()
  to match your nomogram class
- edit the nomogram parameters as normally for pynomo.  Se the pynomo
  documentation, and this excellent article by Ron Doerfler:
  https://deadreckonings.files.wordpress.com/2009/07/creatingnomogramswithpynomo.pdf

- run nomogen
              python3 nomogen
- nomogen.pdf is created, unless you have changed the default
- this takes about 20 or 30 seconds for my setup (Ryzen 3600).


..............................................................................


PyNomo is a Python software or library to build pdf nomographs. It is written by L.R. and is not in active development. 

For documentation, visit https://github.com/lefakkomies/pynomo-doc or older pynomo.org. For simple testing, visit playground.pynomo.org.
