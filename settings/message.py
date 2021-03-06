# Импортируем настройки для отображения эмоджи
from settings.config import KEYBOARD, VERSION, AUTHOR

# Ответ пользователю при посещении TradingStore
trading_store = """
<b>Добро пожаловать в приложение TradingStore!!!</b>

Данное приложение разработано специально для торговых представителей, далее <i>(ТП/СВ)</i>, а также для кладовщиков, 
коммерческих организаций осуществляющих оптово-розничную торговлю.

ТП используя приложение TradingStore, в удобной интуитивной форме смогут особого труда принять заказ от клиента. 
TradingStore поможет сформировать заказ и в удобном виде адресует кладовщику фирмы для дальнейшего комплектования заказа.
"""

# Ответ пользователю при посещении settings
settings = """
<b>Общее руководство приложением:</b>

<i>Навигация:</i>

<b>{} - </b><i>Назад</i>
<b>{} - </b><i>Вперёд</i>
<b>{} - </b><i>Увеличить</i>
<b>{} - </b><i>Уменьшить</i>
<b>{} - </b><i>Следующий</i>
<b>{} - </b><i>Предыдущий</i>

<i>Специальные кнопки:</i>

<b>{} - </b><i>Удалить</i>
<b>{} - </b><i>Заказ</i>
<b>{} - </b><i>Оформить заказ</i>

<i>Общая информация</i>

<b>Версия программы: - </b><i>{}</i>
<b>Разработчик: - </b><i>{}</i>

<b>{}Ваше имя</b>
""".format(
    KEYBOARD['<<'],
    KEYBOARD['>>'],
    KEYBOARD['UP'],
    KEYBOARD['DOWN'],
    KEYBOARD['NEXT_STEP'],
    KEYBOARD['BACK_STEP'],
    KEYBOARD['X'],
    KEYBOARD['ORDER'],
    KEYBOARD['APPLY'],
    VERSION,
    AUTHOR,
    KEYBOARD['COPY'],
)

# Ответ пользователю при посещении product_order
product_order = """
Выбранный товар:

{}
{}
Стоимость: {} руб.

Добавлен в заказ!!!

На складе осталось {} ед.
"""

# Ответ пользователю при посещении order
order = """

<i>Название:</i> <b>{}</b>

<i>Описание:</i> <b>{}</b>
<i>Стоимость:</i> <b>{} руб. за 1 ед.</b>
<i>Количество позиций:</i> <b>{} ед.</b>
"""

order_number = """

<b>Позиция в заказе №</b><i>{}</i>

"""

# Ответ пользователю при посещении no_order
no_order = """
<b>Заказ отсутствует!!!</b>
"""

# Ответ пользователю при посещении Apply
apply = """
<b>Ваш заказ оформлен!!!</b>

<i>Общая стоимость заказ составляет:</i> <b>{} руб.</b>

<i>Общее количество позиций составляет:</i> <b>{} ед.</b>

<b>ЗАКАЗ НАПРАВЛЕН НА СКЛАД ДЛЯ ЕГО КОМПЛЕКТОВАНИЯ!!!</b>
"""

# Словарь ответов пользователю
MESSAGES = {
    'trading_store': trading_store,
    'product_order': product_order,
    'order': order,
    'order_number': order_number,
    'no_order': no_order,
    'apply': apply,
    'settings': settings,
}
