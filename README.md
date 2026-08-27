# Campus Route Finder using BFS

A Java-based campus route finder that uses **Breadth-First Search (BFS)** to find the shortest route between two campus locations in an unweighted graph.

## 1. Problem Statement

A campus can be represented as a graph in which:

- Each campus location is a vertex.
- Each connection between two locations is an edge.
- Every edge represents one hop between locations.
- All connections have equal cost.

The goal of this project is to find the route containing the **minimum number of hops** between a given starting location and destination.

## 2. Why BFS?

Breadth-First Search (BFS) is suitable for this problem because the campus graph is **unweighted**.

BFS explores vertices level by level:

- Level 0 contains the starting location.
- Level 1 contains locations one hop away.
- Level 2 contains locations two hops away.
- And so on.

Therefore, the first time BFS reaches the destination, it has reached it using the minimum possible number of edges.

For example, the campus graph contains two possible routes from Main Gate to Auditorium:

```text
Route 1:
Main Gate → Library → CSE Block → AI Lab → Auditorium
4 hops

Route 2:
Main Gate → Canteen → Admin Block → Auditorium
3 hops
## 3. Features

- Represents campus locations as graph vertices.
- Represents campus connections as undirected edges.
- Uses Breadth-First Search to find the shortest path.
- Accepts the starting location and destination from the user.
- Displays the shortest route.
- Displays the hop count.
- Supports case-insensitive location input.
- Handles invalid locations.
- Handles the case where the start and destination are the same.
- Handles situations where no route exists.
- Includes BFS test cases.

## 4. Campus Locations

The application contains the following campus locations:

- Main Gate
- Library
- CSE Block
- AI Lab
- Canteen
- Admin Block
- Auditorium
- Hostel
- Medical Center

The Medical Center is intentionally isolated so that the test suite can verify the no-route condition.

## 5. Graph Connections

The campus graph contains these connections:

```text
Main Gate — Library
Main Gate — Canteen

Library — CSE Block
CSE Block — AI Lab
AI Lab — Auditorium

Canteen — Admin Block
Admin Block — Auditorium

Auditorium — Hostel
All connections are bidirectional.

## 6. Object-Oriented Design

The project is divided into separate Java classes.

### `Location`

Represents a campus location.

It stores:

- Location name
- List of neighboring locations

### `CampusGraph`

Manages the campus graph.

It provides methods to:

- Add locations
- Find locations
- Add connections
- Retrieve all locations

### `BFS`

Implements the Breadth-First Search algorithm.

It uses:

- A queue to explore locations
- A visited set to avoid repeated visits
- A parent map to reconstruct the shortest path

### `Main`

Provides the command-line interface.

It:

1. Creates the campus graph.
2. Displays available locations.
3. Accepts the start and destination locations.
4. Runs BFS.
5. Displays the shortest route and hop count.

## 7. BFS Algorithm

The BFS algorithm follows these steps:

1. Add the starting location to a queue.
2. Mark the starting location as visited.
3. Store its parent as `null`.
4. Remove a location from the front of the queue.
5. Examine each neighboring location.
6. If a neighbor has not been visited:
   - Mark it as visited.
   - Store the current location as its parent.
   - Add it to the queue.
7. Continue until the destination is reached or the queue becomes empty.
8. Reconstruct the route using the parent map.
9. Reverse the reconstructed route to obtain the path from start to destination.
10. Calculate the hop count.

```text
Hop Count = Number of locations in the path - 1
```
## 9. Complexity Analysis

For a graph containing:

- `V` vertices
- `E` edges

the BFS traversal has:

```text
Time Complexity:  O(V + E)
Space Complexity: O(V)
## 10. Example Execution

### Input

```text
Enter start location: Main Gate
Enter destination: Auditorium
