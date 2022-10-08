.PHONY: all clean uninstall install benchmark lint test dist sdist twine

all:
	@grep -Ee '^[a-z].*:' Makefile | cut -d: -f1 | grep -vF all

clean:
	git clean -dfxq --exclude=*.py --exclude=*.pxd

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

wheel:
	wheel python setup.py bdist_wheel --universal
	auditwheel repair dist/*.whl -w .

egg:
	python setup.py bdist_egg

twine: dist egg
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

lint:
	black .
