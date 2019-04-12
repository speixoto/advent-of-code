from ..common.common import get_input


def calculate_frequency(initial_frequency, frequency_list):
    current_freq = initial_frequency
    for f in frequency_list:
        current_freq += float(f)
        yield current_freq


def run_part_01(input_values):
    final_frequency = [f for f in calculate_frequency(0, input_values)][-1]
    print(f'Final frequency is: {final_frequency}')


def run_part_02(input_values):
    frequency_last_seen = set()
    initial_frequency = 0
    current_freq = 0
    while True:
        for current_freq in calculate_frequency(initial_frequency, input_values):
            if current_freq in frequency_last_seen:
                print(f'{current_freq} was already been seen!!!')
                return
            frequency_last_seen.add(current_freq)
        initial_frequency = current_freq


def run():
    input_values = get_input('day_01')
    run_part_01(input_values)
    run_part_02(input_values)
