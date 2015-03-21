# Makefile for python-openzwave
#

# You can set these variables from the command line.
BUILDDIR      = _build
NOSE          = /usr/local/bin/nosetests
NOSEOPTS      = --verbosity=2
NOSECOVER     = --cover-package=python-openzwave-lib,python-openzwave-api --cover-min-percentage= --with-coverage --cover-inclusive --cover-tests --cover-html --cover-html-dir=docs/html/coverage --with-html --html-file=docs/html/nosetests/nosetests.html
PYLINT        = /usr/local/bin/pylint
PYLINTOPTS    = --max-line-length=140 --max-args=9 --extension-pkg-whitelist=zmq --ignored-classes=zmq --min-public-methods=0

.PHONY: help clean all develop install uninstall cleandoc docs tests devtests pylint commit apt pip travis-deps update build deps

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  develop    to install python-openzwave for developpers"
	@echo "  install    to install python-openzwave for users"
	@echo "  uninstall  to uninstall python-openzwave"
	@echo "  apt        to install packaged dependencies with apt"
	@echo "  pip        to install python dependencies with pip"
	@echo "  docs       to make all documentation"
	@echo "  tests      to launch tests for users"
	@echo "  devtests   to launch detailled tests for developpers"
	@echo "  pylint     to check code quality"
	@echo "  commit     to publish python-openzwave updates on GitHub"
	@echo "  clean      to clean the development directory"
	@echo "  cleandocs  to clean the documentation generated"
	@echo "  update     to update sources of python-openzwave and openzwave"
	@echo "  build      to build python-openzwave and openzwave"

cleandocs: clean
	-rm -rf docs/html
	-rm -rf docs/pdf

clean:
	-rm -rf $(BUILDDIR)
	-find . -name *.pyc -delete
	cd docs && make clean
	-cd openzwave && make clean
	python setup-lib.py clean
	python setup-api.py clean
	-rm -Rf build/
	-rm lib/libopenzwave.cpp

uninstall: clean
	-rm -rf build
	-rm -rf dist
	-rm -Rf python_openzwave_api.egg-info/
	-rm -Rf python_openzwave_lib.egg-info/
	-rm -Rf /usr/local/lib/python*.*/dist-packages/python-openzwave*
	-rm -Rf /usr/local/lib/python*.*/dist-packages/pyozwman*
	-rm -Rf /usr/local/lib/python*.*/dist-packages/openzwave*
	-rm -Rf /usr/local/share/python-openzwave

deps :
	apt-get install -y build-essential python-pip python-dev cython
	apt-get install -y python-dev python-setuptools python-louie
	apt-get install -y build-essential libudev-dev g++ make

travis-deps: deps

pip:
	pip install setuptools
	pip install docutils
	pip install cython

docs: cleandocs
	-mkdir -p docs/html/nosetests
	-mkdir -p docs/html/coverage
	-mkdir -p docs/html/pylint
	$(NOSE) $(NOSEOPTS) $(NOSECOVER) tests/
	-$(PYLINT) --output-format=html $(PYLINTOPTS) lib/ api/ >docs/html/pylint/report.html
	cd docs && make docs
	cp docs/_build/text/README.txt README.md
	cp docs/_build/text/INSTALL_REPO.txt .
	cp docs/_build/text/INSTALL_MAN.txt .
	cp docs/_build/text/INSTALL_ARCH.txt .
	cp docs/_build/text/COPYRIGHT.txt .
	cp docs/_build/text/DEVEL.txt .
	cp docs/_build/text/EXAMPLES.txt .
	@echo
	@echo "Documentation finished."

install: build
	sudo python setup-lib.py install
	sudo python setup-api.py install
	@echo
	@echo "Installation for users finished."

develop: build
	python setup-lib.py develop
	python setup-api.py develop
	@echo
	@echo "Installation for developpers finished."

tests:
	export NOSESKIP=False && $(NOSE) $(NOSEOPTS) tests/ --with-progressive; unset NOSESKIP
	@echo
	@echo "Tests for ZWave network finished."

devtests:
	-mkdir -p docs/html/nosetests
	-mkdir -p docs/html/coverage
	$(NOSE) $(NOSEOPTS) $(NOSECOVER) tests/
	@echo
	@echo "Tests for developpers finished."

commit: clean docs
	git commit -m "Auto-commit for docs" README.md INSTALL_REPO.txt INSTALL_MAN.txt INSTALL_ARCH.txt COPYRIGHT.txt DEVEL.txt EXAMPLES.txt docs/
	git push
	@echo
	@echo "Commits pushed on github."

pylint:
	-mkdir -p docs/html/pylint
	$(PYLINT) $(PYLINTOPTS) lib/ api/
	@echo
	@echo "Pylint finished."

all: clean docs

update: openzwave
	git pull
	cd openzwave && git pull

build: openzwave
	sed -i '253s/.*//' openzwave/cpp/src/value_classes/ValueID.h
	cd openzwave && VERSION_REV=0 make
	python setup-lib.py build
	python setup-api.py build

openzwave:
	git clone git://github.com/OpenZWave/open-zwave.git openzwave
