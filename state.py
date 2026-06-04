from collections import namedtuple

Action = namedtuple("Action", ["direction", "tile"])

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # 0 = blank tile
SIZE = 3

_MOVES = {
    "UP":    -SIZE,
    "DOWN":  +SIZE,
    "LEFT":  -1,
    "RIGHT": +1,
}

_INVALID_LEFT  = {0, 3, 6}
_INVALID_RIGHT = {2, 5, 8}


class State:
    def __init__(self, board: tuple[int, ...], goal: tuple[int, ...] = GOAL_STATE):
        self.board = board
        self.goal = goal

    def is_goal(self) -> bool:
        return self.board == self.goal

    def blank_index(self) -> int:
        return self.board.index(0)

    def successors(self) -> list[tuple["Action", "State"]]:
        blank = self.blank_index()
        results = []
        for direction, delta in _MOVES.items():
            target = blank + delta
            if target < 0 or target >= SIZE * SIZE:
                continue
            if direction == "LEFT"  and blank in _INVALID_LEFT:
                continue
            if direction == "RIGHT" and blank in _INVALID_RIGHT:
                continue
            board = list(self.board)
            board[blank], board[target] = board[target], board[blank]
            tile = board[blank]  # tile that moved into blank's old spot
            results.append((Action(direction, tile), State(tuple(board), self.goal)))
        return results

    def __eq__(self, other) -> bool:
        return self.board == other.board

    def __hash__(self) -> int:
        return hash(self.board)

    def __repr__(self) -> str:
        rows = [self.board[i * SIZE:(i + 1) * SIZE] for i in range(SIZE)]
        return "\n".join(str(list(r)) for r in rows)
