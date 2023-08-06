from typing import List, Tuple

# TODO(infokiller): Figure out
# pylint: disable=no-name-in-module
from keydope import keycodes, mods
from keydope.mods import Modifier

COMBO_SEPARATOR = '-'

_MODIFIER_TO_STRINGS = {
    Modifier.CONTROL: ['Ctrl', 'C'],
    Modifier.ALT: ['Alt', 'M'],
    Modifier.SHIFT: ['Shift'],
    Modifier.SUPER: ['Super'],
    Modifier.ISO_LEVEL3: ['LV3'],
    Modifier.ISO_LEVEL5: ['LV5'],
}


def _invert_dict_to_list(input_dict: dict) -> dict:
    inverted = {}
    for key, values in input_dict.items():
        for value in values:
            inverted[value] = key
    return inverted


_STRING_TO_MODIFIER = _invert_dict_to_list(_MODIFIER_TO_STRINGS)


def parse_key_name(key_name: str) -> List[keycodes.Key]:
    if key_name in _STRING_TO_MODIFIER:
        modifier = _STRING_TO_MODIFIER[key_name]
        modifier_keys = mods.modifier_to_keys(modifier)
        if not modifier_keys:
            raise ValueError(
                'No modifier key is assigned to modifier: {}'.format(
                    modifier.name))
        return modifier_keys
    if not hasattr(keycodes.Key, key_name.upper()):
        raise ValueError('Unknown key: {}'.format(key_name))
    return [getattr(keycodes.Key, key_name.upper())]


def combo_to_str(combo: mods.Combo) -> str:
    mod_keys = combo.get_mod_keys()
    regular_keys = list(combo.keys - set(mod_keys))
    return COMBO_SEPARATOR.join(k.name for k in mod_keys + regular_keys)


def parse_combo(combo_str: str) -> mods.Combo:
    combo_keys = set()
    for key_name in combo_str.split(COMBO_SEPARATOR):
        keys = parse_key_name(key_name)
        combo_keys.add(next(iter(keys)))
    return mods.Combo(combo_keys)


class ComboSpec:

    def __init__(self, key_sets: List[List[keycodes.Key]], exact_match=True):
        key_tuples = []
        for keys in key_sets:
            key_tuples.append(tuple(keys))
        self.key_sets = tuple(key_tuples)
        self.exact_match: bool = exact_match

    def match(self, combo):
        # Every list in key_sets must have at least one key satisfied by the
        # combo.
        matched_combo_keys = set()
        for keys in self.key_sets:
            matched_key = None
            for k in combo.keys:
                if k in keys:
                    matched_key = k
                    break
            if not matched_key:
                return False
            matched_combo_keys.add(matched_key)
        if self.exact_match and matched_combo_keys != combo.keys:
            return False
        return True

    def __eq__(self, other):
        if isinstance(other, ComboSpec):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        return hash(frozenset((self.key_sets, self.exact_match)))


def parse_combo_spec(keyspec_str: str, exact_match: bool = True) -> ComboSpec:
    key_sets = []
    for key_name in keyspec_str.split(COMBO_SEPARATOR):
        key_sets.append(parse_key_name(key_name))
    return ComboSpec(key_sets, exact_match)
