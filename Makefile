.PHONY: all clean uninstall install benchmark lint test dist sdist twine

all:
	@grep -Ee '^[a-z].*:' Makefile | cut -d: -f1 | grep -vF all

clean:
	rm -rf build/ dist/ *.egg-info/ mazelib/*.c mazelib/*.so mazelib/*.h mazelib/__pycache__ mazelib/*/*.c mazelib/*/*.so mazelib/*/*.h mazelib/*/__pycache__ test/__pycache__ lint.html

uninstall: clean
	@echo pip uninstalling mazelib
	$(shell pip uninstall -y mazelib >/dev/null 2>/dev/null)
	$(shell pip uninstall -y mazelib >/dev/null 2>/dev/null)
	$(shell pip uninstall -y mazelib >/dev/null 2>/dev/null)

install: uninstall
	pip install .

benchmark:
	python benchmarks/benchmarks.py

test:
	python test/test_maze.py
	python test/test_generators.py
	python test/test_solvers.py
	python test/test_transmuters.py

dist: install
	python setup.py sdist

sdist: dist

twine: dist
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

lint:
	flake8 --statistics --max-line-length=120 --exit-zero --ignore=E221,E241,E272,E402,W503,W504,W292 mazelib/ test/ benchmarks.py setup.py > lint.html
