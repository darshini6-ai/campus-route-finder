from python_src.campus_graph import CampusGraph
from python_src.csp.timetable_csp import TimetableCSP
from python_src.csp.timetable_data import (
    CLASSES,
    ROOMS,
    TIME_SLOTS,
    MAX_HOPS,
)


def build_campus_graph():
    """Build the same campus map used by the route finder."""
    graph = CampusGraph()

    locations = [
        "Main Gate",
        "Library",
        "CSE Block",
        "AI Lab",
        "Canteen",
        "Admin Block",
        "Auditorium",
        "Hostel",
        "Medical Center",
    ]

    connections = [
        ("Main Gate", "Library"),
        ("Main Gate", "Canteen"),
        ("Library", "CSE Block"),
        ("CSE Block", "AI Lab"),
        ("AI Lab", "Auditorium"),
        ("Canteen", "Admin Block"),
        ("Admin Block", "Auditorium"),
        ("Auditorium", "Hostel"),
    ]

    for location in locations:
        graph.add_location(location)

    for first, second in connections:
        graph.add_connection(first, second)

    return graph


def make_solver():
    """Create the CSP solver using the real timetable data."""
    return TimetableCSP(
        classes=CLASSES,
        rooms=ROOMS,
        time_slots=TIME_SLOTS,
        campus_graph=build_campus_graph(),
        max_hops=MAX_HOPS,
    )


def assert_valid_timetable(solver, solution):
    """Check that every class is scheduled and all constraints hold."""
    assert solution is not None
    assert set(solution) == set(CLASSES)

    for class_name, (room_name, time_slot) in solution.items():
        assert room_name in ROOMS
        assert time_slot in TIME_SLOTS

        assert solver.is_consistent(class_name, solution)


def test_real_dataset_backtracking_finds_valid_timetable():
    solver = make_solver()

    solution = solver.solve_backtracking()

    assert_valid_timetable(solver, solution)
    assert solver.nodes_checked > 0


def test_real_dataset_ac3_finds_valid_timetable():
    solver = make_solver()

    solution = solver.solve_with_ac3()

    assert_valid_timetable(solver, solution)
    assert solver.nodes_checked_with_propagation > 0


def test_bfs_distance_uses_campus_connections():
    solver = make_solver()

    # Main Gate -> Canteen -> Admin Block
    assert solver._bfs_distance("Main Gate", "Admin Block") == 2

    # Medical Center is isolated in the campus graph.
    assert solver._bfs_distance("Main Gate", "Medical Center") is None


def test_lab_classes_are_assigned_to_lab_rooms():
    solver = make_solver()

    solution = solver.solve_with_ac3()

    assert solution is not None

    for class_name, (room_name, _) in solution.items():
        if CLASSES[class_name]["type"] == "lab":
            assert ROOMS[room_name]["is_lab"] is True


def test_room_capacity_is_sufficient():
    solver = make_solver()

    solution = solver.solve_with_ac3()

    assert solution is not None

    for class_name, (room_name, _) in solution.items():
        assert (
            ROOMS[room_name]["capacity"]
            >= CLASSES[class_name]["students"]
        )