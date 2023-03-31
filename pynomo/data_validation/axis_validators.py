from typing import Dict, Union, List, Any, Callable

from cerberus import Validator

from pynomo.data_validation.axis_schemas import axis_schema_type_9_axis, axis_schema_type_9_grid, axis_schema_type_1, \
    axis_schema_type_2, axis_schema_type_3, axis_schema_type_4, axis_schema_type_5, axis_schema_type_6, \
    axis_schema_type_7, axis_schema_type_8, axis_schema_type_10, axis_schema_type_10_w
from pynomo.data_validation.dictionary_validation_functions import validate_params_, check_general_axis_params


def validate_axis_params(axis_type: str, params: Dict[str, dict]) -> (bool, Dict[str, Union[str, List[str]]]):
    switcher = {
        'type_1': validate_params_(axis_schema_type_1, params),
        'type_2': validate_params_(axis_schema_type_2, params),
        'type_3': validate_params_(axis_schema_type_3, params),
        'type_4': validate_params_(axis_schema_type_4, params),
        'type_5': validate_params_(axis_schema_type_5, params),
        'type_6': validate_params_(axis_schema_type_6, params),
        'type_7': validate_params_(axis_schema_type_7, params),
        'type_8': validate_params_(axis_schema_type_8, params),
        'type_9_axis': validate_params_(axis_schema_type_9_axis, params),
        'type_9_grid': validate_params_(axis_schema_type_9_grid, params),
        'type_10': validate_params_(axis_schema_type_10, params),
        'type_10_w': validate_params_(axis_schema_type_10_w, params),
    }
    result, errors = switcher.get(axis_type, "Incorrect key")
    if result == "Incorrect key":
        print(f"Internal error: incorrect axis_type '{axis_type}' when getting default values")
        return False, {'error': f'Internal error checking "{axis_type}"'}
    return result, errors


"""
def validate_axis_type_9(params: dict) -> (bool, Dict[str, Union[str, List[str]]]):
    if 'grid' in params.keys():
        if params['grid'] is False:
            return validate_axis_params('type_9_axis')
        if params['grid'] is True:
            return validate_axis_params('type_9_grid')
    else:  # grid not defined assume 'grid' = False
        return validate_axis_params('type_9_axis')
"""


def validate_type_1_axis_params(field: Any, value: Any, error: Callable):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_axis_params('type_1', value)
    if not ok:
        error(field, str(errors))
    return ok, errors

def validate_type_1_axis_params_(field: Any, value: Any, error: Callable):
    validate_type_1_axis_params(field, value, error)

def validate_type_2_axis_params(field: Any, value: Any, error: Callable):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_axis_params('type_2', value)
    if not ok:
        error(field, "Error when inspecting type 2")


def validate_type_3_axis_params(field: Any, value: Any, error: Callable):
    check_general_axis_params(field, value, error)


def validate_type_4_axis_params(field: Any, value: Any, error: Callable):
    check_general_axis_params(field, value, error)


def validate_type_5_axis_params(field: Any, value: Any, error: Callable):
    # TODO run checker for type 5 axis params
    pass


def validate_type_6_axis_params(field: Any, value: Any, error: Callable):
    check_general_axis_params(field, value, error)


def validate_type_7_axis_params(field: Any, value: Any, error: Callable):
    # TODO run checker for type 7 axis params
    pass


def validate_type_8_axis_params(field: Any, value: Any, error: Callable):
    # TODO run checker for type 8 axis params
    pass


def validate_type_9_axis_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    if type(value) is not dict:
        return False, "Parameter need to be a dictionary"
    if 'grid' in value.keys():
        if value['grid'] is False:
            return validate_axis_params('type_9_axis', value)
        if value['grid'] is True:
            return validate_axis_params('type_9_grid', value)
    else:  # grid not defined assume 'grid' = False
        return validate_axis_params('type_9_axis', value)


def validate_type_10_axis_params(field: Any, value: Any, error: Callable):
    # TODO run checker for type 9 axis params
    pass


def validate_type_10_w_axis_params(field: Any, value: Any, error: Callable):
    # TODO run checker for type 9 axis params
    pass
