.PHONY: all clean uninstall install benchmark test dist sdist twine

all:
	@grep -Ee '^[a-z].*:' Makefile | cut -d: -f1 | grep -vF all

clean:
	rm -rf build/ dist/ *.egg-info/ mazelib/*.c mazelib/*.so mazelib/*.h mazelib/__pycache__ mazelib/*/*.c mazelib/*/*.so mazelib/*/*.h mazelib/*/__pycache__ test/__pycache__

uninstall: clean
	@echo pip uninstalling mazelib
	$(shell pip uninstall -y mazelib >/dev/null 2>/dev/null)
	$(shell pip uninstall -y mazelib >/dev/null 2>/dev/null)
	$(shell pip uninstall -y mazelib >/dev/null 2>/dev/null)

install: uninstall
	python setup.py install

benchmark:
	python benchmarks/benchmarks.py

test:
	python test/test_*.py

dist: install
	python setup.py sdist

sdist: dist

twine: dist
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

