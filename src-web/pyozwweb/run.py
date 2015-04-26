#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Used to launch the web server.

Credits : https://github.com/mitsuhiko/flask/wiki/Large-app-how-to

"""

__license__ = """

This file is part of **python-openzwave** project https://github.com/bibi21000/python-openzwave.

License : GPL(v3)

**python-openzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**python-openzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with python-openzwave. If not, see http://www.gnu.org/licenses.
"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'

from pyozwweb.app import create_app, run_app

def main():
    app, socketio = create_app(config_object='pyozwweb.config.RunConfig')
    run_app(app, socketio)
    #app.run(debug=True)
    #socketio.run(app)
    #print app

if __name__ == '__main__':
    main()
