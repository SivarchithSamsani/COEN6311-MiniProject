from dataclasses import dataclass
from itertools import count
from Models.Role import Role


@dataclass
class User:
    id: int
    name: str
    _role: Role
    _password: str
    _iterator = count(1)

    def __init__(self, name, password, role="user"):
        self.id = next(self._iterator)
        self.name = name
        self._password = password
        self._role = Role(role)

    def get_role(self):
        return self._role

    def get_password(self):
        return self._password

    def get_name(self):
        return self.name

    def __repr__(self):
        return "ID: " + str(self.id) + " | Name: " + self.name + " | Role: " + self.get_role().name

    def __str__(self):
        return "ID: " + str(self.id) + " | Name: " + self.name + " | Role: " + self.get_role().name
