from dataclasses import dataclass
from typing import Dict, List, Optional

from .ac3 import AC3Solver
from .constraints import (
    assignment_is_valid,
    assignments_conflict,
    consecutive_batch_distance_satisfied,
)
from .timetable import Assignment


@dataclass
class AC3SolverStats:
    assignments_tried: int = 0
    backtracks: int = 0
    propagation_calls: int = 0
    values_removed: int = 0


class AC3BacktrackingSolver:
    """Backtracking search enhanced with AC-3 constraint propagation."""

    def __init__(
        self,
        domains: Dict[str, List[Assignment]],
        graph=None,
        k: int = 3,
    ) -> None:
        self.original_domains = {
            variable: list(values)
            for variable, values in domains.items()
        }
        self.graph = graph
        self.k = k
        self.stats = AC3SolverStats()

    def solve(self) -> Optional[Dict[str, Assignment]]:
        self.stats = AC3SolverStats()

        domains = {
            variable: list(values)
            for variable, values in self.original_domains.items()
        }

        return self._backtrack(domains, {})

    def _backtrack(
        self,
        domains: Dict[str, List[Assignment]],
        assignment: Dict[str, Assignment],
    ) -> Optional[Dict[str, Assignment]]:
        if len(assignment) == len(domains):
            return assignment.copy()

        variable = self._select_unassigned_variable(domains, assignment)

        for value in domains[variable]:
            self.stats.assignments_tried += 1

            if not self._is_consistent(variable, value, assignment):
                continue

            next_assignment = assignment.copy()
            next_assignment[variable] = value

            reduced_domains = {
                name: list(values)
                for name, values in domains.items()
            }
            reduced_domains[variable] = [value]

            self.stats.propagation_calls += 1

            ac3 = AC3Solver(
                reduced_domains,
                graph=self.graph,
                k=self.k,
            )
            propagated_domains = ac3.solve()

            self.stats.values_removed += ac3.values_removed

            if propagated_domains is None:
                continue

            result = self._backtrack(
                propagated_domains,
                next_assignment,
            )

            if result is not None:
                return result

        self.stats.backtracks += 1
        return None

    def _select_unassigned_variable(
        self,
        domains: Dict[str, List[Assignment]],
        assignment: Dict[str, Assignment],
    ) -> str:
        unassigned = [
            variable
            for variable in domains
            if variable not in assignment
        ]

        return min(
            unassigned,
            key=lambda variable: len(domains[variable]),
        )

    def _is_consistent(
        self,
        variable: str,
        value: Assignment,
        assignment: Dict[str, Assignment],
    ) -> bool:
        if not assignment_is_valid(value):
            return False

        for other_variable, other_value in assignment.items():
            if variable == other_variable:
                continue

            if assignments_conflict(value, other_value):
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
