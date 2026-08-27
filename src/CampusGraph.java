import java.util.HashMap;
import java.util.Map;

public class CampusGraph {

    private Map<String, Location> locations;

    public CampusGraph() {
        locations = new HashMap<>();
    }

    public void addLocation(String name) {
        locations.put(name, new Location(name));
    }

    public Location getLocation(String name) {
        return locations.get(name);
    }

    public void addConnection(String location1, String location2) {

        Location first = locations.get(location1);
        Location second = locations.get(location2);

        first.addNeighbor(second);
        second.addNeighbor(first);
    }
}
