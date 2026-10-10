from python_src.campus_graph import CampusGraph
from python_src.bfs import find_shortest_path
from python_src.smart_navigation import uniform_cost_search, a_star_search


def test_bfs_minimises_hops_while_ucs_and_astar_minimise_cost():
    graph = CampusGraph()
    for location in ["Start", "A", "B", "Goal"]:
        graph.add_location(location)

    for first, second in [
        ("Start", "Goal"),
        ("Start", "A"),
        ("A", "B"),
        ("B", "Goal"),
    ]:
        graph.add_connection(first, second)

    costs = {
        ("Start", "Goal"): 10,
        ("Start", "A"): 1,
        ("A", "B"): 1,
        ("B", "Goal"): 1,
    }

    bfs_path = find_shortest_path(graph, "Start", "Goal")
    ucs_result = uniform_cost_search(
        graph, "Start", "Goal", edge_costs=costs
    )
    astar_result = a_star_search(
        graph, "Start", "Goal", edge_costs=costs
    )

    assert bfs_path == ["Start", "Goal"]
    assert ucs_result["path"] == ["Start", "A", "B", "Goal"]
    assert ucs_result["cost"] == 3
    assert astar_result["path"] == ["Start", "A", "B", "Goal"]
    assert astar_result["cost"] == 3
