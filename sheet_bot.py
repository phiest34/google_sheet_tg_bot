import gspread
import telebot
from telebot import types
from constants import *
from utils import *


class Sheet_bot:
    def __init__(self, token):
        self.reply_message_id = 0
        self.tg_bot = telebot.TeleBot(token)
        self.sheet = gspread.service_account().open_by_key(SHEET_KEY)

    def start_bot(self):
        self.__register_handlers()
        self.tg_bot.polling(none_stop=True)

    def __register_handlers(self):
        @self.tg_bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.__send_welcome(message)

        @self.tg_bot.message_handler(content_types=["text"])
        def message_handler(message):
            self.__reply_handler(message)

        @self.tg_bot.callback_query_handler(func=lambda call: True)
        def query_handler(call):
            self.__menu_handler(call)

    def update_cell(self, old_value, new_value, chat_id):
        try:
            row = self.sheet.sheet1.find(old_value).row
            col = self.sheet.sheet1.find(old_value).col
            self.sheet.sheet1.update_cell(row, col, new_value)

        except Exception:
            self.tg_bot.send_message(chat_id, "Нет такого поля")

    def __send_welcome(self, message):
        keyboard = types.InlineKeyboardMarkup()
        sheets = self.sheet.worksheets()
        sheet_names = set((map(lambda sheet: sheet.title, sheets)))
        buttons = list(
            map(lambda name: types.InlineKeyboardButton(text=name, callback_data=name),
                sheet_names))
        buttons.append(types.InlineKeyboardButton(text="Создать новую таблицу", callback_data=-1))
        keyboard.add(*buttons)
        self.tg_bot.send_message(message.chat.id, "Выбери таблицу для редакирования", reply_markup=keyboard)

    def __menu_handler(self, call):
        if call.data == "-1":
            self.__show_enter_table_name(call.message.chat.id)
        else:
            self.tg_bot.send_message(call.message.chat.id, call.data)

    def __reply_handler(self, message):
        print("reply handler message " + message.text)
        print(message.reply_to_message)
        print(self.__get_message_id())
        if message.reply_to_message.id == self.__get_message_id():
            self.sheet.add_worksheet(title=message.text, rows=100, cols=100)

    def __show_enter_table_name(self, chat_id):
        markup = types.ForceReply(selective=False)
        msg = self.tg_bot.send_message(chat_id, "Введите название таблицы", reply_markup=markup)
        self.__save_message_id(msg.id)

    def __save_message_id(self, message_id):
        self.reply_message_id = message_id

    def __get_message_id(self):
        return self.reply_message_id
