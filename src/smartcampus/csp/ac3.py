from collections import deque
from typing import Dict, List, Optional, Tuple

from .constraints import (
    assignment_is_valid,
    assignments_conflict,
    consecutive_batch_distance_satisfied,
)
from .timetable import Assignment


class AC3Solver:
    """Constraint propagation using the AC-3 algorithm."""

    def __init__(
        self,
        domains: Dict[str, List[Assignment]],
        graph=None,
        k: int = 3,
    ) -> None:
        self.domains = {
            variable: list(values)
            for variable, values in domains.items()
        }
        self.graph = graph
        self.k = k
        self.revisions = 0
        self.values_removed = 0

    def solve(self) -> Optional[Dict[str, List[Assignment]]]:
        """Run AC-3 and return the reduced domains.

        Returns None if propagation makes any domain empty.
        """
        self.revisions = 0
        self.values_removed = 0

        queue = deque(
            (variable_i, variable_j)
            for variable_i in self.domains
            for variable_j in self.domains
            if variable_i != variable_j
        )

        if not self._remove_invalid_values():
            return None

        while queue:
            variable_i, variable_j = queue.popleft()

            if self._revise(variable_i, variable_j):
                if not self.domains[variable_i]:
                    return None

                for variable_k in self.domains:
                    if variable_k != variable_i and variable_k != variable_j:
                        queue.append((variable_k, variable_i))

        return self.domains

    def _remove_invalid_values(self) -> bool:
        """Remove values that violate unary constraints."""
        for variable in self.domains:
            valid_values = [
                value
                for value in self.domains[variable]
                if assignment_is_valid(value)
            ]

            removed = len(self.domains[variable]) - len(valid_values)
            self.values_removed += removed
            self.domains[variable] = valid_values

            if not self.domains[variable]:
                return False

        return True

    def _revise(
        self,
        variable_i: str,
        variable_j: str,
    ) -> bool:
        """Remove values from Xi that have no support in Xj."""
        revised = False
        remaining_values = []

        for value_i in self.domains[variable_i]:
            supported = any(
                self._values_are_compatible(value_i, value_j)
                for value_j in self.domains[variable_j]
            )

            if supported:
                remaining_values.append(value_i)
            else:
                revised = True
                self.values_removed += 1

        if revised:
            self.revisions += 1
            self.domains[variable_i] = remaining_values

        return revised

    def _values_are_compatible(
        self,
        value_i: Assignment,
        value_j: Assignment,
    ) -> bool:
        if assignments_conflict(value_i, value_j):
            return False

        if self.graph is not None:
            if not consecutive_batch_distance_satisfied(
                value_i,
                value_j,
                self.graph,
                self.k,
            ):
                return False

        return True
