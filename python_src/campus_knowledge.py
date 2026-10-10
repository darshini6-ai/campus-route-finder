"""Rule-based campus knowledge base and simple inference."""

from python_src.bfs import find_shortest_path


# Sample ontology facts for the assignment.
# Replace these example properties with verified campus information.
ROOM_FACTS = {
    "CSE Classroom": {
        "is_a": ["Room", "Classroom"],
        "building": "CSE Block",
        "has_projector": True,
        "wheelchair_accessible": True,
    },
    "Robotics Lab": {
        "is_a": ["Room", "Lab"],
        "building": "CSE Block",
        "has_projector": True,
        "wheelchair_accessible": True,
    },
    "AI Lab": {
        "is_a": ["Room", "Lab"],
        "building": "AI Lab",
        "has_projector": True,
        "wheelchair_accessible": True,
    },
    "Library Seminar Room": {
        "is_a": ["Room", "Classroom"],
        "building": "Library",
        "has_projector": True,
        "wheelchair_accessible": True,
    },
    "Auditorium": {
        "is_a": ["Room"],
        "building": "Auditorium",
        "has_projector": True,
        "wheelchair_accessible": True,
    },
}


def infer_room_type(room_name, room_type):
    """Infer whether a room belongs to a requested ontology type."""
    facts = ROOM_FACTS.get(room_name, {})
    return room_type in facts.get("is_a", [])


def nearest_accessible_lab_with_projector(start_location, campus_graph):
    """
    Find the nearest lab with a projector and wheelchair access.

    Returns a result dictionary with the route and an inference trace,
    or None when no matching room is reachable.
    """
    candidates = []

    for room_name, facts in ROOM_FACTS.items():
        if not infer_room_type(room_name, "Lab"):
            continue

        if not facts.get("has_projector", False):
            continue

        if not facts.get("wheelchair_accessible", False):
            continue

        building = facts["building"]
        path = find_shortest_path(
            campus_graph, start_location, building
        )

        if path:
            candidates.append({
                "room": room_name,
                "building": building,
                "path": path,
                "distance_hops": len(path) - 1,
                "inference_trace": [
                    f"{room_name} is a Lab.",
                    f"{room_name} has a projector.",
                    f"{room_name} is wheelchair-accessible.",
                    f"The route from {start_location} to {building} "
                    f"has {len(path) - 1} hops.",
                ],
            })

    if not candidates:
        return None

    candidates.sort(key=lambda item: item["distance_hops"])
    selected = candidates[0]
    selected["inference_trace"].append(
        f"Selection: {selected[chr(114)+chr(111)+chr(111)+chr(109)]} is the nearest reachable room satisfying all three conditions: Lab, projector available, and wheelchair-accessible."
    )
    return selected
