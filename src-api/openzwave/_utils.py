# -*- coding: utf-8 -*-
"""
.. module:: openzwave._utils

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave API

.. moduleauthor: Kevin Schlosser (@kdschlosser)

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

# This module contains decorators that enable data path debugging. It also
# contains a decorator for notification of depreciated items. This includes
# classes, functions, methods, properties (set and get separately), and also
# variables. variables only produce a warning when the actual variable is
# accessed.


from __future__ import print_function

import warnings
import logging
import inspect
import threading
import traceback
import sys
import time
from functools import update_wrapper

logger = logging.getLogger(__name__)

PY3 = sys.version_info[0] > 2

DEPRECATED_LOGGING_TEMPLATE = '''\
[DEPRECATED]\
{thread_name}\
[{thread_id}] - \
{object_type}
src: {calling_obj} [{calling_filename}:{calling_line_no}]
dst: {called_obj} [{called_filename}:{called_line_no}]
'''

LOGGING_TEMPLATE = '''\
[DEBUG-DATA PATH]\
{{0}} - \
{thread_name}\
[{thread_id}]
src: {calling_obj} [{calling_filename}:{calling_line_no}]
dst: {called_obj} [{called_filename}:{called_line_no}]
{msg}
'''


def _get_line_and_file(stacklevel=2):
    """
    Gets the filename and also the line number in the file where the code is
    that is making a call and also where it is calling.
    """
    try:
        caller = sys._getframe(stacklevel)
    except ValueError:
        glbs = sys.__dict__
        line_no = 1
    else:
        glbs = caller.f_globals
        line_no = caller.f_lineno
    if '__name__' in glbs:
        module = glbs['__name__']
    else:
        module = "<string>"
    filename = glbs.get('__file__')
    if filename:
        fnl = filename.lower()
        if fnl.endswith((".pyc", ".pyo")):
            filename = filename[:-1]
    else:
        if module == "__main__":
            try:
                filename = sys.argv[0]
            except AttributeError:
                # embedded interpreters don't have sys.argv, see bug #839151
                filename = '__main__'
        if not filename:
            filename = module

    return filename, int(line_no)


def _get_stack(frame):
    frames = []
    while frame:
        frames += [frame]
        frame = frame.f_back
    return frames


def _caller_name(start=2):
    """
    This function creates a `"."` separated name for where the call is being
    made from. an example would be `"openzwave.node.ZWaveNode.product_id"`

    This function also handles nested functions and classes alike.
    """
    stack = _get_stack(sys._getframe(1))

    def get_name(s):
        if len(stack) < s + 1:
            return []
        parent_frame = stack[s]

        name = []
        module = inspect.getmodule(parent_frame)
        if module:
            name.append(module.__name__)

        codename = parent_frame.f_code.co_name
        if codename not in ('<module>', '__main__'):  # top level usually
            frame = parent_frame
            if 'self' in frame.f_locals:
                name.append(frame.f_locals['self'].__class__.__name__)
                name.append(codename)  # function or a method
            else:
                name.append(codename)  # function or a method
                frame = frame.f_back
                while codename in frame.f_locals:
                    codename = frame.f_code.co_name
                    if codename in ('<module>', '__main__'):
                        break
                    name.append(codename)
                    frame = frame.f_back

        del parent_frame
        return name

    res = get_name(start)

    if not res or 'pydev_run_in_console' in res:
        res = get_name(start - 1)

    if res == ['<module>'] or res == ['__main__']:
        res = get_name(start - 1)
        if 'log_it' in res:
            res = get_name(start)

    if 'wrapper' in res:
        res = get_name(start + 1) + get_name(start - 1)[-1:]

    return ".".join(res)


def log_it(func):
    """
    log_it

    This function is a decorator. It's sole purpose is to be able to track
    the data path. It is a very useful tool during the debugging process.

    It creates a debugging log entry containing where the call is made from.
    the location of the function\method\property. that has been wrapped by
    this decorator. As well as the parameter names and data that was passed
    including any defaulted parameters.
    """
    if PY3:
        if func.__code__.co_flags & 0x20:
            return func
    else:
        if func.func_code.co_flags & 0x20:
            return func

    lgr = logging.getLogger(func.__module__)
    func_name = _caller_name(1)
    if func_name:
        func_name += '.' + func.__name__
    else:
        func_name = func.__module__ + '.' + func.__name__

    called_filename, called_line_no = _get_line_and_file(2)
    called_line_no += 1

    def wrapper(*args, **kwargs):
        if lgr.getEffectiveLevel() == logging.DEBUG:
            calling_filename, calling_line_no = _get_line_and_file(2)
            thread = threading.current_thread()
            arg_string = _func_arg_string(func, args, kwargs)
            calling_obj = _caller_name()
            msg = LOGGING_TEMPLATE.format(
                thread_name=thread.getName(),
                thread_id=thread.ident,
                calling_obj=calling_obj,
                calling_filename=calling_filename,
                calling_line_no=calling_line_no,
                called_obj=func_name,
                called_filename=called_filename,
                called_line_no=called_line_no,
                msg=func_name + arg_string
            )
            lgr.debug(msg)

        return func(*args, **kwargs)

    return update_wrapper(wrapper, func)


def log_it_with_return(func):
    """
    log_it_with_return

    This id a decorator just like log_it. It functions exactly the same
    except it will also log the data that is being returned by the wrapped
    function\method\property.
    """
    if PY3:
        if func.__code__.co_flags & 0x20:
            return func
    else:
        if func.func_code.co_flags & 0x20:
            return func

    lgr = logging.getLogger(func.__module__)
    func_name = _caller_name(1)
    if func_name:
        func_name += '.' + func.__name__
    else:
        func_name = func.__module__ + '.' + func.__name__

    called_filename, called_line_no = _get_line_and_file(2)
    called_line_no += 1

    def wrapper(*args, **kwargs):
        if lgr.getEffectiveLevel() == logging.DEBUG:
            calling_filename, calling_line_no = _get_line_and_file(2)
            thread = threading.current_thread()
            arg_string = _func_arg_string(func, args, kwargs)
            calling_obj = _caller_name()
            msg = LOGGING_TEMPLATE.format(
                thread_name=thread.getName(),
                thread_id=thread.ident,
                calling_obj=calling_obj,
                calling_filename=calling_filename,
                calling_line_no=calling_line_no,
                called_obj=func_name,
                called_filename=called_filename,
                called_line_no=called_line_no,
                msg=func_name + arg_string
            )
            lgr.debug(msg)
            result = func(*args, **kwargs)
            msg = LOGGING_TEMPLATE.format(
                thread_name=thread.getName(),
                thread_id=thread.ident,
                calling_obj=calling_obj,
                calling_filename=calling_filename,
                calling_line_no=calling_line_no,
                called_obj=func_name,
                called_filename=called_filename,
                called_line_no=called_line_no,
                msg='{0} => {1}'.format(func_name, repr(result))
            )
            lgr.debug(msg)
        else:
            result = func(*args, **kwargs)

        return result

    return update_wrapper(wrapper, func)


def log_it_with_timer(func):
    """
    log_it_with_timer

    Another decorator, this function does exactly the same thing as the log_it
    decorator and adds on how long it took to run the wrapped
    function\method\property. It is a handy tool to isolate slow code.
    """

    if PY3:
        if func.__code__.co_flags & 0x20:
            return func
    else:
        if func.func_code.co_flags & 0x20:
            return func

    lgr = logging.getLogger(func.__module__)

    func_name = _caller_name(1)
    if func_name:
        func_name += '.' + func.__name__
    else:
        func_name = func.__module__ + '.' + func.__name__

    called_filename, called_line_no = _get_line_and_file(2)
    called_line_no += 1

    def wrapper(*args, **kwargs):
        if lgr.getEffectiveLevel() == logging.DEBUG:
            calling_filename, calling_line_no = _get_line_and_file(2)
            thread = threading.current_thread()
            arg_string = _func_arg_string(func, args, kwargs)
            calling_obj = _caller_name()
            msg = LOGGING_TEMPLATE.format(
                thread_name=thread.getName(),
                thread_id=thread.ident,
                calling_obj=calling_obj,
                calling_filename=calling_filename,
                calling_line_no=calling_line_no,
                called_obj=func_name,
                called_filename=called_filename,
                called_line_no=called_line_no,
                msg=''
            )
            lgr.debug(msg + func_name + arg_string)

            start = time.time()
            result = func(*args, **kwargs)
            stop = time.time()

            resolutions = (
                (1, 'sec'),
                (1000, 'ms'),
                (1000000, u'us'),
                (1000000000, 'ns'),
            )

            for divider, suffix in resolutions:
                duration = int(round((stop - start) / divider))
                if duration > 0:
                    break
            else:
                duration = 'unknown'
                suffix = ''

            lgr.debug(msg + 'duration: {0} {1} - {2} => {3}'.format(
                    duration,
                    suffix,
                    func_name,
                    repr(result)
                )
            )
        else:
            result = func(*args, **kwargs)

        return result

    return update_wrapper(wrapper, func)


def _func_arg_string(func, args, kwargs):
    """
    This function is used to get the parameter names and also any default
    arguments.
    """

    if PY3:
        # noinspection PyUnresolvedReferences
        arg_names = inspect.getfullargspec(func)[0]
    else:
        arg_names = inspect.getargspec(func)[0]

    start = 0
    if arg_names:
        if arg_names[0] == "self":
            start = 1

    res = []
    append = res.append

    for key, value in list(zip(arg_names, args))[start:]:
        append(str(key) + "=" + repr(value).replace('.<locals>.', '.'))

    for key, value in kwargs.items():
        append(str(key) + "=" + repr(value).replace('.<locals>.', '.'))

    return "(" + ", ".join(res) + ")"


def deprecated(obj, msg=''):
    """
    deprecated

    This is my crowning jewel of utilities. It is a decorator that is used to
    display deprecated warnings.

    This decorator works like no other you have seen before it. It can handle
    functions, methods, classes, properties and all variables of any data type.

    If used as a decorator a custom message cannot be supplied. if wanting to
    only deprecate the set portion of a property and not the get you cannot
    use this as a decorator. you cannot decorate a variable either. I have
    code examples below of how to use this function.


    Example without any custom messages

    .. code-block:: python

        some_module_level_variable = deprecated('any data type')

        @deprecated
        def some_function():
            some_function_variable = deprecated(5)

        @deprecated
        class SomeClass(object):
            some_class_level_variable = deprecated(['list', 1, 2, 3])


            @deprecated
            def some_method(self):
               some_method_level_variable = deprecated({'dict key': 'dict value'})

                @deprecated
                def some_nested_function():
                    some_nested_function_variable = deprecated(('tuple', 1, 2, 3, 4))
                    pass

            @deprecated
            @property
            def get_set_property(self):
                pass

            @deprecated
            @get_set_property.setter
            def get_set_property(self, value):
                pass

            @deprecated
            @property
            def only_get_property(self):
                pass

            @only_get_property.setter
            def only_get_property(self, value):
                pass

            @property
            def __get_only_set_property(self):
                pass

            def __set_only_set_property(self, value):
                pass

            only_set_property = property(fset=__set_only_set_property)
            only_set_property = deprecated(only_set_property)
            only_set_property.fget = __get_only_set_property


    Example with custom messages

    .. code-block:: python

        some_module_level_variable = deprecated('any data type', 'custom message')

        def some_function():
            some_function_variable = deprecated(5, 'custom message')

        some_function = deprecated(some_function, 'custom message')

        class SomeClass(object):
            some_class_level_variable = deprecated(['list', 1, 2, 3], 'custom message')


            @deprecated
            def some_method(self):
               some_method_level_variable = deprecated({'dict key': 'dict value'}, 'custom message')

                def some_nested_function():
                    some_nested_function_variable = deprecated(('tuple', 1, 2, 3, 4), 'custom message')
                    pass

                some_nested_function = deprecated(some_nested_function, 'custom message')

            some_method = deprecated(some_method, 'custom message')

            def get_set_property(self):
                pass

            get_set_property = property(fget=get_set_property)

            get_set_property = deprecated(get_set_property, 'custom get message')

            def __get_set_property(self, value):
                pass

            get_set_property = deprecated(get_set_property.setter(__get_set_property), 'custom set message')

            @property
            def only_get_property(self):
                pass

            only_get_property = deprecated(only_get_property, 'custom message')

            @only_get_property.setter
            def only_get_property(self, value):
                pass

            @property
            def only_set_property(self):
                pass

            @deprecated
            @only_set_property.setter
            def only_set_property(self, value):
                pass

        SomeClass = deprecated(SomeClass, 'custom message')
    """

    func_name = _caller_name(1)

    called_filename, called_line_no = _get_line_and_file(2)
    called_line_no += 1

    if isinstance(obj, property):
        class FSetWrapper(object):

            def __init__(self, fset_object):
                self._fset_object = fset_object
                if func_name:
                    self._f_name = func_name + '.' + fset_object.__name__
                else:
                    self._f_name = (
                        fset_object.__module__ + '.' + fset_object.__name__
                    )

            def __call__(self, *args, **kwargs):
                # turn off filter
                warnings.simplefilter('always', DeprecationWarning)

                message = "deprecated set property [{0}].\n{1}".format(
                    self._f_name,
                    msg
                )

                if logger.getEffectiveLevel() == logging.DEBUG:
                    calling_filename, calling_line_no = _get_line_and_file(2)
                    thread = threading.current_thread()
                    calling_obj = _caller_name()

                    debug_msg = DEPRECATED_LOGGING_TEMPLATE.format(
                        thread_name=thread.getName(),
                        thread_id=thread.ident,
                        object_type='property (set)',
                        calling_obj=calling_obj,
                        calling_filename=calling_filename,
                        calling_line_no=calling_line_no,
                        called_obj=func_name,
                        called_filename=called_filename,
                        called_line_no=called_line_no
                    )

                    logger.debug(debug_msg)

                warnings.warn(
                    message,
                    category=DeprecationWarning,
                    stacklevel=2
                )
                # reset filter

                warnings.simplefilter('default', DeprecationWarning)
                return self._fset_object(*args, **kwargs)


        class FGetWrapper(object):

            def __init__(self, fget_object):
                self._fget_object = fget_object
                if func_name:
                    self._f_name = func_name + '.' + fget_object.__name__
                else:
                    self._f_name = (
                        fget_object.__module__ + '.' + fget_object.__name__
                    )

            def __call__(self, *args, **kwargs):
                # turn off filter
                warnings.simplefilter('always', DeprecationWarning)
                if logger.getEffectiveLevel() == logging.DEBUG:
                    calling_filename, calling_line_no = _get_line_and_file(2)
                    thread = threading.current_thread()
                    calling_obj = _caller_name()

                    debug_msg = DEPRECATED_LOGGING_TEMPLATE.format(
                        thread_name=thread.getName(),
                        thread_id=thread.ident,
                        object_type='property (get)',
                        calling_obj=calling_obj,
                        calling_filename=calling_filename,
                        calling_line_no=calling_line_no,
                        called_obj=func_name,
                        called_filename=called_filename,
                        called_line_no=called_line_no
                    )

                    logger.debug(debug_msg)

                message = "deprecated get property [{0}].\n{1}".format(
                    self._f_name,
                    msg
                )

                warnings.warn(
                    message,
                    category=DeprecationWarning,
                    stacklevel=2
                )
                # reset filter

                warnings.simplefilter('default', DeprecationWarning)
                return self._fget_object(*args, **kwargs)

        try:
            if obj.fset is not None:
                fset = FSetWrapper(obj.fset)
                fget = obj.fget
                return property(fget, fset)

            elif obj.fget is not None:
                fget = FGetWrapper(obj.fget)
                fset = obj.fset
                return property(fget, fset)

        except:
            traceback.print_exc()
            return obj

    elif inspect.isfunction(obj):
        if func_name:
            f_name = func_name + '.' + obj.__name__
        else:
            f_name = obj.__module__ + '.' + obj.__name__

        def wrapper(*args, **kwargs):
            # turn off filter
            warnings.simplefilter('always', DeprecationWarning)

            if PY3:
                # noinspection PyUnresolvedReferences
                arg_names = inspect.getfullargspec(obj)[0]
            else:
                arg_names = inspect.getargspec(obj)[0]

            if arg_names and arg_names[0] == "self":
                call_type = 'method'
            else:
                call_type = 'function'

            if logger.getEffectiveLevel() == logging.DEBUG:
                calling_filename, calling_line_no = _get_line_and_file(2)
                thread = threading.current_thread()
                calling_obj = _caller_name()

                debug_msg = DEPRECATED_LOGGING_TEMPLATE.format(
                    thread_name=thread.getName(),
                    thread_id=thread.ident,
                    object_type=call_type,
                    calling_obj=calling_obj,
                    calling_filename=calling_filename,
                    calling_line_no=calling_line_no,
                    called_obj=func_name,
                    called_filename=called_filename,
                    called_line_no=called_line_no
                )

                logger.debug(debug_msg)

            message = "deprecated {0} [{1}].\n{2}".format(
                call_type,
                f_name,
                msg
            )

            warnings.warn(
                message,
                category=DeprecationWarning,
                stacklevel=2
            )
            # reset filter

            warnings.simplefilter('default', DeprecationWarning)
            return obj(*args, **kwargs)

        return update_wrapper(wrapper, obj)

    elif inspect.isclass(obj):
        if func_name:
            class_name = func_name + '.' + obj.__name__
        else:
            class_name = obj.__module__ + '.' + obj.__name__

        def wrapper(*args, **kwargs):
            # turn off filter
            warnings.simplefilter('always', DeprecationWarning)

            if logger.getEffectiveLevel() == logging.DEBUG:
                calling_filename, calling_line_no = _get_line_and_file(2)
                thread = threading.current_thread()
                calling_obj = _caller_name()

                debug_msg = DEPRECATED_LOGGING_TEMPLATE.format(
                    thread_name=thread.getName(),
                    thread_id=thread.ident,
                    object_type='class',
                    calling_obj=calling_obj,
                    calling_filename=calling_filename,
                    calling_line_no=calling_line_no,
                    called_obj=func_name,
                    called_filename=called_filename,
                    called_line_no=called_line_no
                )

                logger.debug(debug_msg)

            message = "deprecated class [{0}].\n{1}".format(
                class_name,
                msg
            )

            warnings.warn(
                message,
                category=DeprecationWarning,
                stacklevel=2
            )
            # reset filter

            warnings.simplefilter('default', DeprecationWarning)
            return obj(*args, **kwargs)

        return update_wrapper(wrapper, obj)
    else:
        frame = sys._getframe().f_back
        source = inspect.findsource(frame)[0]
        called_line_no -= 1

        if msg:
            while (
                '=deprecated' not in source[called_line_no] and
                '= deprecated' not in source[called_line_no] and
                '=utils.deprecated' not in source[called_line_no] and
                '= utils.deprecated' not in source[called_line_no]
            ):
                called_line_no -= 1

        symbol = source[called_line_no].split('=')[0].strip()

        if func_name:
            symbol_name = func_name + '.' + symbol
        else:
            symbol_name = symbol

        def wrapper(*_, **__):
            # turn off filter
            warnings.simplefilter('always', DeprecationWarning)

            if logger.getEffectiveLevel() == logging.DEBUG:
                object_type = str(type(obj)).split(' ', 1)[-1]
                object_type = object_type[1:-2]
                calling_filename, calling_line_no = _get_line_and_file(2)
                thread = threading.current_thread()
                calling_obj = _caller_name()

                debug_msg = DEPRECATED_LOGGING_TEMPLATE.format(
                    thread_name=thread.getName(),
                    thread_id=thread.ident,
                    object_type=object_type,
                    calling_obj=calling_obj,
                    calling_filename=calling_filename,
                    calling_line_no=calling_line_no,
                    called_obj=func_name,
                    called_filename=called_filename,
                    called_line_no=called_line_no
                )

                logger.debug(debug_msg)

            message = "deprecated symbol [{0}].\n{1}".format(
                symbol_name,
                msg
            )

            warnings.warn(
                message,
                category=DeprecationWarning,
                stacklevel=2
            )
            # reset filter

            warnings.simplefilter('default', DeprecationWarning)
            return obj

        return property(wrapper)


# This is rather odd to see.
# I am using sys.excepthook to alter the displayed traceback data.
# The reason why I am doing this is to remove any lines that are generated
# from any of the code in this file. It adds a lot of complexity to the
# output traceback when any lines generated from this file do not really need
# to be displayed.

def trace_back_hook(tb_type, tb_value, tb):
    tb = "".join(
        traceback.format_exception(
            tb_type,
            tb_value,
            tb,
            limit=None
        )
    )
    if tb_type == DeprecationWarning:
        sys.stderr.write(tb)
    else:
        new_tb = []
        skip = False
        for line in tb.split('\n'):
            if line.strip().startswith('File'):
                if __file__ in line:
                    skip = True
                else:
                    skip = False
            if skip:
                continue

            new_tb += [line]

        sys.stderr.write('\n'.join(new_tb))


sys.excepthook = trace_back_hook
