import java.util.*;

public class BFS {

    public List<Location> findShortestPath(Location start, Location target) {

        Queue<Location> queue = new LinkedList<>();
        Set<Location> visited = new HashSet<>();
        Map<Location, Location> parent = new HashMap<>();

        queue.add(start);
        visited.add(start);
        parent.put(start, null);

        while (!queue.isEmpty()) {

            Location current = queue.remove();

            if (current == target) {
                break;
            }

            for (Location neighbor : current.getNeighbors()) {

                if (!visited.contains(neighbor)) {

                    visited.add(neighbor);
                    parent.put(neighbor, current);
                    queue.add(neighbor);
                }
            }
        }

        return buildPath(parent, start, target);
    }

    private List<Location> buildPath(
            Map<Location, Location> parent,
            Location start,
            Location target) {

        List<Location> path = new ArrayList<>();

        Location current = target;

        while (current != null) {
            path.add(current);
            current = parent.get(current);
        }

        Collections.reverse(path);

        if (path.isEmpty() || path.get(0) != start) {
            return new ArrayList<>();
        }

        return path;
    }
}
