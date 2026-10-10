import html
import streamlit as st
import streamlit.components.v1 as components

from python_src.campus_graph import CampusGraph
from python_src.bfs import find_shortest_path
from python_src.csp.timetable_csp import TimetableCSP
from python_src.csp.timetable_data import CLASSES, ROOMS, TIME_SLOTS, MAX_HOPS
from python_src.campus_knowledge import nearest_accessible_lab_with_projector
from python_src.smart_navigation import uniform_cost_search, a_star_search


st.set_page_config(
    page_title="Campus Route Finder",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ---------------------------------------------------------
# Campus data
# ---------------------------------------------------------

LOCATIONS = [
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

CONNECTIONS = [
    ("Main Gate", "Library"),
    ("Main Gate", "Canteen"),
    ("Library", "CSE Block"),
    ("CSE Block", "AI Lab"),
    ("AI Lab", "Auditorium"),
    ("Canteen", "Admin Block"),
    ("Admin Block", "Auditorium"),
    ("Auditorium", "Hostel")
]


MAP_POSITIONS = {
    "Main Gate": (90, 330),
    "Library": (250, 210),
    "CSE Block": (400, 120),
    "AI Lab": (560, 120),
    "Canteen": (250, 350),
    "Admin Block": (440, 300),
    "Auditorium": (610, 270),
    "Hostel": (770, 350),
    "Medical Center": (760, 120)
}


def build_campus_graph():
    graph = CampusGraph()

    for location in LOCATIONS:
        graph.add_location(location)

    for first, second in CONNECTIONS:
        graph.add_connection(first, second)

    return graph


graph = build_campus_graph()


# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    .crf-brand {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 4px;
    }

    .crf-logo {
        width: 42px;
        height: 42px;
        border: 1px solid #d8ded9;
        border-radius: 10px;
        background: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 23px;
    }

    .crf-brand-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #132238;
        letter-spacing: -0.2px;
    }

    .crf-nav {
        margin: 4px 0 28px 56px;
        display: flex;
        gap: 24px;
    }

    .crf-nav a {
        color: #64748b;
        text-decoration: none;
        font-size: 0.9rem;
    }

    .crf-nav a:hover {
        color: #1f6f54;
    }

    .crf-hero {
        border-bottom: 1px solid #e4e8e5;
        padding: 12px 0 28px 0;
        margin-bottom: 28px;
    }

    .crf-eyebrow {
        color: #1f6f54;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .crf-title {
        color: #132238;
        font-size: 2.55rem;
        font-weight: 750;
        line-height: 1.08;
        letter-spacing: -1.3px;
        margin: 0;
    }

    .crf-subtitle {
        color: #64748b;
        font-size: 1rem;
        max-width: 720px;
        line-height: 1.6;
        margin-top: 12px;
    }

    .crf-section-title {
        color: #132238;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .crf-section-text {
        color: #64748b;
        line-height: 1.5;
        margin-bottom: 18px;
    }

    .crf-panel {
        background: #ffffff;
        border: 1px solid #e1e7e3;
        border-radius: 12px;
        padding: 22px 24px 12px 24px;
        margin-bottom: 20px;
    }

    .crf-panel-label {
        color: #1f6f54;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 1.1px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .crf-panel-title {
        color: #132238;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .crf-panel-text {
        color: #64748b;
        font-size: 0.92rem;
        margin-bottom: 18px;
    }

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e1e7e3;
        border-radius: 10px;
        padding: 12px 14px;
    }

    [data-testid="stMetricLabel"] {
        color: #64748b;
    }

    [data-testid="stMetricValue"] {
        color: #132238;
    }

    .crf-result {
        border-left: 4px solid #1f6f54;
        background: #f4f8f5;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin: 18px 0;
    }

    .crf-result-title {
        color: #1b5d46;
        font-weight: 750;
        font-size: 1rem;
        margin-bottom: 4px;
    }

    .crf-result-route {
        color: #132238;
        line-height: 1.6;
    }

    .crf-timeline {
        position: relative;
        margin: 16px 0 8px 8px;
        padding-left: 28px;
    }

    .crf-timeline::before {
        content: "";
        position: absolute;
        left: 7px;
        top: 10px;
        bottom: 10px;
        width: 2px;
        background: #d8e2dc;
    }

    .crf-step {
        position: relative;
        margin-bottom: 18px;
    }

    .crf-dot {
        position: absolute;
        left: -28px;
        top: 1px;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: #ffffff;
        border: 3px solid #1f6f54;
    }

    .crf-step-number {
        color: #1f6f54;
        font-size: 0.73rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    .crf-step-name {
        color: #132238;
        font-size: 1rem;
        font-weight: 650;
        margin-top: 2px;
    }

    .crf-step-note {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 2px;
    }

    .crf-info {
        background: #ffffff;
        border: 1px solid #e1e7e3;
        border-radius: 12px;
        padding: 22px 24px;
        line-height: 1.65;
        color: #475569;
    }

    .crf-info strong {
        color: #132238;
    }

    .crf-footer {
        border-top: 1px solid #e4e8e5;
        margin-top: 32px;
        padding-top: 18px;
        color: #94a3b8;
        font-size: 0.8rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Header / navigation
# ---------------------------------------------------------

st.markdown(
    """
    <div class="crf-brand">
        <div class="crf-logo">🧭</div>
        <div class="crf-brand-name">Campus Route Finder</div>
    </div>

    <div class="crf-nav">
        <a href="#campus-map">Map</a>
        <a href="#find-route">Find Route</a>
        <a href="#about-bfs">About</a>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="crf-hero">
        <div class="crf-eyebrow">Smart Campus Navigation</div>
        <div class="crf-title">Find the shortest way around campus.</div>
        <div class="crf-subtitle">
            Explore campus locations and discover the minimum-hop route using
            Breadth-First Search on an unweighted campus graph.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Route finder
# ---------------------------------------------------------

st.markdown('<div id="find-route"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="crf-section-title">Find a route</div>
    <div class="crf-section-text">
        Select where you are and where you want to go.
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)

with col1:
    start = st.selectbox(
        "Starting location",
        LOCATIONS,
        index=LOCATIONS.index("Main Gate")
    )

with col2:
    destination = st.selectbox(
        "Destination",
        LOCATIONS,
        index=LOCATIONS.index("Auditorium")
    )


find_route = st.button(
    "Find Shortest Route",
    type="primary",
    use_container_width=False
)


if "route" not in st.session_state:
    st.session_state.route = []


if find_route:
    st.session_state.route = find_shortest_path(
        graph,
        start,
        destination
    )


path = st.session_state.route


# ---------------------------------------------------------
# Route result
# ---------------------------------------------------------

if path:

    hop_count = len(path) - 1

    st.markdown(
        f"""
        <div class="crf-result">
            <div class="crf-result-title">Route found</div>
            <div class="crf-result-route">
                {html.escape(" → ".join(path))}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    stat1, stat2, stat3, stat4 = st.columns(4)

    with stat1:
        st.metric("Locations on route", len(path))

    with stat2:
        st.metric("Campus locations", len(LOCATIONS))

    with stat3:
        st.metric("Connections", len(CONNECTIONS))

    with stat4:
        st.metric("Shortest distance", f"{hop_count} hops")


    left, right = st.columns([1, 1.25], gap="large")

    with left:

        st.markdown(
            """
            <div class="crf-panel">
                <div class="crf-panel-label">Navigation</div>
                <div class="crf-panel-title">Route timeline</div>
                <div class="crf-panel-text">
                    Follow the route step by step.
                </div>
            """,
            unsafe_allow_html=True
        )

        timeline_html = '<div class="crf-timeline">'

        for index, location in enumerate(path):
            if index == 0:
                note = "Starting point"
            elif index == len(path) - 1:
                note = "Destination"
            else:
                note = "Continue to next location"

            timeline_html += f"""
                <div class="crf-step">
                    <div class="crf-dot"></div>
                    <div class="crf-step-number">Step {index + 1}</div>
                    <div class="crf-step-name">{html.escape(location)}</div>
                    <div class="crf-step-note">{note}</div>
                </div>
            """

        timeline_html += "</div>"

        components.html(
            f"""
            <style>
                body {{
                    margin: 0;
                    font-family: Arial, sans-serif;
                    background: transparent;
                }}

                .timeline {{
                    position: relative;
                    margin: 4px 0 8px 10px;
                    padding-left: 28px;
                }}

                .timeline::before {{
                    content: "";
                    position: absolute;
                    left: 7px;
                    top: 10px;
                    bottom: 10px;
                    width: 2px;
                    background: #d8e2dc;
                }}

                .step {{
                    position: relative;
                    margin-bottom: 20px;
                }}

                .dot {{
                    position: absolute;
                    left: -28px;
                    top: 2px;
                    width: 14px;
                    height: 14px;
                    border-radius: 50%;
                    background: #ffffff;
                    border: 3px solid #1f6f54;
                }}

                .number {{
                    color: #1f6f54;
                    font-size: 11px;
                    font-weight: 700;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                }}

                .name {{
                    color: #132238;
                    font-size: 15px;
                    font-weight: 650;
                    margin-top: 3px;
                }}

                .note {{
                    color: #94a3b8;
                    font-size: 12px;
                    margin-top: 3px;
                }}
            </style>

            <div class="timeline">
                {timeline_html}
            </div>
            """,
            height=max(170, len(path) * 82),
            scrolling=False
        )


    with right:

        st.markdown(
            '<div id="campus-map"></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="crf-panel">
                <div class="crf-panel-label">Campus map</div>
                <div class="crf-panel-title">Route overview</div>
            """,
            unsafe_allow_html=True
        )

        route_edges = {
            frozenset((path[index], path[index + 1]))
            for index in range(len(path) - 1)
        }

        svg_parts = [
            """
            <svg
                width="100%"
                viewBox="0 0 860 450"
                xmlns="http://www.w3.org/2000/svg"
                style="
                    background:#fbfcfa;
                    border:1px solid #e1e7e3;
                    border-radius:10px;
                    display:block;
                "
            >
            """
        ]

        # Light campus blocks
        svg_parts.extend(
            [
                '<rect x="45" y="55" width="310" height="145" rx="8" fill="#f2f5f2"/>',
                '<rect x="390" y="55" width="200" height="145" rx="8" fill="#f2f5f2"/>',
                '<rect x="625" y="55" width="185" height="145" rx="8" fill="#f2f5f2"/>',
                '<rect x="45" y="245" width="330" height="150" rx="8" fill="#f2f5f2"/>',
                '<rect x="405" y="225" width="205" height="150" rx="8" fill="#f2f5f2"/>',
                '<rect x="640" y="260" width="175" height="135" rx="8" fill="#f2f5f2"/>'
            ]
        )

        # Base connections
        for first, second in CONNECTIONS:
            x1, y1 = MAP_POSITIONS[first]
            x2, y2 = MAP_POSITIONS[second]

            svg_parts.append(
                f"""
                <line
                    x1="{x1}" y1="{y1}"
                    x2="{x2}" y2="{y2}"
                    stroke="#c9d4ce"
                    stroke-width="4"
                    stroke-linecap="round"
                />
                """
            )

        # Highlight route connections
        for first, second in CONNECTIONS:
            if frozenset((first, second)) in route_edges:
                x1, y1 = MAP_POSITIONS[first]
                x2, y2 = MAP_POSITIONS[second]

                svg_parts.append(
                    f"""
                    <line
                        x1="{x1}" y1="{y1}"
                        x2="{x2}" y2="{y2}"
                        stroke="#1f6f54"
                        stroke-width="7"
                        stroke-linecap="round"
                    />
                    """
                )

        # Nodes
        for location in LOCATIONS:
            x, y = MAP_POSITIONS[location]
            is_route = location in path

            fill = "#1f6f54" if is_route else "#ffffff"
            stroke = "#1f6f54" if is_route else "#8da098"
            text_color = "#334155"

            svg_parts.append(
                f"""
                <circle
                    cx="{x}"
                    cy="{y}"
                    r="17"
                    fill="{fill}"
                    stroke="{stroke}"
                    stroke-width="3"
                />
                <text
                    x="{x}"
                    y="{y + 39}"
                    text-anchor="middle"
                    font-size="13"
                    font-family="Arial, sans-serif"
                    fill="{text_color if is_route else "#334155"}"
                    font-weight="{700 if is_route else 500}"
                >
                    {html.escape(location)}
                </text>
                """
            )

        svg_parts.append(
            """
            <text
                x="65"
                y="35"
                font-family="Arial, sans-serif"
                font-size="12"
                fill="#64748b"
            >
                CAMPUS PATH NETWORK
            </text>
            </svg>
            """
        )

        components.html(
            "".join(svg_parts),
            height=470
        )

        st.markdown("</div>", unsafe_allow_html=True)


else:

    if find_route:
        st.warning(
            f"No route found between {start} and {destination}."
        )
    else:
        st.info(
            "Select a starting location and destination, then choose "
            "\"Find Shortest Route\" to calculate the route."
        )

# ---------------------------------------------------------
# BFS explanation
# ---------------------------------------------------------

st.markdown(
    '<div id="about-bfs"></div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="crf-section-title">How BFS finds the route</div>
    <div class="crf-section-text">
        The route finder treats the campus as an unweighted graph.
    </div>

    <div class="crf-info">
        <strong>Breadth-First Search</strong> explores the campus
        level by level, starting from the selected location. It visits
        all locations one hop away before exploring locations two hops
        away, then three hops away, and so on.
        <br><br>
        Because every campus connection has the same cost of one hop,
        the first time BFS reaches the destination, it has found a
        path with the fewest number of edges.
        <br><br>
        <strong>Time complexity:</strong> O(V + E)
        &nbsp;&nbsp;•&nbsp;&nbsp;
        <strong>Space complexity:</strong> O(V)
    </div>

    <div class="crf-footer">
        Campus Route Finder · Phase-1 BFS extended with a Streamlit web interface
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# Smart Campus Timetable Scheduling (CSP + AC-3)
# ---------------------------------------------------------

st.markdown("---")
st.markdown(
    '<div id="timetable"></div>',
    unsafe_allow_html=True
)
st.markdown("## 📅 Smart Campus Timetable Scheduling")
st.write(
    "Generate a timetable using Constraint Satisfaction Problem (CSP) "
    "backtracking and compare it with AC-3 constraint propagation."
)

with st.spinner("Generating and validating timetables..."):
    # Solve without AC-3 propagation.
    basic_solver = TimetableCSP(
        CLASSES, ROOMS, TIME_SLOTS,
        campus_graph=graph,
        max_hops=MAX_HOPS
    )
    basic_schedule = basic_solver.solve_backtracking()
    basic_nodes = basic_solver.nodes_checked

    # Solve with AC-3 propagation.
    ac3_solver = TimetableCSP(
        CLASSES, ROOMS, TIME_SLOTS,
        campus_graph=graph,
        max_hops=MAX_HOPS
    )
    ac3_schedule = ac3_solver.solve_with_ac3()
    ac3_nodes = ac3_solver.nodes_checked_with_propagation

schedule = ac3_schedule or basic_schedule

if schedule:
    timetable_rows = []

    for class_name, (room_name, time_slot) in schedule.items():
        course = CLASSES[class_name]
        room = ROOMS[room_name]

        timetable_rows.append({
            "Time Slot": time_slot,
            "Class": class_name,
            "Batch": course["batch"],
            "Faculty": course["faculty"],
            "Room": room_name,
            "Class Type": course["type"].title(),
            "Capacity": room["capacity"],
        })

    slot_order = {slot: index for index, slot in enumerate(TIME_SLOTS)}
    timetable_rows.sort(
        key=lambda row: (
            slot_order.get(row["Time Slot"], len(TIME_SLOTS)),
            row["Class"]
        )
    )

    st.success("A valid timetable was generated.")

    st.dataframe(
        timetable_rows,
        use_container_width=True,
        hide_index=True
    )

    # Report simultaneous room, faculty, and batch clashes.
    clashes = []

    for i, first in enumerate(timetable_rows):
        for second in timetable_rows[i + 1:]:
            if first["Time Slot"] != second["Time Slot"]:
                continue

            if first["Room"] == second["Room"]:
                clashes.append(
                    f'{first["Time Slot"]}: room clash between '
                    f'{first["Class"]} and {second["Class"]}.'
                )

            if first["Faculty"] == second["Faculty"]:
                clashes.append(
                    f'{first["Time Slot"]}: faculty clash between '
                    f'{first["Class"]} and {second["Class"]}.'
                )

            if first["Batch"] == second["Batch"]:
                clashes.append(
                    f'{first["Time Slot"]}: batch clash between '
                    f'{first["Class"]} and {second["Class"]}.'
                )

    st.markdown("### 🔎 Clash Report")

    if clashes:
        for clash in clashes:
            st.error(clash)
    else:
        st.success(
            "No simultaneous room, faculty, or student-batch clashes detected."
        )

    st.caption(
        "The CSP solver also enforces room capacity, lab-only room "
        "requirements, and the configured walking-distance constraint "
        "for consecutive classes of the same batch."
    )

else:
    st.error(
        "No valid timetable was found. Review the room, class, and "
        "time-slot constraints."
    )

st.markdown("### ⚙️ Search Efficiency: Backtracking vs AC-3")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Nodes checked without AC-3",
        basic_nodes
    )

with col2:
    st.metric(
        "Nodes checked with AC-3",
        ac3_nodes
    )

if basic_schedule and ac3_schedule:
    if basic_nodes > 0:
        reduction = (basic_nodes - ac3_nodes) / basic_nodes * 100
        st.write(
            f"Change in search nodes with AC-3: **{reduction:.1f}%** "
            "(negative means AC-3 checked more nodes for this dataset)."
        )

    st.caption(
        "Node counts measure recursive search states, not total runtime. "
        "AC-3 preprocessing work is not included in the recursive-node count."
    )


# ---------------------------------------------------------
# Knowledge Base and Campus Ontology
# ---------------------------------------------------------

st.markdown("---")
st.markdown("## 🧠 Campus Knowledge Base & Reasoning")
st.write(
    "Use campus facts and BFS to infer the nearest reachable "
    "wheelchair-accessible lab equipped with a projector."
)

knowledge_start = st.selectbox(
    "Starting location for knowledge query",
    LOCATIONS,
    index=0,
    key="knowledge_start_location",
)

if st.button("Find Nearest Accessible Lab", key="find_accessible_lab"):
    knowledge_result = nearest_accessible_lab_with_projector(
        knowledge_start,
        graph,
    )

    if knowledge_result:
        st.success(
            f"Nearest matching room: {knowledge_result['room']}"
        )

        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("Building", knowledge_result["building"])
        with metric_col2:
            st.metric("Distance", f"{knowledge_result['distance_hops']} hops")

        st.markdown("### 🗺️ Inferred route")
        st.write(" → ".join(knowledge_result["path"]))

        st.markdown("### 🔍 Inference trace")
        for step_number, explanation in enumerate(
            knowledge_result["inference_trace"], start=1
        ):
            st.write(f"**Step {step_number}.** {explanation}")

        st.caption(
            "The result depends on the sample room facts in "
            "python_src/campus_knowledge.py. Verify accessibility and "
            "projector information against the real campus before use."
        )
    else:
        st.warning(
            "No reachable lab satisfies all the required conditions "
            "from this starting location."
        )


# ---------------------------------------------------------
# Smart Navigation: blocked paths and congestion
# ---------------------------------------------------------

st.markdown("---")
st.markdown("## 🚦 Smart Navigation Under Congestion")
st.write(
    "Simulate construction closures and peak-hour travel costs. "
    "Compare shortest-hop routing with cost-aware search."
)

nav_col1, nav_col2 = st.columns(2)

with nav_col1:
    nav_start = st.selectbox(
        "Navigation starting point",
        LOCATIONS,
        index=0,
        key="smart_nav_start",
    )

with nav_col2:
    nav_goal = st.selectbox(
        "Navigation destination",
        LOCATIONS,
        index=6,
        key="smart_nav_goal",
    )

edge_labels = [
    f"{first} ↔ {second}"
    for first, second in CONNECTIONS
]
edge_lookup = {
    f"{first} ↔ {second}": (first, second)
    for first, second in CONNECTIONS
}

blocked_labels = st.multiselect(
    "Simulate blocked connections (construction/closure)",
    options=edge_labels,
    default=[],
    key="smart_nav_blocked",
)

peak_hour = st.checkbox(
    "Enable peak-hour congestion costs",
    value=True,
    key="smart_nav_peak_hour",
)

# Base costs are one unit per connection.
# Higher costs represent illustrative peak-hour delays.
base_edge_costs = {
    edge: 1.0 for edge in CONNECTIONS
}

peak_edge_costs = {
    ("Main Gate", "Library"): 1.0,
    ("Main Gate", "Canteen"): 3.0,
    ("Library", "CSE Block"): 1.0,
    ("CSE Block", "AI Lab"): 1.0,
    ("AI Lab", "Auditorium"): 1.0,
    ("Canteen", "Admin Block"): 1.0,
    ("Admin Block", "Auditorium"): 1.0,
    ("Auditorium", "Hostel"): 1.0,
}

active_edge_costs = (
    peak_edge_costs if peak_hour else base_edge_costs
)
blocked_edges = {
    edge_lookup[label] for label in blocked_labels
}

if st.button("Compare Navigation Algorithms", key="compare_navigation"):
    # Build a graph containing only currently open connections.
    active_graph = CampusGraph()
    for location in LOCATIONS:
        active_graph.add_location(location)

    for first, second in CONNECTIONS:
        if (first, second) not in blocked_edges:
            active_graph.add_connection(first, second)

    # BFS minimises hops on the available, unweighted graph.
    bfs_path = find_shortest_path(
        active_graph, nav_start, nav_goal
    )

    # UCS and A* minimise the configured travel cost.
    ucs_result = uniform_cost_search(
        graph,
        nav_start,
        nav_goal,
        edge_costs=active_edge_costs,
        blocked_edges=blocked_edges,
    )
    astar_result = a_star_search(
        graph,
        nav_start,
        nav_goal,
        edge_costs=active_edge_costs,
        blocked_edges=blocked_edges,
    )

    result_cols = st.columns(3)

    with result_cols[0]:
        st.markdown("### BFS")
        if bfs_path:
            st.write(" → ".join(bfs_path))
            st.metric("Hops", len(bfs_path) - 1)
        else:
            st.warning("No available route.")

    with result_cols[1]:
        st.markdown("### UCS")
        if ucs_result:
            st.write(" → ".join(ucs_result["path"]))
            st.metric("Travel cost", f'{ucs_result["cost"]:.1f}')
            st.caption(
                f'{ucs_result["nodes_checked"]} nodes checked'
            )
        else:
            st.warning("No available route.")

    with result_cols[2]:
        st.markdown("### A*")
        if astar_result:
            st.write(" → ".join(astar_result["path"]))
            st.metric("Travel cost", f'{astar_result["cost"]:.1f}')
            st.caption(
                f'{astar_result["nodes_checked"]} nodes checked'
            )
        else:
            st.warning("No available route.")

    st.markdown("### 📝 Route explanation")

    if blocked_edges:
        st.write(
            "Blocked connections were removed from the available network: "
            + ", ".join(
                f"{first} ↔ {second}"
                for first, second in sorted(blocked_edges)
            )
            + "."
        )
    else:
        st.write("No connections are blocked in this scenario.")

    if peak_hour:
        st.write(
            "Peak-hour costs are enabled. Main Gate ↔ Canteen has an "
            "illustrative cost of 3; the other connections have cost 1."
        )
    else:
        st.write(
            "Peak-hour costs are disabled; each connection has cost 1."
        )

    if ucs_result and astar_result:
        if abs(ucs_result["cost"] - astar_result["cost"]) < 1e-9:
            st.success(
                "UCS and A* found routes with the same minimum travel cost."
            )
        else:
            st.error(
                "UCS and A* returned different costs; investigate the scenario."
            )

    st.caption(
        "These are illustrative costs, not measured travel times. "
        "BFS minimises hops, while UCS and A* minimise weighted travel cost."
    )

