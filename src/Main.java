import java.util.Collection;
import java.util.List;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        System.out.println("========================================");
        System.out.println("          CAMPUS ROUTE FINDER");
        System.out.println("          BFS Shortest Path");
        System.out.println("========================================");     

        CampusGraph graph = new CampusGraph();

        // Add campus locations
        graph.addLocation("Main Gate");
        graph.addLocation("Library");
        graph.addLocation("CSE Block");
        graph.addLocation("AI Lab");
        graph.addLocation("Canteen");
        graph.addLocation("Admin Block");
        graph.addLocation("Auditorium");
        graph.addLocation("Hostel");
        graph.addLocation("Medical Center");

        // Add connections between locations
        graph.addConnection("Main Gate", "Library");
        graph.addConnection("Main Gate", "Canteen");

        graph.addConnection("Library", "CSE Block");
        graph.addConnection("CSE Block", "AI Lab");
        graph.addConnection("AI Lab", "Auditorium");

        graph.addConnection("Canteen","Admin Block");
        graph.addConnection("Admin Block","Auditorium");

        graph.addConnection("Auditorium", "Hostel");

        System.out.println("\nCampus graph created successfully.");
        System.out.println("\nAvailable Locations:");

        Collection<Location> locations = graph.getAllLocations();

        for (Location location : locations) {
            System.out.println("- " + location.getName());
        }

        System.out.println();

        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter start location: ");
        String startName = scanner.nextLine();

        System.out.print("Enter destination: ");
        String targetName = scanner.nextLine();

        Location start = graph.getLocation(startName);
        Location target = graph.getLocation(targetName);

        if (start == null || target == null) {
            System.out.println("\nInvalid location.");
            scanner.close();
            return;
        }

        BFS bfs = new BFS();

        List<Location> path = bfs.findShortestPath(start, target);

        if (path.isEmpty()) {
            System.out.println("No route found.");
        } else {
            System.out.println("\nShortest Route:");

            for (int i = 0; i < path.size(); i++) {
                System.out.println("[" + path.get(i).getName() + "]");

                if (i < path.size() - 1) {
                    System.out.println("     |");
                    System.out.println("     ↓");
                }
            }

            // Number of edges = number of locations - 1
            int hopCount = path.size() - 1;

            System.out.println("\nHop Count: " + hopCount);
        }

        scanner.close();
    }
}

