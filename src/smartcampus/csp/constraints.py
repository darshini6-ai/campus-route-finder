from .timetable import Assignment
from src.smartcampus.graph.bfs import bfs_shortest_path


def room_has_capacity(assignment):
    return assignment.room.capacity >= assignment.course.students


def lab_requirement_satisfied(assignment):
    if assignment.course.is_lab:
        return assignment.room.is_lab
    return True


def same_time(a, b):
    return a.slot == b.slot


def room_conflict(a, b):
    return same_time(a, b) and a.room.name == b.room.name


def faculty_conflict(a, b):
    return same_time(a, b) and a.course.faculty == b.course.faculty


def batch_conflict(a, b):
    return same_time(a, b) and a.course.batch == b.course.batch


def assignments_conflict(a, b):
    return (
        room_conflict(a, b)
        or faculty_conflict(a, b)
        or batch_conflict(a, b)
    )


def assignment_is_valid(a):
    return (
        room_has_capacity(a)
        and lab_requirement_satisfied(a)
    )


def are_consecutive_slots(a, b):
    """Return True when two classes are consecutive on the same day."""
    return (
        a.slot.day == b.slot.day
        and abs(a.slot.period - b.slot.period) == 1
    )


def consecutive_batch_distance_satisfied(
    a,
    b,
    graph,
    k,
):
    """
    Check the BFS-distance constraint for consecutive classes.

    If the classes belong to different batches, the constraint
    does not apply.

    If they are not consecutive on the same day, the constraint
    does not apply.

    Otherwise, the BFS distance between their room locations
    must be at most k.
    """
    if a.course.batch != b.course.batch:
        return True

    if not are_consecutive_slots(a, b):
        return True

    if not a.room.location or not b.room.location:
        return False

    path = bfs_shortest_path(
        graph,
        a.room.location,
        b.room.location,
    )

    if path is None:
         return False

    distance = len(path) - 1
    return distance <= k
