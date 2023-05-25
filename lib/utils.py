from time import perf_counter
from contextlib import contextmanager


class timer:

    def __init__(self, name=""):
        self.name = name

    def __enter__(self, name=""):
        self.time = perf_counter()
        return self

    def __exit__(self, type, value, traceback):
        self.time = perf_counter() - self.time
        self.readout = f'[{self.name}] Time: {self.time:.3f} seconds'
        print(self.readout)