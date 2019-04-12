from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, List, Set, Dict, Optional
from re import search

from ..common.common import get_input


def parse_claim(claim_string: str) -> Tuple[int, ...]:
    """
    Parses a claim string into its parts
    For example #1357 @ 789,377: 13x14 will return (1357, 789, 377, 13, 14)
    """
    match = search(r'#(\d+).+?(\d+),(\d+):.+?(\d+)x(\d+)', claim_string)
    if match:
        return tuple([int(match.group(gi)) for gi in range(1, 6)])
    return 0, 0, 0, 0, 0


@dataclass
class Claim(object):
    id: int = 0
    left: int = 0
    top: int = 0
    width: int = 1
    height: int = 1

    @staticmethod
    def create_claim_from_string(claim_string: str) -> Claim:
        return Claim(*parse_claim(claim_string))

    @property
    def area(self) -> int:
        return self.width * self.height

    @property
    def square_coords(self) -> List[Tuple[int, int]]:
        coords = []
        for x in range(self.width):
            x += self.left
            for y in range(self.height):
                y += self.top
                coords.append((x, y))
        return coords


@dataclass
class FabricSquare(object):
    x: int
    y: int
    claims: Set[int] = field(default_factory=lambda: set())

    def add_claim_id(self, claim_id: int) -> None:
        self.claims.add(claim_id)

    def have_more_than_one_claim(self) -> bool:
        return len(self.claims) > 1


@dataclass
class Fabric(object):
    claims: List[Claim] = field(default_factory=lambda: [])
    squares: Dict[Tuple[int, int], FabricSquare] = field(default_factory=lambda: {})

    def add_claim(self, claim: Claim) -> None:
        self.claims.append(claim)
        self._process_claim_squares(claim)

    def _process_claim_squares(self, claim: Claim) -> None:
        for x, y in claim.square_coords:
            square = self.squares.get((x, y), FabricSquare(x, y))
            self.squares[(x, y)] = square
            square.add_claim_id(claim.id)

    def number_of_squares_with_more_than_one_claim(self) -> int:
        return len([square for square in self.squares.values() if square.have_more_than_one_claim()])

    def find_good_claim(self) -> Optional[Claim]:
        tested_claims = []
        for claim in self.claims:
            if claim not in tested_claims:
                if self._is_claim_good(claim):
                    return claim
                tested_claims.append(claim)

    def _is_claim_good(self, claim: Claim) -> bool:
        num_squares_with_only_one_claim = 0
        for x, y in claim.square_coords:
            if len(self.squares[(x, y)].claims) == 1:
                num_squares_with_only_one_claim += 1
        return num_squares_with_only_one_claim == claim.area


def run_part_01(input_list: list) -> Fabric:
    fabric = Fabric()
    for claim_string in input_list:
        claim = Claim.create_claim_from_string(claim_string)
        fabric.add_claim(claim)
    print(f'There are {fabric.number_of_squares_with_more_than_one_claim()} squares with more than 1 claim')
    return fabric


def run_part_02(fabric: Fabric) -> None:
    good_claim = fabric.find_good_claim()
    print(f'This is the best claim: {good_claim.id}')


def run():
    input_list = get_input('day_03')
    fabric = run_part_01(input_list)
    run_part_02(fabric)




