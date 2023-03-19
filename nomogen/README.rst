Python nomographs (nomograms).
==============================

                            Autogenerate nomograms from a formula

This directory contains the nomogen program.

This program takes the hard work out of making nomograms
because it auto-calculates the lines of a nomogram from a formula.

It is  not restricted to straight line scales, curved scales are handled just fine.


.. image:: example.png


Find the latest version at https://github.com/tevorbl/pynomo/

Currently, it's just a prototype.  Nothing fancy, not much optimisation, just the
bare essentials.  It doesn't always work, but often it does.

Quick start:
------------
- Look at the example nomogram classes, eg fv.py.
- Modify or copy one of these for your formula.
  The u scale is on the left, the v scale is on the right, and the w scale is in
  the middle.
  The linearity argument is technically the degree of the polyniomials needed
  to define the scale lines.  Straight (or nearly straight) line nomograms
  with evenly spaced scales need a small number (say 5), more complicated
  nomograms need a larger number to generate accurate scale lines.  Use the
  smallest number that works because larger numbers make **nomogen** slow.
- you might need to change the scale type to log or log-smart if the spacing
  between numbers gets smaller as the numbers get larger.
- set the upper and lower limits for each scale.  **nomogen** needs to be very fussy
  about this because extrapolating scale lines past their defined range is
  wildly inaccurate..
- edit the nomogram parameters as normally for pynomo, if necessary.  See the pynomo
  documentation, and this excellent article by Ron Doerfler:
  https://deadreckonings.files.wordpress.com/2009/07/creatingnomogramswithpynomo.pdf
  Ignore the stuff about filling in the determinant, **nomogen** does that for you

- run the example
              python3 fv.py
- a pdf file is created, eg fv.py creates fv.pdf
- this takes about 20 or 30 seconds for my setup (Ryzen 3600).

- There's more details and a step-by-step example in user_guide.pdf.  The
  notes.pdf document contains mostly unedited sets of notes about the internals of nomogen



