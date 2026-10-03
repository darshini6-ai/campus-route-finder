from src.smartcampus.graph.campus_data import create_campus_graph
from src.smartcampus.graph.bfs import (
    bfs_shortest_path,
    count_hops
)


def test_main_gate_to_auditorium():

    graph = create_campus_graph()

    path = bfs_shortest_path(
        graph,
        "Main Gate",
        "Auditorium"
    )

    assert path is not None
    assert count_hops(path) == 3


def test_same_location():

    graph = create_campus_graph()

    path = bfs_shortest_path(
        graph,
        "Main Gate",
        "Main Gate"
    )

    assert path == ["Main Gate"]
    assert count_hops(path) == 0


def test_main_gate_to_hostel():

    graph = create_campus_graph()

    path = bfs_shortest_path(
        graph,
        "Main Gate",
        "Hostel"
    )

    assert path is not None
    assert count_hops(path) == 4


def test_no_route():

    graph = create_campus_graph()

    path = bfs_shortest_path(
        graph,
        "Main Gate",
        "Medical Center"
    )

    assert path is None
