:orphan:

=========
Changelog
=========

Known bugs

 * reloader problem : the network stop/start every time the app is realoaded. But in this case, the process terminates normally.
   But there seems to be 2 running instances of the network.

python-openzwave 0.3.0-beta8:
 * Improve unicode
 * Add minimal Python 3 support

python-openzwave 0.3.0-beta3:
 * Add security rewrite support. See https://groups.google.com/forum/#!msg/openzwave/cPjrvJJaESY/toK7QxEgRn0J
 * Add 2 signals for controller commands : ZWaveNetwork.SIGNAL_CONTROLLER_COMMAND and ZWaveNetwork.SIGNAL_CONTROLLER_WAITING
 * Mark old methods and signals as deprecated. It is strongly recommended to use the new schema.
 * Add tests for controller commands.
 * Update isNodeAwake from function to property
 * Rename methods from node to be python compliant : is_awake, is_failed, is_ready, query_stage, is_info_received
 * Add facilities to run controller commands directly from node
 * Add request_state for node
 * Add new destroy method to network : use it to clean all openzwave c++ ressources


python-openzwave 0.3.0-beta2:
 * Move to OpenZWave git organisation


python-openzwave 0.3.0-beta1:
 * Add pyozwman script : after installing you can launch it wit : Usage: ozwsh [--device=/dev/ttyUSB0] [--log=Debug] ...
 * Add pyozwweb confiuration file.
 * Add version management in Makefile.


python-openzwave 0.3.0-alpha3:

 * Fix bug in start/stop in network.
 * Fix bug in start/stop in pyozwweb app and tests.
 * Add map, scenes to PyOzwWeb
 * Add new tests
 * Fix some tests for controller commands
 * Finish the archive install : the lib is already cythonized. No need to install cython anymore.
 * Add a dockerfile
 * Add a branch for dockering with ptyhon 3


python-openzwave 0.3.0-alpha2:

 * Fix bugs in lib
 * Fix bugs in API
 * Add kvals to API : allow user to store parameters with nodes, controllers, networks, ...
 * A a web demo : Flask + socket.io + jquery
 * Add logging facilities in the lib. Define different loggers for lib and api.


python-openzwave 0.3.0-alpha1:

 * Update source tree to use setupttols develop mode : https://bitbucket.org/pypa/setuptools/issue/230/develop-mode-does-not-respect-src
 * Rewrite tests to use nosetest
 * Full implementation and tests of Options
 * PyLogLevels is now a dict of dicts to include doc : replace PyLogLevels[level] with PyLogLevels[level]['value'] in your code
 * Remove old scripts. Replace them with a Makefile
 * Remove old unworking examples.
 * Add a constructor for PyOptions : def __init__(self, config_path=None, user_path=".", cmd_line=""). Please update your code.
