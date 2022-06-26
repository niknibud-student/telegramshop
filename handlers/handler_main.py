# Импортируем класс HandlerCommands - обработка команд
from handlers.handler_com import HandlerCommands
# Импортируем класс HandlerAllText - обработка нажатия на кнопки и иные сообщения
from handlers.handler_all_text import HandlerAllText
from handlers.handler_inline_query import HandlerInlineQuery
from telebot import TeleBot


class HandlerMain:
    """
    Класс компоновщик
    """

    def __init__(self, bot: TeleBot) -> None:
        # Получаем объект бота
        self.bot = bot
        # здесь происходит инициализация обработчиков
        self.handle_commands = HandlerCommands(self.bot)
        self.handler_all_text = HandlerAllText(self.bot)
        self.handler_inline_query = HandlerInlineQuery(self.bot)

    def handle(self) -> None:
        # здесь происходит запуск обработчиков
        self.handle_commands.handle()
        self.handler_all_text.handle()
        self.handler_inline_query.handle()
    