#!/bin/bash/python3
"""SetAccumulator class."""


class Accumulator(object):
    """Add a total attribute to any collection."""

    def __init__(self, iterable={}, base_class=set, add_function="add"):
        """Init accumulator."""
        self.container = base_class()
        self.total = 0
        self.add_function = add_function

        setattr(self, add_function, self.__accumulator_add)

        for e in iterable:
            self.__accumulator_add(e)

    def add_to_base_class(self, e):
        """Add e to container."""
        getattr(self.container, self.add_function)(e)

    def __accumulator_add(self, i):
        """Add i to container and increase total."""
        self.total += i
        self.add_to_base_class(i)

    def __iter__(self):
        """Iterate through inner container."""
        return iter(self.container)

    def __str__(self):
        """Stringify inner container."""
        return str(self.container)

    def __len__(self):
        """Get length of inner container."""
        return len(self.container)

    def __contains__(self, item):
        """Determine if item is in container."""
        return self.container.__contains__(item)

default = Accumulator
