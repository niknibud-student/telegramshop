# Импортируем класс-родитель
from handlers.handler import Handler
# Импортируем настройки и вспомогательные функции
from settings import config, utility
# Импортируем сообщения
from settings.message import MESSAGES
# Типизация
from telebot import TeleBot
from telebot.types import Message


class HandlerAllText(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на кнопки
    """

    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)
        # Шаг в заказе
        self.step = 0

    def pressed_btn_category(self, message: Message) -> None:
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку 'Выбрать товар'

        :param message: Объект сообщения
        """
        self.bot.send_message(
            message.chat.id,
            'Каталог категорий товара',
            reply_markup=self.keyboards.remove_menu()
        )
        self.bot.send_message(
            message.chat.id,
            'Сделай свой выбор',
            reply_markup=self.keyboards.category_menu()
        )

    def pressed_btn_info(self, message: Message) -> None:
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку 'Trading Store'

        :param message: Объект сообщения
        """
        self.bot.send_message(
            message.chat.id,
            MESSAGES['trading_store'],
            parse_mode='HTML',
            reply_markup=self.keyboards.info_menu()
        )

    def pressed_btn_settings(self, message: Message) -> None:
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку 'Settings'

        :param message: Объект сообщения
        """
        self.bot.send_message(
            message.chat.id,
            MESSAGES['settings'],
            parse_mode='HTML',
            reply_markup=self.keyboards.settings_menu()
        )

    def pressed_btn_back(self, message: Message) -> None:
        """
         Обрабатывает входящие текстовые сообщения от нажатия на кнопку Back

        :param message: Объект сообщения
        """
        self.bot.send_message(
            message.chat.id,
            'Вы вернулись назад',
            reply_markup=self.keyboards.start_menu()
        )

    def pressed_btn_product(self, message: Message, product: str) -> None:
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопки каталога товаров

        :param message: Объект Message Телеграмма
        :param product: Название (английское) категории товаров
        """
        self.bot.send_message(
            message.chat.id,
            f'Категория {config.KEYBOARD[product]}',
            reply_markup=self.keyboards.set_select_category(config.CATEGORY[product])
        )
        self.bot.send_message(
            message.chat.id,
            'OK',
            reply_markup=self.keyboards.category_menu()
        )

    def pressed_btn_order(self, message: Message) -> None:
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку 'Заказ'

        :param message: Объект сообщения Телеграмм
        """
        # обнуляем данные шага
        self.step = 0
        # получаем список всех товаров в заказе
        products_id = self.BD.select_all_product_id()
        # получаем количество в каждой позиции товара в заказе
        quantity = self.BD.select_order_quantity(products_id[self.step])

        # отправляем ответ пользователю
        self.send_message_order(products_id[self.step], quantity, message)

    def send_message_order(self, product_id: int, quantity: int, message: Message) -> None:
        """
        Отправляем ответ пользователю при выполнении различных действий

        :param product_id: ИД товара
        :param quantity: количество товара
        :param message: Объект сообщения Телеграмм
        """
        self.bot.send_message(message.chat.id, MESSAGES['order_number'].format(self.step+1), parse_mode='HTML')
        self.bot.send_message(
            message.chat.id,
            MESSAGES['order'].format(
                self.BD.select_single_product_name(product_id),
                self.BD.select_single_product_title(product_id),
                self.BD.select_single_product_price(product_id),
                self.BD.select_single_product_quantity(product_id),
            ),
            parse_mode='HTML',
            reply_markup=self.keyboards.orders_menu(self.step, quantity)
        )

    def pressed_btn_up(self, message: Message) -> None:
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку UP

        :param message: Объект сообщения Телеграм
        """
        # Получаем список всех ИД товаров в заказе
        products_id = self.BD.select_all_product_id()
        # Получаем количество конкретной позиции товара в заказе
        quantity_order = self.BD.select_order_quantity(products_id[self.step])
        # Получаем количество конкретной позиции товара на складе
        quantity_product = self.BD.select_single_product_quantity(products_id[self.step])
        # Если товар есть
        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            # Вносим изменения в таблицу Orders
            self.BD.update_order_quantity(products_id[self.step], 'quantity', quantity_order)
            # Вносим изменения в таблицу Products
            self.BD.update_product_quantity(products_id[self.step], 'quantity', quantity_product)
        # отправляем ответ пользователю
        self.send_message_order(products_id[self.step], quantity_order, message)

    def pressed_btn_down(self, message: Message) -> None:
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку DOWN

        :param message: Объект сообщения Телеграм
        """
        # Получаем список всех ИД товаров в заказе
        products_id = self.BD.select_all_product_id()
        # Получаем количество конкретной позиции товара в заказе
        quantity_order = self.BD.select_order_quantity(products_id[self.step])
        # Получаем количество конкретной позиции товара на складе
        quantity_product = self.BD.select_single_product_quantity(products_id[self.step])
        # Если товар есть
        if quantity_product > 0:
            quantity_order -= 1
            quantity_product += 1
            # Вносим изменения в таблицу Orders
            self.BD.update_order_quantity(products_id[self.step], 'quantity', quantity_order)
            # Вносим изменения в таблицу Products
            self.BD.update_product_quantity(products_id[self. step], 'quantity', quantity_product)
        # отправляем ответ пользователю
        self.send_message_order(products_id[self.step], quantity_order, message)

    def pressed_btn_del(self, message: Message) -> None:
        """
        Обрабатывает входящие текстовые сообщения от нажатия кнопки Х - удалите позицию товара

        :param message: Объект сообщения Телеграм
        """
        # Получаем список всех ИД товаров в заказе
        products_id = self.BD.select_all_product_id()
        # если список не пуст
        if products_id.__len__() > 0:
            # Получаем количество конкретной позиции товара в заказе
            quantity_order = self.BD.select_order_quantity(products_id[self.step])
            # Получаем количество конкретной позиции товара на складе
            quantity_product = self.BD.select_single_product_quantity(products_id[self.step])
            quantity_product += quantity_order
            # Вносим изменения в таблицу Orders
            self.BD.delete_order(products_id[self.step])
            # Вносим изменения в таблицу Products
            self.BD.update_product_quantity(products_id[self.step], 'quantity', quantity_product)
            # Уменьшаем шаг
            if self.step > 0:
                self.step -= 1

        products_id = self.BD.select_all_product_id()
        # если список не пуст
        if products_id.__len__() > 0:
            quantity_order = self.BD.select_order_quantity(products_id[self.step])
            # отправляем ответ пользователю
            self.send_message_order(products_id[self.step], quantity_order, message)
        else:
            # если товара нет в заказе отправляем сообщение
            self.bot.send_message(
                message.chat.id,
                MESSAGES['no_order'],
                parse_mode='HTML',
                reply_markup=self.keyboards.category_menu()
            )

    def pressed_btn_back_step(self, message: Message) -> None:
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку BACK_STEP

        :param message: Объект сообщения Телеграм
        """
        # уменьшаем шаг до тех пока шаг не будет равен 0
        if self.step > 0:
            self.step -= 1
        # Получаем список всех ИД товаров в заказе
        products_id = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(products_id[self.step])

        # отправляем ответ пользователю
        self.send_message_order(products_id[self.step], quantity, message)

    def pressed_btn_next_step(self, message: Message) -> None:
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку NEXT_STEP

        :param message: Объект сообщения Телеграм
        """
        # Увеличивает шаг до тех пор, пока шаг не будет равен количество строк полей заказа
        if self.step < self.BD.count_rows_order() - 1:
            self.step += 1
        # Получаем список всех ИД товаров в заказе
        products_id = self.BD.select_all_product_id()
        # Получаем количество конкретного товара в соответствии с шагом выборки
        quantity = self.BD.select_order_quantity(products_id[self.step])
        # отправляем ответ пользователю
        self.send_message_order(products_id[self.step], quantity, message)

    def pressed_btn_apply(self, message: Message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку 'Оформить заказ'

        :param message: Объект сообщения Телеграм
        """
        self.bot.send_message(
            message.chat.id,
            MESSAGES['apply'].format(
                utility.get_total_cost(self.BD),
                utility.get_total_quantity(self.BD)
            ),
            parse_mode='HTML',
            reply_markup=self.keyboards.category_menu()
        )
        # очищаем данные из заказа
        self.BD.delete_all_order()

    def handle(self) -> None:
        """
        Обработчик (декоратор) сообщений,
        который обрабатывает входящие текстовые сообщения от нажатия кнопок
        """
        @self.bot.message_handler(func=lambda message: True)
        def handle(message: Message) -> None:
            # ********** Меню ********** #
            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)
            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            if message.text == config.KEYBOARD['ORDER']:
                # если есть заказ
                if self.BD.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(
                        message.chat.id,
                        MESSAGES['no_order'],
                        parse_mode='HTML',
                        reply_markup=self.keyboards.category_menu(),
                    )

            # ********** меню (категории товаров, ПФ, Бакалея, Мороженое ***********
            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')

            # ********** меню (Заказа) **********
            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)

            if message.text == config.KEYBOARD['DOWN']:
                self.pressed_btn_down(message)

            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_del(message)

            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)

            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)

            if message.text == config.KEYBOARD['APPLY']:
                self.pressed_btn_apply(message)
            # иные нажатия и ввод данных пользователем
            else:
                self.bot.send_message(message.chat.id, message.text)
