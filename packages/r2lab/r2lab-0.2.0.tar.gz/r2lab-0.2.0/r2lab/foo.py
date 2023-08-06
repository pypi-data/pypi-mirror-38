# pylint: disable=all

from pandas import DataFrame

class Foo(DataFrame):

    def __init__(self, x, *args, **kwds):
        print(f"in x={x}")
        self._x = x
        print(f"out x={x}")
        DataFrame.__init__(self, *args, **kwds)


foo = Foo(x=10)
