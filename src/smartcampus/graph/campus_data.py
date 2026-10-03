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
