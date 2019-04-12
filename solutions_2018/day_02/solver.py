from collections import defaultdict
from typing import List, Union

from ..common.common import get_input


def get_count_per_letter(text):
    results_dict = defaultdict(int)
    for letter in text:
        results_dict[letter] += 1
    return results_dict


def have_letter_repeated(count_per_letter, number_of_repetitions):
    for count in count_per_letter.values():
        if count == number_of_repetitions:
            return True
    return False


def run_part_01(input_list):
    box_ids_with_two = 0
    box_ids_with_three = 0
    for box_id in input_list:
        count_per_letter = get_count_per_letter(box_id)
        if have_letter_repeated(count_per_letter, 2):
            box_ids_with_two += 1
        if have_letter_repeated(count_per_letter, 3):
            box_ids_with_three += 1
    print(f'Checksum is {box_ids_with_two * box_ids_with_three}')


def search_for_similar_box_id(box_id: str, box_id_list_to_search: List[str]) -> Union[bool, str]:
    for box_id_to_compare in box_id_list_to_search:
        if are_box_ids_similar(box_id, box_id_to_compare):
            return box_id_to_compare
    return False


def common_letters(box_id_1: str, box_id_2: str) -> str:
    cl = []
    for index, letter in enumerate(box_id_1):
        if letter == box_id_2[index]:
            cl.append(letter)
    return ''.join(cl)


def are_box_ids_similar(box_id_1: str, box_id_2: str) -> bool:
    cl = common_letters(box_id_1, box_id_2)
    return len(cl) == len(box_id_1) - 1 == len(box_id_2) - 1


def run_part_02(input_list):
    seen_box_ids = []
    for box_id_1 in input_list:
        similar_box_id = search_for_similar_box_id(box_id_1, seen_box_ids)
        if similar_box_id:
            print(common_letters(box_id_1, similar_box_id))
            return
        seen_box_ids.append(box_id_1)


def run():
    input_list = get_input('day_02')
    run_part_01(input_list)
    run_part_02(input_list)
