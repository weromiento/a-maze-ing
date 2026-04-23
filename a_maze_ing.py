from mazegenerator import Maze
from parser import parse_file
import sys


def clear() -> None:
    """
    clear the terminal with uses ANSI espace sequences:
    \\33[H moves the cursor to the home position (top left)
    \\33[J clears akk content from the cursor to the end of the screen
    """
    print("\033[H\033[J", end="")


def main() -> None:
    """
    Entry point of the program
    Loads configuration, generate a maze with a 42 pattern calculate the
    solution path, then runs an interactive loop allowing regeneration,
    path toggle, change colors, switch perfect mode and exit
    """
    if len(sys.argv) < 2:
        print("Usage: python a_maze_ing.py <config_file>")
        return
    config = parse_file(sys.argv[1])
    perfect = config.PERFECT
    maze = Maze(config.WIDTH, config.HEIGHT, config.ENTRY, config.EXIT)
    maze.generate_42()
    maze.generate_maze(perfect)
    path_str = maze.bfs()
    maze.write_maze_file(config.OUTPUT_FILE, path_str)
    path = True
    maze.display(path)
    while True:
        clear()
        maze.display(path)
        print("=== A-Maze-Ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        if perfect:
            print("4. Switch perfect to False")
        else:
            print("4. Switch perfect to True")
        print("5. Quit")
        key = input("Choice? (1-5): ").strip()
        if key == "1":
            maze.reset_maze()
            maze.generate_maze(perfect)
            path_str = maze.bfs()
            maze.write_maze_file(config.OUTPUT_FILE, path_str)
        elif key == "2":
            path = not path
        elif key == "3":
            pass
        elif key == "4":
            perfect = not perfect
        elif key == "5":
            return
        else:
            print("Key must be between 1 and 5")


if __name__ == "__main__":
    try:
        main()
    except PermissionError as e:
        print("Error: ", e)
