# Импортируем библиотеку abc для реализации абстрактных классов
import abc
# Импортируем разметку клавиатуры и клавиш
from markup.markup import Keyboards
# Импортируем класс-менеджер для работы с библиотекой
from data_base.dbalchemy import DBManager
from telebot import TeleBot


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, bot: TeleBot) -> None:
        # Получаем объект бота
        self.bot = bot
        # Инициализируем разметку кнопок
        self.keyboards = Keyboards()
        # Инициализируем менеджер для работы с БД
        self.BD = DBManager()

    @abc.abstractmethod
    def handle(self) -> None:
        pass
