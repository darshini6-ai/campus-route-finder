from src.smartcampus.csp.backtracking import BacktrackingSolver
from src.smartcampus.csp.constraints import (
    assignments_conflict,
    assignment_is_valid,
)
from src.smartcampus.csp.timetable import (
    create_courses,
    create_domains,
    create_rooms,
    create_time_slots,
)


def test_backtracking_finds_solution():
    courses = create_courses()
    rooms = create_rooms()
    slots = create_time_slots()

    domains = create_domains(
        courses,
        rooms,
        slots,
    )

    solver = BacktrackingSolver(domains)

    solution = solver.solve()

    assert solution is not None
    assert len(solution) == len(courses)


def test_solution_assignments_are_valid():
    courses = create_courses()
    rooms = create_rooms()
    slots = create_time_slots()

    domains = create_domains(
        courses,
        rooms,
        slots,
    )

    solver = BacktrackingSolver(domains)

    solution = solver.solve()

    assert solution is not None

    assignments = list(solution.values())

    for assignment in assignments:
        assert assignment_is_valid(assignment)


def test_solution_has_no_conflicts():
    courses = create_courses()
    rooms = create_rooms()
    slots = create_time_slots()

    domains = create_domains(
        courses,
        rooms,
        slots,
    )

    solver = BacktrackingSolver(domains)

    solution = solver.solve()

    assert solution is not None

    assignments = list(solution.values())

    for index, assignment_a in enumerate(assignments):
        for assignment_b in assignments[index + 1:]:
            assert not assignments_conflict(
                assignment_a,
                assignment_b,
            )


def test_solver_records_statistics():
    courses = create_courses()
    rooms = create_rooms()
    slots = create_time_slots()

    domains = create_domains(
        courses,
        rooms,
        slots,
    )

    solver = BacktrackingSolver(domains)

    solution = solver.solve()

    assert solution is not None
    assert solver.stats.assignments_tried > 0
    assert solver.stats.backtracks >= 0
