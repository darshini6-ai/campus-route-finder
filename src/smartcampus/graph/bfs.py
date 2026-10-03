from collections import deque


def bfs_shortest_path(graph, start, goal):
    """
    Find a shortest path from start to goal using BFS.

    Because this is an unweighted graph, BFS returns
    a path containing the minimum number of edges.
    """

    if not graph.has_location(start):
        return None

    if not graph.has_location(goal):
        return None

    if start == goal:
        return [start]

    queue = deque([start])

    visited = {start}

    parent = {
        start: None
    }

    while queue:

        current = queue.popleft()

        if current == goal:
            break

        for neighbor in graph.get_neighbors(current):

            if neighbor not in visited:

                visited.add(neighbor)

                parent[neighbor] = current

                queue.append(neighbor)

    if goal not in parent:
        return None

    return build_path(parent, goal)


def build_path(parent, goal):
    """Reconstruct the path using the parent dictionary."""

    path = []

    current = goal

    while current is not None:

        path.append(current)

        current = parent[current]

    path.reverse()

    return path


def count_hops(path):
    """Return the number of edges in a path."""

    if path is None:
        return None

    return len(path) - 1
