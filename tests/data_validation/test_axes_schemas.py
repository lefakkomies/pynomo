import pytest
from cerberus import Validator

from pynomo.data_validation.axes_schemas import axis_schema_type_1, axis_schema_common, axis_schema_type_2, \
    axis_schema_type_3, axis_schema_type_4, axis_schema_type_5, axis_schema_type_6, \
    axis_schema_type_8, axis_schema_type_7, axis_schema_type_9_axis, axis_schema_type_9_grid, validate_axis_type_9


# Common axis parameters
def test_axis_schema_common_a():
    # Unallowed value
    doc = {'scale_type': 'lineaaaar', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_common)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_common_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_common)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_common_c():
    # Needed fields
    doc = {'scale_type': 'linear'}
    v = Validator(axis_schema_common)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == True


# Type 1 axis parameters
def test_axis_schema_type_1_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_1)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_1_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_1)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_1_c():
    # Required fields
    doc = {'scale_type': 'linear', 'function': lambda x: x, 'u_min': 0, 'u_max': 1.0}
    v = Validator(axis_schema_type_1)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == True


# Type 2 axis parameters
def test_axis_schema_type_2_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_2)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_2_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_2)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_2_c():
    # Required fields
    doc = {'scale_type': 'linear', 'function': lambda x: x, 'u_min': 0, 'u_max': 1.0}
    v = Validator(axis_schema_type_2)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == True


# Type 3 axis parameters
def test_axis_schema_type_3_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_3)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_3_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_3)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_3_c():
    # Required fields
    doc = {'scale_type': 'linear', 'function': lambda x: x, 'u_min': 0, 'u_max': 1.0}
    v = Validator(axis_schema_type_3)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == True


# Type 4 axis parameters
def test_axis_schema_type_4_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_4)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_4_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_4)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_4_c():
    # Required fields
    doc = {'scale_type': 'linear', 'function': lambda x: x, 'u_min': 0, 'u_max': 1.0}
    v = Validator(axis_schema_type_4)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == True


# Type 5 axis parameters
def test_axis_schema_type_5_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_5)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_5_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_5)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_5_c():
    # No fields actually
    doc = {'scale_type': 'linear', 'function': lambda x: x, 'u_min': 0, 'u_max': 1.0}
    v = Validator(axis_schema_type_5)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


# Type 6 axis parameters
def test_axis_schema_type_6_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_6)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_6_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_6)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_6_c():
    # No fields actually
    doc = {'scale_type': 'linear', 'function': lambda x: x, 'u_min': 0, 'u_max': 1.0}
    v = Validator(axis_schema_type_6)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == True


# Type 7 axis parameters
def test_axis_schema_type_7_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_7)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_7_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_7)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_7_c():
    # No fields actually
    doc = {'scale_type': 'linear', 'function': lambda x: x, 'u_min': 0, 'u_max': 1.0}
    v = Validator(axis_schema_type_7)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == True


# Type 8 axis parameters
def test_axis_schema_type_8_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_8)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_8_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_8)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_8_c():
    # No fields actually
    doc = {'scale_type': 'linear', 'function': lambda x: x, 'u_min': 0, 'u_max': 1.0}
    v = Validator(axis_schema_type_8)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == True


# Type 9 axis parameters
def test_axis_schema_type_9_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_9_axis)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_9_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_9_grid)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_9_c():
    # No fields actually
    doc = {'scale_type': 'linear',
           'f': lambda x: x
           }
    v = Validator(axis_schema_type_9_axis)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_9_d():
    # Missing fields
    doc = {'scale_type': 'linear',
           'grid': True,
           'f': lambda x: x,
           'f_grid': lambda x, y: x + y
           }
    v = Validator(axis_schema_type_9_axis)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) == False


def test_axis_schema_type_9_e():
    # No fields actually
    doc = {'scale_type': 'linear',
           'grid': False,
           'f': lambda x: x,
           'g': lambda x: x,
           'h': lambda x: x,
           }
    assert validate_axis_type_9(doc) is True


def test_axis_schema_type_9_f():
    # No fields actually
    doc = {
        'grid': True,
        'f_grid': lambda x, y: x + y,
        'g_grid': lambda x, y: x + y,
        'h_grid': lambda x, y: x + y,
        'u_start': 0.0,
        'u_stop': 0.0,
        'v_start': 0.0,
        'v_stop': 0.0,
    }
    assert validate_axis_type_9(doc) is True
