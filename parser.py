# from typing import Self
from typing_extensions import Self
from pydantic import BaseModel, model_validator


class Config(BaseModel):
    """
    Condiguration model for maze generation.

    This class defines all parameters required to generate a maze,
    including its dimensions, entry/exit points, output file name,
    and whether the maze must be perfect.
    """

    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool

    @model_validator(mode="after")
    def check_data(self) -> Self:
        """
        Validates the configuration values after model initialization.

        Ensures that:
        - WIDTH and HEIGHT are strictly positive
        - ENTRY and EXIT are inside maze boundaries
        Raises:
        ValueError: If any configuration value is invalid.
        """
        if self.WIDTH <= 0 or self.HEIGHT <= 0:
            raise ValueError("WIDTH and HEIGHT must be > 0")
        exit_x, exit_y = self.EXIT
        if exit_x >= self.WIDTH or exit_y >= self.HEIGHT:
            raise ValueError("EXIT must be inside the maze")
        entry_x, entry_y = self.ENTRY
        if entry_x >= self.WIDTH or entry_y >= self.HEIGHT:
            raise ValueError("ENTRY must be inside the maze")
        if self.ENTRY == self.EXIT:
            raise ValueError("ENTRY and EXIT must be different")
        return self


def parse_tuple(value: str) -> tuple[int, int]:
    """
    Parses a string formatted as 'x,y' into a tuple of integers.
    """
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(f"Invalid tuple: {value}")
    return int(parts[0]), int(parts[1])


def parse_bool(value: str) -> bool:
    """
    Converts a string into a boolean value.
    """
    v = value.strip().lower()
    if v == "true":
        return True
    if v == "false":
        return False
    raise ValueError(f"Invalid boolean: {value}")


def parse_file(filename: str) -> Config:
    """
    Parses a configuration file and returns a Config object.

    Reads key=value pairs from the file, validates required fields,
    converts values to proper types, and builds the configuration.
    """
    data: dict[str, str] = {}
    required = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                data[key] = value
    except (FileNotFoundError, PermissionError) as e:
        raise SystemExit(f"Error: {e}")
    missing = required - data.keys()
    if missing:
        raise SystemExit(f"Missing keys {missing} in {filename}")
    return Config(
        WIDTH=int(data["WIDTH"]),
        HEIGHT=int(data["HEIGHT"]),
        ENTRY=parse_tuple(data["ENTRY"]),
        EXIT=parse_tuple(data["EXIT"]),
        OUTPUT_FILE=data["OUTPUT_FILE"],
        PERFECT=parse_bool(data["PERFECT"]),
    )
