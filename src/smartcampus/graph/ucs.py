import heapq
from typing import Dict, List, Optional, Tuple

from .campus_graph import CampusGraph


def uniform_cost_search(
    graph: CampusGraph,
    start: str,
    goal: str,
) -> Tuple[Optional[List[str]], Optional[float]]:
    """
    Find the minimum-cost path between start and goal using UCS.

    Returns:
        (path, total_cost)

    If no route exists:
        (None, None)
    """

    start = start.strip()
    goal = goal.strip()

    if start not in graph.locations or goal not in graph.locations:
        return None, None

    if start == goal:
        return [start], 0

    # Priority queue entries:
    # (total_cost, node)
    priority_queue = [(0, start)]

    # Cheapest known cost from start to each node.
    costs: Dict[str, float] = {start: 0}

    # Used to reconstruct the final route.
    parent: Dict[str, Optional[str]] = {start: None}

    while priority_queue:
        current_cost, current = heapq.heappop(priority_queue)

        # Ignore an outdated queue entry.
        if current_cost > costs[current]:
            continue

        # UCS can stop when the goal is removed
        # from the priority queue with its cheapest cost.
        if current == goal:
            path = _build_path(parent, goal)
            return path, current_cost

        for neighbor, edge_cost in graph.get_weighted_neighbors(current):
            new_cost = current_cost + edge_cost

            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                parent[neighbor] = current

                heapq.heappush(
                    priority_queue,
                    (new_cost, neighbor),
                )

    return None, None


def _build_path(
    parent: Dict[str, Optional[str]],
    goal: str,
) -> List[str]:
    """Reconstruct the path from the parent map."""

    path = []
    current: Optional[str] = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path
