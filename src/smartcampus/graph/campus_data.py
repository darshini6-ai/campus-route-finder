from .campus_graph import CampusGraph


def create_campus_graph():
    """
    Create the initial campus graph from the IA-1
    Campus Route Finder.
    """

    graph = CampusGraph()

    connections = [
        ("Main Gate", "Library"),
        ("Main Gate", "Canteen"),
        ("Library", "CSE Block"),
        ("CSE Block", "AI Lab"),
        ("AI Lab", "Auditorium"),
        ("Canteen", "Admin Block"),
        ("Admin Block", "Auditorium"),
        ("Auditorium", "Hostel"),
    ]

    for location_a, location_b in connections:
        graph.add_connection(location_a, location_b)

    # Medical Center remains isolated,
    # matching the IA-1 test scenario.
    graph.add_location("Medical Center")

    return graph


def create_weighted_campus_graph():
    """
    Create the weighted campus graph for IA-2.

    The weights represent simulated travel costs for
    comparing BFS and Uniform Cost Search (UCS).
    """

    graph = CampusGraph()

    weighted_connections = [
        ("Main Gate", "Library", 2),
        ("Main Gate", "Canteen", 2),
        ("Library", "CSE Block", 2),
        ("CSE Block", "AI Lab", 3),
        ("AI Lab", "Auditorium", 2),
        ("Canteen", "Admin Block", 2),
        ("Admin Block", "Auditorium", 3),
        ("Auditorium", "Hostel", 2),
    ]

    for location_a, location_b, cost in weighted_connections:
        graph.add_connection(location_a, location_b, cost)

    # Medical Center remains isolated,
    # matching the IA-1 test scenario.
    graph.add_location("Medical Center")

    return graph
