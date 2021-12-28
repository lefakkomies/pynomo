Python nomographs (nomograms).
==============================

                            Autogenerate nomograms from a formula

This branch contains the nomogen program.

Generating nomograms is normally hard work.
This program makes it easy because it auto-calculates the lines of a nomogram from a formula.

Currently, it's just a prototype.  Nothing fancy, no optimisation, just the
bare essentials.  It doesn't always work, but mostly it does.


.. image:: example.png

Quick start:
------------
- Look at the example nomogram classes, eg fv.py.
- Modify or copy one of these for your formula.
  The u scale is on the left, the v scale is on the right, and the w scale is in
  the middle.
  The linearity argument is technically the order of the polyniomials needed
  to define the scale lines.  Straight (or nearly straight) line nomograms
  with evenly spaced scales need a small number (say 5), more complicated
  nomograms need a larger number to generate accurate scale lines.  Use the
  smallest number that works because larger numbers make **nomogen** slow.

- set the upper and lower limits for each scale.  **nomogen** needs to be very fussy
  about this because extrapolating scale lines past their defined range is
  wildly inaccurate..
- edit the nomogram parameters as normally for pynomo.  See the pynomo
  documentation, and this excellent article by Ron Doerfler:
  https://deadreckonings.files.wordpress.com/2009/07/creatingnomogramswithpynomo.pdf
  Ignore the stuff about filling in the determinant, **nomogen** does that for you

- run the example
              python3 fv.py
- a pdf file is created, eg fv.py creayes fv.pdf
- this takes about 20 or 30 seconds for my setup (Ryzen 3600).

- nomogen-Notes.pdf is an unedited set of notes about the internals of nomogen

..............................................................................


PyNomo is a Python software or library to build pdf nomographs. It is written by L.R. and is not in active development. 

For documentation, visit https://github.com/lefakkomies/pynomo-doc or older pynomo.org. For simple testing, visit playground.pynomo.org.
