# Компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, String, Integer, Boolean
# Класс-конструктор для работы с декларативным стилем работы с SQLAlchemy
from data_base.dbcore import Base


class Category(Base):
    """
    Класс-модель для описания таблицы "Категория товара",
    основан на декларативном стиле SQLAlchemy
    """
    # название таблицы
    __tablename__ = 'category'

    # поля таблицы
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    is_active = Column(Boolean)

    def __str__(self) -> str:
        """
        Метод возвращает строковое представление объекта класса

        :return: str
        """
        return self.name
