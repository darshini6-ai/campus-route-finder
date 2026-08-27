import java.util.ArrayList;
import java.util.List;

public class Location {

    private String name;
    private List<Location> neighbors;

    public Location(String name) {
        this.name = name;
        this.neighbors = new ArrayList<>();
    }

    public String getName() {
        return name;
    }

    public List<Location> getNeighbors() {
        return neighbors;
    }

    public void addNeighbor(Location location) {
        neighbors.add(location);
    }
}
