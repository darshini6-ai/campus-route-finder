import java.util.List;
public class BFSTest {

    public static void main(String[] args) {

        CampusGraph graph = new CampusGraph();

        // Add locations
        graph.addLocation("Main Gate");
        graph.addLocation("Library");
        graph.addLocation("CSE Block");
        graph.addLocation("AI Lab");
        graph.addLocation("Canteen");
        graph.addLocation("Admin Block");
        graph.addLocation("Auditorium");
        graph.addLocation("Hostel");
        graph.addLocation("Medical Center");

        // Add connections
        graph.addConnection("Main Gate", "Library");
        graph.addConnection("Main Gate", "Canteen");

        graph.addConnection("Library", "CSE Block");
        graph.addConnection("CSE Block", "AI Lab");
        graph.addConnection("AI Lab", "Auditorium");

        graph.addConnection("Canteen", "Admin Block");
        graph.addConnection("Admin Block", "Auditorium");
        
        graph.addConnection("Auditorium", "Hostel");

        BFS bfs = new BFS();

        // Test 1: Shortest path
        testShortestPath(
                bfs,
                graph.getLocation("Main Gate"),
                graph.getLocation("Auditorium"),
                3
        );

        // Test 2: Same start and destination
        testShortestPath(
                bfs,
                graph.getLocation("Main Gate"),
                graph.getLocation("Main Gate"),
                0
        );

        // Test 3: Reverse direction
        testShortestPath(
                bfs,
                graph.getLocation("Auditorium"),
                graph.getLocation("Main Gate"),
                3
        );

        // Test 4: Hostel route
        testShortestPath(
                bfs,
                graph.getLocation("Main Gate"),
                graph.getLocation("Hostel"),
                4
        );

        // Test 5: No route
        testNoRoute(
                bfs,
                graph.getLocation("Main Gate"),
                graph.getLocation("Medical Center")
        );

        System.out.println("\nAll BFS tests completed.");
    }

    private static void testShortestPath(
            BFS bfs,
            Location start,
            Location target,
            int expectedHops) {

        List<Location> path = bfs.findShortestPath(start, target);

        int actualHops = path.size() - 1;

        if (actualHops == expectedHops) {
            System.out.println("PASS: "
                    + start.getName()
                    + " -> "
                    + target.getName()
                    + " | Hops = "
                    + actualHops);
        } else {
            System.out.println("FAIL: "
                    + start.getName()
                    + " -> "
                    + target.getName()
                    + " | Expected = "
                    + expectedHops
                    + ", Actual = "
                    + actualHops);
        }
    }

    private static void testNoRoute(
            BFS bfs,
            Location start,
            Location target) {

        List<Location> path = bfs.findShortestPath(start, target);

        if (path.isEmpty()) {
            System.out.println("PASS: "
                    + start.getName()
                    + " -> "
                    + target.getName()
                    + " | No route found");
        } else {
            System.out.println("FAIL: "
                    + start.getName()
                    + " -> "
                    + target.getName()
                    + " | Expected no route");
        }
    }
}
 
   
                
        

       
        
                
                
              
      
