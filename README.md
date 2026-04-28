*This project has been created as part of the 42 curriculum by romgutie, yflohic.*

# A-Maze-Ing

## Description

A-Maze-Ing is a maze generator written in Python. The program reads a configuration file, generates a random maze of configurable dimensions, embeds a visible **"42" pattern** made of fully walled cells, computes the shortest path from the entry to the exit, and saves the result to a file. It also provides an interactive terminal display with ASCII/ANSI rendering.

The maze can be **perfect** (exactly one path between any two cells) or **imperfect** (extra passages added randomly). The generation is based on an iterative depth-first search algorithm (DFS with backtracking), and the shortest path is found with a breadth-first search (BFS).

---

## Instructions

### Requirements

- Python 3.10 or later
- pip

### Installation

```bash
make install
```

This installs all dependencies listed in `requirements.txt` (pydantic, mypy, flake8).

### Running the program

```bash
make run
```

Or manually:

```bash
python3 a_maze_ing.py config.txt
```

### Debug mode

```bash
make debug
```

### Lint

```bash
make lint
make lint-strict
```

### Clean

```bash
make clean
```

---

## Configuration file format

The configuration file uses `KEY=VALUE` pairs, one per line. Lines starting with `#` are comments and are ignored.

| Key | Type | Description | Example |
|-----|------|-------------|---------|
| `WIDTH` | int | Number of columns | `WIDTH=15` |
| `HEIGHT` | int | Number of rows | `HEIGHT=15` |
| `ENTRY` | x,y | Entry cell coordinates | `ENTRY=0,0` |
| `EXIT` | x,y | Exit cell coordinates | `EXIT=14,14` |
| `OUTPUT_FILE` | string | Path of the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | bool | Perfect maze (True/False) | `PERFECT=True` |

A default `config.txt` is included at the root of the repository.

Example:

```
# Maze configuration
WIDTH=15
HEIGHT=15
ENTRY=0,0
EXIT=14,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

---

## Output file format

The maze is saved to the file specified by `OUTPUT_FILE`. The format is:

1. One hexadecimal character per cell, one row per line. Each character encodes which walls are closed (bit 0 = North, bit 1 = East, bit 2 = South, bit 3 = West). A wall set to 1 is closed, 0 is open.
2. An empty line.
3. Entry coordinates (`x,y`).
4. Exit coordinates (`x,y`).
5. The shortest path from entry to exit as a string of directions: `N`, `E`, `S`, `W`.

Example:

```
D5395513D513D13
97AAB96C396C56A
...

0,0
14,14
WSSEESENESES...
```

---

## Maze generation algorithm

The maze is generated using an **iterative depth-first search (DFS) with backtracking.**

**How it works:**

1. The "42" pattern is drawn first: a set of cells are fully walled and marked as pattern — they will never be carved through.
2. Starting from the ENTRY cell, a stack is used to explore the grid. At each step, a random unvisited non-pattern neighbor is chosen, the wall between the current cell and that neighbor is removed, and the neighbor is pushed onto the stack.
3. When no unvisited neighbor is available, the algorithm backtracks by popping the stack until a cell with available neighbors is found.
4. If `PERFECT=False`, extra walls are randomly removed (5% probability per wall) to create additional paths.
5. A post-processing step detects and fixes any 3×3 open areas by randomly restoring one wall inside them.
6. BFS is then run to find the shortest path and mark it in the maze.

**Why DFS?**

Depth-First Search (DFS) was chosen because it provides a good balance between simplicity, control, and visual quality. It naturally generates long, continuous paths, which makes the maze more interesting to explore and fits well with the overall structure of the project.

---

## Interactive display

Once the maze is generated, a menu is displayed in the terminal:

- **1** — Re-generate a new maze
- **2** — Show/Hide the shortest path from entry to exit
- **3** — Rotate maze colors (random ANSI color palette)
- **4** — Switch between perfect and imperfect mode
- **5** — Quit

The display uses Unicode block characters (`██`) and ANSI escape codes for colors. Entry, exit, path, walls, and the 42 pattern are each rendered in a distinct color.

---

## Reusable module (`mazegen`)

The maze generation logic is packaged as a standalone Python library: `mazegen`.

### Installation (from built package)

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Or build from source:

```bash
pip install build==1.4.4
python -m build
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

### Basic usage

```python
from mazegen import Maze, parse_file

maze = Maze(width=20, height=15, entry=(0, 0), exit=(19, 14))

# Generate (perfect=True for a perfect maze, output_file is the save path)
maze.generate_maze(perfect=True, output_file="maze.txt")

# Access the grid
cell = maze.get_cell(5, 3)
print(cell.walls)       # {'N': True, 'E': False, 'S': True, 'W': False}
print(cell.part_of_path)  # True if cell is on the shortest path
print(cell.pattern)       # True if cell is part of the 42 pattern
```

### Using a config file

```python
from mazegen import parse_file, Maze

config = parse_file("config.txt")
maze = Maze(config.WIDTH, config.HEIGHT, config.ENTRY, config.EXIT)
maze.generate_maze(config.PERFECT, config.OUTPUT_FILE)
```

### Custom parameters

```python
import random

# Set a seed for reproducibility
seed = 42
random.seed(seed)

maze = Maze(width=30, height=20, entry=(0, 0), exit=(29, 19))
maze.generate_maze(perfect=False, output_file="output.txt")
```

### Accessing the solution path

After calling `generate_maze()`, cells on the shortest path have `cell.part_of_path = True`. The path string (directions) is written to the output file and also returned by `bfs()`:

```python
maze.generate_maze(perfect=True, output_file="maze.txt")

path_cells = [
    maze.get_cell(x, y)
    for y in range(maze.height)
    for x in range(maze.width)
    if maze.get_cell(x, y).part_of_path
]
```

### Exported symbols

| Symbol | Type | Description |
|--------|------|-------------|
| `Maze` | class | Main maze class |
| `MazeTooSmallError` | exception | Raised when the maze is too small for the 42 pattern |
| `EntryExitInPatternError` | exception | Raised when entry or exit overlaps the 42 pattern |
| `parse_file` | function | Parses a config file and returns a `Config` object |
| `Config` | class | Pydantic model for maze configuration |

---

## Team and project management

### Roles

- **romgutie** — maze generation algorithm (DFS, pattern 42, wall coherence, open area detection), reusable library packaging, pyproject.toml, Makefile
- **yflohic** — BFS path finding, display (ASCII/ANSI rendering), interactive menu, config parser, README

### Planning

**Initial plan:**
- Do it well but quickly, the blackhole is coming

**How it evolved:**
-We followed the subject step by step, implementing all mandatory requirements in order.
### What worked well

- The iterative DFS approach avoided any recursion limit issues on large mazes.
- Pydantic for config validation caught many edge cases early and gave clear error messages for free.
- Separating the library (`mazegen/`) from the main script (`a_maze_ing.py`) made testing and refactoring much cleaner.

### What could be improved

- The seed is currently not displayed to the user, making it impossible to reproduce a specific maze without noting it manually.
- Only one generation algorithm is supported. Adding alternatives (Prim's, Kruskal's) would make the project more educational.

### Tools used

- The incredible romgutie's **nvim** setup for writing the code
- **Git / GitHub** for version control and collaboration

---

## Resources

### Documentation and references

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Depth-first search — Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [Breadth-first search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [ANSI escape codes reference](https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)
- And many youtube video

### AI usage
Ai (Claude, Le Chat) were used for:
- **Explaining concepts**: Explain certain concepts with examples to improve understanding, like as the BFS algorithm
- **Code verification**: Check if we haven't missed any major mistakes.
