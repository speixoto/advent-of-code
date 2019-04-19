from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
from operator import attrgetter, itemgetter
from collections import Counter
from itertools import product


from ..common.common import get_input


@dataclass(frozen=True)
class Point(object):
    x: int = 0
    y: int = 0


@dataclass
class BoundaryBox(object):
    min_x: int = field(init=False)
    min_y: int = field(init=False)
    max_x: int = field(init=False)
    max_y: int = field(init=False)
    closest_point_grid: Dict[Point, Point] = field(init=False)
    total_distances_point_grid: Dict[Point, int] = field(init=False)
    points: List[Point] = field(repr=False, compare=False)

    def __post_init__(self):
        self._build_grids()

    def _calculate_grid_boundary(self):
        self.min_x = min(self.points, key=attrgetter('x')).x
        self.min_y = min(self.points, key=attrgetter('y')).y
        self.max_x = max(self.points, key=attrgetter('x')).x
        self.max_y = max(self.points, key=attrgetter('y')).y

    def _build_grids(self):
        self._calculate_grid_boundary()
        closest_grid = {}
        total_distance_grid = {}
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                grid_point = Point(x, y)
                closest_point, total_distance = self._get_closest_point_and_distance_to_all(grid_point)
                closest_grid[grid_point] = closest_point
                total_distance_grid[grid_point] = total_distance
        self.closest_point_grid = closest_grid
        self.total_distances_point_grid = total_distance_grid

    def _get_closest_point_and_distance_to_all(self, ref_point: Point) -> Tuple[Optional[Point], int]:
        distance_per_point = {point: manhattan_distance(point, ref_point) for point in self.points}
        closest_point, distance = min(distance_per_point.items(), key=itemgetter(1))

        total_distance = sum(distance_per_point.values())
        if list(distance_per_point.values()).count(distance) == 1:
            return closest_point, total_distance
        else:
            return None, total_distance

    def get_non_infinity_biggest_area(self):
        center_of_infinite_area = set()
        for x, y in product(range(self.min_x, self.max_x + 1), [self.min_y, self.max_y]):
            center_of_infinite_area.add(self.closest_point_grid[Point(x, y)])
        for y, x in product(range(self.min_y, self.max_y + 1), [self.min_x, self.max_x]):
            center_of_infinite_area.add(self.closest_point_grid[Point(x, y)])
        counter = Counter([point for point in self.closest_point_grid.values() if point not in center_of_infinite_area])
        return counter.most_common(1)[0]

    def get_size_of_all_locations_with_distance_less_than(self, size: int) -> int:
        return sum([1 for value in self.total_distances_point_grid.values() if value < size])


def manhattan_distance(point_a: Point, point_b: Point) -> int:
    """Calculate the Manhattan distance between two points"""
    return abs(point_a.x - point_b.x) + abs(point_a.y - point_b.y)


def parse_line(line: str) -> Point:
    x, y = line.split(',')
    return Point(int(x), int(y))


def run():
    input_coords = get_input('day_06')
    points = [parse_line(line) for line in input_coords]
    bb = BoundaryBox(points)
    point, size = bb.get_non_infinity_biggest_area()
    print(f'Largest area have size: {size} closest to {point}')
    print(f'he size of the region containing all locations which have a total distance to all given coordinates of '
          f'less than 10000 is {bb.get_size_of_all_locations_with_distance_less_than(10000)}')



