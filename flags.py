import string
import random
from random import randint


class Flags:
    def __init__(self):
        self.LENGTH = 6

    def generate_flag(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(self.LENGTH))


class Menu_types(Flags):
    def __init__(self):
        super().__init__()
        self.LENGTH = 2

    @property
    def CHOOSE_SHEET_MENU(self):
        return self.generate_flag()

    @property
    def CHOOSE_CATEGORY_MENU(self):
        return self.generate_flag()


class Callback_data(Flags):
    def __init__(self):
        super().__init__()
        self.LENGTH = 2

    @property
    def CREATE_NEW_TABLE(self):
        return self.generate_flag()


class Context_keys(Flags):
    def __init__(self):
        super().__init__()
        self.LENGTH = 6

    def generate_flag(self):
        return randint(0, 10 ** self.LENGTH)

    @property
    def WORKSHEET(self):
        return self.generate_flag()

    @property
    def CATEGORY(self):
        return self.generate_flag()

    @property
    def CHAT_ID(self):
        return self.generate_flag()

    @property
    def FIELDS_COUNT(self):
        return self.generate_flag()


class States(Flags):
    def __init__(self):
        super().__init__()
        self.LENGTH = 6

    def generate_flag(self):
        return randint(0, 10 ** self.LENGTH)

    @property
    def SELECTING_TABLE(self):
        return self.generate_flag()


