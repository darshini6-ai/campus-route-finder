from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Course:
    """A course that must be assigned to a room and time slot."""

    name: str
    faculty: str
    batch: str
    students: int
    is_lab: bool


@dataclass(frozen=True)
class Room:
    name: str
    capacity: int
    is_lab: bool
    location: str = ""


@dataclass(frozen=True)
class TimeSlot:
    """A timetable slot identified by day and period."""

    day: str
    period: int


@dataclass(frozen=True)
class Assignment:
    """A possible assignment of a course to a room and time slot."""

    course: Course
    room: Room
    slot: TimeSlot


def create_courses() -> List[Course]:
    """Create the sample courses used by the CSP."""

    return [
        Course(
            name="Artificial Intelligence",
            faculty="Dr. Kumar",
            batch="AIML-A",
            students=55,
            is_lab=False,
        ),
        Course(
            name="Machine Learning",
            faculty="Dr. Priya",
            batch="AIML-A",
            students=55,
            is_lab=False,
        ),
        Course(
            name="Python Programming Lab",
            faculty="Dr. Kumar",
            batch="AIML-A",
            students=40,
            is_lab=True,
        ),
        Course(
            name="Data Structures",
            faculty="Dr. Arun",
            batch="AIML-B",
            students=50,
            is_lab=False,
        ),
        Course(
            name="AI Programming Lab",
            faculty="Dr. Priya",
            batch="AIML-B",
            students=35,
            is_lab=True,
        ),
    ]


def create_rooms() -> List[Room]:
    return [
        Room(
            "CSE Classroom 1",
            60,
            False,
            "CSE Block",
        ),
        Room(
            "CSE Classroom 2",
            50,
            False,
            "CSE Block",
        ),
        Room(
            "AI Lab",
            40,
            True,
            "AI Lab",
        ),
        Room(
            "ML Lab",
            45,
            True,
            "AI Lab",
        ),
    ]


def create_time_slots() -> List[TimeSlot]:
    """Create the available timetable slots."""

    return [
        TimeSlot(day="Monday", period=1),
        TimeSlot(day="Monday", period=2),
        TimeSlot(day="Monday", period=3),
        TimeSlot(day="Tuesday", period=1),
        TimeSlot(day="Tuesday", period=2),
        TimeSlot(day="Tuesday", period=3),
    ]


def create_domains(
    courses: List[Course],
    rooms: List[Room],
    slots: List[TimeSlot],
) -> dict[str, List[Assignment]]:
    """
    Create the CSP domain for every course.

    Each course initially receives every possible
    room-slot combination. Constraints will later
    remove invalid assignments.
    """

    domains: dict[str, List[Assignment]] = {}

    for course in courses:
        domains[course.name] = [
            Assignment(
                course=course,
                room=room,
                slot=slot,
            )
            for room in rooms
            for slot in slots
        ]

    return domains
