import heapq
import math
import time
from state import State, Action, SIZE

# ---------------------------------------------------------------------------
# Heuristics
# ---------------------------------------------------------------------------

def manhattan_distance(state: State) -> int:
    total = 0
    for i, tile in enumerate(state.board):
        if tile == 0:
            continue
        goal_i = state.goal.index(tile)
        total += abs(i // SIZE - goal_i // SIZE) + abs(i % SIZE - goal_i % SIZE)
    return total


def euclidean_distance(state: State) -> float:
    total = 0.0
    for i, tile in enumerate(state.board):
        if tile == 0:
            continue
        goal_i = state.goal.index(tile)
        dr = i // SIZE - goal_i // SIZE
        dc = i % SIZE  - goal_i % SIZE
        total += math.sqrt(dr * dr + dc * dc)
    return total


def misplaced_tiles(state: State) -> int:
    return sum(
        1 for i, tile in enumerate(state.board)
        if tile != 0 and tile != state.goal[i]
    )


HEURISTICS = {
    "manhattan":  manhattan_distance,
    "euclidean":  euclidean_distance,
    "misplaced":  misplaced_tiles,
}

# ---------------------------------------------------------------------------
# A* search
# ---------------------------------------------------------------------------

def astar(
    initial: State,
    heuristic_name: str = "manhattan",
) -> tuple[list[tuple[Action, State]], int, float]:
    """Return (path, nodes_explored, elapsed_seconds).

    path is a list of (action, resulting_state) pairs from initial → goal.
    Returns ([], nodes_explored, elapsed) if no solution found.
    """
    h = HEURISTICS[heuristic_name]

    t0 = time.perf_counter()

    # heap entry: (f, g, tie_breaker, state, path_so_far)
    counter = 0
    start_h = h(initial)
    heap = [(start_h, 0, counter, initial, [])]
    closed: set[tuple] = set()
    nodes_explored = 0

    while heap:
        f, g, _, current, path = heapq.heappop(heap)

        if current.board in closed:
            continue
        closed.add(current.board)
        nodes_explored += 1

        if current.is_goal():
            return path, nodes_explored, time.perf_counter() - t0

        for action, successor in current.successors():
            if successor.board in closed:
                continue
            new_g = g + 1
            new_h = h(successor)
            new_f = new_g + new_h
            counter += 1
            heapq.heappush(heap, (new_f, new_g, counter, successor, path + [(action, successor)]))

    return [], nodes_explored, time.perf_counter() - t0
