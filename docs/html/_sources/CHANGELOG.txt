:orphan:
=========
Changelog
=========


To do for python-openzwave 0.3.0-final :

 * Finish the archive install
 * Fix pyozwman
 * Add more tests for the library : switches, dimmers, polling, heal, test, ...
 * Fix tests for controller commands
 * Fix reloader problem : the network ist stop/start every time the app is realoaded. But in this case, the process terminates normally. But there seems to be 2 running instances of the network.


python-openzwave 0.3.0-alpha3:

 * Fix bug in start/stop in pyozwwzb app and tests. The listener doesn't stop. So must do a kill -9.
 * Add map, scenes to PyOzwXeb


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
