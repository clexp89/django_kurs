""" 
Typehints in Python (seit 3.6)
"""


def summe(a: int, b: int) -> int:
    return a + b


def f(a: list[int]): ...


summe("a", 3)


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
