# Makefile for python-openzwave
#

# You can set these variables from the command line.
BUILDDIR      = _build
NOSE          = /usr/local/bin/nosetests
NOSEOPTS      = --verbosity=2
NOSECOVER     = --cover-package=python-openzwave-lib,python-openzwave-api --cover-min-percentage= --with-coverage --cover-inclusive --cover-tests --cover-html --cover-html-dir=docs/html/coverage --with-html --html-file=docs/html/nosetests/nosetests.html
PYLINT        = /usr/local/bin/pylint
PYLINTOPTS    = --max-line-length=140 --max-args=9 --extension-pkg-whitelist=zmq --ignored-classes=zmq --min-public-methods=0

ifdef PYTHON_EXEC
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell ${PYTHON_EXEC} --version 2>&1)))
else
PYTHON_EXEC=python
ifdef VIRTUAL_ENV
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell ${VIRTUAL_ENV}/bin/${PYTHON_EXEC} --version 2>&1)))
else
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell ${PYTHON_EXEC} --version 2>&1)))
endif
endif

python_version_major = $(word 1,${python_version_full})
python_version_minor = $(word 2,${python_version_full})
python_version_patch = $(word 3,${python_version_full})

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
	${PYTHON_EXEC} setup-lib.py clean
	${PYTHON_EXEC} setup-api.py clean
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
	@echo Installing dependencies for python : ${VIRTUAL_ENV} ${python_version_full}
ifeq (${python_version_major},2)
	apt-get install -y python-pip python-dev cython
	apt-get install -y python-dev python-setuptools python-louie
endif
ifeq (${python_version_major},3)
	-apt-get install -y python3-pip cython3
	-apt-get install -y python3-dev python3-setuptools
endif
	apt-get install -y build-essential libudev-dev g++

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
	sudo ${PYTHON_EXEC} setup-lib.py install
	sudo ${PYTHON_EXEC} setup-api.py install
	@echo
	@echo "Installation for users finished."

develop: build
	${PYTHON_EXEC} setup-lib.py develop
	${PYTHON_EXEC} setup-api.py develop
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
	${PYTHON_EXEC} setup-lib.py build
	${PYTHON_EXEC} setup-api.py build

openzwave:
	git clone git://github.com/OpenZWave/open-zwave.git openzwave
