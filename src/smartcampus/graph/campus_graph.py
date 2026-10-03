from typing import Dict, List, Tuple


class CampusGraph:
    """Graph representation of the campus."""

    def __init__(self) -> None:
        self.locations: Dict[str, Dict[str, float]] = {}

    def add_location(self, name: str) -> None:
        """Add a campus location if it does not already exist."""
        name = name.strip()

        if name not in self.locations:
            self.locations[name] = {}

    def add_connection(
        self,
        location_a: str,
        location_b: str,
        weight: float = 1,
    ) -> None:
        """
        Add an undirected connection between two locations.

        weight represents the travel cost of the connection.
        For the original BFS graph, the default weight is 1.
        """
        self.add_location(location_a)
        self.add_location(location_b)

        self.locations[location_a][location_b] = weight
        self.locations[location_b][location_a] = weight

    def get_neighbors(self, location: str) -> List[str]:
        """Return neighboring locations."""
        if location not in self.locations:
            return []

        return list(self.locations[location].keys())

    def get_weighted_neighbors(
        self,
        location: str,
    ) -> List[Tuple[str, float]]:
        """Return neighboring locations with their edge costs."""
        if location not in self.locations:
            return []

        return list(self.locations[location].items())

    def has_location(self, name: str) -> bool:
        """Check whether a location exists."""
        return name in self.locations
