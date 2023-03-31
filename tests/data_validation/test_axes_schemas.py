import pytest
from cerberus import Validator

from pynomo.data_validation.axis_schemas import axis_schema_type_1, axis_schema_common, axis_schema_type_2, \
    axis_schema_type_3, axis_schema_type_4, axis_schema_type_5, axis_schema_type_6, \
    axis_schema_type_8, axis_schema_type_7, axis_schema_type_9_axis, axis_schema_type_9_grid, validate_axis_type_9, \
    axis_schema_type_10, axis_schema_type_10_w, give_default_axis_values


# Common axis parameters
def test_axis_schema_common_a():
    # Non-allowed value
    doc = {'scale_type': 'lineaaaar', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_common)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_common_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_common)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_common_c():
    # Needed fields
    doc = {'scale_type': 'linear'}
    v = Validator(axis_schema_common)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is True


# Type 1 axis parameters
def test_axis_schema_type_1_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_1)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_1_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_1)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_1_c():
    # Required fields
    doc = {'scale_type': 'linear', 'function': lambda x: x, 'u_min': 0, 'u_max': 1.0}
    v = Validator(axis_schema_type_1)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is True


# Type 2 axis parameters
def test_axis_schema_type_2_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_2)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_2_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_2)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_2_c():
    # Required fields
    doc = {'scale_type': 'linear', 'function': lambda x: x, 'u_min': 0, 'u_max': 1.0}
    v = Validator(axis_schema_type_2)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is True


# Type 3 axis parameters
def test_axis_schema_type_3_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_3)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_3_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_3)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_3_c():
    # Required fields
    doc = {'scale_type': 'linear', 'function': lambda x: x, 'u_min': 0, 'u_max': 1.0}
    v = Validator(axis_schema_type_3)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is True


# Type 4 axis parameters
def test_axis_schema_type_4_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_4)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_4_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_4)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_4_c():
    # Required fields
    doc = {'scale_type': 'linear', 'function': lambda x: x, 'u_min': 0, 'u_max': 1.0}
    v = Validator(axis_schema_type_4)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is True


# Type 5 axis parameters
def test_axis_schema_type_5_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_5)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_5_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_5)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_5_c():
    # No fields actually
    doc = {'scale_type': 'linear', 'function': lambda x: x, 'u_min': 0, 'u_max': 1.0}
    v = Validator(axis_schema_type_5)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


# Type 6 axis parameters
def test_axis_schema_type_6_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_6)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_6_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_6)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_6_c():
    # No fields actually
    doc = {'scale_type': 'linear', 'function': lambda x: x, 'u_min': 0, 'u_max': 1.0}
    v = Validator(axis_schema_type_6)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is True


# Type 7 axis parameters
def test_axis_schema_type_7_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_7)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_7_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_7)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_7_c():
    # No fields actually
    doc = {'scale_type': 'linear',
           'function': lambda x: x,
           'u_min': 0,
           'u_max': 1.0}
    v = Validator(axis_schema_type_7)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is True


# Type 8 axis parameters
def test_axis_schema_type_8_a():
    # Missing fields
    doc = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v = Validator(axis_schema_type_8)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_8_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_8)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_8_c():
    # No fields actually
    doc = {'scale_type': 'linear',
           'function': lambda x: x,
           'u_min': 0,
           'u_max': 1.0}
    v = Validator(axis_schema_type_8)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is True


# Type 9 axis parameters
def test_axis_schema_type_9_a():
    # Missing fields
    doc = {'scale_type': 'linear',
           'tick_distance_smart': 30,
           'base_stop': None}
    v = Validator(axis_schema_type_9_axis)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_9_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_9_grid)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_9_c():
    # No fields actually
    doc = {'scale_type': 'linear',
           'f': lambda x: x
           }
    v = Validator(axis_schema_type_9_axis)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


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
    assert v.validate(doc) is False


def test_axis_schema_type_9_e():
    # ok
    doc = {'scale_type': 'linear',
           'grid': False,
           'f': lambda x: x,
           'g': lambda x: x,
           'h': lambda x: x,
           }
    assert validate_axis_type_9(doc) is True


def test_axis_schema_type_9_f():
    # ok
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


def test_axis_schema_type_9_g():
    # incorrect function type (1 variable)
    doc = {
        'grid': True,
        'f_grid': lambda x: x,
        'g_grid': lambda x, y: x + y,
        'h_grid': lambda x, y: x + y,
        'u_start': 0.0,
        'u_stop': 0.0,
        'v_start': 0.0,
        'v_stop': 0.0,
    }
    assert validate_axis_type_9(doc) is False


# Type 8 axis parameters
def test_axis_schema_type_10_a():
    # Missing fields
    doc = {'scale_type': 'linear',
           'tick_distance_smart': 30,
           'base_stop': None}
    v = Validator(axis_schema_type_10)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_10_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_10)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_10_c():
    # No fields actually
    doc = {
        'function': lambda x: x,
        'u_min': 0,
        'u_max': 1.0}
    v = Validator(axis_schema_type_10)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is True


def test_axis_schema_type_10_w_a():
    # Missing fields
    doc = {'scale_type': 'linear',
           'tick_distance_smart': 30,
           'base_stop': None}
    v = Validator(axis_schema_type_10_w)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_10_w_b():
    # Invalid document (missing all fields)
    doc = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v = Validator(axis_schema_type_10_w)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_10_w_c():
    # missing field
    doc = {
        'function_3': lambda x: x,
        'u_min': 0,
        'u_max': 1.0}
    v = Validator(axis_schema_type_10_w)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_10_w_d():
    # 'function' should not be
    doc = {
        'function': lambda x: x,
        'function_3': lambda x: x,
        'function_4': lambda x: x,
        'u_min': 0,
        'u_max': 1.0}
    v = Validator(axis_schema_type_10_w)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is False


def test_axis_schema_type_10_w_e():
    # 'function' should not be
    doc = {
        'function_3': lambda x: x,
        'function_4': lambda x: x,
        'u_min': 0,
        'u_max': 1.0}
    v = Validator(axis_schema_type_10_w)
    if not v.validate(doc):
        print(v.errors)
    assert v.validate(doc) is True


def test_give_default_axis_values_a():
    # Get one correct field
    values = give_default_axis_values('type_1')
    assert values['align_x_offset'] == 0.0


def test_give_default_axis_values_b():
    # Get zero with incorrect axis_type
    values = give_default_axis_values('type_z')
    assert len(values) == 0


def test_give_default_axis_values_c():
    # Just run all fields
    _ = give_default_axis_values('type_1')
    _ = give_default_axis_values('type_2')
    _ = give_default_axis_values('type_3')
    _ = give_default_axis_values('type_4')
    _ = give_default_axis_values('type_5')
    _ = give_default_axis_values('type_6')
    _ = give_default_axis_values('type_7')
    _ = give_default_axis_values('type_8')
    _ = give_default_axis_values('type_9_axis')
    _ = give_default_axis_values('type_9_grid')
    _ = give_default_axis_values('type_10')
    _ = give_default_axis_values('type_10_w')
    assert True
