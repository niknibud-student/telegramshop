from os import path
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_base.dbcore import Base

from settings import config, utility
from models.product import Products
from models.order import Order

from typing import Tuple, List


class Singleton(type):
    """
    Паттерн Singleton предоставляет механизм одного
    и только одного объекта класса,
    и представление к нему глобальной точки доступа
    """

    def __init__(cls, name, bases, attrs) -> None:
        """
        Инициализация паттерна Singleton

        :param name: Имя базы данных
        :type name: str
        :param bases: Экземпляры объектов БД
        :type bases: Tuple
        :param attrs: Атрибуты
        """
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs) -> "Singleton":
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    """
    Класс-менеджер для работы с БД
    """

    def __init__(self) -> None:
        """
        Инициализация сессии и подключения к БД
        """
        self.engine = create_engine(config.DATABASE)
        session = sessionmaker(bind=self.engine)
        self._session = session()
        if not path.isfile(config.DATABASE):
            Base.metadata.create_all(self.engine)

    def select_all_products_category(self, category: str) -> List:
        """
        Возвращает все строки товара категории

        :param category: Категория товаров
        :return: Список товаров категории
        """
        result = self._session.query(Products).filter_by(category_id=category).all()
        self.close()
        return result

    def close(self) -> None:
        """ Закрываете сессию """
        self._session.close()

    # Работа с заказом
    # self.BD._add_orders(1, code, 1)
    def add_orders(self, quantity: int, product_id: int, user_id: int) -> None:
        """
        Метод заполнения заказа

        :param quantity: количество
        :param product_id: ИД продукта
        :param user_id: ИД пользователя
        :return: None
        """
        # получаем список всех product_id
        all_id_products = self.select_all_product_id()
        # если данные есть в списке, обновляем таблицы заказа и продуктов
        if product_id in all_id_products:
            quantity_order = self.select_order_quantity(product_id)
            quantity_order += 1
            self.update_order_quantity(product_id, 'quantity', quantity_order)

            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_quantity(product_id, 'quantity', quantity_product)
            return
        # если данных нет, создаем новый объект заказа
        else:
            order = Order(quantity=quantity, product_id=product_id, user_id=user_id, date=datetime.now())
            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_quantity(product_id, 'quantity', quantity_product)

        self._session.add(order)
        self._session.commit()
        self.close()

    def select_all_product_id(self) -> List:
        """
        Возвращает все id товара в заказе

        :return: Список id товаров в заказе
        """
        result = self._session.query(Order.product_id).all()
        self.close()
        # конвертируем результат выборки в вид [1, 3, 5, ...]
        return utility.convert(result)

    def select_order_quantity(self, product_id: int) -> int:
        """
        Возвращает количество товара в заказе

        :param product_id: ИД товара
        :return: количество товара в заказе
        """
        result = self._session.query(Order.quantity).filter_by(product_id=product_id).one()
        self.close()
        return result.quantity

    def select_single_product_quantity(self, product_id: int) -> int:
        """
        Возвращает количество товара на складе в соответствии с номером товара - row_num
        Этот номер определяется при выборе товара в интерфейсе

        :param product_id: номер товара
        :return: количество товара на складе
        """
        result = self._session.query(Products.quantity).filter_by(id=product_id).one()
        self.close()
        return result.quantity

    def update_product_quantity(self, product_id: int, name: str, quantity: int) -> None:
        """
        Обновляет количество товара на складе в соответствии с ИД товара

        :param product_id: ИД товара
        :param name: Название товара
        :param quantity: Количество
        :return: None
        """
        self._session.query(Products).filter_by(id=product_id).update({name: quantity})
        self._session.commit()
        self.close()

    def update_order_quantity(self, product_id: int, name: str, quantity: int) -> None:
        """
        Обновляет данные указанной позиции заказа в соответствии с ИД товара
        :param product_id:
        :param name:
        :param quantity:
        :return: None
        """
        self._session.query(Order).filter_by(product_id=product_id).update({name: quantity})
        self._session.commit()
        self.close()

    def select_single_product_name(self, product_id: int) -> str:
        """
        Возвращает название товара в соответствии с ИД товара

        :param product_id: ИД товара
        :return: Название товара
        """
        result = self._session.query(Products.name).filter_by(id=product_id).one()
        self.close()
        return result.name

    def select_single_product_title(self, product_id: int) -> str:
        """
        Возвращает торговую марку товара в соответствии с ИД товара

        :param product_id: ИД товара
        :return: Торговая марка товара
        """
        result = self._session.query(Products.title).filter_by(id=product_id).one()
        self.close()
        return result.title

    def select_single_product_price(self, product_id: int) -> float:
        """
        Возвращает цена товара в соответствии с ИД товара

        :param product_id: ИД товара
        :return: Цена товара
        """
        result = self._session.query(Products.price).filter_by(id=product_id).one()
        self.close()
        return result.price

    def count_rows_order(self) -> int:
        """
        Возвращает количество позиций в заказе

        :return: количество позиций в заказе
        """
        result = self._session.query(Order).count()
        self.close()
        return result

    def delete_order(self, product_id: int) -> None:
        """
        Удаляет данные указанной строки заказа

        :param product_id: ИД товара
        """
        self._session.query(Order).filter_by(product_id=product_id).delete()
        self._session.commit()
        self.close()

    def delete_all_order(self) -> None:
        """
        Удаляет данные всего заказа
        """
        order_ids = self.select_all_order_id()

        for pid in order_ids:
            self._session.query(Order).filter_by(id=pid).delete()
            self._session.commit()
        self.close()

    def select_all_order_id(self):
        """
        Возвращает все ИД товара из заказа
        """
        result = self._session.query(Order.id).all()
        self.close()
        return utility.convert(result)
