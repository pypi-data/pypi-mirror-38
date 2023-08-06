#!/usr/bin/python3

class RingBuffer:
    
    def __init__(self, iter=[]):
        self.iter = []
        for i in iter:
            self.iter.append(i)

    def push(self, e):
        self.iter.append(e)

    def __iter__(self):
        while True:
            for i in self.iter:
                yield i

class SpiralBuffer(RingBuffer):

    def __iter__(self):
        while True:
            for i in self.iter:
                yield i

            for i in reversed(self.iter):
                yield i
