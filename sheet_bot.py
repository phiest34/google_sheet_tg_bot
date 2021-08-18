import gspread
import telebot
import json
from telebot import types
from constants import *
from utils import *


class Menu_type:
    CHOOSE_SHEET_MENU = 1
    CHOOSE_CATEGORY_MENU = 2


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

        @self.tg_bot.message_handler(func=lambda call: True)
        def test_handler(call):
            print(call.data)

        @self.tg_bot.callback_query_handler(func=lambda call: Menu_type.CHOOSE_SHEET_MENU in json.loads(call.data))
        def sheet_menu_handler(call):
            self.__sheet_menu_handler(call)

        @self.tg_bot.callback_query_handler(func=lambda call: Menu_type.CHOOSE_CATEGORY_MENU in json.loads(call.data))
        def category_menu_handler(call):
            self.__category_menu_handler(call)

    def __send_welcome(self, message):
        keyboard = types.InlineKeyboardMarkup()
        sheets = self.sheet.worksheets()
        sheet_names = self.__get_sheets_names(sheets)
        buttons = list(
            map(lambda name: types.InlineKeyboardButton(text=name,
                                                        callback_data=json.dumps({Menu_type.CHOOSE_SHEET_MENU: name})),
                sheet_names))
        buttons.append(types.InlineKeyboardButton(text="Создать новую таблицу",
                                                  callback_data=json.dumps({Menu_type.CHOOSE_SHEET_MENU: -1})))
        keyboard.add(*buttons)
        self.tg_bot.send_message(message.chat.id, "Выбери таблицу для редактирования", reply_markup=keyboard)

    def __sheet_menu_handler(self, call):
        value = json.loads(call.data)[Menu_type.CHOOSE_SHEET_MENU]
        if value == -1:
            self.__show_enter_table_name(call.message.chat.id)
        else:
            sheet_names = self.__get_sheets_names(self.sheet.worksheets())
            index = index_of(sheet_names, value)
            if index != -1:
                self.__edit_worksheet(call.message.chat.id, self.sheet.worksheets()[index])

    def __category_menu_handler(self, call):
        value = json.loads(call.data)[Menu_type.CHOOSE_CATEGORY_MENU]
        print(value)

    def __reply_handler(self, message):
        if message.reply_to_message.id == self.__get_message_id():
            self.sheet.add_worksheet(title=message.text, rows=0, cols=0)

    def __show_enter_table_name(self, chat_id):
        markup = types.ForceReply(selective=False)
        msg = self.tg_bot.send_message(chat_id, "Введите название таблицы", reply_markup=markup)
        self.__save_message_id(msg.id)

    def __save_message_id(self, message_id):
        self.reply_message_id = message_id

    def __get_message_id(self):
        return self.reply_message_id

    def __edit_worksheet(self, chat_id, sheet):
        keyboard = types.InlineKeyboardMarkup()
        menu_string = starts_with_hash(sheet.get_all_values())
        buttons = []
        for item in menu_string:
            buttons.append(types.InlineKeyboardButton(
                text=item, callback_data=json.dumps({Menu_type.CHOOSE_CATEGORY_MENU, item}))
            )
        keyboard.add(*buttons)
        self.tg_bot.send_message(chat_id, "Выбери категорию", reply_markup=keyboard)

    def __get_sheets_names(self, sheets):
        return list(map(lambda sheet: sheet.title, sheets))
