from mazegenerator import Maze
from parser import parse_file
import sys


def clear() -> None:
    print("\033[H\033[J", end="")


def main() -> None:
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
        key = input("Choice? (1-4): ").strip()
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
            print("Key must be between 1 and 4")


if __name__ == "__main__":
    try:
        main()
    except PermissionError as e:
        print("Error: ", e)
