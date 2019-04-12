from pathlib import Path
from typing import List


def get_input(day_name: str) -> List[str]:
    with open(Path('solutions_2018', day_name, 'input.txt')) as f:
        return [x.strip() for x in f.readlines()]
