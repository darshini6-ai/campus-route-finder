from python_src.csp.timetable_csp import TimetableCSP


CLASSES = {
    "AI Lecture": {
        "faculty": "Dr. Kumar",
        "batch": "II-A",
        "type": "lecture",
        "students": 40
    },
    "ML Lab": {
        "faculty": "Dr. Priya",
        "batch": "II-A",
        "type": "lab",
        "students": 30
    },
    "Data Science": {
        "faculty": "Dr. Ravi",
        "batch": "II-B",
        "type": "lecture",
        "students": 35
    }
}


ROOMS = {
    "Room 101": {
        "capacity": 50,
        "is_lab": False
    },
    "AI Lab": {
        "capacity": 40,
        "is_lab": True
    }
}


TIME_SLOTS = [
    "09:00-10:00",
    "10:00-11:00"
]


def test_backtracking_finds_valid_timetable():
    csp = TimetableCSP(
        CLASSES,
        ROOMS,
        TIME_SLOTS
    )

    solution = csp.solve_backtracking()

    assert solution is not None
    assert len(solution) == len(CLASSES)


def test_solution_respects_constraints():
    csp = TimetableCSP(
        CLASSES,
        ROOMS,
        TIME_SLOTS
    )

    solution = csp.solve_backtracking()

    assert solution is not None

    for class_name in solution:
        assert csp.is_consistent(
            class_name,
            solution
        )
def test_ac3_finds_valid_timetable():
    csp = TimetableCSP(
        CLASSES,
        ROOMS,
        TIME_SLOTS
    )

    solution = csp.solve_with_ac3()

    assert solution is not None
    assert len(solution) == len(CLASSES)

    for class_name in solution:
        assert csp.is_consistent(
            class_name,
            solution
        )
def test_ac3_tracks_search_nodes():
    csp = TimetableCSP(
        CLASSES,
        ROOMS,
        TIME_SLOTS
    )

    solution_without_ac3 = csp.solve_backtracking()

    assert solution_without_ac3 is not None

    nodes_without_ac3 = csp.nodes_checked

    solution_with_ac3 = csp.solve_with_ac3()

    assert solution_with_ac3 is not None

    nodes_with_ac3 = csp.nodes_checked_with_propagation

    assert nodes_without_ac3 > 0
    assert nodes_with_ac3 > 0