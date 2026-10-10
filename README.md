# Campus Route Finder — Smart Campus AI System

An AI-based campus navigation and planning project that combines graph search, constraint satisfaction, knowledge-based reasoning, and a Streamlit dashboard.

The project preserves the original Java BFS implementation and extends it with Python-based interactive navigation and smart campus planning features.

## 1. Project Objectives

- Find the shortest-hop route between campus locations using Breadth-First Search (BFS).
- Compare unweighted BFS routes with cost-aware Uniform Cost Search (UCS) and A* search.
- Generate campus timetables using backtracking and constraint propagation with AC-3.
- Demonstrate rule-based knowledge reasoning for finding suitable campus facilities.
- Visualize routes and AI results through a Streamlit dashboard.

## 2. Technologies

- Java and object-oriented programming
- Python
- Streamlit
- Graph search: BFS, UCS, and A*
- Constraint satisfaction: backtracking and AC-3
- Rule-based knowledge representation
- Git and GitHub
- pytest for Python tests

## 3. Features

### Campus Route Finding

Campus locations are represented as graph vertices, and connections are represented as edges. BFS finds a route with the minimum number of edges when all connections have equal cost.

### Smart Navigation

UCS and A* support cost-aware routing. The smart navigation module can model blocked connections and estimated congestion costs to compare routes under different scenarios.

Congestion values are illustrative estimates, not measured live traffic data.

### Timetable Constraint Satisfaction

The timetable module uses backtracking and AC-3 constraint propagation to help generate schedules while checking the implemented room, faculty, batch, and other scheduling constraints.

### Knowledge-Based Reasoning

A rule-based campus knowledge module stores facility properties and uses graph distances to identify suitable nearby facilities. Results depend on the facts and rules defined in the project.

### Interactive Dashboard

The Streamlit application provides a visual interface for route finding and the implemented AI demonstrations.

## 4. Campus Graph

The current campus graph includes:

- Main Gate
- Library
- CSE Block
- AI Lab
- Canteen
- Admin Block
- Auditorium
- Hostel
- Medical Center

The main graph connections are:

- Main Gate — Library
- Main Gate — Canteen
- Library — CSE Block
- CSE Block — AI Lab
- AI Lab — Auditorium
- Canteen — Admin Block
- Admin Block — Auditorium
- Auditorium — Hostel

The Medical Center is isolated in the route-finding graph to demonstrate the no-route condition.

## 5. Repository Structure

```text
campus-route-finder/
├── app.py
├── python_src/
├── src/
├── tests/
├── docs/
│   ├── Campus Route Finder (IA-2).pdf
│   └── report.pdf
├── requirements.txt
├── dependencies.txt
├── pytest.ini
├── README.md
└── LICENSE
```

The Java source files are retained in `src/`. The Python AI modules are in `python_src/`, and the Streamlit interface is in `app.py`.

## 6. Setup and Run

### Requirements

- Python installed
- Git
- Internet access for the initial dependency installation

### Install Python dependencies

From the repository root, run:

```bash
python3 -m pip install -r requirements.txt
```

### Launch the Streamlit dashboard

```bash
python3 -m streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser.

### Run the Python tests

```bash
python3 -m pytest -v
```

### Run the original Java application

If JDK 17 or later is installed, compile and run the Java version:

```bash
javac -d out src/*.java
java -cp out Main
```

## 7. Algorithm Overview

| Algorithm | Purpose |
|---|---|
| BFS | Finds minimum-hop paths in an unweighted graph |
| UCS | Finds minimum-cost paths with non-negative edge costs |
| A* | Uses path cost and a heuristic to guide cost-aware search |
| Backtracking | Searches for valid timetable assignments |
| AC-3 | Propagates constraint restrictions to reduce possible assignments |
| Rule-based reasoning | Uses stored facts and rules to identify suitable facilities |

## 8. Complexity

For a graph with \(V\) vertices and \(E\) edges, BFS takes \(O(V+E)\) time and \(O(V)\) auxiliary space when using an adjacency-list representation.

UCS and A* performance depends on the graph, edge costs, and heuristic. Backtracking timetable search can be exponential in the number of variables in the worst case. AC-3 reduces domains through constraint propagation, but does not eliminate the worst-case complexity of the full CSP search.

## 9. Testing and Evaluation

The repository includes Python tests for the implemented graph search, navigation, timetable, and knowledge modules.

Run:

```bash
python3 -m pytest -v
```

Use the actual test output and dashboard screenshots in the report when presenting results. Congestion experiments use estimated scenario costs; they should not be described as real-world traffic measurements.

## 10. Limitations and Future Improvements

- Campus connections and facility facts are manually defined.
- Congestion costs are illustrative rather than live measurements.
- Accessibility information must be verified against the actual campus.
- A* performance depends on the quality and validity of its heuristic.
- Timetable results depend on the constraints and domains encoded in the program.

Future work could include verified campus accessibility data, real walking distances, live congestion information, a larger timetable dataset, and additional evaluation across more scenarios.

## 11. Academic Integrity

This project demonstrates the algorithms and implementation included in the repository. Reported performance should be based on actual program runs and tests. Any AI assistance or external sources should be disclosed according to the course requirements.

## 12. Author

Darshini S.  
B.E. Computer Science and Engineering  
Specialization: Artificial Intelligence and Machine Learning

