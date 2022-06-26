# импортируем класс родитель
from handlers.handler import Handler
from telebot import TeleBot
from telebot.types import Message


class HandlerCommands(Handler):
    """
    Класс обрабатывает входящие команды /start и /help и т.п.
    """

    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def pressed_btn_start(self, message: Message) -> None:
        """
        Обрабатывает входящие /start команды
        :param message: Message
        """
        self.bot.send_message(
            message.chat.id,
            f'{message.from_user.first_name},'
            f' здравствуйте! Жду дальнейших задач.',
            reply_markup=self.keyboards.start_menu()
        )

    def handle(self) -> None:
        """
        Обработчик (декоратор) сообщений,
        который обрабатывает входящие /start команды.
        """
        @self.bot.message_handler(commands=['start'])
        def handle(message: Message) -> None:
            # FIXME: Сомнительное условие, особенно потому что проверяется выше
            if message.text == '/start':
                self.pressed_btn_start(message)
