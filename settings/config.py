import os
import os.path
# Импортируем модуль emoji для отображения эмоджи
from emoji import emojize
from decouple import config

# Токен выдается при регистрации бота в BotFather
TOKEN = os.getenv('TOKEN')
# База данных
NAME_DB = 'products.db'
# Версия приложения
VERSION = '0.0.1'
# Автор приложения
AUTHOR = 'User'

# Родительская директория
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Путь до базы данных
DATABASE = os.path.join('sqlite:///' + BASE_DIR, NAME_DB)

COUNT = 0

# Кнопки управления
KEYBOARD = {
    'CHOOSE_GOODS': emojize(':open_file_folder: Выбрать товар'),
    'INFO': emojize(':speech_balloon: О магазине'),
    'SETTINGS': emojize('⚙ Настройки'),
    'SEMIPRODUCT': emojize(':pizza: Полуфабрикаты'),
    'GROCERY': emojize(':bread: Бакалея'),
    'ICE_CREAM': emojize(':shaved_ice: Мороженное'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀'),
    'NEXT_STEP': emojize('▶'),
    'ORDER': emojize('✔ ЗАКАЗ'),
    'X': emojize('❌'),
    'DOWN': emojize('🔽'),
    'UP': emojize('🔼'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'APPLY': '✔ Оформить заказ',
    'COPY': '©  ',
}

# ID категорий товаров
CATEGORY = {
    'SEMIPRODUCT': 1,
    'GROCERY': 2,
    'ICE_CREAM': 3,
}

# Названия команд
COMMANDS = {
    'START': 'start',
    'HELP': 'help',
}
