from collections import deque


class TimetableCSP:
    """
    Campus Timetabling Constraint Satisfaction Problem.

    Variables:
        Classes that need to be scheduled.

    Domains:
        Possible (room, time_slot) assignments.

    Constraints:
        1. A room cannot host two classes at the same time.
        2. A faculty member cannot teach two classes at the same time.
        3. A student batch cannot attend two classes at the same time.
        4. Lab classes must use laboratory rooms.
        5. Room capacity must be sufficient.
        6. Consecutive classes of the same batch must be within
           max_hops campus connections of one another.
    """

    def __init__(
        self,
        classes,
        rooms,
        time_slots,
        campus_graph=None,
        max_hops=2,
    ):
        self.classes = classes
        self.rooms = rooms
        self.time_slots = time_slots
        self.campus_graph = campus_graph
        self.max_hops = max_hops

        # Each variable starts with all possible room/time assignments.
        self.domains = {
            class_name: [
                (room_name, time_slot)
                for room_name in rooms
                for time_slot in time_slots
                if self._unary_constraints_allow(
                    class_name, room_name
                )
            ]
            for class_name in classes
        }

        self.nodes_checked = 0
        self.nodes_checked_with_propagation = 0

    # ---------------------------------------------------------
    # Unary constraints: room type and capacity
    # ---------------------------------------------------------

    def _unary_constraints_allow(self, class_name, room_name):
        course = self.classes[class_name]
        room = self.rooms[room_name]

        if course["type"] == "lab" and not room["is_lab"]:
            return False

        if room["capacity"] < course["students"]:
            return False

        return True

    # ---------------------------------------------------------
    # Campus graph and BFS distance
    # ---------------------------------------------------------

    def _room_location(self, room_name):
        """Return the campus location associated with a room."""
        return self.rooms[room_name].get("location", room_name)

    def _bfs_distance(self, start, goal):
        """
        Return the shortest path length in edges using BFS.

        The campus graph may be either a CampusGraph object
        or a plain adjacency dictionary.
        Return None if no route exists.
        """
        if start == goal:
            return 0

        if self.campus_graph is None:
            return None

        if hasattr(self.campus_graph, "get_neighbors"):
            get_neighbors = self.campus_graph.get_neighbors
        else:
            get_neighbors = lambda location: self.campus_graph.get(
                location, []
            )

        queue = deque([(start, 0)])
        visited = {start}

        while queue:
            current, distance = queue.popleft()

            for neighbour in get_neighbors(current):
                if neighbour == goal:
                    return distance + 1

                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, distance + 1))

        return None

    # ---------------------------------------------------------
    # Consecutive-class walking constraint
    # ---------------------------------------------------------

    def _satisfies_hop_constraint(self, class_name, assignment):
        """
        Check walking distance between adjacent scheduled classes
        belonging to the same batch.

        Classes are adjacent when their time slots are consecutive
        in the supplied time_slots list.
        """
        if self.campus_graph is None:
            return True

        current_course = self.classes[class_name]
        current_room, current_slot = assignment[class_name]
        current_batch = current_course["batch"]

        for other_name, (other_room, other_slot) in assignment.items():
            if other_name == class_name:
                continue

            other_course = self.classes[other_name]

            if other_course["batch"] != current_batch:
                continue

            try:
                current_index = self.time_slots.index(current_slot)
                other_index = self.time_slots.index(other_slot)
            except ValueError:
                return False

            # Check only adjacent time slots, not every pair of classes.
            if abs(current_index - other_index) != 1:
                continue

            current_location = self._room_location(current_room)
            other_location = self._room_location(other_room)

            distance = self._bfs_distance(
                current_location, other_location
            )

            # No known route also means the transition is infeasible.
            if distance is None or distance > self.max_hops:
                return False

        return True

    # ---------------------------------------------------------
    # Binary constraint checking
    # ---------------------------------------------------------

    def _pair_is_compatible(self, class_a, value_a, class_b, value_b):
        """Check constraints involving two different classes."""
        room_a, time_a = value_a
        room_b, time_b = value_b

        course_a = self.classes[class_a]
        course_b = self.classes[class_b]

        if time_a == time_b:
            if room_a == room_b:
                return False

            if course_a["faculty"] == course_b["faculty"]:
                return False

            if course_a["batch"] == course_b["batch"]:
                return False

        # Check walking distance for adjacent classes of the same batch.
        if course_a["batch"] == course_b["batch"]:
            try:
                index_a = self.time_slots.index(time_a)
                index_b = self.time_slots.index(time_b)
            except ValueError:
                return False

            if abs(index_a - index_b) == 1 and self.campus_graph is not None:
                location_a = self._room_location(room_a)
                location_b = self._room_location(room_b)

                distance = self._bfs_distance(location_a, location_b)

                if distance is None or distance > self.max_hops:
                    return False

        return True

    def is_consistent(self, class_name, assignment):
        """Check whether a partial assignment satisfies all constraints."""
        if class_name not in assignment:
            return False

        room_name, _ = assignment[class_name]

        if not self._unary_constraints_allow(class_name, room_name):
            return False

        for other_name, other_value in assignment.items():
            if other_name == class_name:
                continue

            if not self._pair_is_compatible(
                class_name,
                assignment[class_name],
                other_name,
                other_value,
            ):
                return False

        return self._satisfies_hop_constraint(class_name, assignment)

    # ---------------------------------------------------------
    # MRV: Minimum Remaining Values
    # ---------------------------------------------------------

    def _select_unassigned_variable(self, assignment, domains):
        """Choose the unassigned class with the smallest domain."""
        unassigned = [
            name for name in self.classes if name not in assignment
        ]

        return min(unassigned, key=lambda name: len(domains[name]))

    # ---------------------------------------------------------
    # LCV: Least Constraining Value
    # ---------------------------------------------------------

    def _order_domain_values(self, class_name, assignment, domains):
        """Try values that rule out the fewest neighbour choices first."""
        scored_values = []

        for value in domains[class_name]:
            eliminated = 0

            for other_name in self.classes:
                if other_name == class_name or other_name in assignment:
                    continue

                for other_value in domains[other_name]:
                    if not self._pair_is_compatible(
                        class_name, value, other_name, other_value
                    ):
                        eliminated += 1

            scored_values.append((eliminated, value))

        scored_values.sort(key=lambda item: item[0])
        return [value for _, value in scored_values]

    # ---------------------------------------------------------
    # AC-3 constraint propagation
    # ---------------------------------------------------------

    def _revise(self, domains, xi, xj):
        """
        Remove values from Xi that have no compatible value in Xj.
        Return True if Xi's domain changed.
        """
        revised = False

        for value_i in domains[xi][:]:
            has_support = any(
                self._pair_is_compatible(xi, value_i, xj, value_j)
                for value_j in domains[xj]
            )

            if not has_support:
                domains[xi].remove(value_i)
                revised = True

        return revised

    def _ac3(self, domains):
        """Apply AC-3 until all arcs are consistent or a domain is empty."""
        queue = deque(
            (xi, xj)
            for xi in self.classes
            for xj in self.classes
            if xi != xj
        )

        while queue:
            xi, xj = queue.popleft()

            if self._revise(domains, xi, xj):
                if not domains[xi]:
                    return False

                for xk in self.classes:
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))

        return True

    # ---------------------------------------------------------
    # Backtracking search
    # ---------------------------------------------------------

    def solve_backtracking(self):
        """Solve with backtracking, MRV and LCV, without AC-3."""
        self.nodes_checked = 0

        domains = {
            name: list(values) for name, values in self.domains.items()
        }

        return self._backtrack({}, domains, use_propagation=False)

    def solve_with_ac3(self):
        """Solve with AC-3 propagation and backtracking."""
        self.nodes_checked_with_propagation = 0

        domains = {
            name: list(values) for name, values in self.domains.items()
        }

        if not self._ac3(domains):
            return None

        return self._backtrack({}, domains, use_propagation=True)

    def _backtrack(self, assignment, domains, use_propagation=False):
        """Recursively assign classes until a valid timetable is found."""
        if len(assignment) == len(self.classes):
            return assignment.copy()

        if use_propagation:
            self.nodes_checked_with_propagation += 1
        else:
            self.nodes_checked += 1

        class_name = self._select_unassigned_variable(assignment, domains)

        for value in self._order_domain_values(
            class_name, assignment, domains
        ):
            assignment[class_name] = value

            if not self.is_consistent(class_name, assignment):
                del assignment[class_name]
                continue

            new_domains = {
                name: list(values) for name, values in domains.items()
            }
            new_domains[class_name] = [value]

            if use_propagation and not self._ac3(new_domains):
                del assignment[class_name]
                continue

            result = self._backtrack(
                assignment,
                new_domains,
                use_propagation=use_propagation,
            )

            if result is not None:
                return result

            del assignment[class_name]

        return None