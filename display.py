import sys
import time
from state import State, SIZE

# ANSI colour codes — degrade gracefully on non-colour terminals
_COLOUR = sys.stdout.isatty()
_GREEN  = "\033[32m" if _COLOUR else ""
_YELLOW = "\033[33m" if _COLOUR else ""
_BOLD   = "\033[1m"  if _COLOUR else ""
_RESET  = "\033[0m"  if _COLOUR else ""


def _cell(tile: int, goal_index: int, board_index: int) -> str:
    if tile == 0:
        return "   "
    label = f" {tile} "
    if board_index == goal_index:
        return f"{_GREEN}{label}{_RESET}"
    return f"{_YELLOW}{label}{_RESET}"


def render_board(state: State) -> str:
    top    = "┌───┬───┬───┐"
    mid    = "├───┼───┼───┤"
    bottom = "└───┴───┴───┘"
    rows = []
    rows.append(top)
    for r in range(SIZE):
        cells = []
        for c in range(SIZE):
            idx  = r * SIZE + c
            tile = state.board[idx]
            goal_idx = state.goal.index(tile) if tile != 0 else -1
            cells.append(_cell(tile, goal_idx, idx))
        rows.append("│" + "│".join(cells) + "│")
        if r < SIZE - 1:
            rows.append(mid)
    rows.append(bottom)
    return "\n".join(rows)


def print_solution(
    initial: State,
    path: list,          # list of (Action, State)
    nodes_explored: int,
    elapsed: float,
    advisor_fn=None,
    step_delay: float = 0.0,
) -> None:
    print(f"\n{_BOLD}Initial state:{_RESET}")
    print(render_board(initial))

    if not path:
        print("\nNo solution found.")
        return

    print(f"\n{_BOLD}Solving… ({len(path)} steps){_RESET}\n")

    for step, (action, state) in enumerate(path, 1):
        print(f"Step {step}: {action.direction} (tile {action.tile})")
        if advisor_fn:
            print(f"  {advisor_fn(action, state)}")
        print(render_board(state))
        print()
        if step_delay:
            time.sleep(step_delay)

    print(f"{_BOLD}{'─' * 40}{_RESET}")
    print(f"  Nodes explored : {nodes_explored}")
    print(f"  Path length    : {len(path)} moves")
    print(f"  Time           : {elapsed:.4f}s")
    print(f"{_BOLD}{'─' * 40}{_RESET}\n")
