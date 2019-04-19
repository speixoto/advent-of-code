from .solver import manhattan_distance, Point, BoundaryBox

mock_points = [Point(1, 1), Point(1, 6), Point(8, 3), Point(3, 4), Point(5, 5), Point(8, 9)]


def test_manhattan_distance():
    assert manhattan_distance(Point(2, 5), Point(4, 8)) == 5


def test_boundary_box():
    boundary_box = BoundaryBox(mock_points)
    assert boundary_box.min_x == 1
    assert boundary_box.min_y == 1
    assert boundary_box.max_x == 8
    assert boundary_box.max_y == 9

    closest_point_grid = boundary_box.closest_point_grid
    assert closest_point_grid[Point(1, 1)] == Point(1, 1)
    assert closest_point_grid[Point(2, 2)] == Point(1, 1)
    assert closest_point_grid[Point(4, 1)] == Point(1, 1)
    assert closest_point_grid[Point(4, 2)] == Point(3, 4)
    assert closest_point_grid[Point(5, 1)] is None
    assert closest_point_grid[Point(3, 6)] is None
    assert closest_point_grid[Point(3, 7)] is None
    assert closest_point_grid[Point(3, 8)] is None

    assert boundary_box.get_non_infinity_biggest_area() == (Point(5, 5), 17)

    assert boundary_box.get_size_of_all_locations_with_distance_less_than(32) == 16
