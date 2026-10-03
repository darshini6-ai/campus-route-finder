from src.smartcampus.graph.campus_data import create_weighted_campus_graph
from src.smartcampus.graph.ucs import uniform_cost_search


def test_main_gate_to_auditorium():
    graph = create_weighted_campus_graph()

    path, cost = uniform_cost_search(
        graph,
        "Main Gate",
        "Auditorium",
    )

    assert path is not None
    assert cost is not None
    assert path[0] == "Main Gate"
    assert path[-1] == "Auditorium"
    assert cost == 7


def test_same_location():
    graph = create_weighted_campus_graph()

    path, cost = uniform_cost_search(
        graph,
        "Main Gate",
        "Main Gate",
    )

    assert path == ["Main Gate"]
    assert cost == 0


def test_main_gate_to_hostel():
    graph = create_weighted_campus_graph()

    path, cost = uniform_cost_search(
        graph,
        "Main Gate",
        "Hostel",
    )

    assert path is not None
    assert cost is not None
    assert path[0] == "Main Gate"
    assert path[-1] == "Hostel"
    assert cost == 9


def test_no_route():
    graph = create_weighted_campus_graph()

    path, cost = uniform_cost_search(
        graph,
        "Main Gate",
        "Medical Center",
    )

    assert path is None
    assert cost is None
