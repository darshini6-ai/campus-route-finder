import java.util.HashMap;
import java.util.Map;
import java.util.Collection;

public class CampusGraph {

    private Map<String, Location> locations;

    public CampusGraph() {
        locations = new HashMap<>();
    }

    public void addLocation(String name) {
        locations.put(name.toLowerCase(), new Location(name));
    }

    public Location getLocation(String name) {
        if (name == null) {
            return null;
        }

        return locations.get(name.toLowerCase());
    }

    public void addConnection(String location1, String location2) {

        Location first = getLocation(location1);
        Location second = getLocation(location2);

        if (first == null || second == null) {
            return;
        }

        first.addNeighbor(second);
        second.addNeighbor(first);
    }
    
    public Collection<Location> getAllLocations() {
        return locations.values();
    }
}
