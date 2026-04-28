PYTHON = python3
PIP = pip
MAIN = a_maze_ing.py
ARG = config.txt

all: install

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(ARG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(ARG)

clean:
	rm -rf __pycache__ .mypy_cache mazegen.egg-info */__pycache__
lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict

build:
	$(PIP) install build==1.4.4
	$(PYTHON) -m build
