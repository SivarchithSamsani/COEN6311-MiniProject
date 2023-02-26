from dataclasses import dataclass
from itertools import count


# from enum import Enum

@dataclass
class Notification:
    id: int
    body: str
    is_seen: bool 
    _iterator = count(1)

    def __init__(self, body):
        self.id = next(self._iterator)
        self.body = body
        self.is_seen = False

    def notification_read(self):
        self.is_seen = True

    def __str__(self):
        return "ID: " + str(self.id) + " | Subject: " + self.body

    def __repr__(self):
        return "ID: " + str(self.id) + " | Subject: " + self.body
