# Приложение для анализа транзакций


## Установка

1. Клонируйте репозиторий:
```
git clone https://github.com/username/project-x.git
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
## Содержание:
### Главная страница
#### Функционал:
* date_transactions():

    """Формирует список транзакций на заявленный месяц"""
* greeting():

    """Функция выводит приветствие, в зависимости от времени суток"""
* read_excel():

    """Преобразует файл xlsx в список словарей"""
* filter_cards():

    """Фильтр списков по номерам карт"""
* list_cards(list_transactions, nan=None):

    """Формирует общие затраты по картам"""
* top_transactions(excel_file_list):

    """Определяет 5 самых крупных транзакций"""
* list_formatted(top_spent):

    """Формирует список для вывода топ транзакций"""
* read_json(json_file = '../user_settings.json'):

    """Преобразует Json файл в список"""
* currency_rate(user_settings):

    """Выводит актуальный обменный курс"""
*  stock_rate(user_settings):

    """Выводит актуальную стоимость акций"""

### Пример Json-ответа:
`{
  "greeting": "Добрый день",

  "cards": [

    {
      "last_digits": "5814",
      "total_spent": 1262.00,
      "cashback": 12.62
    },
    {
      "last_digits": "7512",
      "total_spent": 7.94,
      "cashback": 0.08
    }
  ],
  "top_transactions": [

    {
      "date": "21.12.2021",
      "amount": 1198.23,
      "category": "Переводы",
      "description": "Перевод Кредитная карта. ТП 10.2 RUR"
    },
    {
      "date": "20.12.2021",
      "amount": 829.00,
      "category": "Супермаркеты",
      "description": "Лента"
    },
    {
      "date": "20.12.2021",
      "amount": 421.00,
      "category": "Различные товары",
      "description": "Ozon.ru"
    },
    {
      "date": "16.12.2021",
      "amount": -14216.42,
      "category": "ЖКХ",
      "description": "ЖКУ Квартира"
    },
    {
      "date": "16.12.2021",
      "amount": 453.00,
      "category": "Бонусы",
      "description": "Кешбэк за обычные покупки"
    }
  ],
  "currency_rates": [

    {
      "currency": "USD",
      "rate": 73.21
    },
    {
      "currency": "EUR",
      "rate": 87.08
    }
  ],
  "stock_prices": [

    {
      "stock": "AAPL",
      "price": 150.12
    },
    {
      "stock": "AMZN",
      "price": 3173.18
    },
    {
      "stock": "GOOGL",
      "price": 2742.39
    },
    {
      "stock": "MSFT",
      "price": 296.71
    },
    {
      "stock": "TSLA",
      "price": 1007.08
    }
  ]
}`

## Сервисы

### Функционал
* prof_cashback(data: pd.DataFrame, year: str, month: str) -> Any:\
"""Выводит сумму кэшбэка для каждой категории на выбранный период"""

* investment_bank(month: str, transactions: pd.DataFrame, limit: int) -> float:

    """Выводит конечную сумму "инвесткопилки" за выбранный период"""

## Отчеты
### Функционал
* spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:

    """Выводит общую сумму трат по выбранной категории за последние 3 месяца""" 
* spending_by_weekday(
    transactions: pd.DataFrame, date: Optional[str] = None
) -> list[Any]:

    """ "Выводит среднюю сумму затрат для каждого дня недели, за последние три месяца"""


_________________________________________________________

* ___coverage: platform win32, python 3.13.7-final-0 ___
* Name_______Cover
-----------------------------------------
* src\__init__.py____________100%
* src\services.py__________97%
* src\utils.py_____________90%
* tests\__init_____________100%
* tests\conftest.py_________95%
* tests\test_services.py____100%
* tests\test_utils.py________100% 

-----------------------------------------
TOTAL____191_______94%
`