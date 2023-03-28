import pytest
from cerberus import Validator

from pynomo.data_validation.axes_schemas import axis_schema_type_1

def test_axis_schema_common():
    # Valid document
    doc1 = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    v1 = Validator(axis_schema_type_1)
    if not v1.validate(doc1):
        print(v1.errors)
    assert v1.validate(doc1) == False

    # Invalid document (missing 'age' field)
    doc2 = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
    v2 = Validator(axis_schema_type_1)
    if not v2.validate(doc2):
        print(v2.errors)
    assert v2.validate(doc2) == False
