# Campus Route Finder using BFS

A Java-based campus route finder that uses Breadth-First Search (BFS) to find the shortest route between two campus locations in an unweighted graph.

## 1. Problem Statement

A campus can be represented as a graph.

- Each campus location is a vertex.
- Each connection between two locations is an edge.
- Every connection represents one hop.
- All connections have equal cost.

The goal is to find the route with the minimum number of hops between a starting location and a destination.

## 2. Why BFS?

Breadth-First Search is suitable because the campus graph is unweighted.

BFS explores the graph level by level.

- Level 0: starting location
- Level 1: locations one hop away
- Level 2: locations two hops away
- Level 3: locations three hops away

Therefore, when BFS first reaches the destination, it has found a path with the minimum possible number of edges.

For example, there are two possible routes from Main Gate to Auditorium.

```text
Route 1:
Main Gate -> Library -> CSE Block -> AI Lab -> Auditorium

Hop count: 4

Route 2:
Main Gate -> Canteen -> Admin Block -> Auditorium

Hop count: 3
```

BFS selects Route 2 because it contains fewer edges.

## 3. Features

- Represents campus locations as graph vertices.
- Represents connections as undirected edges.
- Uses Breadth-First Search.
- Finds the shortest route.
- Displays the route visually.
- Displays the hop count.
- Accepts user input.
- Supports case-insensitive location names.
- Handles invalid locations.
- Handles the same start and destination.
- Handles destinations with no available route.
- Includes BFS test cases.

## 4. Campus Locations

The project contains:

- Main Gate
- Library
- CSE Block
- AI Lab
- Canteen
- Admin Block
- Auditorium
- Hostel
- Medical Center

The Medical Center is intentionally isolated for testing the no-route condition.

## 5. Graph Connections


The graph contains these connections:

```text
Main Gate — Library
Main Gate — Canteen
Library — CSE Block
CSE Block — AI Lab
AI Lab — Auditorium
Canteen — Admin Block
Admin Block — Auditorium
Auditorium — Hostel
```text
All connections are bidirectional.

## 6. Object-Oriented Design

### Location

Represents an individual campus location.

It stores the location name and its neighboring locations.

### CampusGraph

Manages the campus graph.

It provides methods for:

- Adding locations
- Finding locations
- Adding connections
- Retrieving all locations

### BFS

Implements the Breadth-First Search algorithm.

It uses:

- Queue
- Visited set
- Parent map

The parent map is used to reconstruct the shortest route.

### Main

Provides the command-line interface.

It:

1. Creates the campus graph.
2. Displays available locations.
3. Accepts the start location.
4. Accepts the destination.
5. Runs BFS.
6. Displays the shortest route.
7. Displays the hop count.

## 7. BFS Algorithm

The algorithm works as follows:

1. Add the starting location to a queue.
2. Mark it as visited.
3. Set its parent to null.
4. Remove a location from the queue.
5. Check its neighboring locations.
6. If a neighbor has not been visited:
   - Mark it as visited.
   - Store its parent.
   - Add it to the queue.
7. Continue until the destination is reached or the queue becomes empty.
8. Reconstruct the route using the parent map.
9. Reverse the route.
10. Calculate the hop count.

Hop Count = Number of locations in the path - 1

## 8. Why BFS Gives the Fewest-Edge Path

In an unweighted graph, every edge represents one hop.

BFS explores all locations at distance 1 before locations at distance 2, and all locations at distance 2 before locations at distance 3.

Therefore, when the destination is first reached, all shorter paths have already been considered.

This guarantees that BFS finds a path containing the minimum number of edges.

## 9. Complexity Analysis

For a graph containing V vertices and E edges:

Time Complexity: O(V + E)

Space Complexity: O(V)

BFS visits each vertex and edge at most a constant number of times.

The queue, visited set, and parent map require space proportional to the number of vertices.

## 10. Example Execution

Input:

Enter start location: Main Gate

Enter destination: Auditorium

Output:

Shortest Route:

[Main Gate]
     |
     ↓
[Canteen]
     |
     ↓
[Admin Block]
     |
     ↓
[Auditorium]

Hop Count: 3

## 11. Test Cases

The project includes five test cases.

1. Main Gate -> Auditorium
   Expected: 3 hops

2. Main Gate -> Main Gate
   Expected: 0 hops

3. Auditorium -> Main Gate
   Expected: 3 hops

4. Main Gate -> Hostel
   Expected: 4 hops

5. Main Gate -> Medical Center
   Expected: No route

All current BFS tests pass.

## 12. How to Run

Requirements:

- JDK 17 or later
- Terminal
- No external libraries

Compile the application:

javac -d out src/*.java

Run the application:

java -cp out Main

Compile the tests:

javac -d out src/*.java tests/BFSTest.java

Run the tests:

java -cp out BFSTest

## 13. Project Structure

campus-route-finder/

src/
    Main.java
    Location.java
    CampusGraph.java
    BFS.java

tests/
    BFSTest.java

docs/

README.md
dependencies.txt
.gitignore
LICENSE

## 14. Limitations

This project uses an unweighted graph.

Therefore:

- Every connection is treated as one hop.
- Physical distance is not considered.
- Walking time is not considered.
- Traffic is not considered.
- Accessibility conditions are not considered.
- The graph is manually defined in the source code.
- The application currently uses a command-line interface.

A future version could use weighted graphs and Dijkstra's algorithm to consider actual distances or travel times.

## 15. Technologies

- Java
- Object-Oriented Programming
- Graph Data Structures
- Breadth-First Search
- Git
- GitHub

## 16. Academic Objective

This project demonstrates the practical application of Breadth-First Search to a real-world campus navigation problem.

The project specifically demonstrates why BFS produces the minimum-edge path when all graph edges have equal weight.

## 17. Author

Darshini

B.E. Computer Science and Engineering
Specialization: Artificial Intelligence and Machine Learning
