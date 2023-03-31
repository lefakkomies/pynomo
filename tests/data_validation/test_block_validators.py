import pytest

from pynomo.data_validation.block_validators import validate_type_1_block_params


@pytest.fixture
def fixture():
    def error(errors, message):
        print(message)

    return error


def test_validate_type_1_block_params_a(fixture):
    # incorrect input
    error = fixture
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_1_block_params(True, params, error)
    print(errors)
    assert ok is False


def test_validate_type_1_block_params_b(fixture):
    # correct input
    error = fixture
    params = {'f1_params': True,
              'f2_params': True,
              'f3_params': True,
              'f4_params': True
              }
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_1_block_params(True, params, error)
    #print(errors)
    assert ok is False
