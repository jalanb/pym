import os
import sys
from contextlib import contextmanager
from importlib import import_module


def make_import_name_errors(method):
    """Experimental"""

    @contextmanager
    def import_name_errors(*args, **kwargs):
        """Experimental"""
        try:
            method(*args, **kwargs)
        except NameError as e:
            name = name_error(e)
            if not name:
                return False
            if name in sys.modules:
                return False
            module = import_module(name)
            globals()[name] = module
            method(*args, **kwargs)
            if name not in importable:
                importable[name] = module

    importable = {"os": os}
    return import_name_errors


def fred(method):
    runner = make_import_name_errors(method)
    with runner:
        runner("some", args="here")


class NameErrorHandler(object):
    """Experimental"""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context, returning truthiness to suppress exception.

        If an exception occurred while executing the body of the with statement,
            the arguments contain the exception type, value and traceback information.
            Otherwise, all three arguments are None.

        Returning a true value from this method will cause the with statement to suppress the exception and continue execution with the statement immediately following the with statement. Otherwise the exception continues propagating after this method has finished executing. Exceptions that occur during execution of this method will replace any exception that occurred in the body of the with statement.

        The exception passed in should never be reraised explicitly - instead, this method should return a false value to indicate that the method completed successfully and does not want to suppress the raised exception. This allows context management code to easily detect whether or not an __exit__() method has actually failed.
        """


def try_import_on_name_error(method):
    try:
        method()
    except NameError as e:
        importable = ["os"]
        name = name_error(e)
        if name and name in importable:
            from importlib import __import__

            __import__(name)
            method()


def name_error(exception):
    """Experimental"""
    string = str(exception)
    words = string.split(" ")
    if words[0] != "name":
        return None
    if "'" == words[1][-1] == words[1][0]:
        name = words[1][1:-1]
        return name
    return None
