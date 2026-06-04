from state import State, Action, SIZE
from search import manhattan_distance


def advise(action: Action, state: State) -> str:
    """Return a human-readable explanation for the move that produced *state*."""
    direction = action.direction
    tile = action.tile
    dist = manhattan_distance(state)

    tile_pos = state.board.index(tile)
    goal_pos = state.goal.index(tile)
    tile_row, tile_col = divmod(tile_pos, SIZE)
    goal_row, goal_col = divmod(goal_pos, SIZE)

    if tile_row == goal_row and tile_col == goal_col:
        placement = f"tile {tile} is now in its goal position"
    elif tile_row == goal_row:
        placement = f"tile {tile} is on the correct row"
    elif tile_col == goal_col:
        placement = f"tile {tile} is on the correct column"
    else:
        placement = f"tile {tile} still needs to reach row {goal_row+1}, col {goal_col+1}"

    if dist == 0:
        urgency = "Puzzle solved!"
    elif dist <= 2:
        urgency = "Almost there —"
    elif dist <= 5:
        urgency = "Good progress —"
    else:
        urgency = "Working toward solution —"

    direction_map = {
        "UP":    "up",
        "DOWN":  "down",
        "LEFT":  "left",
        "RIGHT": "right",
    }
    move_desc = f"moved tile {tile} {direction_map[direction]}"

    return f"{urgency} {move_desc}. {placement.capitalize()}. Manhattan distance remaining: {dist}."
