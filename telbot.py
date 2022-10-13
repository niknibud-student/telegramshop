# Импортируем класс создания объекта бота
from telebot import TeleBot
# Импортируем основные настройки проекта
from settings import config
# Импортируем главный класс-обработчик бота
from handlers.handler_main import HandlerMain


class TelBot:
    """
    Основной класс телеграм-бота (сервер), в основе которого
    используется библиотека pyTelegramBotAPI
    """

    __version__ = config.VERSION
    __author__ = config.AUTHOR

    def __init__(self) -> None:
        """
        Инициализация бота
        """
        # Получаем токен
        self._token: str = config.TOKEN
        # Инициализируем бот на основе зарегистрированного токена
        self.bot = TeleBot(self._token)
        # Инициализируем обработчик событий
        self.handler = HandlerMain(self.bot)

    def start(self) -> None:
        """
        Метод предназначен для старта обработчика событий
        """
        self.handler.handle()

    def run_bot(self) -> None:
        """
        Метод запускает основные события сервера
        """
        # Обработчик событий
        self.start()
        # Служит для запуска бота (в режиме нон-стоп)
        self.bot.polling(none_stop=True)


if __name__ == '__main__':
    bot = TelBot()
    bot.run_bot()
