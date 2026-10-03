from src.smartcampus.csp.ac3_backtracking import (
    AC3BacktrackingSolver,
)
from src.smartcampus.csp.constraints import (
    assignment_is_valid,
    assignments_conflict,
)
from src.smartcampus.csp.timetable import (
    create_courses,
    create_rooms,
    create_time_slots,
    create_domains,
)
from src.smartcampus.graph.campus_data import create_campus_graph


def test_ac3_backtracking_finds_solution():
    courses = create_courses()
    rooms = create_rooms()
    slots = create_time_slots()

    domains = create_domains(courses, rooms, slots)
    graph = create_campus_graph()

    solver = AC3BacktrackingSolver(
        domains,
        graph=graph,
        k=3,
    )

    solution = solver.solve()

    assert solution is not None
    assert len(solution) == len(courses)


def test_ac3_backtracking_solution_is_valid():
    courses = create_courses()
    rooms = create_rooms()
    slots = create_time_slots()

    domains = create_domains(courses, rooms, slots)
    graph = create_campus_graph()

    solver = AC3BacktrackingSolver(
        domains,
        graph=graph,
        k=3,
    )

    solution = solver.solve()

    assert solution is not None

    assignments = list(solution.values())

    for assignment in assignments:
        assert assignment_is_valid(assignment)

    for index, assignment_a in enumerate(assignments):
        for assignment_b in assignments[index + 1:]:
            assert not assignments_conflict(
                assignment_a,
                assignment_b,
            )


def test_ac3_backtracking_records_statistics():
    courses = create_courses()
    rooms = create_rooms()
    slots = create_time_slots()

    domains = create_domains(courses, rooms, slots)
    graph = create_campus_graph()

    solver = AC3BacktrackingSolver(
        domains,
        graph=graph,
        k=3,
    )

    solution = solver.solve()

    assert solution is not None
    assert solver.stats.assignments_tried > 0
    assert solver.stats.propagation_calls > 0
    assert solver.stats.values_removed >= 0
    assert solver.stats.backtracks >= 0
