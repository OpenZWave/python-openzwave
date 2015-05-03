# -*- coding: utf-8 -*-

"""Storing all the module configurations. Here, the database is setup to use SQLite, because it's a very convenient dev env database.
Most likely /config.py won't be a part of your repository and will be different on your test and production servers.

 - _basedir is a trick for you to get the folder where the script runs
 - DEBUG indicates that it is a dev environment, you'll get the very helpful error page from flask when an error occurs.
 - SECRET_KEY will be used to sign cookies. Change it and all your users will have to login again.
 - ADMINS will be used if you need to email information to the site administrators.
 - SQLALCHEMY_DATABASE_URI and DATABASE_CONNECT_OPTIONS are SQLAlchemy connection options (hard to guess)
 - THREAD_PAGE my understanding was 2/core... might be wrong :)
 - CSRF_ENABLED and CSRF_SESSION_KEY are protecting against form post fraud
 - RECAPTCHA_* WTForms comes with a RecaptchaField ready to use... just need to go to recaptcha website and get your public and private key.

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

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    RELOADER = False
    DATABASE_URI = 'sqlite://:memory:'

    HOST = "127.0.0.1"
    PORT = "5000"

    LOGGING_CONF = 'logging.conf'
    APP_CONF = 'app.conf'

    SECRET_KEY = 'This string will be replaced with a proper key in production.'

    THREADS_PER_PAGE = 8

    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "somethingimpossibletoguess"

    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
    RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
    RECAPTCHA_OPTIONS = {'theme': 'white'}

    ZWAVE_DEVICE = "/dev/ttyUSB1"
    ZWAVE_DEBUG = "Debug"
    ZWAVE_LOGGING = True
    ZWAVE_DIR = None
    USER_DIR = "."

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'
    ZWAVE_DEBUG = "Warning"

class RunConfig(Config):
    TESTING = True
    DEBUG = True
    ZWAVE_DIR = "../../openzwave/config"

class ReloadConfig(Config):
    TESTING = True
    DEBUG = True
    RELOADER = True
    ZWAVE_DIR = "../../openzwave/config"

class TestingConfig(Config):
    TESTING = True
    LOGGING_CONF = 'tests/logging.conf'
    DEBUG = True

