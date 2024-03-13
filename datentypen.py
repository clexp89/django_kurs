""" 
Typehints in Python (seit 3.6)
"""

from functools import partial


def summe(a: int, b: int) -> int:
    return a + b


def f(a: list[int]): ...


summe(3, 3)


class ExporterMixin:
    def export(self):
        print("exporting...")


class DataManager(ExporterMixin):
    def generate_data(self):
        print(
            "werden daten generiert asdf asdf asdf asdf asdf sadf asdf asdf asdf asfd "
        )


dm = DataManager()
dm.generate_data()
dm.export()


def fn(a, b):
    print(a, b)


a = 1
f = partial(fn, "a1")
f("b2")


class A:
    def hello(self):
        print("Hello from A")


class B:
    def hello(self):
        print("Hello from B")


class C(A, B):
    def bello(self):
        print("Hello from C")


print(C.__mro__)
c = C()
print(c.hello())
