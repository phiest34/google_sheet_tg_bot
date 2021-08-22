from flags import *

BOT_TOKEN = "1986859160:AAH3orsGfaNkicVhUs4oYQqBZD3z-5cPkCw"

DEBUG_KEY = "1AFY3k-jftyOPo6TNGUKhpjGUhl_V0FrZ1uVnwlaGD54"
LIVE_KEY = "1Jap3p2hXbr1_J6fJtFwRY4-zNUzrUUZXks9PQruJf1o"

debug = True

SHEET_KEY = DEBUG_KEY if debug else LIVE_KEY


# strings:
class Strings:
    CONNECT_TO_DEV = "Если вы нашли баг или есть проблемы в работе бота,пишите в телеграм: @phiest34"
    SELECT_TABLE = "Выбери таблицу для редактирования"
    CREATE_NEW_TABLE = "Создать новую таблицу"
    ENTER_TABLE_NAME = "Введите название таблицы"
    SELECT_CATEGORY = "Выбери категорию"
    ENTER_FIELDS = "Введите: "
    ENTER_FIELDS_COUNT_EXCEPTION = "Вы ввели неверное количество данных, Введите: "


# menu
__menu_types_instance = Menu_types()
CHOOSE_SHEET_MENU = __menu_types_instance.CHOOSE_SHEET_MENU
CHOOSE_CATEGORY_MENU = __menu_types_instance.CHOOSE_CATEGORY_MENU

# callback data
__callback_data_instance = Callback_data()
CREATE_NEW_TABLE = __callback_data_instance.CREATE_NEW_TABLE

# context keys
__context_keys = Context_keys()
WORKSHEET = __context_keys.WORKSHEET
CATEGORY = __context_keys.CATEGORY
CHAT_ID = __context_keys.CHAT_ID
FIELDS_COUNT = __context_keys.FIELDS_COUNT

# states
states = States()
SELECTING_TABLE = states.SELECTING_TABLE
