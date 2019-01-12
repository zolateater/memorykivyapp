import json
from collections import defaultdict
from typing import List, Optional


DIGIT_GROUPS = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', # For 0-9
]
DIGIT_GROUP_NAMES = [
    '00-09', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99', '0-9'
]


def get_numbers_keys_for_group(group: str) -> List[str]:
    return [group + str(i) for i in range(0, 10)]

def get_number_values_for_group(group: str) -> List[str]:
    if group == '_':
        group = ''
    return [group + str(i) for i in range(0, 10)]

def get_all_keys() -> List[str]:
    return [key for g in DIGIT_GROUPS for key in get_numbers_keys_for_group(g)]


class NumberConfig:
    def __init__(self, data: Optional[dict] = None) -> None:
        self._data = dict()
        for key in get_all_keys():
            self._data[key] = data[key]['person'] if data and key in data else ''

    def get_value_for(self, assoc: str) -> str:
        return self._data[assoc]

    def set_value_for(self, assoc: str, value: str) -> None:
        self._data[assoc] = value

    def digit_group_filled(self, group: str) -> bool:
        return all([self._data[key] for key in get_numbers_keys_for_group(group)])

    @staticmethod
    def get_named_groups():
        return zip(DIGIT_GROUPS, DIGIT_GROUP_NAMES)


def read_config_from_stream(stream) -> NumberConfig:
    return NumberConfig(json.loads(stream.read()))


def write_config_to_stream(stream, config: NumberConfig) -> None:
    result = {k: {'person': config.get_value_for(k)} for k in get_all_keys()}
    stream.write(json.dumps(result))
