from typing import List


class Cell:
    """
    Represents a single cell in the maze grid.

    Each cell stores its position (x, y) ans the state of its four walls
    (North, East, South, West), the state of a wall is represents
    by a boolean (True = active, False inactive).
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        self.walls = {"N": True, "E": True, "S": True, "W": True}

        self.visited = False


class Maze:
    """
    Represents a maze grid composed of cells.

    This class handles maze creation, cell management and wall manipulation.
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

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
