from dataclasses import dataclass
from itertools import count


@dataclass
class Role:
    id: int
    name: str
    _iterator = count(1)

    def __init__(self, name):
        self.id = next(self._iterator)
        self.name = name

    def get_role_name(self):
        return self.name

    def __repr__(self):
        return "ID: " + str(self.id) + " | Title: " + self.name

    def __str__(self):
        return "ID: " + str(self.id) + "| Title: " + self.name
