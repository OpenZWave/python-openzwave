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

WHL_PYTHON2 := $(shell ls dist/*.whl 2>/dev/null|grep ${python_openzwave_version}|grep [0-9]-cp2)
WHL_PYTHON3 := $(shell ls dist/*.whl 2>/dev/null|grep ${python_openzwave_version}|grep [0-9]-cp3)
 
ARCHNAME     = python-openzwave-${python_openzwave_version}
ARCHDIR      = ${ARCHBASE}/${ARCHNAME}

.PHONY: help clean all update develop install install-api uninstall clean-docs docs autobuild-tests tests pylint commit developper-deps python-deps autobuild-deps arch-deps common-deps cython-deps check venv-clean venv2 venv3

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
	${PYTHON_EXEC} setup.py clean --all --build-base $(BUILDDIR)/python_openzwave
	-rm -f lib/libopenzwave.cpp
	-rm -f libopenzwave.so
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
	-rm -rf openzwave-git
	-rm -rf openzwave-embed
	-rm -rf open-zwave-master
	-rm -rf dist
	-rm -rf tmp
	-rm -rf venv2 venv3

uninstall:
	-rm -rf $(BUILDDIR)
	-rm -rf $(DISTDIR)
	-yes | ${PIP_EXEC} uninstall python-openzwave-lib
	-yes | ${PIP_EXEC} uninstall python-openzwave-api
	-yes | ${PIP_EXEC} uninstall libopenzwave
	-yes | ${PIP_EXEC} uninstall openzwave
	-yes | ${PIP_EXEC} uninstall pyozwman
	-yes | ${PIP_EXEC} uninstall pyozwweb
	-yes | ${PIP_EXEC} uninstall python_openzwave
	${PYTHON_EXEC} setup-lib.py develop --uninstall --flavor=dev
	${PYTHON_EXEC} setup-api.py develop --uninstall
	${PYTHON_EXEC} setup-manager.py develop --uninstall
	${PYTHON_EXEC} setup-web.py develop --uninstall
	${PYTHON_EXEC} setup.py develop --uninstall --flavor=dev
	-rm -f libopenzwave.so
	-rm -f src-lib/libopenzwave*.so
	-rm -f libopenzwave/liopenzwave.so
	-rm -Rf python_openzwave_api.egg-info/
	-rm -Rf src-api/python_openzwave_api.egg-info/
	-rm -Rf src-api/openzwave.egg-info/
	-rm -Rf src-manager/pyozwman.egg-info/
	-rm -Rf python_openzwave.egg-info/
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
	
ci-deps:
	apt-get install --force-yes -y python-pip python-dev python-docutils python-setuptools python-virtualenv
	-apt-get install --force-yes -y python3-pip python3-docutils python3-dev python3-setuptools
	apt-get install --force-yes -y build-essential libudev-dev g++ libyaml-dev

common-deps:
	@echo Installing dependencies for python : ${python_version_full}
ifeq (${python_version_major},2)
	apt-get install --force-yes -y python-pip python-dev python-docutils python-setuptools
endif
ifeq (${python_version_major},3)
	-apt-get install --force-yes -y python3-pip python3-docutils python3-dev python3-setuptools
endif
	apt-get install --force-yes -y build-essential libudev-dev g++ libyaml-dev

tests-deps:
	${PIP_EXEC} install nose-html
	${PIP_EXEC} install nose-progressive
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
	cp docs/_build/text/COPYRIGHT.txt LICENSE.txt
	cp docs/_build/text/CHANGELOG.txt .
	cp docs/_build/text/DEVEL.txt .
	cp docs/_build/text/EXAMPLES.txt .
	cp -Rf docs/_build/html/* docs/html/
	cp -Rf docs/_build/joomla/* docs/joomla/
	@echo
	@echo "Documentation finished."

install-lib: build
	${PYTHON_EXEC} setup-lib.py install --flavor=git
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

develop: src-lib/libopenzwave/libopenzwave.cpp
	${PYTHON_EXEC} setup-lib.py develop --flavor=dev
	${PYTHON_EXEC} setup-api.py develop
	${PYTHON_EXEC} setup-manager.py develop
	${PYTHON_EXEC} setup-web.py develop
	${PYTHON_EXEC} setup.py develop --flavor=dev
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

src-lib/libopenzwave/libopenzwave.cpp: openzwave/.lib/
	${PYTHON_EXEC} setup-lib.py build --flavor=dev

openzwave:
	git clone git://github.com/OpenZWave/open-zwave.git openzwave

openzwave.gzip:
	wget --no-check-certificate https://codeload.github.com/OpenZWave/open-zwave/zip/master
	mv master open-zwave-master.zip
	unzip open-zwave-master.zip
	mv open-zwave-master openzwave
	
openzwave/.lib/: openzwave
	cd openzwave && $(MAKE) -j 4

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
	mv $(DISTDIR)/python-openzwave-${python_openzwave_version}.tgz $(ARCHIVES)/
	@echo
	@echo "Archive for version ${python_openzwave_version} created"

embed_openzave_master:clean-archive src-lib/libopenzwave/libopenzwave.cpp
	-rm -Rf $(ARCHBASE)/open-zwave-master
	-mkdir -p $(ARCHBASE)/open-zwave-master/python-openzwave/src-lib/libopenzwave
	cp -Rf openzwave/* $(ARCHBASE)/open-zwave-master/
	cp -f openzwave/cpp/src/vers.cpp $(ARCHBASE)/open-zwave-master/python-openzwave/openzwave.vers.cpp
	cp -f src-lib/libopenzwave/libopenzwave.cpp $(ARCHBASE)/open-zwave-master/python-openzwave/src-lib/libopenzwave/
	-find $(ARCHBASE)/open-zwave-master -name \*.pyc -delete 2>/dev/null || true
	-find $(ARCHBASE)/open-zwave-master -name zwcfg_\*.xml -delete 2>/dev/null || true
	-find $(ARCHBASE)/open-zwave-master -name OZW_Log.log -delete 2>/dev/null || true
	-find $(ARCHBASE)/open-zwave-master -name OZW_Log.txt -delete 2>/dev/null || true
	-find $(ARCHBASE)/open-zwave-master -name ozwsh.log -delete 2>/dev/null || true
	-find $(ARCHBASE)/open-zwave-master -name errors.log -delete 2>/dev/null || true
	-find $(ARCHBASE)/open-zwave-master -name zwscene.xml -delete 2>/dev/null || true
	-find $(ARCHBASE)/open-zwave-master -name zwbutton.xml -delete 2>/dev/null || true
	-find $(ARCHBASE)/open-zwave-master -name pyozw.db -delete 2>/dev/null || true
	-cd $(ARCHBASE)/open-zwave-master && $(MAKE) clean
	-rm -Rf $(ARCHBASE)/open-zwave-master/.git
	-rm -f $(ARCHBASE)/open-zwave-master/open-zwave-master.zip
	-rm -Rf $(ARCHBASE)/open-zwave-master/docs/*
	-rm -Rf $(ARCHBASE)/open-zwave-master/dotnet/*
	cp -f $(ARCHBASE)/open-zwave-master/python-openzwave/openzwave.vers.cpp $(ARCHBASE)/open-zwave-master/cpp/src/vers.cpp
	-mkdir -p $(DISTDIR)
	cd $(ARCHBASE) && zip -r ../$(DISTDIR)/open-zwave-master-${python_openzwave_version}.zip open-zwave-master
	mv $(DISTDIR)/open-zwave-master-${python_openzwave_version}.zip $(ARCHIVES)/
	@echo
	@echo "embed_openzave_master for version ${python_openzwave_version} created"

pypi_package:clean-archive
	-rm -Rf $(ARCHBASE)/python_openzwave/
	${PYTHON_EXEC} setup.py egg_info
	-mkdir -p $(ARCHBASE)/python_openzwave/
	cp -Rf src-python_openzwave $(ARCHBASE)/python_openzwave/
	cp -Rf src-lib $(ARCHBASE)/python_openzwave/
	cp -Rf src-api $(ARCHBASE)/python_openzwave/
	cp -Rf src-manager $(ARCHBASE)/python_openzwave/
	cp -f setup.cfg $(ARCHBASE)/python_openzwave/
	cp -f setup.py $(ARCHBASE)/python_openzwave/
	cp -f pyozw_pkgconfig.py $(ARCHBASE)/python_openzwave/
	cp -f pyozw_setup.py $(ARCHBASE)/python_openzwave/
	cp -f pyozw_version.py $(ARCHBASE)/python_openzwave/
	cp -f python_openzwave.egg-info/PKG-INFO $(ARCHBASE)/python_openzwave/	
	-find $(ARCHBASE)/python_openzwave/ -name \*.pyc -delete 2>/dev/null || true
	-find $(ARCHBASE)/python_openzwave/ -name \*.so -delete 2>/dev/null || true
	-find $(ARCHBASE)/python_openzwave/ -type d -name \*.egg-info -exec rm -rf '{}' \; 2>/dev/null || true
	-find $(ARCHBASE)/python_openzwave/ -name zwcfg_\*.xml -delete
	-find $(ARCHBASE)/python_openzwave/ -name OZW_Log.log -delete
	-find $(ARCHBASE)/python_openzwave/ -name OZW_Log.txt -delete
	-find $(ARCHBASE)/python_openzwave/ -name ozwsh.log -delete
	-find $(ARCHBASE)/python_openzwave/ -name errors.log -delete
	-find $(ARCHBASE)/python_openzwave/ -name zwscene.xml -delete
	-find $(ARCHBASE)/python_openzwave/ -name zwbutton.xml -delete
	-find $(ARCHBASE)/python_openzwave/ -name pyozw.db -delete
	-rm -f $(ARCHBASE)/python_openzwave/src-lib/libopenzwave/libopenzwave.cpp
	-mkdir -p $(DISTDIR) || src-lib/
	cd $(ARCHBASE) && zip -r ../$(DISTDIR)/python_openzwave-${python_openzwave_version}.zip python_openzwave
	mv $(DISTDIR)/python_openzwave-${python_openzwave_version}.zip $(ARCHIVES)/
	@echo
	@echo "pypi_package for version ${python_openzwave_version} created"

push: develop
	-git commit -m "Auto-commit for docs" README.rst INSTALL_REPO.rst INSTALL_MAC.rst INSTALL_WIN.rst INSTALL_ARCH.rst COPYRIGHT.txt DEVEL.txt EXAMPLES.txt CHANGELOG.txt docs/
	-git push
	@echo
	@echo "Commits for branch master pushed on github."

commit: push
	@echo
	@echo "Commits for branches master pushed on github."

tag:
	git tag v${python_openzwave_version}
	git push origin v${python_openzwave_version}
	@echo
	@echo "Tag pushed on github."

validate-pr: uninstall clean update develop
	$(MAKE) venv-dev-autobuild-tests
	$(MAKE) venv-bdist_wheel-whl-autobuild-tests 
	$(MAKE) venv-bdist_wheel-autobuild-tests
#~ 	$(MAKE) venv-tests

new-version: validate-pr
	-$(MAKE) docs
	-git commit -m "Auto-commit for new-version" README.rst INSTALL_REPO.rst INSTALL_MAC.rst INSTALL_WIN.rst INSTALL_ARCH.rst LICENSE.txt COPYRIGHT.txt DEVEL.txt EXAMPLES.txt CHANGELOG.txt docs/
	git commit -m "Update pyozw_version to ${python_openzwave_version}" pyozw_version.py
	-$(MAKE) embed_openzave_master 
	-$(MAKE) pypi_package 
	-git add $(ARCHIVES)/python_openzwave-${python_openzwave_version}.zip && git commit -m "Add new pypi package" $(ARCHIVES)/python_openzwave-${python_openzwave_version}.zip && git push
	-git add $(ARCHIVES)/open-zwave-master-${python_openzwave_version}.zip && git commit -m "Add new embed package" $(ARCHIVES)/open-zwave-master-${python_openzwave_version}.zip && git push
	-git checkout $(ARCHIVES)/*
	-twine upload archives/python_openzwave-${python_openzwave_version}.zip -r pypitest
	-twine upload archives/python_openzwave-${python_openzwave_version}.zip -r pypi
	-$(MAKE) tag
	-$(MAKE) commit
	@echo
	@echo "New version ${python_openzwave_version} created and published"

debch:
	dch --newversion ${python_openzwave_version} --maintmaint "Automatic release from upstream"

deb:
	dpkg-buildpackage

venv-deps: common-deps
	apt-get install --force-yes -y python-all python-dev python3-all python3-dev python-virtualenv python-pip
#~ 	apt-get install --force-yes -y python-wheel-common python3-wheel python-wheel python-pip-whl
	apt-get install --force-yes -y pkg-config wget unzip zip
	pip install Cython
	pip install wheel

venv2:
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo
	@echo "New venv for python2"
	@echo
	@echo

	virtualenv --python=python2 venv2
	venv2/bin/pip install nose
	venv2/bin/pip install Cython wheel six
	venv2/bin/pip install 'Louie>=1.1'
	chmod 755 venv2/bin/activate
	-rm -f src-lib/libopenzwave/libopenzwave.cpp

	@echo
	@echo
	@echo "Venv for python2 created"
	@echo
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	
venv3:
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo
	@echo "New venv for python3"
	@echo
	@echo

	virtualenv --python=python3 venv3
	venv3/bin/pip install nose
	venv3/bin/pip install Cython wheel six
	venv3/bin/pip install 'PyDispatcher>=2.0.5'
	chmod 755 venv3/bin/activate
	-rm -f src-lib/libopenzwave/libopenzwave.cpp

	@echo
	@echo
	@echo "Venv for python3 created"
	@echo
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

venv2-dev: venv2 src-lib/libopenzwave/libopenzwave.cpp
	venv2/bin/python setup-lib.py install --flavor=dev
	venv2/bin/python setup-api.py install
	venv2/bin/python setup-manager.py install
	
venv3-dev: venv3 src-lib/libopenzwave/libopenzwave.cpp
	venv3/bin/python setup-lib.py install --flavor=dev
	venv3/bin/python setup-api.py install
#~  	venv3/bin/python setup-manager.py install

venv2-shared: venv2 src-lib/libopenzwave/libopenzwave.cpp
	venv2/bin/python setup-lib.py install --flavor=shared
	venv2/bin/python setup-api.py install
	venv2/bin/python setup-manager.py install
	
venv3-shared: venv3 src-lib/libopenzwave/libopenzwave.cpp
	venv3/bin/python setup-lib.py install --flavor=shared
	venv3/bin/python setup-api.py install
#~ 	venv3/bin/python setup-manager.py install

venv-clean:
	@echo "Clean files in venvs"
	-rm -rf venv2
	-rm -rf venv3
	-rm -f src-lib/libopenzwave/libopenzwave.cpp

venv-tests: venv2-dev venv3-dev
	@echo ==========================================================================================
	@echo
	@echo
	@echo "Launch tests for venv-autobuild-autobuild-tests."
	@echo
	@echo

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python2
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	-$(MAKE) PYTHON_EXEC=venv2/bin/python NOSE_EXEC=venv2/bin/nosetests tests
	
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python3
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	-$(MAKE) PYTHON_EXEC=venv3/bin/python NOSE_EXEC=venv3/bin/nosetests tests

	@echo
	@echo
	@echo "Tests for venv-autobuild-autobuild-tests done."
	@echo
	@echo
	@echo ==========================================================================================
	@echo

venv-autobuild-tests: clean
	@echo ==========================================================================================
	@echo
	@echo
	@echo "Launch tests for venv-autobuild-autobuild-tests."
	@echo
	@echo

	$(MAKE) venv-pypitest-autobuild-tests 
	$(MAKE) venv-pypilive-autobuild-tests
	$(MAKE) venv-embed-autobuild-tests 
	$(MAKE) venv-bdist_wheel-whl-autobuild-tests 
	$(MAKE) venv-bdist_wheel-autobuild-tests
	$(MAKE) venv-pypi-autobuild-tests 
	$(MAKE) venv-dev-autobuild-tests
	$(MAKE) venv-git-autobuild-tests 

	@echo
	@echo
	@echo "Tests for venv-autobuild-autobuild-tests done."
	@echo
	@echo
	@echo ==========================================================================================
	@echo

venv-continuous-autobuild-tests:
	@echo ==========================================================================================
	@echo
	@echo
	@echo "Launch tests for venv-continuous-autobuild-tests."
	@echo
	@echo

	-$(MAKE) venv-embed-autobuild-tests
	-$(MAKE) venv-embed_shared-autobuild-tests
	-$(MAKE) venv-git-autobuild-tests
	-$(MAKE) venv-git_shared-autobuild-tests
	-$(MAKE) venv-bdist_wheel-whl-autobuild-tests 
	-$(MAKE) venv-bdist_wheel-autobuild-tests
	-$(MAKE) venv-pypi-autobuild-tests 

	@echo
	@echo
	@echo "Tests for venv-continuous-autobuild-tests done."
	@echo
	@echo
	@echo ==========================================================================================
	@echo

venv-git-autobuild-tests: venv-clean venv2 venv3
	@echo ==========================================================================================
	@echo
	@echo
	@echo "Launch tests for venv-git-autobuild-tests."
	@echo
	@echo

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python2
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	venv2/bin/python setup-lib.py install --flavor=git
	venv2/bin/python setup-api.py install
	venv2/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python3
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	venv3/bin/python setup-lib.py install --flavor=git
	venv3/bin/python setup-api.py install
	venv3/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild

	@echo
	@echo
	@echo "Tests for venv-git-autobuild-tests done."
	@echo
	@echo
	@echo ==========================================================================================
	@echo

venv-pypitest-autobuild-tests: venv-clean venv2 venv3
	@echo ==========================================================================================
	@echo
	@echo
	@echo "Launch tests for venv-pypitest-autobuild-tests."
	@echo
	@echo

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python2
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	-rm -f libopenzwave*.so
	venv2/bin/pip install "urwid>=1.1.1"
	venv2/bin/pip install -i https://testpypi.python.org/pypi -vvv python_openzwave
	venv2/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	venv2/bin/pip install "Cython"
	venv2/bin/pip install -i https://testpypi.python.org/pypi -vvv python_openzwave --install-option="--flavor=git"
	venv2/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	venv2/bin/pip install -i https://testpypi.python.org/pypi -vvv python_openzwave --force --install-option="--flavor=git"
	venv2/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	venv2/bin/python  venv2/bin/pyozw_check
	venv2/bin/python  venv2/bin/pyozw_shell --help
	venv2/bin/pip uninstall python_openzwave -y

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python3
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	-rm -f libopenzwave*.so
	venv3/bin/pip install "urwid>=1.1.1"
	venv3/bin/pip install -i https://testpypi.python.org/pypi -vvv python_openzwave
	venv3/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	venv3/bin/pip install "Cython"
	venv3/bin/pip install -i https://testpypi.python.org/pypi -vvv python_openzwave --install-option="--flavor=git"
	venv3/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	venv3/bin/pip install -i https://testpypi.python.org/pypi -vvv python_openzwave --force --install-option="--flavor=git"
	venv3/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	venv3/bin/python  venv3/bin/pyozw_check
	venv3/bin/python  venv3/bin/pyozw_shell --help
	venv3/bin/pip uninstall python_openzwave -y

	-rm -f libopenzwave*.so
	@echo
	@echo "Tests for venv-pypitest-autobuild-tests done."
	@echo
	@echo
	@echo ==========================================================================================
	@echo

venv-pypilive-autobuild-tests: venv-clean
	@echo ==========================================================================================
	@echo
	@echo
	@echo "Launch tests for venv-pypilive-autobuild-tests."
	@echo
	@echo

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python2
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	-rm -Rf venv2/
	virtualenv --python=python2 venv2
	chmod 755 venv2/bin/activate
	-rm -f src-lib/libopenzwave/libopenzwave.cpp
	-rm -f libopenzwave*.so
	venv2/bin/pip install "urwid>=1.1.1"
	venv2/bin/pip install "nose"
	venv2/bin/pip install -vv python_openzwave
	venv2/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
#~ 	venv2/bin/pip install Cython wheel
	venv2/bin/pip install -vv python_openzwave --upgrade --install-option="--flavor=git"
	venv2/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	venv2/bin/pip uninstall python_openzwave -y
	venv2/bin/pip install -vv python_openzwave --upgrade --install-option="--flavor=git"
	venv2/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	venv2/bin/pip uninstall python_openzwave -y

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python3
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	-rm -Rf venv3/
	virtualenv --python=python3 venv3
	chmod 755 venv3/bin/activate
	-rm -f src-lib/libopenzwave/libopenzwave.cpp
	-rm -f libop1enzwave*.so
	venv3/bin/pip install "nose"
	venv3/bin/pip install "urwid>=1.1.1"
	venv3/bin/pip install -vv python_openzwave
	venv3/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
#~ 	venv3/bin/pip install Cython wheel
	venv3/bin/pip install -vv python_openzwave --upgrade --install-option="--flavor=git"
	venv3/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	venv3/bin/pip uninstall python_openzwave -y
	venv3/bin/pip install -vv python_openzwave --upgrade --install-option="--flavor=git"
	venv3/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	venv3/bin/pip uninstall python_openzwave -y

	-rm -f libopenzwave*.so
	@echo
	@echo "Tests for venv-pypilive-autobuild-tests done."
	@echo
	@echo
	@echo ==========================================================================================
	@echo

venv-git_shared-autobuild-tests: venv-clean venv2 venv3
	@echo ==========================================================================================
	@echo
	@echo
	@echo "Launch tests for venv-git_shared-autobuild-tests."
	@echo
	@echo

	$(MAKE) uninstall
	$(MAKE) uninstallso
	-pkg-config --libs libopenzwave
	
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python2
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	venv2/bin/python setup-lib.py install --flavor=git_shared
	venv2/bin/python setup-api.py install
	venv2/bin/python setup-manager.py install
	venv2/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild
	find /usr/local/etc/openzwave -iname device_classes.xml -type f -exec cat '{}' \;|grep open-zwave
	test -f venv2/lib/python*/site-packages/libopenzwave*.so
	venv2/bin/python  venv2/bin/pyozw_check
	pkg-config --libs libopenzwave

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python3
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	venv3/bin/python setup-lib.py install --flavor=git_shared
	venv3/bin/python setup-api.py install
#~ 	venv3/bin/python setup-manager.py install
	venv3/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild
	find /usr/local/etc/openzwave -iname device_classes.xml -type f -exec cat '{}' \;|grep open-zwave
	test -f venv3/lib/python*/site-packages/libopenzwave*.so
	venv3/bin/python  venv3/bin/pyozw_check
	pkg-config --libs libopenzwave

	@echo
	@echo
	@echo "Tests for venv-git-autobuild-tests done."
	@echo
	@echo
	@echo ==========================================================================================
	@echo

venv-embed-autobuild-tests: venv-clean venv2 venv3
	@echo ==========================================================================================
	@echo
	@echo
	@echo "Launch tests for venv-embed-autobuild-tests."
	@echo
	@echo

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python2
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	-rm -f libopenzwave*.so
	venv2/bin/pip uninstall -y wheel
	venv2/bin/pip install "urwid>=1.1.1"
	venv2/bin/pip uninstall -y Cython
	venv2/bin/python setup.py install --flavor=embed
	venv2/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	test -f venv2/lib/python*/site-packages/libopenzwave*.so

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python3
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	-rm -f libopenzwave*.so
	venv3/bin/pip uninstall -y wheel
	venv3/bin/pip install "urwid>=1.1.1"
	venv3/bin/pip uninstall -y Cython
	venv3/bin/python setup.py install --flavor=embed
	venv3/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	test -f venv3/lib/python*/site-packages/libopenzwave*.so

	-rm -f libopenzwave*.so
	@echo
	@echo
	@echo "Tests for venv-embed-autobuild-tests done."
	@echo
	@echo
	@echo ==========================================================================================
	@echo

venv-embed_shared-autobuild-tests: venv-clean venv2 venv3
	@echo ==========================================================================================
	@echo
	@echo
	@echo "Launch tests for venv-embed_shared-autobuild-tests."
	@echo
	@echo

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python2
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	-rm -f libopenzwave*.so
	venv2/bin/pip install "urwid>=1.1.1"
	venv2/bin/pip uninstall -y Cython
	venv2/bin/python setup.py install --flavor=embed_shared
	venv2/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	test -f venv2/lib/python*/site-packages/libopenzwave*.so

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python3
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	-rm -f libopenzwave*.so
	venv3/bin/pip install "urwid>=1.1.1"
	venv3/bin/pip uninstall -y Cython
	venv3/bin/python setup.py install --flavor=embed_shared
	venv3/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	test -f venv3/lib/python*/site-packages/libopenzwave*.so

	-rm -f libopenzwave*.so
	@echo
	@echo
	@echo "Tests for venv-embed-autobuild-tests done."
	@echo
	@echo
	@echo ==========================================================================================
	@echo

venv-pypi-autobuild-tests: venv-clean pypi_package
	@echo ==========================================================================================
	@echo
	@echo
	@echo "Launch tests for venv-pypi-autobuild-tests."
	@echo
	@echo

	-rm -f dist/*.whl
	-rm -Rf tmp/pypi_test/
	-mkdir -p tmp/pypi_test/
	cd tmp/pypi_test/ && unzip ../../$(ARCHIVES)/python_openzwave-${python_openzwave_version}.zip

	virtualenv --python=python2 venv2
	chmod 755 venv2/bin/activate
	-rm -f src-lib/libopenzwave/libopenzwave.cpp
	-rm -f libopenzwave*.so
	venv2/bin/pip install "wheel"
	venv2/bin/pip install "urwid>=1.1.1"
	venv2/bin/pip install "Cython"
	. venv2/bin/activate && cd tmp/pypi_test/python_openzwave && python setup.py install
	. venv2/bin/activate && cd tmp/pypi_test/python_openzwave && python setup.py bdist_wheel --flavor=git
	
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python2
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	virtualenv --python=python3 venv3
	chmod 755 venv3/bin/activate
	-rm -f src-lib/libopenzwave/libopenzwave.cpp
	-rm -f libop1enzwave*.so
	venv3/bin/pip install "wheel"
	venv3/bin/pip install "urwid>=1.1.1"
	venv3/bin/pip install "Cython"
	. venv2/bin/activate && cd tmp/pypi_test/python_openzwave && python setup.py install
	. venv2/bin/activate && cd tmp/pypi_test/python_openzwave && python setup.py bdist_wheel --flavor=git

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python3
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	. venv3/bin/activate && cd tmp/pypi_test/python_openzwave && python setup.py bdist_wheel --flavor=git
	
	-mkdir -p dist	
	cp tmp/pypi_test/python_openzwave/dist/*.whl dist/
	
	$(MAKE) venv-bdist_wheel-autobuild-tests

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python2
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	. venv2/bin/activate && cd tmp/pypi_test/python_openzwave && python setup.py install --force --flavor=git
	. venv2/bin/activate && python  venv2/bin/pyozw_check
	. venv2/bin/activate && cd tmp/pypi_test/python_openzwave && python setup.py clean --all --flavor=git
	find venv2/lib/ -iname device_classes.xml -type f -print|cat

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python3
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	. venv3/bin/activate && cd tmp/pypi_test/python_openzwave && python setup.py install --force --flavor=git
	. venv3/bin/activate && python venv3/bin/pyozw_check
	. venv3/bin/activate && cd tmp/pypi_test/python_openzwave && python setup.py clean --all --flavor=git
	find venv3/lib/ -iname device_classes.xml -type f -print|cat
	
	@echo
	@echo
	@echo "Tests for venv-pypi-autobuild-tests done."
	@echo
	@echo
	@echo ==========================================================================================
	@echo

venv-bdist_wheel-whl-autobuild-tests: venv-clean venv2 venv3
	@echo ==========================================================================================
	@echo
	@echo
	@echo "Create tests whl for venv-bdist_wheel-autobuild-tests."
	@echo
	@echo
	
	-rm -f dist/*.whl

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python2
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	venv2/bin/python setup.py install --flavor=git
	venv2/bin/python setup.py bdist_wheel --flavor=git

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python3
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	venv3/bin/python setup.py install --flavor=git
	venv3/bin/python setup.py bdist_wheel --flavor=git
	
	@echo
	@echo
	@echo "Tests for venv-bdist_wheel-autobuild-tests created."
	@echo
	@echo
	@echo ==========================================================================================
	@echo

venv-bdist_wheel-autobuild-tests: venv-clean
	@echo ==========================================================================================
	@echo
	@echo
	@echo "Launch tests for venv-bdist_wheel-autobuild-tests."
	@echo
	@echo

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python2
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	
	-rm -Rf venv2
	virtualenv --python=python2 venv2
	chmod 755 venv2/bin/activate
	-rm -f src-lib/libopenzwave/libopenzwave.cpp
	-rm -f libopenzwave*.so

	venv2/bin/pip install "wheel"
	venv2/bin/pip install "nose"
#~ 	venv2/bin/pip install "Cython"
	venv2/bin/pip install "urwid>=1.1.1"
	
	venv2/bin/pip install dist/python_openzwave-${python_openzwave_version}-cp2*
	venv2/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	find venv2/lib/ -iname device_classes.xml -type f -exec cat '{}' \;|grep open-zwave
	test -f venv2/lib/python*/site-packages/libopenzwave*.so
	venv2/bin/pip uninstall -y "${WHL_PYTHON2}"
	#test ! -f venv2/lib/python*/site-packages/libopenzwave*.so

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python3
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	-rm -Rf venv3
	virtualenv --python=python3 venv3
	chmod 755 venv3/bin/activate
	-rm -f src-lib/libopenzwave/libopenzwave.cpp
	-rm -f libopenzwave*.so

	venv2/bin/pip install "wheel"
	venv3/bin/pip install "nose"
#~ 	venv3/bin/pip install "Cython"
	venv3/bin/pip install "urwid>=1.1.1"
	venv3/bin/pip install dist/python_openzwave-${python_openzwave_version}-cp3*
	venv3/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	find venv3/lib/ -iname device_classes.xml -type f -exec cat '{}' \;|grep open-zwave
	test -f venv3/lib/python*/site-packages/libopenzwave*.so
	venv3/bin/pip uninstall -y "${WHL_PYTHON3}"
	#test ! -f venv3/lib/python*/site-packages/libopenzwave*.so
	
	@echo
	@echo
	@echo "Tests for venv-bdist_wheel-autobuild-tests done."
	@echo
	@echo
	@echo ==========================================================================================
	@echo

venv-dev-autobuild-tests: venv-clean venv2 venv3 src-lib/libopenzwave/libopenzwave.cpp
	@echo ==========================================================================================
	@echo
	@echo
	@echo "Launch tests for venv-dev-autobuild-tests."
	@echo
	@echo

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python2
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	-rm -f libopenzwave*.so
	venv2/bin/python setup-lib.py install --flavor=dev
	venv2/bin/python setup-api.py install
	venv2/bin/python setup-manager.py install
	venv2/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild tests/manager/autobuild
	venv2/bin/python  venv2/bin/pyozw_check	

	venv2/bin/python2 -u -c "import setuptools, tokenize;__file__='setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/install-record.txt --single-version-externally-managed --compile --install-headers venv2/include/site/python2.7/python-openzwave "--flavor=git"

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python3
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	-rm -f libopenzwave*.so
	venv3/bin/python setup-lib.py install --flavor=dev
	venv3/bin/python setup-api.py install
#~ 	venv3/bin/python setup-manager.py install
	venv3/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild
	venv3/bin/python  venv3/bin/pyozw_check	
	
	venv3/bin/python3 -u -c "import setuptools, tokenize;__file__='setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/install-record.txt --single-version-externally-managed --compile --install-headers venv3/include/site/python3.5/python-openzwave "--flavor=git"

	-rm -f libopenzwave*.so
	@echo
	@echo
	@echo "Tests for venv-dev-autobuild-tests done."
	@echo
	@echo
	@echo ==========================================================================================
	@echo

venv-shared-autobuild-tests: venv-clean venv2-shared venv3-shared
	@echo ==========================================================================================
	@echo
	@echo
	@echo "Launch tests for venv-shared-autobuild-tests."
	@echo
	@echo

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python2
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	venv2/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild
	venv2/bin/python  venv2/bin/pyozw_check

	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo
	@echo Tests for python3
	@echo
	@echo ////////////////////////////////////////////////////////////////////////////////////////////
	@echo

	venv3/bin/nosetests --verbose tests/lib/autobuild tests/api/autobuild
	venv3/bin/python  venv3/bin/pyozw_check
	
	@echo
	@echo
	@echo "Tests for venv-shared-autobuild-tests done."
	@echo
	@echo
	@echo ==========================================================================================
	@echo

buildso: openzwave/.lib/
	cd openzwave && $(MAKE) install    

uninstallso:
	rm -f /usr/local/lib/x86_64-linux-gnu/pkgconfig/libopenzwave.pc
	rm -f /usr/local/lib64/libopenzwave.so.1.4
	rm -f /usr/local/lib64/libopenzwave.so
	rm -Rf /usr/local/include/openzwave
	rm -Rf /usr/local/etc/openzwave
	rm -Rf /usr/local/share/doc/openzwave*
	
pyozw_pkgconfig.py:
	wget https://raw.githubusercontent.com/matze/pkgconfig/master/pkgconfig/pkgconfig.py
	mv pkgconfig.py pyozw_pkgconfig.py
