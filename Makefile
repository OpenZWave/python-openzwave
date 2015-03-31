# Makefile for python-openzwave
#

# You can set these variables from the command line.
BUILDDIR      = build
DISTDIR       = dist
NOSE          = /usr/local/bin/nosetests
NOSEOPTS      = --verbosity=2
NOSECOVER     = --cover-package=libopenzwave,openzwave,pyozwman --cover-min-percentage= --with-coverage --cover-inclusive --cover-tests --cover-html --cover-html-dir=docs/html/coverage --with-html --html-file=docs/html/nosetests/nosetests.html
PYLINT        = /usr/local/bin/pylint
PYLINTOPTS    = --max-line-length=140 --max-args=9 --extension-pkg-whitelist=zmq --ignored-classes=zmq --min-public-methods=0

-include CONFIG.make

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

PIP_EXEC=pip
ifeq (${python_version_major},3)
	PIP_EXEC=pip3
endif

python_version_major = $(word 1,${python_version_full})
python_version_minor = $(word 2,${python_version_full})
python_version_patch = $(word 3,${python_version_full})
EASYPTH       = /usr/local/lib/python${python_version_major}.${python_version_minor}/dist-packages/easy-install.pth

.PHONY: help clean all develop install uninstall cleandoc docs tests devtests pylint commit apt pip travis-deps update build deps

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  build      to build python-openzwave and openzwave"
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

cleandocs:
	cd docs && make clean
	-rm -rf docs/html
	-rm -rf docs/pdf

clean:
	-rm -rf $(BUILDDIR)
	-rm -rf $(DISTDIR)
	-find . -name *.pyc -delete
	-cd openzwave && make clean
	${PYTHON_EXEC} setup-lib.py clean --all --build-base $(BUILDDIR)/lib
	${PYTHON_EXEC} setup-api.py clean --all --build-base $(BUILDDIR)/api
	${PYTHON_EXEC} setup-manager.py clean --all --build-base $(BUILDDIR)/manager
	-rm lib/libopenzwave.cpp
	-rm src-lib/libopenzwave/libopenzwave.cpp

uninstall:
	-rm -rf $(BUILDDIR)
	-rm -rf $(DISTDIR)
	-yes | ${PIP_EXEC} uninstall python-openzwave-lib
	-yes | ${PIP_EXEC} uninstall python-openzwave-api
	-yes | ${PIP_EXEC} uninstall libopenzwave
	-yes | ${PIP_EXEC} uninstall openzwave
	-yes | ${PIP_EXEC} uninstall pyozwman
	${PYTHON_EXEC} setup-lib.py develop --uninstall
	${PYTHON_EXEC} setup-api.py develop --uninstall
	${PYTHON_EXEC} setup-manager.py develop --uninstall
	-rm -f libopenzwave.so
	-rm -f src-lib/liopenzwave.so
	-rm -f libopenzwave/liopenzwave.so
	-rm -Rf python_openzwave_api.egg-info/
	-rm -Rf src-api/python_openzwave_api.egg-info/
	-rm -Rf src-api/openzwave.egg-info/
	-rm -Rf src-manager/pyozwman.egg-info/
	-rm -Rf src-lib/python_openzwave_lib.egg-info/
	-rm -Rf src-lib/libopenzwave.egg-info/
	-rm -Rf /usr/local/lib/python${python_version_major}.${python_version_minor}/dist-packages/python-openzwave*
	-rm -Rf /usr/local/lib/python${python_version_major}.${python_version_minor}/dist-packages/python_openzwave*
	-rm -Rf /usr/local/lib/python${python_version_major}.${python_version_minor}/dist-packages/libopenzwave*
	-rm -Rf /usr/local/lib/python${python_version_major}.${python_version_minor}/dist-packages/openzwave*
	-rm -Rf /usr/local/lib/python${python_version_major}.${python_version_minor}/dist-packages/pyozwman*
	-rm -Rf /usr/local/share/python-openzwave
	-rm -Rf /usr/local/share/openzwave
	#-[ -f ${EASYPTH} ] && [ ! -f ${EASYPTH}.back ] && cp ${EASYPTH} ${EASYPTH}.back
	#-[ -f ${EASYPTH} ] && cat ${EASYPTH} | sed -e "/.*python-openzwave.*/d" | tee ${EASYPTH} >/dev/null

deps :
	@echo Installing dependencies for python : ${python_version_full}
ifeq (${python_version_major},2)
	apt-get install -y python-pip python-dev
	apt-get install -y python-dev python-setuptools python-louie
endif
ifeq (${python_version_major},3)
	-apt-get install -y python3-pip
	-apt-get install -y python3-dev python3-setuptools
endif
	apt-get install -y build-essential libudev-dev g++
	${PIP_EXEC} install setuptools
	${PIP_EXEC} install "Cython>=0.20"

travis-deps: deps

tests-deps:
	${PIP_EXEC} install nose-html
	${PIP_EXEC} install nose-progressive
	${PIP_EXEC} install nose

pip:
	${PIP_EXEC} install docutils

docs: cleandocs
	-mkdir -p docs/html/nosetests
	-mkdir -p docs/html/coverage
	-mkdir -p docs/html/pylint
	$(NOSE) $(NOSEOPTS) $(NOSECOVER) tests/
	-$(PYLINT) --output-format=html $(PYLINTOPTS) src-lib/libopenzwave/ src-api/openzwave/ >docs/html/pylint/report.html
	cd docs && make docs
	cp docs/_build/text/README.txt README.md
	cp docs/_build/text/INSTALL_REPO.txt .
	cp docs/_build/text/INSTALL_ARCH.txt .
	cp docs/_build/text/COPYRIGHT.txt .
	cp docs/_build/text/DEVEL.txt .
	cp docs/_build/text/EXAMPLES.txt .
	@echo
	@echo "Documentation finished."

install:
	sudo ${PYTHON_EXEC} setup-lib.py install
	sudo ${PYTHON_EXEC} setup-api.py install
	sudo ${PYTHON_EXEC} setup-manager.py install
	@echo
	@echo "Installation for users finished."

develop:
	${PYTHON_EXEC} setup-lib.py develop
	${PYTHON_EXEC} setup-api.py develop
	${PYTHON_EXEC} setup-manager.py develop
	@echo
	@echo "Installation for developpers finished."

dist: build
	${PYTHON_EXEC} setup-lib.py sdist
	${PYTHON_EXEC} setup-api.py sdist
	${PYTHON_EXEC} setup-manager.py sdist
	${PYTHON_EXEC} setup-lib.py bdist_egg --bdist-dir $(DISTDIR)/lib
	${PYTHON_EXEC} setup-api.py bdist_egg --bdist-dir $(DISTDIR)/api
	${PYTHON_EXEC} setup-manager.py bdist_egg --bdist-dir $(DISTDIR)/manager
	@echo
	@echo "Eggs are finished."

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

commit: docs
	git commit -m "Auto-commit for docs" README.md INSTALL_REPO.txt INSTALL_ARCH.txt COPYRIGHT.txt DEVEL.txt EXAMPLES.txt docs/
	git push
	@echo
	@echo "Commits pushed on github."

pylint:
	-mkdir -p docs/html/pylint
	$(PYLINT) $(PYLINTOPTS) src-lib/libopenzwave/ src-api/openzwave/
	@echo
	@echo "Pylint finished."

all: clean docs

update: openzwave
	git pull
	cd openzwave && git pull

build: openzwave/libopenzwave.a
	${PYTHON_EXEC} setup-lib.py build --build-base $(BUILDDIR)/lib
	#${PYTHON_EXEC} setup-api.py build --build-base $(BUILDDIR)/api
	#${PYTHON_EXEC} setup-manager.py build --build-base $(BUILDDIR)/manager

openzwave:
	git clone git://github.com/OpenZWave/open-zwave.git openzwave

openzwave/libopenzwave.a: openzwave
	sed -i '253s/.*//' openzwave/cpp/src/value_classes/ValueID.h
	cd openzwave && VERSION_REV=0 make
