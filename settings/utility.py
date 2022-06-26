from typing import List, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from data_base.dbalchemy import DBManager


def convert(list_convert: List[Tuple]) -> List:
    """
    Конвертирует список из [(5,), (8,), ...] в [5, 8, ...]

    :param list_convert: Список кортежей
    :return: List
    """
    return [item[0] for item in list_convert]


def total_cost(list_quantity: List, list_price: List) -> float:
    """
    Считает общую сумму заказа и возвращает результат

    :param list_quantity: Список количества товара
    :param list_price: Список цен на товары
    :return: Общая сумма заказа
    """
    return sum(map(lambda x: x[0] * x[1], zip(list_quantity, list_price)))


def total_quantity(list_quantity: List) -> int:
    """
    Считаем общее количество единиц товара и возвращаем результат

    :param list_quantity: Список количества товара
    :return: Общее количество товара
    """
    return sum(list_quantity)


def get_total_cost(bd: 'DBManager') -> float:
    """
    Возвращает общую стоимость заказа

    :param bd: Объект менеджера базы данных
    :return: общая стоимость заказа
    """
    # Получаем список всех ИД товара из заказа
    products_id = bd.select_all_product_id()
    # Получаем список стоимости по всем позициям заказа в виде обычного списка
    prices = [bd.select_single_product_price(product_id) for product_id in products_id]
    # Получаем список количества по всем позициям заказа в видео обычного списка
    quantities = [bd.select_order_quantity(product_id) for product_id in products_id]
    # Возвращаем общую стоимость заказа
    return total_cost(quantities, prices)


def get_total_quantity(bd: 'DBManager') -> int:
    """
    Возвращает общее количество заказанного товара

    :param bd: Объект менеджера базы данных
    :return: Общее количество заказанного товара
    """
    # Получаем список всех ИД товара из заказа
    products_id = bd.select_all_product_id()
    # Получаем список количества по всем позициям заказа в видео обычного списка
    quantities = [bd.select_order_quantity(product_id) for product_id in products_id]
    # Возвращаем общую стоимость заказа
    return total_quantity(quantities)


if __name__ == '__main__':
    print(total_cost([1, 2, 3], [1.2, 3.4, 5.6]))
