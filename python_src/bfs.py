from collections import deque


def find_shortest_path(graph, start, target):
    if start not in graph.graph or target not in graph.graph:
        return []

    queue = deque([start])
    visited = {start}
    parent = {start: None}

    while queue:
        current = queue.popleft()

        if current == target:
            break

        for neighbor in graph.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    if target not in parent:
        return []

    path = []
    current = target

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    return path
