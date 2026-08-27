import java.util.List;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        System.out.println("Campus Route Finder");
        System.out.println("--------------------");

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

        // Add connections between locations
        graph.addConnection("Main Gate", "Library");
        graph.addConnection("Main Gate", "Canteen");

        graph.addConnection("Library", "CSE Block");
        graph.addConnection("CSE Block", "AI Lab");
        graph.addConnection("AI Lab", "Auditorium");

        graph.addConnection("Canteen","Admin Block");
        graph.addConnection("Admin Block","Auditorium");

        graph.addConnection("Auditorium", "Hostel");

        System.out.println("Campus graph created successfully.");

        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter start location: ");
        String startName = scanner.nextLine();

        System.out.print("Enter destination: ");
        String targetName = scanner.nextLine();

        Location start = graph.getLocation(startName);
        Location target = graph.getLocation(targetName);

        if (start == null || target == null) {
            System.out.println("Invalid location.");
            return;
        }

        BFS bfs = new BFS();

        List<Location> path = bfs.findShortestPath(start, target);

        if (path.isEmpty()) {
            System.out.println("No route found.");
        } else {
            System.out.println("\nShortest Route:");

            for (int i = 0; i < path.size(); i++) {
                System.out.print(path.get(i).getName());

                if (i < path.size() - 1) {
                    System.out.print(" -> ");
                }
            }

            int hopCount = path.size() - 1;

            System.out.println("\nHop Count: " + hopCount);
        }

        scanner.close();
    }
}
