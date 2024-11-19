##########################################
#    Just a handy set of dev shortcuts   #
##########################################
.PHONY: all clean uninstall install lint test benchmark wheel twine

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
	pip install -U pip
	pip install .

lint:
	black .

test:
	python test/test_maze.py
	python test/test_generators.py
	python test/test_solvers.py
	python test/test_transmuters.py

benchmark:
	python benchmarks/benchmarks.py

wheel:
	pip install -U pip
	pip install -U wheel
	mkdir -f dist
	pip wheel . -w dist/
	rm dist/Cython*.whl
	rm dist/numpy*.whl
	auditwheel repair dist/mazelib*.whl -w .

twine: wheel
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
