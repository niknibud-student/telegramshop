# импортируем класс родитель
from handlers.handler import Handler
# импортируем сообщения пользователю
from settings.message import MESSAGES
from telebot import TeleBot
from telebot.types import CallbackQuery


class HandlerInlineQuery(Handler):
    """
    Класс обрабатывает входящие текстовые
    сообщения от нажатия на инлайн кнопки
    """

    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def pressed_btn_product(self, call: CallbackQuery, code: int) -> None:
        """
        Обрабатывает входящие запросы на нажатие inline-кнопок товара
        :param call: Callback
        :param code:
        :return: None
        """
        # создаем запись в БД по факту заказа
        self.BD.add_orders(1, code, 1)

        self.bot.answer_callback_query(
            call.id,
            MESSAGES['product_order'].format(
                self.BD.select_single_product_name(code),
                self.BD.select_single_product_title(code),
                self.BD.select_single_product_price(code),
                self.BD.select_single_product_quantity(code),
            ),
            show_alert=True,
        )

    def handle(self) -> None:
        # обработчик (декоратор) запросов от нажатия на кнопки товара
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call: CallbackQuery) -> None:
            code = call.data
            if code.isdigit():
                code = int(code)

            self.pressed_btn_product(call, code)
