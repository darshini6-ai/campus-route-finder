import streamlit as st

from python_src.campus_graph import CampusGraph
from python_src.bfs import find_shortest_path


st.set_page_config(
    page_title="Campus Route Finder",
    page_icon="🧭",
    layout="wide"
)


def build_campus_graph():
    graph = CampusGraph()

    locations = [
        "Main Gate",
        "Library",
        "CSE Block",
        "AI Lab",
        "Canteen",
        "Admin Block",
        "Auditorium",
        "Hostel",
        "Medical Center"
    ]

    for location in locations:
        graph.add_location(location)

    connections = [
        ("Main Gate", "Library"),
        ("Main Gate", "Canteen"),
        ("Library", "CSE Block"),
        ("CSE Block", "AI Lab"),
        ("AI Lab", "Auditorium"),
        ("Canteen", "Admin Block"),
        ("Admin Block", "Auditorium"),
        ("Auditorium", "Hostel")
    ]

    for first, second in connections:
        graph.add_connection(first, second)

    return graph


graph = build_campus_graph()
locations = graph.get_locations()

st.title("🧭 Campus Route Finder")
st.subheader("BFS Shortest Path Navigation")

st.write(
    "Find the shortest route between two campus locations "
    "using Breadth-First Search (BFS)."
)

col1, col2 = st.columns(2)

with col1:
    start = st.selectbox(
        "Starting Location",
        locations,
        index=locations.index("Main Gate")
    )

with col2:
    destination = st.selectbox(
        "Destination",
        locations,
        index=locations.index("Auditorium")
    )

if st.button("Find Shortest Route", type="primary"):
    path = find_shortest_path(graph, start, destination)

    if path:
        hop_count = len(path) - 1

        st.success("Route found!")

        st.write("### Shortest Route")
        st.write(" → ".join(path))

        st.metric("Hop Count", hop_count)

        st.write("### Route Steps")

        for index, location in enumerate(path, start=1):
            st.write(f"{index}. {location}")

    else:
        st.error("No route found between the selected locations.")

st.divider()

st.caption(
    "Campus Route Finder - Streamlit Dashboard"
)
