from dataclasses import dataclass
from typing import Dict, List, Optional

from .constraints import (
    assignment_is_valid,
    assignments_conflict,
    consecutive_batch_distance_satisfied,
)
from .timetable import Assignment


@dataclass
class SolverStats:
    assignments_tried: int = 0
    backtracks: int = 0


class BacktrackingSolver:
    def __init__(
        self,
        domains: Dict[str, List[Assignment]],
        graph=None,
        k: int = 3,
    ) -> None:
        self.domains = domains
        self.graph = graph
        self.k = k
        self.stats = SolverStats()

    def solve(self) -> Optional[Dict[str, Assignment]]:
        self.stats = SolverStats()
        assignment = {}
        return self._backtrack(assignment)

    def _backtrack(self, assignment):
        if len(assignment) == len(self.domains):
            return assignment.copy()

        variable = self._select_unassigned_variable(assignment)

        for value in self.domains[variable]:
            self.stats.assignments_tried += 1

            if self._is_consistent(
                variable,
                value,
                assignment,
            ):
                assignment[variable] = value

                result = self._backtrack(assignment)

                if result is not None:
                    return result

                del assignment[variable]

        self.stats.backtracks += 1
        return None

    def _select_unassigned_variable(self, assignment):
        for variable in self.domains:
            if variable not in assignment:
                return variable

        raise RuntimeError(
            "No unassigned variable remains."
        )

    def _is_consistent(
        self,
        variable,
        value,
        assignment,
    ):
        if not assignment_is_valid(value):
            return False

        for other_variable, other_value in assignment.items():
            if variable == other_variable:
                continue

            if assignments_conflict(
                value,
                other_value,
            ):
                return False

            if self.graph is not None:
                if not consecutive_batch_distance_satisfied(
                    value,
                    other_value,
                    self.graph,
                    self.k,
                ):
                    return False

        return True
