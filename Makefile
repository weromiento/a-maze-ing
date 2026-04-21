PYTHON = python3
PIP = pip
MAIN = a_maze_ing.py

all: install

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(MAIN) config.txt

debug:
	$(PYTHON) -m pdb $(MAIN) config.txt

clean:
	rm -rf __pycache__
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
