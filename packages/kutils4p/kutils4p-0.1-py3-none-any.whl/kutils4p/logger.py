#!/bin/bash/python3
"""Sparse Logger class."""

class Logger(object):
    """Sparse Logger Class."""

    log_level = 1

    def __init__(self, log_level=1):
        """Init Logger set whether active by default."""
        self.log_level = log_level

    def print(self, level, *args, **kwargs):
        """Log string if logger active."""
        if self.log_level >= level:
            print(*args, **kwargs)

    def set_level(self, lvl):
        """Set log level to particular value."""
        self.log_level = lvl

