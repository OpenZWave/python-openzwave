# Makefile for python-openzwave
#

# You can set these variables from the command line.
ARCHBASE      = archive
BUILDDIR      = build
DISTDIR       = dists
NOSE          = $(shell which nosetests)
NOSEOPTS      = --verbosity=2
NOSECOVER     = --cover-package=libopenzwave,openzwave,pyozwman,pyozwweb --cover-min-percentage= --with-coverage --cover-inclusive --cover-tests --cover-html --cover-html-dir=docs/html/coverage --with-html --html-file=docs/html/nosetests/nosetests.html
PYLINT        = $(shell which pylint)
PYLINTOPTS    = --max-line-length=140 --max-args=9 --extension-pkg-whitelist=zmq --ignored-classes=zmq --min-public-methods=0

-include CONFIG.make

ifndef PYTHON_EXEC
PYTHON_EXEC=python
endif

ifdef VIRTUAL_ENV
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell ${VIRTUAL_ENV}/bin/${PYTHON_EXEC} --version 2>&1)))
else
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell ${PYTHON_EXEC} --version 2>&1)))
endif

python_openzwave_version := $(shell ${PYTHON_EXEC} pyozw_version.py)

PIP_EXEC=pip
ifeq (${python_version_major},3)
	PIP_EXEC=pip3
endif

python_version_major = $(word 1,${python_version_full})
python_version_minor = $(word 2,${python_version_full})
python_version_patch = $(word 3,${python_version_full})
EASYPTH       = /usr/local/lib/python${python_version_major}.${python_version_minor}/dist-packages/easy-install.pth

ARCHNAME     = python-openzwave-${python_openzwave_version}
ARCHDIR      = ${ARCHBASE}/${ARCHNAME}

.PHONY: help clean all update build develop install uninstall clean-docs docs autobuild-tests tests pylint commit developper-deps python-deps autobuild-deps arch-deps common-deps cython-deps

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  build           : build python-openzwave and openzwave"
	@echo "  develop         : install python-openzwave for developpers"
	@echo "  install         : install python-openzwave for users"
	@echo "  uninstall       : uninstall python-openzwave"
	@echo "  developper-deps : install dependencies for developpers"
	@echo "  deps            : install dependencies for users"
	@echo "  docs       	 : make documentation"
	@echo "  tests           : launch tests"
	@echo "  commit          : publish python-openzwave updates on GitHub"
	@echo "  clean           : clean the development directory"
	@echo "  update          : update sources of python-openzwave and openzwave"

clean-docs:
	cd docs && make clean
	-rm -Rf docs/html
	-rm -Rf docs/joomla
	-rm -Rf docs/pdf

clean: clean-docs
	-rm -rf $(ARCHBASE)
	-rm -rf $(BUILDDIR)
	-find . -name \*.pyc -delete
	-cd openzwave && make clean
	${PYTHON_EXEC} setup-lib.py clean --all --build-base $(BUILDDIR)/lib
	${PYTHON_EXEC} setup-api.py clean --all --build-base $(BUILDDIR)/api
	${PYTHON_EXEC} setup-manager.py clean --all --build-base $(BUILDDIR)/manager
	${PYTHON_EXEC} setup-web.py clean --all --build-base $(BUILDDIR)/web
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
	-yes | ${PIP_EXEC} uninstall pyozwweb
	${PYTHON_EXEC} setup-lib.py develop --uninstall
	${PYTHON_EXEC} setup-api.py develop --uninstall
	${PYTHON_EXEC} setup-manager.py develop --uninstall
	-rm -f libopenzwave.so
	-rm -f src-lib/libopenzwave.so
	-rm -f libopenzwave/liopenzwave.so
	-rm -Rf python_openzwave_api.egg-info/
	-rm -Rf src-api/python_openzwave_api.egg-info/
	-rm -Rf src-api/openzwave.egg-info/
	-rm -Rf src-manager/pyozwman.egg-info/
	-rm -Rf src-lib/python_openzwave_lib.egg-info/
	-rm -Rf src-lib/libopenzwave.egg-info/
	-rm -Rf src-web/pyozwweb.egg-info/
	-rm -Rf /usr/local/lib/python${python_version_major}.${python_version_minor}/dist-packages/python-openzwave*
	-rm -Rf /usr/local/lib/python${python_version_major}.${python_version_minor}/dist-packages/python_openzwave*
	-rm -Rf /usr/local/lib/python${python_version_major}.${python_version_minor}/dist-packages/libopenzwave*
	-rm -Rf /usr/local/lib/python${python_version_major}.${python_version_minor}/dist-packages/openzwave*
	-rm -Rf /usr/local/lib/python${python_version_major}.${python_version_minor}/dist-packages/pyozwman*
	-rm -Rf /usr/local/lib/python${python_version_major}.${python_version_minor}/dist-packages/pyozwweb*
	-rm -Rf /usr/local/share/python-openzwave
	-rm -Rf /usr/local/share/openzwave
	#-[ -f ${EASYPTH} ] && [ ! -f ${EASYPTH}.back ] && cp ${EASYPTH} ${EASYPTH}.back
	#-[ -f ${EASYPTH} ] && cat ${EASYPTH} | sed -e "/.*python-openzwave.*/d" | tee ${EASYPTH} >/dev/null

developper-deps : common-deps cython-deps tests-deps pip-deps doc-deps
	@echo
	@echo "Dependencies for developpers of python-openzwave installed (python ${python_version_full})"

autobuild-deps : common-deps cython-deps tests-deps pip-deps
	apt-get install -y git
	@echo
	@echo "Dependencies for autobuilders (docker, travis, ...) installed (python ${python_version_full})"

arch-deps : common-deps pip-deps
	@echo
	@echo "Dependencies for users installed (python ${python_version_full})"

python-deps:
ifeq (${python_version_major},2)
	apt-get install -y python2.7 python2.7-dev python2.7-minimal
endif
ifeq (${python_version_major},3)
	-apt-get install -y python3 python3-dev python3-minimal
endif

cython-deps:
ifeq (${python_version_major},2)
	apt-get install -y cython
endif
ifeq (${python_version_major},3)
	-apt-get install -y cython3
endif

common-deps:
	@echo Installing dependencies for python : ${python_version_full}
ifeq (${python_version_major},2)
	apt-get install -y python-pip python-dev python-docutils python-setuptools python-louie
endif
ifeq (${python_version_major},3)
	-apt-get install -y python3-pip python3-docutils python3-dev python3-setuptools
endif
	apt-get install -y build-essential libudev-dev g++

tests-deps:
	${PIP_EXEC} install nose-html
	${PIP_EXEC} install nose-progressive
	${PIP_EXEC} install coverage
	${PIP_EXEC} install nose
	${PIP_EXEC} install pylint

doc-deps:
	-apt-get install -y python-sphinx
	${PIP_EXEC} install sphinxcontrib-blockdiag sphinxcontrib-actdiag sphinxcontrib-nwdiag sphinxcontrib-seqdiag

pip-deps:
	#${PIP_EXEC} install docutils
	#${PIP_EXEC} install setuptools
	#The following line crashes with a core dump
	#${PIP_EXEC} install "Cython==0.22"

docs: clean-docs
	-mkdir -p docs/html/nosetests
	-mkdir -p docs/html/coverage
	-mkdir -p docs/html/pylint
	-mkdir -p docs/joomla/nosetests
	-mkdir -p docs/joomla/coverage
	-mkdir -p docs/joomla/pylint
	$(NOSE) $(NOSEOPTS) $(NOSECOVER) tests/
	cp docs/html/nosetests/* docs/joomla/nosetests
	cp docs/html/coverage/* docs/joomla/coverage
	-$(PYLINT) --output-format=html $(PYLINTOPTS) src-lib/libopenzwave/ src-api/openzwave/ >docs/html/pylint/report.html
	cp docs/html/pylint/* docs/joomla/pylint/
	cd docs && make docs
	cp docs/_build/text/README.txt README.md
	cp docs/_build/text/INSTALL_REPO.txt .
	cp docs/_build/text/INSTALL_ARCH.txt .
	cp docs/_build/text/INSTALL_MAC.txt .
	cp docs/_build/text/INSTALL_WIN.txt .
	cp docs/_build/text/COPYRIGHT.txt .
	cp docs/_build/text/CHANGELOG.txt .
	cp docs/_build/text/DEVEL.txt .
	cp docs/_build/text/EXAMPLES.txt .
	cp -Rf docs/_build/html/* docs/html/
	cp -Rf docs/_build/joomla/* docs/joomla/
	@echo
	@echo "Documentation finished."

install:
	${PYTHON_EXEC} setup-lib.py install
	${PYTHON_EXEC} setup-api.py install
	${PYTHON_EXEC} setup-manager.py install
	${PYTHON_EXEC} setup-web.py install
	@echo
	@echo "Installation for users finished."

develop:
	${PYTHON_EXEC} setup-lib.py develop
	${PYTHON_EXEC} setup-api.py develop
	${PYTHON_EXEC} setup-manager.py develop
	${PYTHON_EXEC} setup-web.py develop
	@echo
	@echo "Installation for developpers of python-openzwave finished."

tests:
	#export NOSESKIP=False && $(NOSE) $(NOSEOPTS) tests/ --with-progressive; unset NOSESKIP
	export NOSESKIP=False && $(NOSE) $(NOSEOPTS) tests ; unset NOSESKIP
	@echo
	@echo "Autobuild-tests for ZWave network finished."

autobuild-tests:
	$(NOSE) $(NOSEOPTS) tests/lib/autobuild tests/api/autobuild
	@echo
	@echo "Tests for ZWave network finished."

commit: clean docs
	git commit -m "Auto-commit for docs" README.md INSTALL_REPO.txt INSTALL_MAC.txt INSTALL_WIN.txt INSTALL_ARCH.txt COPYRIGHT.txt DEVEL.txt EXAMPLES.txt CHANGELOG.txt docs/
	git push
	@echo
	@echo "Commits pushed on github."

tag: commit
	git tag v${python_openzwave_version}
	git push origin v${python_openzwave_version}
	@echo
	@echo "Tag pushed on github."

pylint:
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
	cd openzwave && make

$(ARCHDIR):
	-mkdir -p $(ARCHDIR)/src-lib
	-mkdir -p $(ARCHDIR)/src-api
	-mkdir -p $(ARCHDIR)/src-manager
	cp -Rf openzwave $(ARCHDIR)/
	cp -Rf src-lib/libopenzwave $(ARCHDIR)/src-lib
	cp -Rf src-lib/libopenzwave/libopenzwave.cpp $(ARCHDIR)/src-lib/libopenzwave/
	cp -Rf src-api/openzwave $(ARCHDIR)/src-api
	cp -Rf src-manager/pyozwman $(ARCHDIR)/src-manager
	cp -Rf src-manager/scripts $(ARCHDIR)/src-manager
	-find $(ARCHDIR) -name \*.pyc -delete
	-cd $(ARCHDIR)/openzwave && make clean
	-rm -Rf $(ARCHDIR)/openzwave/.git

tgz: $(ARCHDIR) docs
	cp docs/_build/text/README.txt $(ARCHDIR)/
	cp docs/_build/text/INSTALL_REPO.txt $(ARCHDIR)/
	cp docs/_build/text/INSTALL_ARCH.txt $(ARCHDIR)/
	cp docs/_build/text/INSTALL_WIN.txt $(ARCHDIR)/
	cp docs/_build/text/INSTALL_MAC.txt $(ARCHDIR)/
	cp docs/_build/text/COPYRIGHT.txt $(ARCHDIR)/
	cp docs/_build/text/EXAMPLES.txt $(ARCHDIR)/
	cp docs/_build/text/CHANGELOG.txt $(ARCHDIR)/
	mkdir -p $(ARCHDIR)/docs
	cp -Rf docs/_build/html/* $(ARCHDIR)/docs/
	cp Makefile $(ARCHDIR)/
	cp setup-lib.py $(ARCHDIR)/
	cp setup-api.py $(ARCHDIR)/
	cp setup-manager.py $(ARCHDIR)/
	-mkdir -p $(DISTDIR)
	tar cvzf $(DISTDIR)/python-openzwave-${python_openzwave_version}.tgz -C $(ARCHBASE) ${ARCHNAME}
	rm -Rf $(ARCHBASE)
	@echo
	@echo "Archive for version ${python_openzwave_version} created"
