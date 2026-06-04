# CLAUDE.md — AI Puzzle Solver

## Project overview

A terminal-based AI system that solves an 8-puzzle or maze using classical AI algorithms. This is NOT a machine learning project — it implements classical AI: search algorithms, heuristics, and a rule-based reasoning engine. No external AI APIs. Pure Python.

## What this project demonstrates

- Search & problem solving: A* algorithm with pluggable heuristics
- Knowledge representation: structured State class encoding board, goals, constraints
- Reasoning: rule-based advisor that explains moves in natural language
- AI programming patterns: agent loop, priority queues, open/closed sets

## Project structure

```
ai_puzzle_solver/
├── main.py       # Entry point. Ties together state, search, advisor, display
├── state.py      # Knowledge representation — State class, successors, goal check
├── search.py     # A* search engine, heuristics (Manhattan, Euclidean, Misplaced)
├── advisor.py    # Rule-based reasoning engine — explains each move in English
└── display.py    # Terminal rendering — board, path, stats
```

## Core concepts in code

### state.py — Knowledge representation
- State = immutable tuple representing board configuration
- State.successors() returns (action, new_state) pairs
- State.is_goal() compares against target configuration
- No mutable state — each move creates a new State object

### search.py — Search & problem solving
- A* = f(n) = g(n) + h(n) where g = cost so far, h = heuristic estimate
- Three heuristics available: manhattan_distance, euclidean_distance, misplaced_tiles
- Uses heapq (min-heap) as the priority queue (open set)
- Tracks visited states in a set (closed set) to avoid cycles
- Returns the full path of (action, state) pairs to the goal

### advisor.py — Reasoning engine
- Inspects current state and chosen action
- Applies rule conditions: distance to goal, direction of movement, obstacle proximity
- Returns a human-readable explanation string per move
- Rules are explicit if/elif chains — transparent, inspectable, educational

### display.py — Terminal rendering
- Renders board as a grid with box-drawing characters
- Colour-codes solved tiles vs unsolved (ANSI codes, graceful fallback)
- Prints step-by-step with advisor commentary
- Final stats: nodes explored, path length, time taken

## Build order

1. state.py — define State class, is_goal(), successors()
2. search.py — implement A*, add heuristics one at a time
3. main.py skeleton — wire state + search, print raw path
4. display.py — render board nicely
5. advisor.py — add commentary last (it's additive, not blocking)

## Key design decisions

- State is a tuple of ints (hashable, immutable) — required for the closed set
- Heuristics are standalone functions, not methods on State — makes them swappable
- Advisor is pure (no side effects) — takes state + action, returns string
- display.py knows nothing about search logic — clean separation

## Running the project

```bash
python main.py               # default: 8-puzzle, Manhattan heuristic
python main.py --mode maze   # maze mode
python main.py --heuristic euclidean
python main.py --heuristic misplaced
```

## What NOT to do

- Do not use external AI/ML libraries (no sklearn, no torch, no openai)
- Do not use networkx for the graph — implement the open/closed sets manually
- Do not put display logic inside state.py or search.py
- Do not make State mutable — always return new State objects from successors()

## Python requirements

- Python 3.10+
- No external packages (stdlib only: heapq, time, random, argparse, copy)

## Useful stdlib references

- heapq.heappush / heapq.heappop — priority queue for A*
- collections.namedtuple — clean action representation
- time.perf_counter — precise timing for stats
- copy.deepcopy — if you ever need deep copies (avoid if possible — use tuples)
