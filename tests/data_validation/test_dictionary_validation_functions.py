# -*- coding: utf-8 -*-
#
#    This file is part of PyNomo -
#    a program to create nomographs with Python (https://github.com/lefakkomies/pynomo)
#
#    Copyright (C) 2007-2023  Leif Roschier  <leif.roschier@iki.fi>
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

""" Testing of dictionary validation functions

    Testing of main params defined in dictionary_validation_functions.py

"""
import sys
from pprint import pprint

import pytest
import logging

from pyx import text, path
from numpy import pi
from pyx import color

from pynomo.data_validation.dictionary_validation_functions import check_text_format_string


def test_check_text_format_string():
    errors = []

    def error(field, value):
        errors.append([True, field, value])

    # incorrect input
    strings = [
        ("This is a $%3.0f$ string", True),
        ("$%2.5f$ This is another example", True),
        ("No $  $ number given", False),
        ("$%1.23e$ contains a number and opening/closing dollars", True),
        ("Incorrect $%pattern$ here", False),
        ("$%123.456f$ has an even number of dollar signs$$", True),
        ("%1.0f", True),
        ("%1.0f$", False),
    ]
    for string, ok in strings:
        check_text_format_string("", string, error)
        error_found = False
        if len(errors) > 0:
            error_found = True
        if error_found is True and ok is True:
            print(errors[0])
            assert error_found is not ok
        if error_found is False and ok is False:
            print(f"failed: {string}")
            assert error_found is not ok
        errors = []

