from typing import Dict, Union, List, Any, Callable

from pynomo.data_validation.axis_schemas import axis_schema_type_10
from pynomo.data_validation.block_schemas import block_schema_type_1, block_schema_type_2, block_schema_type_3, \
    block_schema_type_4, block_schema_type_5, block_schema_type_6, block_schema_type_7, block_schema_type_8, \
    block_schema_type_9
from pynomo.data_validation.dictionary_validation_functions import validate_params_


def validate_block_params(block_type: str, params: Dict[str, dict]) -> (bool, Dict[str, Union[str, List[str]]]):
    switcher = {
        'type_1': validate_params_(block_schema_type_1, params),
        'type_2': validate_params_(block_schema_type_2, params),
        'type_3': validate_params_(block_schema_type_3, params),
        'type_4': validate_params_(block_schema_type_4, params),
        'type_5': validate_params_(block_schema_type_5, params),
        'type_6': validate_params_(block_schema_type_6, params),
        'type_7': validate_params_(block_schema_type_7, params),
        'type_8': validate_params_(block_schema_type_8, params),
        'type_9': validate_params_(block_schema_type_9, params),
        'type_10': validate_params_(axis_schema_type_10, params)
    }
    result, errors = switcher.get(block_type, "Incorrect key")
    if result == "Incorrect key":
        print(f"Internal error: incorrect block_type '{block_type}' when getting default values")
        return False, {'error': f'Internal error checking "{block_type}"'}
    return result, errors


def validate_type_1_block_params(field: Any, value: Any, error: Callable) -> (bool, Dict[str, Union[str, List[str]]]):
    ok: bool
    errors: Dict[str, Union[str, List[str]]]
    ok, errors = validate_block_params('type_1', value)
    if not ok:
        error(errors, "Error when inspecting type 1 block")
    return ok, errors

if __name__ == "__main__":
    params = {'scale_type': 'linear', 'tick_distance_smart': 30, 'base_stop': None}
    params = {'f1_params': {},
              'f2_params': {},
              'f3_params': {},
              'f4_params': {}
              }
    def error(errors, message):
        print(message)
    validate_type_1_block_params(True, params, error)