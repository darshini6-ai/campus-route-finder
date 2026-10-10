"""
Realistic campus timetable data for the CSP extension.

The room locations reuse the same campus locations as the
Phase-1 BFS graph.
"""

CLASSES = {
    "AI Lecture": {
        "faculty": "Dr. Kumar",
        "batch": "II-A",
        "type": "lecture",
        "students": 40,
    },
    "ML Lab": {
        "faculty": "Dr. Priya",
        "batch": "II-A",
        "type": "lab",
        "students": 30,
    },
    "Data Science": {
        "faculty": "Dr. Ravi",
        "batch": "II-B",
        "type": "lecture",
        "students": 35,
    },
    "Python Lab": {
        "faculty": "Dr. Kumar",
        "batch": "II-B",
        "type": "lab",
        "students": 30,
    },
}


ROOMS = {
    "CSE Classroom": {
        "capacity": 50,
        "is_lab": False,
        "location": "CSE Block",
    },
    "AI Lab": {
        "capacity": 40,
        "is_lab": True,
        "location": "AI Lab",
    },
    "Library Seminar Room": {
        "capacity": 45,
        "is_lab": False,
        "location": "Library",
    },
    "Auditorium": {
        "capacity": 100,
        "is_lab": False,
        "location": "Auditorium",
    },
}


TIME_SLOTS = [
    "09:00-10:00",
    "10:00-11:00",
    "11:00-12:00",
]


MAX_HOPS = 2