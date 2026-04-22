from typing import List
import random


class Cell:
    """
    Represents a single cell in the maze grid.

    Each cell stores its position (x, y) ans the state of its four walls
    (North, East, South, West), the state of a wall is represents
    by a boolean (True = active, False inactive) and if is part of the pattern.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        self.walls = {"N": True, "E": True, "S": True, "W": True}
        self.visited = False
        self.part_of_path = False
        self.pattern = False


class Maze:
    """
    Represents a maze grid composed of cells.

    This class handles maze creation, cell management and wall manipulation.
    """

    def __init__(self, width: int, height: int, entry: tuple, exit: tuple):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit

        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]

    def get_cell(self, x: int, y: int) -> Cell:
        """Returns the cell located at coordinates (x, y)."""
        return self.grid[y][x]

    def in_bounds(self, x: int, y: int) -> bool:
        """Return a bool to know if the cell is in bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def remove_wall(self, c1: Cell, c2: Cell) -> None:
        """Removes the Wall between two adjacent cells."""
        dx = c2.x - c1.x
        dy = c2.y - c1.y

        if dx == 1:
            c1.walls["E"] = False
            c2.walls["W"] = False

        elif dx == -1:
            c1.walls["W"] = False
            c2.walls["E"] = False

        elif dy == 1:
            c1.walls["S"] = False
            c2.walls["N"] = False

        elif dy == -1:
            c1.walls["N"] = False
            c2.walls["S"] = False

    def get_neighbors(self, cell: Cell) -> List:
        """Return neighbors of a cell."""
        directions = [
            ("N", 0, -1),
            ("E", 1, 0),
            ("S", 0, 1),
            ("W", -1, 0),
        ]

        neighbors = []

        for _, dx, dy in directions:
            nx, ny = cell.x + dx, cell.y + dy

            if self.in_bounds(nx, ny):
                neighbors.append(self.get_cell(nx, ny))

        return neighbors

    def generate_maze(self) -> None:
        """Generate a perfect maze using iterative depth-first search (DFS).

        Starts from cell with the coordinates of ENTRY and carves passages
        through unvisited neighbors using a stack-based backtracking approach.
        Cells already marked as visited are left untouched.
        """
        start_cell = self.get_cell(self.entry[0], self.entry[1])
        stack = [start_cell]
        start_cell.visited = True
        while stack:
            current = stack[-1]
            neighbors = self.get_neighbors(current)
            unvisited = [
                n for n in neighbors if not n.visited and not n.pattern
            ]
            if unvisited:
                next_cell = random.choice(unvisited)
                self.remove_wall(current, next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

    def generate_42(self) -> None:
        """Generate the 42 pattern in the maze"""
        if self.height < 6 or self.width < 9:
            raise ValueError("The maze is to small to generate the pattern 42")
        start_x = self.width // 2 - 3
        start_y = self.height // 2 - 2
        draw = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]
        for y, row in enumerate(draw):
            for x, case in enumerate(row):
                if case != 1:
                    continue
                c = self.get_cell(start_x + x, start_y + y)
                if self.entry == (c.x, c.y) or self.exit == (c.x, c.y):
                    raise ValueError("Entry or Exit is in the 42 pattern")
                c.walls["N"] = True
                c.walls["E"] = True
                c.walls["S"] = True
                c.walls["W"] = True
                c.pattern = True
                for nx, ny, direction in [
                    (c.x, c.y - 1, "N"),
                    (c.x + 1, c.y, "E"),
                    (c.x, c.y + 1, "S"),
                    (c.x - 1, c.y, "W"),
                ]:
                    if self.in_bounds(nx, ny):
                        n = self.get_cell(nx, ny)
                        if direction == "N":
                            n.walls["S"] = True
                        elif direction == "E":
                            n.walls["W"] = True
                        elif direction == "S":
                            n.walls["N"] = True
                        elif direction == "W":
                            n.walls["E"] = True

    def cell_to_hex(self, cell: Cell) -> str:
        """
        generate an hexadecimal value
        compared with the state of each wall
        """
        value = 0
        if cell.walls["N"]:
            value += 1
        if cell.walls["E"]:
            value += 2
        if cell.walls["S"]:
            value += 4
        if cell.walls["W"]:
            value += 8
        return f"{value:X}"

    def write_maze_file(self, filename: str, path: str) -> None:
        """
        Write the output file which contains the maze in hexadecimal
        and the coordinates of the entry and exit,
        and also the path from the entry to the exit.
        """
        try:
            with open(filename, "w") as f:
                for y in range(self.height):
                    line = []
                    for x in range(self.width):
                        cell = self.get_cell(x, y)
                        line.append(self.cell_to_hex(cell))
                    f.write("".join(line) + "\n")
                f.write("\n")
                f.write(f"{self.entry[0]},{self.entry[1]}\n")
                f.write(f"{self.exit[0]},{self.exit[1]}\n")
                f.write(path + "\n")
        except (
            PermissionError,
            FileNotFoundError,
            IsADirectoryError,
            OSError,
        ) as e:
            print(f"Error: {e}")

    def display(self) -> None:
        """
        Display the maze in the terminal unsing ASCII characters.

        Wall are drawn with block characters, and entry/exit are highlighted.
        Cells belonging to the pattern ot the pattern are displayed with a
        different colors.
        """
        colors = {
            "wall": "\033[34m",
            "entry": "\033[32m",
            "exit": "\033[31m",
            "empty": "\033[0m",
            "pattern": "\033[36m",
            "path": "\033[33m",
        }
        RESET = "\033[0m"
        WALL = "██"
        EMPTY = "  "
        for x in range(self.width):
            print(colors["wall"] + WALL + RESET, end="")
            if self.get_cell(x, 0).walls["N"]:
                print(colors["wall"] + WALL + RESET, end="")
            else:
                print(EMPTY, end="")
        print(colors["wall"] + WALL + RESET)
        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell(x, y)
                if cell.walls["W"]:
                    print(colors["wall"] + WALL + RESET, end="")
                else:
                    print(EMPTY, end="")
                if (x, y) == self.entry:
                    print(colors["entry"] + WALL + RESET, end="")
                elif (x, y) == self.exit:
                    print(colors["exit"] + WALL + RESET, end="")
                elif self.get_cell(x, y).pattern:
                    print(colors["pattern"] + WALL + RESET, end="")
                elif self.get_cell(x, y).part_of_path:
                    print(colors["path"] + WALL + RESET, end="")
                else:
                    print(EMPTY, end="")
            if self.get_cell(self.width - 1, y).walls["E"]:
                print(colors["wall"] + WALL + RESET)
            else:
                print(EMPTY)
            for x in range(self.width):
                cell = self.get_cell(x, y)
                print(colors["wall"] + WALL + RESET, end="")
                if cell.walls["S"]:
                    print(colors["wall"] + WALL + RESET, end="")
                else:
                    print(EMPTY, end="")
            print(colors["wall"] + WALL + RESET)

    def bfs(self) -> None:
        start_cell = self.get_cell(self.entry[0], self.entry[1])
        exit_cell = self.get_cell(self.exit[0], self.exit[1])
        queue = []
        queue.append(start_cell)
        parent = {}
        parent[start_cell] = None
        visited = set()
        visited.add((start_cell.x, start_cell.y))
        while queue:
            current = queue.pop(0)
            if current == exit_cell:
                break

            if not current.walls["N"]:
                neighbor = self.get_cell(current.x, current.y - 1)
                if (neighbor.x, neighbor.y) not in visited:
                    visited.add((neighbor.x, neighbor.y))
                    parent[neighbor] = current
                    queue.append(neighbor)

            if not current.walls["E"]:
                neighbor = self.get_cell(current.x + 1, current.y)
                if (neighbor.x, neighbor.y) not in visited:
                    visited.add((neighbor.x, neighbor.y))
                    parent[neighbor] = current
                    queue.append(neighbor)

            if not current.walls["S"]:
                neighbor = self.get_cell(current.x, current.y + 1)
                if (neighbor.x, neighbor.y) not in visited:
                    visited.add((neighbor.x, neighbor.y))
                    parent[neighbor] = current
                    queue.append(neighbor)

            if not current.walls["W"]:
                neighbor = self.get_cell(current.x - 1, current.y)
                if (neighbor.x, neighbor.y) not in visited:
                    visited.add((neighbor.x, neighbor.y))
                    parent[neighbor] = current
                    queue.append(neighbor)
        path = []
        current = exit_cell
        while current is not None:
            path.append(current)
            current = parent.get(current)
        path.reverse()
        for cell in path:
            cell.part_of_path = True
        print(len(path))


maze = Maze(10, 10, (0, 0), (9, 9))
maze.generate_42()
maze.generate_maze()
maze.bfs()
maze.display()
# maze.write_maze_file("maze.txt", "pas de path encore")
