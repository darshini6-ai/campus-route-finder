from src.smartcampus.csp.ac3 import AC3Solver
from src.smartcampus.csp.timetable import (
    Assignment,
    Course,
    Room,
    TimeSlot,
)
from src.smartcampus.graph.campus_data import create_campus_graph


def test_ac3_removes_room_conflicts():
    course_a = Course(
        "Course A", "Faculty A", "AIML-A", 30, False
    )
    course_b = Course(
        "Course B", "Faculty B", "AIML-B", 30, False
    )

    room = Room("Room 1", 40, False, "CSE Block")
    slot = TimeSlot("Monday", 1)

    assignment_a = Assignment(course_a, room, slot)
    assignment_b = Assignment(course_b, room, slot)

    domains = {
        "Course A": [assignment_a],
        "Course B": [assignment_b],
    }

    solver = AC3Solver(domains)
    result = solver.solve()

    assert result is None


def test_ac3_removes_invalid_lab_assignment():
    course = Course(
        "AI Lab", "Faculty A", "AIML-A", 30, True
    )

    classroom = Room(
        "Classroom", 40, False, "CSE Block"
    )

    assignment = Assignment(
        course,
        classroom,
        TimeSlot("Monday", 1),
    )

    domains = {
        "AI Lab": [assignment],
    }

    solver = AC3Solver(domains)
    result = solver.solve()

    assert result is None


def test_ac3_preserves_compatible_assignments():
    course_a = Course(
        "Course A", "Faculty A", "AIML-A", 30, False
    )
    course_b = Course(
        "Course B", "Faculty B", "AIML-B", 30, False
    )

    room_a = Room("Room A", 40, False, "CSE Block")
    room_b = Room("Room B", 40, False, "AI Lab")

    assignment_a = Assignment(
        course_a,
        room_a,
        TimeSlot("Monday", 1),
    )

    assignment_b = Assignment(
        course_b,
        room_b,
        TimeSlot("Monday", 1),
    )

    domains = {
        "Course A": [assignment_a],
        "Course B": [assignment_b],
    }

    solver = AC3Solver(domains)
    result = solver.solve()

    assert result is not None
    assert len(result["Course A"]) == 1
    assert len(result["Course B"]) == 1


def test_ac3_applies_bfs_distance_constraint():
    graph = create_campus_graph()

    course_a = Course(
        "Course A", "Faculty A", "AIML-A", 30, False
    )
    course_b = Course(
        "Course B", "Faculty B", "AIML-A", 30, False
    )

    room_a = Room(
        "Room A", 40, False, "CSE Block"
    )
    room_b = Room(
        "Room B", 40, False, "Hostel"
    )

    assignment_a = Assignment(
        course_a,
        room_a,
        TimeSlot("Monday", 1),
    )

    assignment_b = Assignment(
        course_b,
        room_b,
        TimeSlot("Monday", 2),
    )

    domains = {
        "Course A": [assignment_a],
        "Course B": [assignment_b],
    }

    solver = AC3Solver(domains, graph=graph, k=2)
    result = solver.solve()

    assert result is None
