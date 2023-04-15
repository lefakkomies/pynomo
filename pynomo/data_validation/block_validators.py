from pprint import pprint
from typing import Dict, Union, List, Any, Callable

from pynomo.data_validation.axis_schemas import axis_schema_type_10, give_default_axis_values
from pynomo.data_validation.block_schemas import block_schema_type_1, block_schema_type_2, block_schema_type_3, \
    block_schema_type_4, block_schema_type_5, block_schema_type_6, block_schema_type_7, block_schema_type_8, \
    block_schema_type_9
from pynomo.data_validation.dictionary_validation_functions import validate_params_


def validate_block_params(block_type: str, params: Dict[str, dict]) -> (bool, Dict[str, Union[str, List[str]]]):
    switcher = {
        'type_1': lambda: validate_params_(block_schema_type_1, params),
        'type_2': lambda: validate_params_(block_schema_type_2, params),
        'type_3': lambda: validate_params_(block_schema_type_3, params),
        'type_4': lambda: validate_params_(block_schema_type_4, params),
        'type_5': lambda: validate_params_(block_schema_type_5, params),
        'type_6': lambda: validate_params_(block_schema_type_6, params),
        'type_7': lambda: validate_params_(block_schema_type_7, params),
        'type_8': lambda: validate_params_(block_schema_type_8, params),
        'type_9': lambda: validate_params_(block_schema_type_9, params),
        'type_10': lambda: validate_params_(axis_schema_type_10, params)
    }
    result, errors = switcher.get(block_type, "Incorrect key")()
    if result == "Incorrect key":
        print(f"Internal error: incorrect block_type '{block_type}' when getting default values")
        return False, {'error': f'Internal error checking "{block_type}"'}
    return result, errors


def validate_type_1_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_block_params('type_1', value)
    if not ok:
        error(errors, str(errors))
    return ok, errors


def validate_type_2_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_block_params('type_2', value)
    if not ok:
        error(errors, errors)
    return ok, errors


def validate_type_3_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_block_params('type_3', value)
    if not ok:
        error(errors, errors)
    return ok, errors


def validate_type_4_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_block_params('type_4', value)
    if not ok:
        error(errors, errors)
    return ok, errors


def validate_type_5_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_block_params('type_5', value)
    if not ok:
        error(errors, errors)
    return ok, errors


def validate_type_6_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_block_params('type_6', value)
    if not ok:
        error(errors, errors)
    return ok, errors


def validate_type_7_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_block_params('type_7', value)
    if not ok:
        error(errors, errors)
    return ok, errors


def validate_type_8_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_block_params('type_8', value)
    if not ok:
        error(errors, str(errors))
    return ok, errors


def validate_type_9_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_block_params('type_9', value)
    if not ok:
        error(errors, errors)
    return ok, errors


def validate_type_10_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_block_params('type_10', value)
    if not ok:
        error(errors, errors)
    return ok, errors


if __name__ == "__main__":
    default_values = give_default_axis_values('type_1')
    required_values = {'function': lambda x: x, 'u_min': 0.0, 'u_max': 1.0}
    params = {'f1_params': {**default_values, **required_values},
              'f2_params': {**default_values, **required_values},
              'f3_params': {**default_values, **required_values}
              }
    # error(errors, "Error when inspecting type 1")
    ok, errors = validate_type_1_block_params('para', params, lambda a, b: print(a, b))
    print(errors)
    # pprint(give_default_axis_values('type_1'))
