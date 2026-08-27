public class Main {

    public static void main(String[] args) {

        System.out.println("Campus Route Finder");

        CampusGraph graph = new CampusGraph();

        graph.addLocation("Main Gate");
        graph.addLocation("Library");
        graph.addLocation("CSE Block");
        graph.addLocation("Canteen");
        graph.addLocation("Auditorium");

        graph.addConnection("Main Gate", "Library");
        graph.addConnection("Main Gate", "Canteen");
        graph.addConnection("Library", "CSE Block");
        graph.addConnection("CSE Block", "Auditorium");

        System.out.println("Campus graph created successfully.");
    }
}
