import gspread
import telebot
from telebot import types
from constants import *


class Sheet_bot:
    def __init__(self, token):
        self.tg_bot = telebot.TeleBot(token)
        self.keyboard = types.InlineKeyboardMarkup()
        self.sheet = gspread.service_account().open_by_key(SHEET_KEY)

    def start_bot(self):
        self.__register_handlers()
        self.tg_bot.polling(none_stop=True)


    def __register_handlers(self):
        @self.tg_bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            self.__send_welcome(message)

        @self.tg_bot.callback_query_handler(func=lambda call: True)
        def menu_handler(call):
            print("menu handler")
            self.__menu_handler(call)

    def update_cell(self, old_value, new_value, chat_id):
        try:
            row = self.sheet.sheet1.find(old_value).row
            col = self.sheet.sheet1.find(old_value).col
            self.sheet.sheet1.update_cell(row, col, new_value)

        except Exception:
            self.tg_bot.send_message(chat_id, "Нет такого поля")

    def __send_welcome(self, message):
        self.tg_bot.reply_to(message, "ПРИВЕТСТВУЮ ТЕБЯ ЧЕМПИОН")
        self.tg_bot.send_message(message.chat.id, "ЧЕМПИОН ЗВЕРЕЙ", timeout=1000)
        self.tg_bot.send_message(message.chat.id, "ЧЕМПИОН ЛЮДЕЙ", timeout=1000)
        but_1 = types.InlineKeyboardButton(text="NumberOne", callback_data="NumberOne")
        but_2 = types.InlineKeyboardButton(text="NumberTwo", callback_data="NumberTwo")
        but_3 = types.InlineKeyboardButton(text="NumberTree", callback_data="NumberTree")
        but_4 = types.InlineKeyboardButton(text="Number4", callback_data="Number4")
        self.keyboard.add(but_1, but_2, but_3, but_4)
        msg = self.tg_bot.send_message(message.chat.id, "ВЫБЕРИТЕ КНОПКУ", reply_markup=self.keyboard)

    def __menu_handler(self, call):
        print(call.data)
