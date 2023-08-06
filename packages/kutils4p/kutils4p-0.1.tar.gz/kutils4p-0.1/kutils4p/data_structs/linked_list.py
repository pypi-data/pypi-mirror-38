#!/bin/bash/python3
"""LinkedList class."""


class RemoveFromEmptyLinkedList(Exception):
    """Exception raised when popping from empty LL."""

    pass


class LinkedList(object):
    """Linked List class."""

    def __init__(self, iter=None):
        """Initialize LinkedList with values in iter (empty o/w)."""
        self.head = None
        self.tail = None
        self.length = 0

        try:
            for i in iter:
                self.add(i)
        except TypeError:
            pass

    def node_added(self):
        """Modify length and total based on new node."""
        self.length += 1

    def node_removed(self):
        """Modify length and total based on removed node."""
        self.length -= 1

    def add_to_empty(self, node):
        """Add node to empty list."""
        self.head = node
        self.tail = node

    def add(self, val):
        """Add value to end of LinkedList."""
        new_node = LinkedListNode(val)

        if self.length == 0:
            self.add_to_empty(new_node)
        else:
            self.tail.set_next(new_node)
            self.tail = new_node

        self.node_added()

    def push(self, val):
        """Add value to beggining of LinkedList."""
        new_node = LinkedListNode(val)

        if self.length == 0:
            self.add_to_empty(new_node)
        else:
            new_node.set_next(self.head)
            self.head = new_node

        self.node_added()

    def extend(self, linked_list):
        """Add another linked list to the end of the current."""
        if self.head is None:
            self.head = linked_list.head
            self.tail = linked_list.tail
        else:
            self.tail.set_next(linked_list.head)
            self.tail = linked_list.tail

    def pop(self):
        """Remove and return value at end of Linked List."""
        return_val = None
        if self.length >= 1:
            return_val = self.tail.val
            self.tail = self.tail.prev
            if self.length > 1:
                self.tail.set_next(None)

            self.node_removed()
            return return_val

        raise RemoveFromEmptyLinkedList

    def deque(self):
        """Remove and return value at head of Linked List."""
        return_val = None
        if self.length >= 1:
            return_val = self.head.val
            self.head = self.head.next
            if self.length > 1:
                self.head.set_prev(None)

            self.node_removed()
            return return_val

        raise RemoveFromEmptyLinkedList

    def __iter__(self):
        """Return iterable Linked List."""
        return LinkedListIterator(self.head)

    def __str__(self):
        """Print Linked List."""
        to_print = "["
        for f in self:
            to_print += str(f.val)
            if f.next is not None:
                to_print += "]->["
        to_print += "]"
        return to_print

    def __len__(self):
        """Return length of LinkedList."""
        return self.length

    def to_set(self):
        """Return a set rep of the LL."""
        s = set()
        for el in self:
            s.add(int(el))

        return s


class LinkedListNode(object):
    """Linked List Node class."""

    def __init__(self, val, next=None, prev=None):
        """Initialize LinkedListNode with value and next item."""
        self.val = val
        self.next = next
        self.prev = prev

    def __str__(self):
        """Print Linked List Node val."""
        return str(self.val)

    def print_all(self):
        """Print all info related to LinkedListNode."""
        print("val: " + str(self.val))
        print("next: " + str(self.next))
        print("prev: " + str(self.prev))

    def set_next(self, node):
        """Set node as this node's next."""
        self.next = node
        try:
            node.prev = self
        except AttributeError:
            pass

    def set_prev(self, node):
        """Set node as this node's prev."""
        self.set_prev = node
        try:
            node.next = self
        except AttributeError:
            pass

    def __int__(self):
        """Return value as integer."""
        return self.val


class LinkedListIterator(object):
    """Linked List Iterator."""

    def __init__(self, first):
        """Initiliaze Iterator."""
        self.next = first

    def __iter__(self):
        """Return self."""
        return self

    def __next__(self):
        """Return next item in linked list."""
        if self.next is None:
            raise StopIteration

        to_return = self.next
        self.next = self.next.next

        return to_return

default = LinkedList
