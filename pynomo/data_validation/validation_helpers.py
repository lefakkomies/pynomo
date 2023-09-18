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

""" Helper functions for validation

"""
from typing import Dict


def give_required_fields(dict_in: Dict[str, dict]) -> Dict[str, dict]:
    result = []
    # this is easier to read than dict comprehensions...
    for key in dict_in.keys():
        if 'required' in dict_in[key]:
            if dict_in[key]['required']:
                result += [key]
    return result


def _give_dictionary_dropping_rules(dict_in: Dict[str, dict]) -> Dict[str, dict]:
    result = {}
    # this is easier to read than dict comprehensions...
    for key in dict_in.keys():
        result[key] = dict_in[key]['rules']
    return result


def _give_dictionary_default_values(dict_in: Dict[str, dict]) -> Dict[str, dict]:
    result = {}
    # this is easier to read than dict comprehensions...
    for key in dict_in.keys():
        if dict_in[key]['default'] is not None:
            result[key] = dict_in[key]['default']
    return result


def _give_rules_from_dictionaries(*dicts):
    return _give_dictionary_dropping_rules({k: v for d in dicts for k, v in d.items()})


def _give_default_values_from_dictionaries(*dicts):
    return _give_dictionary_default_values({k: v for d in dicts for k, v in d.items()})
