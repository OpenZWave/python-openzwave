# Makefile for python-openzwave
#

# You can set these variables from the command line.
ARCHBASE      = archive
ARCHIVES      = archives
BUILDDIR      = build
DISTDIR       = dists
NOSEOPTS      = --verbosity=2
NOSECOVER     = --cover-package=openzwave,pyozwman,pyozwweb --with-coverage --cover-inclusive --cover-tests --cover-html --cover-html-dir=docs/html/coverage --with-html --html-file=docs/html/nosetests/nosetests.html
PYLINT        = $(shell which pylint)
PYLINTOPTS    = --max-line-length=140 --max-args=9 --extension-pkg-whitelist=zmq --ignored-classes=zmq --min-public-methods=0

-include CONFIG.make

ifndef PYTHON_EXEC
PYTHON_EXEC=python
endif

ifndef NOSE_EXEC
NOSE_EXEC=$(shell which nosetests)
endif

ifdef VIRTUAL_ENV
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell ${VIRTUAL_ENV}/bin/${PYTHON_EXEC} --version 2>&1)))
else
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell ${PYTHON_EXEC} --version 2>&1)))
endif

python_openzwave_version := $(shell ${PYTHON_EXEC} pyozw_version.py)

python_version_major = $(word 1,${python_version_full})
python_version_minor = $(word 2,${python_version_full})
python_version_patch = $(word 3,${python_version_full})

PIP_EXEC=pip
ifeq (${python_version_major},3)
	PIP_EXEC=pip3
endif

ARCHNAME     = python-openzwave-${python_openzwave_version}
ARCHDIR      = ${ARCHBASE}/${ARCHNAME}

.PHONY: help clean all update develop install install-api uninstall clean-docs docs autobuild-tests tests pylint commit developper-deps python-deps autobuild-deps arch-deps common-deps cython-deps merge-python3 check

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  build           : build python-openzwave and openzwave"
	@echo "  develop         : install python-openzwave for developpers"
	@echo "  install         : install python-openzwave for users"
	@echo "  install-api     : install python-openzwave (API only) for users"
	@echo "  uninstall       : uninstall python-openzwave"
	@echo "  developper-deps : install dependencies for developpers"
	@echo "  deps            : install dependencies for users"
	@echo "  docs       	 : make documentation"
	@echo "  tests           : launch tests"
	@echo "  commit          : publish python-openzwave updates on GitHub"
	@echo "  clean           : clean the development directory"
	@echo "  update          : update sources of python-openzwave and openzwave"

clean: clean-docs clean-archive
	-rm -rf $(BUILDDIR)
	-find . -name \*.pyc -delete
	-cd openzwave && $(MAKE) clean
	${PYTHON_EXEC} setup-lib.py clean --all --build-base $(BUILDDIR)/lib
	${PYTHON_EXEC} setup-api.py clean --all --build-base $(BUILDDIR)/api
	${PYTHON_EXEC} setup-manager.py clean --all --build-base $(BUILDDIR)/manager
	${PYTHON_EXEC} setup-web.py clean --all --build-base $(BUILDDIR)/web
	-rm lib/libopenzwave.cpp
	-rm src-lib/libopenzwave/libopenzwave.cpp
	-rm -rf debian/python-openzwave-api/
	-rm -rf debian/python-openzwave-doc/
	-rm -rf debian/python-openzwave-lib/
	-rm -rf debian/python-openzwave-manager/
	-rm -rf debian/python-openzwave-web/
	-rm debian/files
	-rm debian/*.debhelper
	-rm debian/*.debhelper.log
	-rm debian/*.substvars
	-rm -rf .tests_user_path/

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
	${PYTHON_EXEC} setup-web.py develop --uninstall
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

check: .git

.git:
	@echo "Invalid git repository" && exit 1

developper-deps: common-deps cython-deps tests-deps pip-deps doc-deps
	@echo
	@echo "Dependencies for developpers of python-openzwave installed (python ${python_version_full})"

repo-deps: common-deps cython-deps tests-deps pip-deps
	@echo
	@echo "Dependencies for users installed (python ${python_version_full})"

autobuild-deps: common-deps cython-deps tests-deps pip-deps
	apt-get install --force-yes -y git
	@echo
	@echo "Dependencies for autobuilders (docker, travis, ...) installed (python ${python_version_full})"

arch-deps: common-deps pip-deps
	@echo
	@echo "Dependencies for users installed (python ${python_version_full})"

python-deps:
ifeq (${python_version_major},2)
	apt-get install --force-yes -y python2.7 python2.7-dev python2.7-minimal libyaml-dev python-pip
endif
ifeq (${python_version_major},3)
	apt-get install --force-yes -y python3 python3-dev python3-minimal libyaml-dev python3-pip
endif

cython-deps:
ifeq (${python_version_major},2)
	apt-get install --force-yes -y cython
endif
ifeq (${python_version_major},3)
	 apt-get install --force-yes -y cython3
endif

common-deps:
	@echo Installing dependencies for python : ${python_version_full}
ifeq (${python_version_major},2)
	apt-get install --force-yes -y python-pip python-dev python-docutils python-setuptools python-louie
endif
ifeq (${python_version_major},3)
	-apt-get install --force-yes -y python3-pip python3-docutils python3-dev python3-setuptools
endif
	apt-get install --force-yes -y build-essential libudev-dev g++ libyaml-dev

tests-deps:
	${PIP_EXEC} install nose-html
	${PIP_EXEC} install coverage
	${PIP_EXEC} install nose
	${PIP_EXEC} install pylint

doc-deps:
	-apt-get install --force-yes -y python-sphinx
	${PIP_EXEC} install sphinxcontrib-blockdiag sphinxcontrib-actdiag sphinxcontrib-nwdiag sphinxcontrib-seqdiag

pip-deps:
	#${PIP_EXEC} install docutils
	#${PIP_EXEC} install setuptools
	#The following line crashes with a core dump
	#${PIP_EXEC} install "Cython==0.22"

merge-python3:
	git checkout python3
	git merge -m "Auto-merge from master" master
	git push
	git checkout master
	@echo
	@echo "Commits for branch python3 pushed on github."

clean-docs:
	cd docs && $(MAKE) clean
	-rm -Rf docs/html
	-rm -Rf docs/joomla
	-rm -Rf docs/pdf

docs: clean-docs
	-mkdir -p docs/html/nosetests
	-mkdir -p docs/html/coverage
	-mkdir -p docs/html/pylint
	-mkdir -p docs/joomla/nosetests
	-mkdir -p docs/joomla/coverage
	-mkdir -p docs/joomla/pylint
	#${NOSE_EXEC} $(NOSEOPTS) $(NOSECOVER) tests/
	#${NOSE_EXEC} $(NOSEOPTS) tests/
	-cp docs/html/nosetests/* docs/joomla/nosetests
	-cp docs/html/coverage/* docs/joomla/coverage
	#-$(PYLINT) --output-format=html $(PYLINTOPTS) src-lib/libopenzwave/ src-api/openzwave/ src-manager/pyozwman/ src-web/pyozwweb/>docs/html/pylint/report.html
	-cp docs/html/pylint/* docs/joomla/pylint/
	cd docs && $(MAKE) docs
	cp docs/README.rst README.rst
	cp docs/INSTALL_REPO.rst .
	cp docs/INSTALL_ARCH.rst .
	cp docs/INSTALL_MAC.rst .
	cp docs/INSTALL_WIN.rst .
	cp docs/_build/text/COPYRIGHT.txt .
	cp docs/_build/text/CHANGELOG.txt .
	cp docs/_build/text/DEVEL.txt .
	cp docs/_build/text/EXAMPLES.txt .
	cp -Rf docs/_build/html/* docs/html/
	cp -Rf docs/_build/joomla/* docs/joomla/
	@echo
	@echo "Documentation finished."

install-lib: build
	${PYTHON_EXEC} setup-lib.py install
	@echo
	@echo "Installation of lib finished."

install-api: install-lib
	${PYTHON_EXEC} setup-api.py install
	@echo
	@echo "Installation of API finished."

install-manager: install-api
	${PYTHON_EXEC} setup-manager.py install
	@echo
	@echo "Installation of manager finished."

install: install-manager
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
	#export NOSESKIP=False && ${NOSE_EXEC} $(NOSEOPTS) tests/ --with-progressive; unset NOSESKIP
	export NOSESKIP=False && ${NOSE_EXEC} $(NOSEOPTS) tests/lib tests/api tests/manager ; unset NOSESKIP
	@echo
	@echo "Tests for ZWave network finished."

autobuild-tests:
	${NOSE_EXEC} $(NOSEOPTS) tests/lib/autobuild tests/api/autobuild
	@echo
	@echo "Autobuild-tests for ZWave network finished."

pylint:
	$(PYLINT) $(PYLINTOPTS) src-lib/libopenzwave/ src-api/openzwave/ src-manager/pyozwman/ src-web/pyozwweb/
	@echo
	@echo "Pylint finished."

update: openzwave
	git pull
	cd openzwave && git pull

build: openzwave/.lib/
	${PYTHON_EXEC} setup-lib.py build

openzwave:
	git clone git://github.com/OpenZWave/open-zwave.git openzwave

openzwave/.lib/: openzwave
	#sed -i -e '253s/.*//' openzwave/cpp/src/value_classes/ValueID.h
	cd openzwave && $(MAKE)

clean-archive:
	-rm -rf $(ARCHBASE)

$(ARCHDIR):
	-mkdir -p $(ARCHDIR)/src-lib
	-mkdir -p $(ARCHDIR)/src-api
	-mkdir -p $(ARCHDIR)/src-manager
	-mkdir -p $(ARCHDIR)/src-web
	cp -Rf openzwave $(ARCHDIR)/
	cp -f openzwave/cpp/src/vers.cpp $(ARCHDIR)/openzwave.vers.cpp
	cp -Rf src-lib/libopenzwave $(ARCHDIR)/src-lib
	cp -f src-lib/libopenzwave/libopenzwave.cpp $(ARCHDIR)/src-lib/libopenzwave/
	cp -Rf src-api/openzwave $(ARCHDIR)/src-api
	cp -Rf src-manager/pyozwman $(ARCHDIR)/src-manager
	cp -Rf src-manager/scripts $(ARCHDIR)/src-manager
	cp -Rf src-web/pyozwweb $(ARCHDIR)/src-web
	cp -Rf examples $(ARCHDIR)
	-find $(ARCHDIR) -name \*.pyc -delete
	-find $(ARCHDIR) -name zwcfg_\*.xml -delete
	-find $(ARCHDIR) -name OZW_Log.log -delete
	-find $(ARCHDIR) -name OZW_Log.txt -delete
	-find $(ARCHDIR) -name ozwsh.log -delete
	-find $(ARCHDIR) -name errors.log -delete
	-find $(ARCHDIR) -name zwscene.xml -delete
	-find $(ARCHDIR) -name zwbutton.xml -delete
	-find $(ARCHDIR) -name pyozw.db -delete
	-cd $(ARCHDIR)/openzwave && $(MAKE) clean
	-rm -Rf $(ARCHDIR)/openzwave/.git
	cp -f $(ARCHDIR)/openzwave.vers.cpp $(ARCHDIR)/openzwave/cpp/src/vers.cpp

tgz: clean-archive $(ARCHDIR) docs
	cp docs/_build/text/README.txt $(ARCHDIR)/
	cp docs/_build/text/INSTALL_ARCH.txt $(ARCHDIR)/
	cp docs/_build/text/INSTALL_WIN.txt $(ARCHDIR)/
	cp docs/_build/text/INSTALL_MAC.txt $(ARCHDIR)/
	cp docs/_build/text/COPYRIGHT.txt $(ARCHDIR)/
	cp docs/_build/text/EXAMPLES.txt $(ARCHDIR)/
	cp docs/_build/text/CHANGELOG.txt $(ARCHDIR)/
	mkdir -p $(ARCHDIR)/docs
	cp -Rf docs/_build/html/* $(ARCHDIR)/docs/
	cp Makefile.archive $(ARCHDIR)/Makefile
	cp setup-lib.py $(ARCHDIR)/
	sed -i 's|src-lib/libopenzwave/libopenzwave.pyx|src-lib/libopenzwave/libopenzwave.cpp|g' $(ARCHDIR)/setup-lib.py
	cp setup-api.py $(ARCHDIR)/
	cp setup-manager.py $(ARCHDIR)/
	cp setup-web.py $(ARCHDIR)/
	cp -Rf pyozw_version.py $(ARCHDIR)/pyozw_version.py
	-mkdir -p $(DISTDIR)
	tar cvzf $(DISTDIR)/python-openzwave-${python_openzwave_version}.tgz -C $(ARCHBASE) ${ARCHNAME}
	rm -Rf $(ARCHBASE)
	mv $(DISTDIR)/python-openzwave-${python_openzwave_version}.tgz $(ARCHIVES)
	git add $(ARCHIVES)/python-openzwave-${python_openzwave_version}.tgz
	git commit -m "Add new archive" $(ARCHIVES)/python-openzwave-${python_openzwave_version}.tgz
	@echo
	@echo "Archive for version ${python_openzwave_version} created"

push: develop
	-git commit -m "Auto-commit for docs" README.rst INSTALL_REPO.rst INSTALL_MAC.rst INSTALL_WIN.rst INSTALL_ARCH.rst COPYRIGHT.txt DEVEL.txt EXAMPLES.txt CHANGELOG.txt docs/
	-git push
	@echo
	@echo "Commits for branch master pushed on github."

commit: push merge-python3
	@echo
	@echo "Commits for branches master/python3 pushed on github."

tag:
	git tag v${python_openzwave_version}
	git push origin v${python_openzwave_version}
	@echo
	@echo "Tag pushed on github."

new-version: commit tgz tag commit
	git push
	@echo
	@echo "New version ${python_openzwave_version} created and published"

debch:
	dch --newversion ${python_openzwave_version} --maintmaint "Automatic release from upstream"

deb:
	dpkg-buildpackage

venv-deps: common-deps
	apt-get install --force-yes -y python-all python-dev python3-all python3-dev

venv2:
	virtualenv --python=python2 venv2
	venv2/bin/pip install cython
	venv2/bin/pip install nose
	-rm -f src-lib/libopenzwave/libopenzwave.cpp
	$(MAKE) PYTHON_EXEC=venv2/bin/python install
	
venv3:
	virtualenv --python=python3 venv3
	venv3/bin/pip install cython
	venv3/bin/pip install nose
	-rm -f src-lib/libopenzwave/libopenzwave.cpp
	$(MAKE) PYTHON_EXEC=venv3/bin/python install

venv-tests: venv2 venv3
	$(MAKE) PYTHON_EXEC=venv2/bin/python install >/dev/null
	$(MAKE) PYTHON_EXEC=venv3/bin/python install >/dev/null
	@echo "Files installed in venv"
	-$(MAKE) PYTHON_EXEC=venv2/bin/python NOSE_EXEC=venv2/bin/nosetests tests
	-$(MAKE) PYTHON_EXEC=venv3/bin/python NOSE_EXEC=venv3/bin/nosetests tests

venv-autobuild-tests: venv2 venv3
	-venv2/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild
	-venv3/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild
