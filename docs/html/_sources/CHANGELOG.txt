:orphan:
=========
Changelog
=========


To do for python-openzwave 0.3.0-final :

 * Fix pyozwman
 * Add more tests for the library : switches, dimmers, polling, heal, test, ...
 * Fix reloader problem : the network ist stop/start every time the app is realoaded. But in this case, the process terminates normally. But there seems to be 2 running instances of the network.


python-openzwave 0.3.0-alpha3:

 * Fix bug in start/stop in network.
 * Fix bug in start/stop in pyozwweb app and tests.
 * Add map, scenes to PyOzwWeb
 * Add new tests
 * Fix some tests for controller commands
 * Finish the archive install : the lib is already cythonized. No need to install cython anymore.


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
