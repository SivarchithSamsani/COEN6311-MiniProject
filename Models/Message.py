import datetime
from dataclasses import dataclass
from itertools import count
from Models.User import User


@dataclass
class Message:
    id: int
    message: str
    sent_by: User
    sent_to: User
    is_seen: bool
    _iterator = count(1)

    def __init__(self, message, sent_to, sent_by):
        self.id = next(self._iterator)
        self.message = message
        self.sent_by = sent_by
        self.sent_to = sent_to
        self.is_seen = False
        self.created_at = datetime.datetime.now()

    def message_read(self):
        self.is_seen = True

    def __str__(self):
        return "Time: " + str(self.created_at.hour) + ":" + str(self.created_at.minute) + " | " \
            + "From: " + self.sent_by.name + " | To: " + self.sent_to.name + " | Message: " + self.message

    def __repr__(self):
        return "Time: " + str(self.created_at.hour) + ":" + str(self.created_at.minute) + " | " \
            + "From: " + self.sent_by.name + " | To: " + self.sent_to.name + " | Message: " + self.message
