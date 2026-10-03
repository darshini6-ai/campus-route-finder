class CampusGraph:
    """
    Represents the campus as an unweighted graph.

    Each campus location is a node.
    Each connection between locations is an edge.
    """

    def __init__(self):
        self.adjacency = {}

    def add_location(self, location):
        """Add a location to the graph."""
        if location not in self.adjacency:
            self.adjacency[location] = []

    def add_connection(self, location_a, location_b):
        """
        Add a two-way connection between two campus locations.
        """

        self.add_location(location_a)
        self.add_location(location_b)

        if location_b not in self.adjacency[location_a]:
            self.adjacency[location_a].append(location_b)

        if location_a not in self.adjacency[location_b]:
            self.adjacency[location_b].append(location_a)

    def get_neighbors(self, location):
        """Return locations directly connected to a location."""
        return self.adjacency.get(location, [])

    def get_locations(self):
        """Return all campus locations."""
        return list(self.adjacency.keys())

    def has_location(self, location):
        """Check whether a location exists."""
        return location in self.adjacency
