from string import ascii_lowercase
from operator import itemgetter
from typing import List

from ..common.common import get_input


def units_react(unit_1: str, unit_2: str) -> bool:
    """
    Units will react if they are the same letter but different polarity
    For example: a and A will react but A and A will not neither c and Z
    """
    return unit_1 != unit_2 and unit_1.upper() == unit_2.upper()


def polymer_reaction(polymer: str) -> str:
    """Remove all the consecutive units that react from the polymer string and return polymer after the reaction"""
    polymer_list = list(polymer)[::-1]
    result_polymer: List[str] = []
    while len(polymer_list) > 0:
        unit = polymer_list.pop()
        if len(result_polymer) > 0 and units_react(unit, result_polymer[-1]):
            result_polymer.pop()
        else:
            result_polymer.append(unit)
    return ''.join(result_polymer)


def clean_polymer(polymer: str, unit: str) -> str:
    """Cleans the polymer from all the selected unit (all polarities will be removed)"""
    return ''.join([x for x in polymer if x.upper() != unit.upper()])


def run():
    input_polymer = get_input('day_05')[0]
    after_reactions = polymer_reaction(input_polymer)
    print(f'Polymer after reactions has {len(after_reactions)} units!')

    results = []
    for unit in ascii_lowercase:
        results.append((unit, len(polymer_reaction(clean_polymer(input_polymer, unit)))))
    unit, length = min(results, key=itemgetter(1))
    print(f'Removing unit {unit} produces the shortest polymer with length {length}')

