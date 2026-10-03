from src.smartcampus.csp.constraints import (
    room_has_capacity,
    lab_requirement_satisfied,
    room_conflict,
    faculty_conflict,
    batch_conflict,
    assignment_is_valid,
    consecutive_batch_distance_satisfied,
)

from src.smartcampus.csp.timetable import (
    Course,
    Room,
    TimeSlot,
    Assignment,
)

from src.smartcampus.graph.campus_data import create_campus_graph
def test_room_capacity():
    course = Course(
        name="AI",
        faculty="Dr. Kumar",
        batch="AIML-A",
        students=50,
        is_lab=False,
    )

    room = Room(
        name="Classroom",
        capacity=60,
        is_lab=False,
    )

    assignment = Assignment(
        course=course,
        room=room,
        slot=TimeSlot("Monday", 1),
    )

    assert room_has_capacity(assignment)


def test_room_capacity_violation():
    course = Course(
        name="AI",
        faculty="Dr. Kumar",
        batch="AIML-A",
        students=70,
        is_lab=False,
    )

    room = Room(
        name="Classroom",
        capacity=60,
        is_lab=False,
    )

    assignment = Assignment(
        course=course,
        room=room,
        slot=TimeSlot("Monday", 1),
    )

    assert not room_has_capacity(assignment)


def test_lab_requires_lab_room():
    course = Course(
        name="AI Lab",
        faculty="Dr. Kumar",
        batch="AIML-A",
        students=35,
        is_lab=True,
    )

    lab = Room(
        name="AI Lab",
        capacity=40,
        is_lab=True,
    )

    assignment = Assignment(
        course=course,
        room=lab,
        slot=TimeSlot("Monday", 1),
    )

    assert lab_requirement_satisfied(assignment)


def test_lab_cannot_use_classroom():
    course = Course(
        name="AI Lab",
        faculty="Dr. Kumar",
        batch="AIML-A",
        students=35,
        is_lab=True,
    )

    classroom = Room(
        name="Classroom",
        capacity=60,
        is_lab=False,
    )

    assignment = Assignment(
        course=course,
        room=classroom,
        slot=TimeSlot("Monday", 1),
    )

    assert not lab_requirement_satisfied(assignment)


def test_room_conflict():
    course_a = Course(
        name="AI",
        faculty="Dr. Kumar",
        batch="AIML-A",
        students=50,
        is_lab=False,
    )

    course_b = Course(
        name="ML",
        faculty="Dr. Priya",
        batch="AIML-B",
        students=45,
        is_lab=False,
    )

    room = Room("Classroom", 60, False)
    slot = TimeSlot("Monday", 1)

    assignment_a = Assignment(course_a, room, slot)
    assignment_b = Assignment(course_b, room, slot)

    assert room_conflict(assignment_a, assignment_b)


def test_faculty_conflict():
    course_a = Course(
        name="AI",
        faculty="Dr. Kumar",
        batch="AIML-A",
        students=50,
        is_lab=False,
    )

    course_b = Course(
        name="Python",
        faculty="Dr. Kumar",
        batch="AIML-B",
        students=45,
        is_lab=False,
    )

    room_a = Room("Classroom 1", 60, False)
    room_b = Room("Classroom 2", 60, False)
    slot = TimeSlot("Monday", 1)

    assignment_a = Assignment(course_a, room_a, slot)
    assignment_b = Assignment(course_b, room_b, slot)

    assert faculty_conflict(assignment_a, assignment_b)


def test_batch_conflict():
    course_a = Course(
        name="AI",
        faculty="Dr. Kumar",
        batch="AIML-A",
        students=50,
        is_lab=False,
    )

    course_b = Course(
        name="ML",
        faculty="Dr. Priya",
        batch="AIML-A",
        students=45,
        is_lab=False,
    )

    room_a = Room("Classroom 1", 60, False)
    room_b = Room("Classroom 2", 60, False)
    slot = TimeSlot("Monday", 1)

    assignment_a = Assignment(course_a, room_a, slot)
    assignment_b = Assignment(course_b, room_b, slot)

    assert batch_conflict(assignment_a, assignment_b)


def test_valid_assignment():
    course = Course(
        name="AI",
        faculty="Dr. Kumar",
        batch="AIML-A",
        students=50,
        is_lab=False,
    )

    room = Room("Classroom", 60, False)
    slot = TimeSlot("Monday", 1)

    assignment = Assignment(course, room, slot)

    assert assignment_is_valid(assignment)
def test_consecutive_batch_classes_within_k_hops():
    graph = create_campus_graph()

    course_a = Course(
        "Course A",
        "Faculty A",
        "AIML-A",
        30,
        False,
    )

    course_b = Course(
        "Course B",
        "Faculty B",
        "AIML-A",
        30,
        False,
    )

    room_a = Room(
        "Room A",
        40,
        False,
        "CSE Block",
    )

    room_b = Room(
        "Room B",
        40,
        False,
        "AI Lab",
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

    assert consecutive_batch_distance_satisfied(
        assignment_a,
        assignment_b,
        graph,
        k=1,
    )


def test_consecutive_batch_classes_beyond_k_hops():
    graph = create_campus_graph()

    course_a = Course(
        "Course A",
        "Faculty A",
        "AIML-A",
        30,
        False,
    )

    course_b = Course(
        "Course B",
        "Faculty B",
        "AIML-A",
        30,
        False,
    )

    room_a = Room(
        "Room A",
        40,
        False,
        "CSE Block",
    )

    room_b = Room(
        "Room B",
        40,
        False,
        "Hostel",
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

    assert not consecutive_batch_distance_satisfied(
        assignment_a,
        assignment_b,
        graph,
        k=2,
    )


def test_non_consecutive_classes_ignore_distance_constraint():
    graph = create_campus_graph()

    course_a = Course(
        "Course A",
        "Faculty A",
        "AIML-A",
        30,
        False,
    )

    course_b = Course(
        "Course B",
        "Faculty B",
        "AIML-A",
        30,
        False,
    )

    room_a = Room(
        "Room A",
        40,
        False,
        "CSE Block",
    )

    room_b = Room(
        "Room B",
        40,
        False,
        "Hostel",
    )

    assignment_a = Assignment(
        course_a,
        room_a,
        TimeSlot("Monday", 1),
    )

    assignment_b = Assignment(
        course_b,
        room_b,
        TimeSlot("Monday", 3),
    )

    assert consecutive_batch_distance_satisfied(
        assignment_a,
        assignment_b,
        graph,
        k=0,
    )
