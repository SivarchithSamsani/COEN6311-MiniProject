import datetime
from itertools import count
from Models.User import User


class Transaction:
    id: int
    row: int
    column: int
    price: float
    user: User
    reserved_on: datetime.date
    created_at: datetime.datetime
    updated_at: datetime.datetime
    _iterator = count(1)

    def __init__(self, user, row, column, price, reserved_on):
        self.id = next(self._iterator)
        self.row = row
        self.column = column
        self.price = price
        self.user = user
        self.reserved_on = reserved_on
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def edit_transaction(self, row, column, reserved_on):
        self.row = row
        self.column = column
        self.reserved_on = reserved_on
        self.updated_at = datetime.datetime.now()

    def __repr__(self):
        return "ID: " + str(
            self.id) + " | Seat: (" + str(self.row) + "," + str(
            self.column) + ") | User: " + self.user.name + " | Reserved Date: " + str(
            self.reserved_on) + " | Price: " + str(self.price)

    def __str__(self):
        return "ID: " + str(
            self.id) + " | Seat: (" + str(self.row) + "," + str(
            self.column) + ") | User: " + self.user.name + " | Reserved Date: " + str(
            self.reserved_on) + " | Price: " + str(self.price)
