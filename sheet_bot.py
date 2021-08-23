import sys

import gspread
import telebot

from gspread import Worksheet, Cell
from telebot import types
from telebot.types import Message

from constants import *
from utils import *
from string_int_converter import String_int_converter


class Sheet_bot:
    def __init__(self, token: str):
        self.add_worksheet_reply_message_id = 0
        self.enter_values_reply_message_id = 0
        self.tg_bot = telebot.TeleBot(token)
        self.sheet = gspread.service_account().open_by_key(SHEET_KEY)
        self.converter = String_int_converter()
        self.context = {WORKSHEET: None,
                        CATEGORY: None,
                        CHAT_ID: None,
                        FIELDS_COUNT: None}

    def start_bot(self):
        self.__register_handlers()
        self.tg_bot.polling(none_stop=True)

    def __register_handlers(self):
        @self.tg_bot.message_handler(commands=['info'])
        def send_info(message):
            self.__send_info(message)

        @self.tg_bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.__send_welcome(message)

        @self.tg_bot.message_handler(content_types=["text"])
        def message_handler(message):
            self.__reply_handler(message)

        @self.tg_bot.callback_query_handler(func=lambda call: CHOOSE_SHEET_MENU in from_json(call.data))
        def sheet_menu_handler(call):
            self.__sheet_menu_handler(call)

        @self.tg_bot.callback_query_handler(func=lambda call: CHOOSE_CATEGORY_MENU in from_json(call.data))
        def category_menu_handler(call):
            self.__category_menu_handler(call)

    def __send_info(self, message: Message):
        self.tg_bot.send_message(message.chat.id, Strings.CONNECT_TO_DEV)

    def __send_welcome(self, message: Message):
        self.context[CHAT_ID] = message.chat.id
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        sheets = self.sheet.worksheets()
        sheet_names = self.__get_sheets_names(sheets)
        buttons = []
        for name in sheet_names:
            self.converter.set_string(name)
            buttons.append(types.InlineKeyboardButton(text=name, callback_data=dict_to_json(
                {CHOOSE_SHEET_MENU: self.converter.get_int(name)})))
        buttons.append(types.InlineKeyboardButton(text=Strings.CREATE_NEW_TABLE,
                                                  callback_data=dict_to_json(
                                                      {CHOOSE_SHEET_MENU: CREATE_NEW_TABLE})
                                                  ))
        keyboard.add(*buttons)
        self.tg_bot.send_message(message.chat.id, Strings.SELECT_TABLE, reply_markup=keyboard)

    def __sheet_menu_handler(self, call):
        value = json.loads(call.data)[CHOOSE_SHEET_MENU]
        if value == CREATE_NEW_TABLE:
            self.context[WORKSHEET] = SELECTING_TABLE
            self.__show_enter_table_name()
        else:
            string_value = self.converter.get_string(int(value))
            sheet_names = self.__get_sheets_names(self.sheet.worksheets())
            index = index_of(sheet_names, string_value)
            if index != -1:
                cur_sheet = self.sheet.worksheets()[index]
                self.context[WORKSHEET] = cur_sheet
                text = Strings.CURRENT_SHEET + cur_sheet.title
                self.tg_bot.send_message(self.context[CHAT_ID], text)
                self.context[CATEGORY] = None
                self.__edit_worksheet(call.message.chat.id, cur_sheet)

    def __category_menu_handler(self, call):
        coordinates = from_json(call.data)[CHOOSE_CATEGORY_MENU]
        cell = self.context[CATEGORY] = self.context[WORKSHEET].cell(coordinates[0] + 1, coordinates[1] + 1)
        if cell is not None:
            text = Strings.CURRENT_CATEGORY + cell.value
            self.tg_bot.send_message(self.context[CHAT_ID], text)
            self.__send_enter_fields_values_message(Strings.ENTER_FIELDS)

    def __send_enter_fields_values_message(self, text):
        chat_id = self.context[CHAT_ID]
        markup = types.ForceReply(selective=False)
        fields = self.__get_fields()
        enter_message = text
        for field in fields:
            enter_message += str(field) + ' '
        msg = self.tg_bot.send_message(chat_id, enter_message, reply_markup=markup)
        self.enter_values_reply_message_id = msg.id

    def __reply_handler(self, message):
        if message.reply_to_message is not None:
            if message.reply_to_message.id == self.add_worksheet_reply_message_id:
                self.sheet.add_worksheet(title=message.text, rows=0, cols=0)
            if message.reply_to_message.id == self.enter_values_reply_message_id:
                self.__handle_values_message(message.text)

    def __show_enter_table_name(self):
        markup = types.ForceReply(selective=False)
        chat_id = self.context[CHAT_ID]
        msg = self.tg_bot.send_message(chat_id, Strings.CREATE_NEW_TABLE, reply_markup=markup)
        self.add_worksheet_reply_message_id = msg.id

    def __edit_worksheet(self, chat_id: int, sheet: Worksheet):
        keyboard = types.InlineKeyboardMarkup()
        sheet_data = starts_with_hash(sheet.get_all_values())
        buttons = []
        for item in sheet_data:
            callback_data = dict_to_json({CHOOSE_CATEGORY_MENU: item})
            cell = sheet.cell((item[0] + 1), (item[1] + 1))
            text = cell.value
            buttons.append(types.InlineKeyboardButton(text=text, callback_data=callback_data))
        keyboard.add(*buttons)
        if buttons:
            self.tg_bot.send_message(chat_id, Strings.SELECT_CATEGORY, reply_markup=keyboard)
        else:
            self.tg_bot.send_message(chat_id, Strings.CATEGORY_EMPTY_EXCEPTION)

    def __get_sheets_names(self, sheets: [Worksheet]):
        return list(map(lambda sheet: sheet.title, sheets))

    def __get_fields(self):
        sheet = self.context[WORKSHEET]
        cell = self.context[CATEGORY]
        values = sheet.row_values(cell.row)
        index = values.index(cell.value)
        sliced = values[index + 1:]
        fields = [values[index]]
        for item in sliced:
            if item == '' or item.startswith('#'):
                break
            else:
                fields.append(item)
        self.context[FIELDS_COUNT] = len(fields)
        return fields

    def __handle_values_message(self, text):
        values = text.split()
        fields_count = self.context[FIELDS_COUNT]
        if fields_count != len(values):
            self.__send_enter_fields_values_message(Strings.ENTER_FIELDS_COUNT_EXCEPTION)
            return
        coordinates = self.context[CATEGORY].row, self.context[CATEGORY].col
        dx = 0
        while True:
            if not self.context[WORKSHEET].cell(coordinates[0] + dx, coordinates[1]).value:
                break
            dx += 1
        for dy in range(len(values)):
            self.context[WORKSHEET].update_cell(coordinates[0] + dx, coordinates[1] + dy, values[dy])
