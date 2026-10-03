import heapq
from typing import Dict, List, Optional, Tuple

from .campus_graph import CampusGraph


def astar_search(
    graph: CampusGraph,
    start: str,
    goal: str,
    heuristic: Dict[str, float],
) -> Tuple[Optional[List[str]], Optional[float]]:
    """
    Find a minimum-cost path using A* Search.

    f(n) = g(n) + h(n)

    g(n): cost from start to current node
    h(n): estimated cost from current node to goal

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
    # (f_cost, g_cost, node)
    priority_queue = [
        (heuristic.get(start, 0), 0, start)
    ]

    # Cheapest known cost from start to each node.
    costs: Dict[str, float] = {start: 0}

    # Used to reconstruct the final route.
    parent: Dict[str, Optional[str]] = {start: None}

    while priority_queue:
        _, current_cost, current = heapq.heappop(priority_queue)

        # Ignore an outdated queue entry.
        if current_cost > costs[current]:
            continue

        if current == goal:
            path = _build_path(parent, goal)
            return path, current_cost

        for neighbor, edge_cost in graph.get_weighted_neighbors(current):
            new_cost = current_cost + edge_cost

            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                parent[neighbor] = current

                estimated_cost = (
                    new_cost + heuristic.get(neighbor, 0)
                )

                heapq.heappush(
                    priority_queue,
                    (estimated_cost, new_cost, neighbor),
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
