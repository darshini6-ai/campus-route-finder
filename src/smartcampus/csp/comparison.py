import time
from dataclasses import dataclass

from .ac3_backtracking import AC3BacktrackingSolver
from .backtracking import BacktrackingSolver
from .timetable import (
    create_courses,
    create_domains,
    create_rooms,
    create_time_slots,
)
from src.smartcampus.graph.campus_data import create_campus_graph


@dataclass
class CSPComparisonResult:
    method: str
    solution_found: bool
    assignments_tried: int
    backtracks: int
    propagation_calls: int
    values_removed: int
    runtime_ms: float


def compare_csp_solvers(k: int = 3) -> list[CSPComparisonResult]:
    """Compare plain backtracking with AC-3 + backtracking."""

    courses = create_courses()
    rooms = create_rooms()
    slots = create_time_slots()
    graph = create_campus_graph()

    domains = create_domains(courses, rooms, slots)

    # Plain backtracking
    start_time = time.perf_counter()

    backtracking_solver = BacktrackingSolver(
        domains,
        graph=graph,
        k=k,
    )
    backtracking_solution = backtracking_solver.solve()

    backtracking_runtime = (
        time.perf_counter() - start_time
    ) * 1000

    plain_result = CSPComparisonResult(
        method="Backtracking",
        solution_found=backtracking_solution is not None,
        assignments_tried=backtracking_solver.stats.assignments_tried,
        backtracks=backtracking_solver.stats.backtracks,
        propagation_calls=0,
        values_removed=0,
        runtime_ms=backtracking_runtime,
    )

    # AC-3 + backtracking
    start_time = time.perf_counter()

    ac3_solver = AC3BacktrackingSolver(
        domains,
        graph=graph,
        k=k,
    )
    ac3_solution = ac3_solver.solve()

    ac3_runtime = (
        time.perf_counter() - start_time
    ) * 1000

    ac3_result = CSPComparisonResult(
        method="AC-3 + Backtracking",
        solution_found=ac3_solution is not None,
        assignments_tried=ac3_solver.stats.assignments_tried,
        backtracks=ac3_solver.stats.backtracks,
        propagation_calls=ac3_solver.stats.propagation_calls,
        values_removed=ac3_solver.stats.values_removed,
        runtime_ms=ac3_runtime,
    )

    return [plain_result, ac3_result]
