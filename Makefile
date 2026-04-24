PYTHON = python3
PIP = pip
MAIN = a_maze_ing.py
ARG = config.txt
PYCACHE = __pycache__

all: install

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(ARG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(ARG)

clean:
	rm -rf $(PYCACHE)
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
