# Компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
# Импортируем модуль для связки таблиц
from sqlalchemy.orm import relationship, backref
# Класс-конструктор для работы с декларативным стилем работы с SQLAlchemy
from data_base.dbcore import Base
# Импортируем модель Категория для связки моделей
from models.category import Category


class Products(Base):
    """
    Класс для создания таблицы "Товар",
    основан на декларативном стиле SQLAlchemy
    """
    # Название таблицы
    __tablename__ = 'products'

    # Поля таблицы
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    title = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    is_active = Column(Boolean)
    category_id = Column(Integer, ForeignKey('category.id'))

    # Для каскадного удаления данных из таблицы
    category = relationship(
        Category,
        backref=backref(
            'products',
            uselist=True,
            cascade='delete, all'
        )
    )

    def __str__(self) -> str:
        """
        Метод возвращает строковое представление объекта класса

        :return: str
        """
        return f'{self.name} {self.title} {self.price}'
