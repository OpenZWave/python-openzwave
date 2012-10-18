#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    This application requires Flask.

    Application is based in large part upon Francisco Souza's flask REST
    example (https://github.com/franciscosouza/flask-rest-example)

    /info       basic system information
    /nodes
    /nodes?class=BATTERY: only show nodes containing specified command class

    /nodes/{n}   basic node information
    /nodes/{n}/[id,name*,location*,capabilities,neighbors,manufacturer*,product*,productType]

    /nodes/2?command=[on,off,dim,bright] - simple, straightforward, turn on or off
    /nodes/2?command=level&value=38

    /nodes/2/groups: list groups
    /nodes/2/groups/1/

    /nodes/{n}/values
    /nodes/2/values?class=SWITCH_MULTILEVEL

    /nodes/{n}/values/{v}: v can be id or label
    /nodes/2/values/Basic?method=put&value=255
'''
from collections import namedtuple
import logging
import threading
import time

from werkzeug import url_decode
from openzwave.wrapper.wrapper import ZWaveWrapper, ZWaveNode, ZWaveValueNode
from flask import Flask, render_template, request, redirect, url_for, flash, g
from functools import wraps

from flaskext import wtf
from flaskext.wtf import validators

class MethodRewriteMiddleware(object):
    """Middleware for HTTP method rewriting.

    Snippet: http://flask.pocoo.org/snippets/38/
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if 'METHOD_OVERRIDE' in environ.get('QUERY_STRING', ''):
            args = url_decode(environ['QUERY_STRING'])
            method = args.get('__METHOD_OVERRIDE__')
            if method:
                method = method.encode('ascii', 'replace')
                environ['REQUEST_METHOD'] = method
        return self.app(environ, start_response)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret'
app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)

FORMAT='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
log = logging.getLogger('zwave_server')

ZWaveInfo = namedtuple('ZWaveInfo', ['device','library','version','homeId','controller', 'controllerId','nodeCount','sleepingCount'])

def get_info():
    w = g.wrapper
    return ZWaveInfo(device=w.device, library=w.libraryTypeName, version=w.libraryVersion,
                     homeId=w.homeId, controller=w.controllerDescription, controllerId=w.controllerNodeId,
                     nodeCount=w.nodeCount, sleepingCount=w.sleepingNodeCount)

def requires_network(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.wrapper.initialized:
            return redirect(url_for('show_status'))
        return f(*args, **kwargs)
    return decorated_function

def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator

def get_nodes(criteria=None):
    return g.wrapper.nodes.itervalues()

def get_node(id):
    # TODO: node needs flags/list/etc to indicate what fields are editable
    return g.wrapper.nodes[id]

class dummy:
    _i = False
    initialized = property(lambda self: self._i)

@app.before_request
def before_request():
    g.wrapper = ZWaveWrapper.getInstance(device='/dev/ttyUSB0', config='../openzwave/config/', log=log)
    #g.wrapper = dummy()

@app.route('/')
@templated(template='status.html')
def show_info():
    return {'wrapper':g.wrapper}

@app.route('/status')
@templated(template='status.html')
def show_status():
    # TODO: mark process start/end time in wrapper, display elapsed time
    return {'wrapper':g.wrapper}

@app.route('/nodes')
@templated()
@requires_network
def list_nodes():
    # TODO: list criteria
    # TODO: how to communicate available commands for node to client?
    return dict(nodes=get_nodes())

@app.route('/nodes/<id>', methods=['GET','PUT'])
@templated()
@requires_network
def show_node(id):
    node = get_node(int(id))
    if request.method == 'GET':
        if 'command' in request.args:
            qs = request.args['command']
            levelChange = 0

            if qs == 'on':
                g.wrapper.setNodeOn(node)
            elif qs == 'off':
                g.wrapper.setNodeOff(node)
            elif qs in ['dim', 'bright']:
                if qs == 'dim': 
                    levelChange = -10
                elif qs == 'bright': 
                    levelChange = 10
                curLevel = node.level
                print "current level: " + str(curLevel)
                newLevel = curLevel + levelChange
                print "new level: " + str(newLevel)
                if (0 <= newLevel and newLevel <= 100):
                    g.wrapper.setNodeLevel(node, newLevel)
             
    return dict(node=node)

    # TODO: command param, execute if set (and if method is put)
    # /nodes/<id>?command=on <-- validate command
    # TODO: how to communicate available commands for node to client?
    # TODO: form post for basic values
    # TODO: how to communicate which fields are editable to client?
    # TODO: add classes

@app.route('/nodes/<id>/groups')
@templated()
@requires_network
def list_groups(id):
    pass

@app.route('/nodes/<id>/groups/<gid>', methods=['GET','PUT','DELETE'])
@templated()
@requires_network
def show_group(id, gid):
    pass
    # TODO: edit group label (PUT)
    # TODO: remove item from group (DELETE)
    # TODO: add item to group (PUT)

@app.route('/nodes/<id>/values')
@templated()
@requires_network
def list_values(id):
    pass

@app.route('/nodes/<id>/values/<vid>', methods=['GET','PUT'])
@templated()
@requires_network
def show_value(id, vid):
    pass

if __name__ == '__main__':
    app.run('0.0.0.0')
