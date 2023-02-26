import datetime
from itertools import count
from Models.Transaction import Transaction
from Models.User import User
from Models.Notification import Notification
from Models.Message import Message


class Booking:
    _iterator = count(1)
    id: int
    size: int
    base_price: float
    user: User
    sell_list: [Transaction]
    _transactions: [Transaction]
    _users: [User]
    _notifications: [Notification]
    _messages: [Message]

    def __init__(self):
        self.id = next(self._iterator)
        self.user = None
        self.sell_list = []
        self._transactions = []
        self._users = []
        self._notifications = []
        self._messages = []
        self.size = None
        self.base_price = None

    def is_username_unique(self, username):
        try:
            if not len(self._users):
                return True
            is_unique = True
            for user in self._users:
                if user.name == username:
                    is_unique = False
                    break
            return is_unique
        except AttributeError:
            return True

    def menu(self):
        while True:
            if not self.user:
                self.login_menu()
            elif self.user.get_role().name == "admin":
                self.admin_menu()
            elif self.user.get_role().name == "user":
                self.user_menu()
            elif self.user.get_role().name == "owner":
                self.owner_menu()

    def login_menu(self):
        print('''
User Menu
1. Login
2. Register

0. quit application
        ''')
        try:
            input_prompt = int(input(">"))
            if input_prompt == 1:
                username_input = input("Username: ")
                password_input = input("Password: ")
                print(self.login(username_input, password_input))
            elif input_prompt == 2:
                while True:
                    username_input = input("Username: ")
                    if not self.is_username_unique(username_input):
                        print("Username cannot be duplicate, change username")
                        continue
                    else:
                        break
                password_input = input("Password: ")
                role_input = int(input("Role:\n1. Admin\n2. User\n3. Owner\n>  "))
                if role_input == 1:
                    print(self.register(username_input, password_input, "admin"))
                elif role_input == 3:
                    print(self.register(username_input, password_input, "owner"))
                elif role_input == 2:
                    print(self.register(username_input, password_input))
                else:
                    print("Invalid Role")
                    return
            elif input_prompt == 0:
                exit(0)
            else:
                print("Invalid option")
        except ValueError:
            print("Invalid option")

    def user_menu(self):
        if not self.user:
            return
        elif not self.user.get_role().name == "user":
            return
        elif not self.size and not self.base_price:
            print("There is no venue, come back later")
            self.user = None
            return
        print('''
App Menu
1. Show reserved seats
2. Book a seat
3. Show my transactions
4. Show sell list
5. Buy from sell list
6. Sell my reservation
7. Show notifications
8. Show Messages
9. Send Message
10. Cancel Reservation

11. Logout
0. Quit
''')
        try:
            input_prompt = int(input("> "))
            if input_prompt == 1:
                date = None
                date_choice = int(input("Date:\n1. Today\n2. Tomorrow\n3. Day after tomorrow\n> "))
                if date_choice == 1:
                    date = datetime.date.today()
                elif date_choice == 2:
                    date = datetime.date.today() + datetime.timedelta(days=1)
                elif date_choice == 3:
                    date = datetime.date.today() + datetime.timedelta(days=2)
                reservation_room = self.get_reservations(date)
                print("Venue Bookings:")
                for row in range(self.size):
                    for column in range(self.size):
                        print(str(reservation_room[row][column]), sep=" ", end=" ")
                    print()
            elif input_prompt == 2:
                date = None
                date_choice = int(input("Date:\n1. Today\n2. Tomorrow\n3. Day after tomorrow\n> "))
                if date_choice == 1:
                    date = datetime.date.today()
                elif date_choice == 2:
                    date = datetime.date.today() + datetime.timedelta(days=1)
                elif date_choice == 3:
                    date = datetime.date.today() + datetime.timedelta(days=2)
                try:
                    row = int(input("Row: "))
                    column = int(input("Column: "))
                except ValueError:
                    print("Row and Columns must be integers")
                print(self.book_seat(row, column, date))
            elif input_prompt == 3:
                print("My Transactions: ")
                transactions = self.get_my_transactions()
                if len(transactions) == 0:
                    print("There are no transactions at this time.")
                else:
                    for transaction in transactions:
                        print(transaction)
            elif input_prompt == 4:
                print("Selling List: ")
                transactions = self.get_sell_list()
                if len(transactions) == 0:
                    print("There are no transactions right now in the selling list")
                else:
                    for transaction in transactions:
                        print(transaction)
            elif input_prompt == 5:
                print("Book a seat from selling list ")
                transactions = self.get_sell_list()
                if len(transactions) == 0:
                    print("No Seats to book")
                else:
                    for transaction in transactions:
                        print(transaction)
                    transaction_input = int(input("Id: "))
                    print(self.buy_from_sell_list(transaction_input))
            elif input_prompt == 6:
                print("List of seats you want to sell: ")
                transactions = self.get_my_transactions()
                if len(transactions) == 0:
                    print("There are no transactions at this time.")
                else:
                    for transaction in self._transactions:
                        if transaction.user.id == self.user.id:
                            print(transaction)
                    transaction_input = int(input("Id: "))
                    print(self.add_to_sell_list(transaction_input))
            elif input_prompt == 7:
                print("Notifications:")
                if len(self._notifications) == 0:
                    print("There are no notifications.")
                else:
                    for notification in self._notifications:
                        print(notification)
            elif input_prompt == 8:
                print("Messages:")
                if len(self._messages) == 0:
                    print("There are no messages")
                else:
                    for message in self.get_my_messages():
                        print(message)
            elif input_prompt == 9:
                for user in self._users:
                    print(user)
                user_prompt = int(input("User Id:"))
                message_prompt = input("Message: ")
                sent_to = None
                for user in self._users:
                    if user.id == user_prompt:
                        sent_to = user
                if not sent_to:
                    print("Invalid user id selected")
                    return
                message = Message(message_prompt, sent_to, self.user)
                self._messages.append(message)
                print("Message sent!")
            elif input_prompt == 10:
                transactions = self.get_my_transactions()
                if len(transactions) == 0:
                    print("There are no transactions at this time.")
                else:
                    print("Cancel Transactions: ")
                    for transaction in self._transactions:
                        if transaction.user.id == self.user.id:
                            print(transaction)
                    cancel_prompt = int(input("Transaction id: "))
                    transaction_index = -1
                    for index in range(len(self._transactions)):
                        if self._transactions[index].id == cancel_prompt:
                            transaction_index = index
                            break
                    if transaction_index >= 0:
                        self._transactions.pop(transaction_index)
                        print("Reservation cancelled")
                    else:
                        print("Invalid transactionId")
            elif input_prompt == 11:
                self.user = None
            elif input_prompt == 0:
                exit(0)
            else:
                print("Invalid option")
        except ValueError:
            print("Invalid value")
        except IndexError:
            print("Invalid input")

    def admin_menu(self):
        if not self.user:
            return
        elif not self.user.get_role().name == "admin":
            return
        print('''
Admin Menu
1. Show reserved Seats
2. Show all Transactions
3. Show messages (complaints)
4. Send Message

9. logout
0. quit application
        ''')
        try:
            input_prompt = int(input("> "))
            if input_prompt == 1:
                date = None
                if not self.size and not self.base_price:
                    print("Venue size and price setup not completed")
                    return
                date_choice = int(input("Date:\n1. Today\n2. Tomorrow\n3. Day after tomorrow\n> "))
                if date_choice == 1:
                    date = datetime.date.today()
                elif date_choice == 2:
                    date = datetime.date.today() + datetime.timedelta(days=1)
                elif date_choice == 3:
                    date = datetime.date.today() + datetime.timedelta(days=2)
                reservation_room = self.get_reservations(date)
                print("Venue Bookings:")
                for row in range(self.size):
                    for column in range(self.size):
                        print(str(reservation_room[row][column]), sep=" ", end=" ")
                    print()
            elif input_prompt == 2:
                print("All the Transactions: ")
                for transaction in self._transactions:
                        print(transaction)
            elif input_prompt == 3:
                print("Messages:")
                if len(self._messages) == 0:
                    print("There are no messages")
                else:
                    for message in self.get_my_messages():
                        print(message)
            elif input_prompt == 4:
                for user in self._users:
                    print(user)
                user_prompt = int(input("User Id:"))
                message_prompt = input("Message: ")
                sent_to = None
                for user in self._users:
                    if user.id == user_prompt:
                        sent_to = user
                if not sent_to:
                    print("Invalid user id selected")
                    return
                message = Message(message_prompt, sent_to, self.user)
                self._messages.append(message)
                print("Message sent!")
            elif input_prompt == 9:
                self.user = None
                print("Logged out!")
            elif input_prompt == 0:
                exit(0)
            else:
                print("Invalid option")
        except ValueError:
            print("Invalid option")

    def owner_menu(self):
        if not self.user:
            return
        elif not self.user.get_role().name == "owner":
            return
        print('''
Business Owner Menu
1. Create Venue
2. Set base price
3. Show reserved seats
4. Show all transactions
5. Show Messages
6. Send Message
7. Cancel bookings

9. logout
0. quit application
        ''')
        try:
            input_prompt = int(input("> "))
            if input_prompt == 1:
                size_prompt = int(input("Size of the venue: "))
                self.size = size_prompt
                print("Size of the venue is set")
            elif input_prompt == 2:
                price_prompt = float(input("Base price: "))
                self.base_price = price_prompt
                print("Base price of a seat in the venue is set")
            elif input_prompt == 3:
                date = None
                if not self.size and not self.base_price:
                    print("Venue size and price setup not completed")
                    return
                date_choice = int(input("Date:\n1. Today\n2. Tomorrow\n3. Day after tomorrow\n> "))
                if date_choice == 1:
                    date = datetime.date.today()
                elif date_choice == 2:
                    date = datetime.date.today() + datetime.timedelta(days=1)
                elif date_choice == 3:
                    date = datetime.date.today() + datetime.timedelta(days=2)
                reservation_room = self.get_reservations(date)
                print("Venue Bookings:")
                for row in range(self.size):
                    for column in range(self.size):
                        print(str(reservation_room[row][column]), sep=" ", end=" ")
                    print()
            elif input_prompt == 4:
                print("All the Transactions: ")
                for transaction in self._transactions:
                        print(transaction)
            elif input_prompt ==5:
                print("Messages:")
                if len(self._messages) == 0:
                    print("There are no messages")
                else:
                    for message in self.get_my_messages():
                        print(message)
            elif input_prompt == 6:
                for user in self._users:
                    print(user)
                user_prompt = int(input("User Id:"))
                message_prompt = input("Message: ")
                sent_to = None
                for user in self._users:
                    if user.id == user_prompt:
                        sent_to = user
                if not sent_to:
                    print("Invalid user id selected")
                    return
                message = Message(message_prompt, sent_to, self.user)
                self._messages.append(message)
                print("Message sent!")
            elif input_prompt == 7:
                print("Cancel Transactions: ")
                for transaction in self._transactions:
                        print(transaction)
                cancel_prompt = int(input("Transaction id: "))
                transaction_index = -1
                for index in range(len(self._transactions)):
                    if self._transactions[index].id == cancel_prompt:
                        transaction_index = index
                        break
                if transaction_index >= 0:
                    self._transactions.pop(transaction_index)
                    print("Reservation cancelled")
                else:
                    print("Invalid transactionId")
            elif input_prompt == 9:
                self.user = None
                print("Logged out!")
            elif input_prompt == 0:
                exit(0)
            else:
                print("Invalid option")
        except ValueError:
            print("Invalid option")

    def register(self, name, password, role="user"):
        user = User(name, password, role)
        self._users.append(user)
        return "Account Created"

    def login(self, name, password):
        try:
            if not len(self._users):
                return "Invalid credentials"
            for user in self._users:
                if user.name == name and user.get_password() == password:
                    self.user = user
                    return "Logged in!"
            if not self.user:
                return "Invalid credentials"
        except AttributeError:
            return "Invalid credentials"

    def get_reservations(self, date=datetime.date.today()):
        room = [[0] * self.size for i in range(self.size)]
        for transaction in self._transactions:
            if transaction.reserved_on == date:
                room[transaction.row][transaction.column] = 'X'
        return room

    def get_seat_price(self, row, column):
        if self.size - row == 1:
            return self.base_price * 2
        elif self.size - row == self.size - 1:
            return self.base_price * 0.75
        elif self.size - row >= 2 or self.size - row <= 2:
            return self.base_price * 1.25
        else:
            return self.base_price

    def get_my_messages(self):
        return filter(lambda message: message.sent_to.id == self.user.id, self._messages)

    def get_my_transactions(self):
        transactions = []
        for transaction in self._transactions:
            if transaction.user == self.user:
                transactions.append(transaction)
        return transactions

    def get_sell_list(self):
        return self.sell_list

    def buy_from_sell_list(self, transaction_id):
        if not self.user:
            return "Login to buy"
        is_successful = False
        for index in range(len(self.sell_list)):
            if self.sell_list[index].id == transaction_id:
                self.sell_list[index].user = self.user
                self.sell_list.pop(index)
                is_successful = True
                break
        if is_successful:
            return "Transaction successful"
        else:
            return "Transaction failed"

    def add_to_sell_list(self, transaction_id):
        if not self.user:
            return "Login to sell"
        is_successful = False
        for transaction in self._transactions:
            if transaction.id == transaction_id:
                self.sell_list.append(transaction)
                is_successful = True
                break
        if is_successful:
            notification = Notification("New seat(" + str(transaction.row) + "," + str(transaction.column)
                                        + ") on " + str(transaction.reserved_on)
                                        + " added to sell listing by user: " + str(transaction.user.name))
            self._notifications.append(notification)
            return "Transaction successful"
        else:
            return "Transaction failed"

    def book_seat(self, row, column, date):
        if not self.user:
            return "Login to continue the reservation"
        else:
            seat_available = True
            for transaction in self._transactions:
                if transaction.reserved_on == date and transaction.row == row and transaction.column == column:
                    seat_available = False
                    break
            if seat_available:
                price = self.get_seat_price(row, column)
                print("Price for booking the ticket is " + str(price))
                confirm_prompt = int(input("Confirm\n1. Yes\n2. No\n>"))
                if confirm_prompt == 1:
                    transaction = Transaction(user=self.user, row=row, column=column,
                                              price=self.get_seat_price(row, column),
                                              reserved_on=date)
                    self._transactions.append(transaction)
                    return "Seat reserved"
                else:
                    return "Seat reservation cancelled"
            else:
                return "Seat is not available"

    def add_notification(self, notification_msg):
        notification = Notification(notification_msg)
        self._notifications.append(notification)

    def get_notifications(self):
        # print(self.user.get_role())
        if self.user.get_role().name == "admin":
            return self._notifications
        else:
            print("No authorization")
            return []
