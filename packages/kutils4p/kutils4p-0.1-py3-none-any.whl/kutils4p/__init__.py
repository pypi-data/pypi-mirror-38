"""Initialize package path values and importer class."""

import inspect
import os
from functools import wraps


def func_name():
    """Use inspect stack to print top level function name."""
    return inspect.stack()[0].function


def generate_files_of_type(ftype="", dir="."):
    """Find all files of type ftype in dir."""
    for file in os.listdir(dir):
        if file.endswith(ftype):
            yield os.path.join(dir, file)


def is_non_zero_file(fpath):
    """Determine if file is empty or doesn't exist."""
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


class KException(Exception):
    """Abort excecution of function (potentially raised by _KDecorator.before())."""

    def handle(self):
        """Handle exception."""
        pass


class _KDecorator:
    """generic Decorator class."""

    def __new__(cls, func, *args, **kargs):
        """Set wrapped function."""
        obj = super().__new__(cls)

        @wraps(func)
        def wrapper(*args, **kargs):
            try:
                args, kargs = obj.before(*args, **kargs)
                result = func(*args, **kargs)
                return obj.after(result)
            except KException as e:
                e.handle()
        return wrapper

    def __init__(self, func):
        """Set wrapped func."""
        self.func = func

    def before(self, *args, **kargs):
        """Call before wrapped function."""
        return args, kargs

    def after(self, result):
        """Call after wrapped function."""
        return result

    def __repr__(self):
        """Official str rep."""
        return "<KDecorator wrapping function " + str(self.func) + ">"


class KDecorator(_KDecorator):
    """Public generic Decorator."""

    def __new__(cls, *args, **kargs):
        """Call parent new."""
        return super().__new__(cls, *args, **kargs)


def is_number(s):
    """Check if string is a number."""
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
