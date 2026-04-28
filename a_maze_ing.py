from mazegen import parse_file, Maze, EntryExitInPatternError
import sys
import random


def random_colors() -> dict[str, str]:
    """Returns a dict of 6 different ANSI colors for the display"""
    all_colors = [
        "\033[31m",
        "\033[32m",
        "\033[33m",
        "\033[34m",
        "\033[35m",
        "\033[36m",
        "\033[37m",
    ]
    colors = random.sample(all_colors, 6)
    colors_dict = {
        "wall": colors[0],
        "entry": colors[1],
        "exit": colors[2],
        "empty": colors[3],
        "pattern": colors[4],
        "path": colors[5],
    }
    return colors_dict


def clear() -> None:
    """
    clear the terminal with uses ANSI espace sequences:
    \\033[H moves the cursor to the home position (top left)
    \\033[J clears all content from the cursor to the end of the screen
    """
    print("\033[H\033[J", end="")


def main() -> None:
    """
    Entry point of the program
    Loads configuration, generate a maze with a 42 pattern calculate the
    solution path, then runs an interactive loop allowing regeneration,
    path toggle, change colors, switch perfect mode and exit.
    """
    if len(sys.argv) < 2:
        print("Usage: python a_maze_ing.py <config_file>")
        return
    colors = random_colors()
    seed = random.randint(0, 10000000)
    random.seed(seed)
    config = parse_file(sys.argv[1])
    perfect = config.PERFECT
    maze = Maze(config.WIDTH, config.HEIGHT, config.ENTRY, config.EXIT)
    pattern_ok = True
    try:
        pattern_ok = maze.generate_maze(perfect, config.OUTPUT_FILE)
    except EntryExitInPatternError as e:
        print(e)
        return
    path = True
    while True:
        clear()
        if not pattern_ok:
            print("The maze is too small to generate the pattern '42'.")
        maze.display(path, colors)
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
            seed = random.randint(0, 10000000)
            random.seed(seed)
            maze.reset_maze()
            maze.generate_maze(perfect, config.OUTPUT_FILE)
        elif key == "2":
            path = not path
        elif key == "3":
            colors = random_colors()
        elif key == "4":
            perfect = not perfect
        elif key == "5":
            return
        else:
            print("Key must be between 1 and 5.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error: ", e)
