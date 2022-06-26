# Импортируем специальные типы телеграм бота для создания элементов интерфейса
from telebot.types import (KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
                           InlineKeyboardMarkup, InlineKeyboardButton)
# Импортируем настройки и утилиты
from settings import config
# Импортируем класс-менеджер для работы с библиотекой DBAlchemy
from data_base.dbalchemy import DBManager

from models.product import Products


class Keyboards:
    """
    Класс Keyboards предназначен для создания и разметки интерфейса бота
    """

    # Инициализация разметки
    def __init__(self) -> None:
        self.markup = None
        # Инициализируем менеджер для работы в БД
        self.BD = DBManager()

    def set_btn(self, name, step: int = 0, quantity: int = 0) -> KeyboardButton:
        """
        Создает и возвращает кнопку по входным параметрам

        :param name: Внутреннее имя кнопки
        :param step: Номер позиции в заказе товаров
        :param quantity: Количество товара
        :return: Объект кнопки
        """
        if name == 'AMOUNT_ORDERS':
            config.KEYBOARD['AMOUNT_ORDERS'] = '{} {} {}'.format(step + 1, ' из ', str(self.BD.count_rows_order()))

        if name == 'AMOUNT_PRODUCT':
            config.KEYBOARD['AMOUNT_PRODUCT'] = '{}'.format(quantity)

        return KeyboardButton(config.KEYBOARD[name])

    def start_menu(self) -> ReplyKeyboardMarkup:
        """
        Создает разметку в основном меню и возвращает разметку

        :return: Объект клавиатуры
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('CHOOSE_GOODS')
        itm_btn_2 = self.set_btn('INFO')
        itm_btn_3 = self.set_btn('SETTINGS')
        # Расположение кнопок в меню
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2, itm_btn_3)
        return self.markup

    def info_menu(self) -> ReplyKeyboardMarkup:
        """
        Создаем разметку кнопок в меню info

        :return: ReplyKeyboardMarkup
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        # Расположение кнопок в меню
        self.markup.row(itm_btn_1)
        return self.markup

    def settings_menu(self) -> ReplyKeyboardMarkup:
        """
        Создаем разметку кнопок в меню settings

        :return: Объект клавиатуры
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        # Расположение кнопок в меню
        self.markup.row(itm_btn_1)
        return self.markup

    @staticmethod
    def remove_menu() -> ReplyKeyboardRemove:
        """
        Удаляет данные кнопки и возвращает её

        :return: Объект удаления клавиатуры
        """
        return ReplyKeyboardRemove()

    def category_menu(self) -> ReplyKeyboardMarkup:
        """
        Создает разметку кнопок в меню категорий товара и возвращает разметку

        :return: Объект клавиатуры
        """
        self.markup = ReplyKeyboardMarkup(True, True, row_width=1)
        self.markup.add(self.set_btn('SEMIPRODUCT'))
        self.markup.add(self.set_btn('GROCERY'))
        self.markup.add(self.set_btn('ICE_CREAM'))
        self.markup.row(self.set_btn('<<'), self.set_btn('ORDER'))
        return self.markup

    @staticmethod
    def set_inline_btn(product: Products) -> InlineKeyboardButton:
        """
        Создает и возвращает инлайн кнопку по входным параметрам

        :param product: Объект товара
        :return: Объект строковой кнопки
        """
        return InlineKeyboardButton(
            str(product),
            callback_data=str(product.id)
        )

    def set_select_category(self, category: str) -> InlineKeyboardMarkup:
        """
        Создаёт разметку инлайн кнопок в выбранной категории товаров и возвращает разметку

        :param category: Название категории
        :return: Объект строковой клавиатуры
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        # Загружаем в название инлайн кнопок данные из БД
        # в соответствии с категорий товара
        for item in self.BD.select_all_products_category(category):
            self.markup.add(self.set_inline_btn(item))

        return self.markup

    def orders_menu(self, step: int, quantity: int) -> ReplyKeyboardMarkup:
        """
        Создает разметку кнопок в заказе товара и возвращает разметку

        :param step: номера товаров в заказе
        :param quantity: количество товара
        """
        self.markup = ReplyKeyboardMarkup(True, True, row_width=4)
        itm_btn_1 = self.set_btn('X', step, quantity)
        itm_btn_2 = self.set_btn('DOWN', step, quantity)
        itm_btn_3 = self.set_btn('AMOUNT_PRODUCT', step, quantity)
        itm_btn_4 = self.set_btn('UP', step, quantity)
        itm_btn_5 = self.set_btn('BACK_STEP', step, quantity)
        itm_btn_6 = self.set_btn('AMOUNT_ORDERS', step, quantity)
        itm_btn_7 = self.set_btn('NEXT_STEP', step, quantity)
        itm_btn_8 = self.set_btn('APPLY', step, quantity)
        itm_btn_9 = self.set_btn('<<', step, quantity)

        # Расположение кнопок
        self.markup.add(itm_btn_1, itm_btn_2, itm_btn_3, itm_btn_4)
        self.markup.add(itm_btn_5, itm_btn_6, itm_btn_7)
        self.markup.add(itm_btn_9, itm_btn_8)

        return self.markup
