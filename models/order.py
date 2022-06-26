# Компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, Integer, ForeignKey, DateTime
# Импортируем модуль для связки таблиц
from sqlalchemy.orm import relationship, backref
# Класс-конструктор для работы с декларативным стилем работы с SQLAlchemy
from data_base.dbcore import Base
# Импортируем модель продуктов для связки моделей
from models.product import Products


class Order(Base):
    """
    Класс для создания таблицы "Заказ",
    основан на декларативном стиле SQLAlchemy
    """
    # Название таблицы
    __tablename__ = 'orders'

    # Поля таблицы
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    date = Column(DateTime)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer)

    # Для каскадного удаления данных из таблицы
    products = relationship(
        Products,
        backref=backref(
            'orders',
            uselist=True,
            cascade='delete, all'
        )
    )

    def __str__(self) -> str:
        """
        Метод возвращает строковое представление объекта класса

        :return: str
        """
        return f'{self.quantity} {self.date}'
