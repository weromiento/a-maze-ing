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
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

build:
	pip install build==1.4.4
	python -m build
