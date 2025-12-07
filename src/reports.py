import datetime
import logging
import os
from typing import Any, Optional

import pandas as pd

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(base_dir, "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "reports.log")
log_file_json = os.path.join(log_dir, "spending_by_category.json")
log_file_csv = os.path.join(log_dir, "spending_by_weekday.csv")
logger = logging.getLogger("reports.py")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(filename=log_file, encoding="utf-8", mode="w")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def my_log(filename=None):
    def decorator(function):
        def wrapper(*args, **kwargs):
            """Декоратор выводит данные работы функции в консоль или в файл"""
            function_name = function.__name__
            try:
                result = function(*args, **kwargs)
                if filename:
                    file = open(filename, "w", encoding="utf-8")
                    file.write(f"{result}")
                    file.close()
                else:
                    print(f"{result}")
            except Exception as e:
                if filename:
                    file = open(filename, "a", encoding="utf-8")
                    file.write(f"{function_name} error: {e} " + "\n")
                    file.close()
                else:
                    print(f"{function.__name__} error: {e}")

        return wrapper

    return decorator


@my_log(log_file_json)
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    """Выводит общую сумму трат по выбранной категории за последние 3 месяца"""
    global transaction_date
    if date:
        transactions_end = datetime.datetime.strptime(date, "%Y-%m-%d")
        transactions_start = transactions_end - datetime.timedelta(days=92)
    else:
        transactions_end = datetime.datetime.today()
        transactions_start = transactions_end - datetime.timedelta(days=92)
    transaction_list = []
    logger.info(
        f'Период поиска: {transactions_start.strftime("%Y-%m-%d")} - {transactions_end.strftime("%Y-%m-%d")}'
    )
    for transaction in transactions:
        if str(transaction.get("Дата платежа")) != "nan":
            transaction_date = datetime.datetime.strptime(
                str(transaction.get("Дата платежа")), "%d.%m.%Y"
            )
        if (
            transaction_date
            and transactions_start <= transaction_date <= transactions_end
        ):
            transaction_list.append(transaction)
            category_list = []
            for items in transaction_list:
                if str(items.get("Категория")).lower() == category.lower():
                    category_list.append(abs(items.get("Сумма платежа")))
            result = [{category.title(): sum(category_list)}]
        else:
            logger.info("Нет данных, удовлетворяющих запросу")
            result = []
    logger.info("Успешное завершение функции")
    return result


@my_log(log_file_csv)
def spending_by_weekday(
    transactions: pd.DataFrame, date: Optional[str] = None
) -> list[Any]:
    """ "Выводит среднюю сумму затрат для каждого дня недели, за последние три месяца"""
    global week_dict
    if date:
        transactions_end = datetime.datetime.strptime(date, "%Y-%m-%d")
        transactions_start = transactions_end - datetime.timedelta(days=92)
    else:
        transactions_end = datetime.datetime.today()
        transactions_start = transactions_end - datetime.timedelta(days=92)
    transaction_list = []
    for transaction in transactions:
        if str(transaction.get("Дата платежа")) != "nan":
            transaction_date = datetime.datetime.strptime(
                str(transaction.get("Дата платежа")), "%d.%m.%Y"
            )
        if (
            transaction_date
            and transactions_start <= transaction_date <= transactions_end
        ):
            transaction_list.append(transaction)
    week_list = []
    days_list = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    for week_day in days_list:
        weekday_list = []
        week_dict = {}
        for item in transaction_list:
            date_transaction = datetime.datetime.strptime(
                str(item.get("Дата платежа")), "%d.%m.%Y"
            )
            weekday = datetime.datetime.strftime(date_transaction, "%A")
            if weekday == week_day:
                weekday_list.append(abs(item.get("Сумма платежа")))
                if len(weekday_list) != 0:
                    week_dict[weekday] = round(sum(weekday_list) / len(weekday_list), 2)
                else:
                    week_dict[weekday] = 0
        if len(week_dict) != 0:
            week_list.append(week_dict)
    logger.info("Успешное завершение функции")
    return week_list
