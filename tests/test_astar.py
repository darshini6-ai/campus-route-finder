from src.smartcampus.graph.astar import astar_search
from src.smartcampus.graph.campus_data import create_weighted_campus_graph


HEURISTIC_TO_AUDITORIUM = {
    "Main Gate": 5,
    "Library": 4,
    "CSE Block": 3,
    "AI Lab": 2,
    "Canteen": 5,
    "Admin Block": 3,
    "Auditorium": 0,
    "Hostel": 2,
    "Medical Center": 0,
}


def test_main_gate_to_auditorium():
    graph = create_weighted_campus_graph()

    path, cost = astar_search(
        graph,
        "Main Gate",
        "Auditorium",
        HEURISTIC_TO_AUDITORIUM,
    )

    assert path is not None
    assert cost is not None
    assert path[0] == "Main Gate"
    assert path[-1] == "Auditorium"
    assert cost == 7


def test_same_location():
    graph = create_weighted_campus_graph()

    path, cost = astar_search(
        graph,
        "Main Gate",
        "Main Gate",
        HEURISTIC_TO_AUDITORIUM,
    )

    assert path == ["Main Gate"]
    assert cost == 0


def test_main_gate_to_hostel():
    graph = create_weighted_campus_graph()

    heuristic = {
        "Main Gate": 7,
        "Library": 6,
        "CSE Block": 5,
        "AI Lab": 4,
        "Canteen": 7,
        "Admin Block": 5,
        "Auditorium": 2,
        "Hostel": 0,
        "Medical Center": 0,
    }

    path, cost = astar_search(
        graph,
        "Main Gate",
        "Hostel",
        heuristic,
    )

    assert path is not None
    assert cost is not None
    assert path[0] == "Main Gate"
    assert path[-1] == "Hostel"
    assert cost == 9


def test_no_route():
    graph = create_weighted_campus_graph()

    path, cost = astar_search(
        graph,
        "Main Gate",
        "Medical Center",
        HEURISTIC_TO_AUDITORIUM,
    )

    assert path is None
    assert cost is None
