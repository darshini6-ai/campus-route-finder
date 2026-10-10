"""Congestion-aware campus navigation using UCS and A*."""

import heapq
import itertools
from collections import deque


def _edge_key(first, second):
    """Represent an undirected connection consistently."""
    return tuple(sorted((first, second)))


def _edge_is_blocked(first, second, blocked_edges):
    return _edge_key(first, second) in {
        _edge_key(a, b) for a, b in blocked_edges
    }


def _edge_cost(first, second, edge_costs):
    """Get the travel cost for an edge, defaulting to one."""
    for (a, b), cost in edge_costs.items():
        if _edge_key(a, b) == _edge_key(first, second):
            if cost <= 0:
                raise ValueError("Edge travel costs must be positive.")
            return float(cost)
    return 1.0


def _hop_heuristic(graph, current, goal, blocked_edges, min_cost):
    """
    Estimate remaining cost using unweighted hop distance.

    Multiplying the minimum available edge cost by the fewest remaining
    hops gives an admissible heuristic for A*.
    """
    queue = deque([(current, 0)])
    visited = {current}

    while queue:
        location, hops = queue.popleft()

        if location == goal:
            return hops * min_cost

        for neighbor in graph.get_neighbors(location):
            if neighbor in visited:
                continue
            if _edge_is_blocked(location, neighbor, blocked_edges):
                continue

            visited.add(neighbor)
            queue.append((neighbor, hops + 1))

    return 0.0


def _search(graph, start, goal, edge_costs, blocked_edges, use_astar):
    """Shared implementation for UCS and A*."""
    if start not in graph.graph or goal not in graph.graph:
        return None

    if start == goal:
        return {"path": [start], "cost": 0.0, "nodes_checked": 0}

    blocked = {_edge_key(a, b) for a, b in blocked_edges}
    available_costs = [
        float(cost)
        for (a, b), cost in edge_costs.items()
        if _edge_key(a, b) not in blocked
    ]

    if any(cost <= 0 for cost in available_costs):
        raise ValueError("Edge travel costs must be positive.")

    min_cost = min(available_costs, default=1.0)
    counter = itertools.count()
    initial_h = (
        _hop_heuristic(graph, start, goal, blocked_edges, min_cost)
        if use_astar else 0.0
    )

    frontier = [(initial_h, 0.0, next(counter), start)]
    best_cost = {start: 0.0}
    parent = {}
    nodes_checked = 0

    while frontier:
        _, cost_so_far, _, current = heapq.heappop(frontier)

        if cost_so_far != best_cost.get(current):
            continue

        nodes_checked += 1

        if current == goal:
            path = [goal]
            while path[-1] != start:
                path.append(parent[path[-1]])
            path.reverse()

            return {
                "path": path,
                "cost": cost_so_far,
                "nodes_checked": nodes_checked,
            }

        for neighbor in graph.get_neighbors(current):
            if _edge_key(current, neighbor) in blocked:
                continue

            new_cost = cost_so_far + _edge_cost(
                current, neighbor, edge_costs
            )

            if new_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = new_cost
                parent[neighbor] = current

                heuristic = (
                    _hop_heuristic(
                        graph, neighbor, goal, blocked_edges, min_cost
                    )
                    if use_astar else 0.0
                )

                heapq.heappush(
                    frontier,
                    (
                        new_cost + heuristic,
                        new_cost,
                        next(counter),
                        neighbor,
                    ),
                )

    return None


def uniform_cost_search(
    graph, start, goal, edge_costs=None, blocked_edges=None
):
    """Return the minimum-cost route, or None if unreachable."""
    return _search(
        graph, start, goal,
        edge_costs or {},
        blocked_edges or set(),
        use_astar=False,
    )


def a_star_search(
    graph, start, goal, edge_costs=None, blocked_edges=None
):
    """Return an A* minimum-cost route, or None if unreachable."""
    return _search(
        graph, start, goal,
        edge_costs or {},
        blocked_edges or set(),
        use_astar=True,
    )
