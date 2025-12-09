import datetime
import json
import logging
import os
from typing import Any

import pandas as pd

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(base_dir, "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "services.log")
logger = logging.getLogger("services.py")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(filename=log_file, encoding="utf-8", mode="w")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def prof_cashback(data: pd.DataFrame, year: str, month: str) -> Any:
    """Выводит сумму кэшбэка для каждой категории на выбранный период"""
    date_list = []
    cashback_dict = {}
    for transaction in data:
        if str(transaction.get("Дата платежа")) != "nan":
            date_transactions = datetime.datetime.strptime(
                str(transaction.get("Дата платежа")), "%d.%m.%Y"
            )
            if date_transactions.year == int(year) and date_transactions.month == int(
                month
            ):
                date_list.append(transaction)
            if len(date_list) > 0:
                list_category = []
                for transactions in date_list:
                    list_category.append(transactions.get("Категория"))
                    set_category = set(list_category)
                for category in set_category:
                    cash_list = []
                    for transactions in date_list:
                        if (
                            transactions.get("Категория") == category
                            and transactions.get("Кэшбэк") > 0
                        ):
                            cash_list.append(transactions.get("Кэшбэк"))
                            cashback_dict[transactions.get("Категория")] = sum(
                                cash_list
                            )
                            sorted_dict = dict(
                                sorted(
                                    cashback_dict.items(),
                                    key=lambda x: x[1],
                                    reverse=True,
                                )
                            )
                            json_str = json.dumps(
                                sorted_dict, indent=4, ensure_ascii=False
                            )
            else:
                json_str = {}
    logger.info("Успешное завершение функции")
    return json_str


def form_list_transactions(transactions_list: list[dict[str, Any]]) -> float:
    """Формируем список transactions"""
    new_list = []
    for transaction in transactions_list:
        if str(transaction.get("Дата платежа")) != "nan":
            transaction_dict = {}
            day_pay = datetime.datetime.strptime(
                str(transaction.get("Дата платежа")), "%d.%m.%Y"
            )
            transaction_dict["Дата операции"] = day_pay.strftime("%Y-%m-%d")
            transaction_dict["Сумма операции"] = round(
                abs(transaction.get("Сумма операции"))
            )
            new_list.append(transaction_dict)
    return new_list


def investment_bank(month: str, transactions: pd.DataFrame, limit: int) -> float:
    """Выводит конечную сумму "инвесткопилки" за выбранный период"""
    month_actual = datetime.datetime.strptime(month, "%Y-%m")
    month_actual_format = month_actual.strftime("%Y-%m")
    date_list = []
    for transaction in transactions:
        date_transaction = datetime.datetime.strptime(
            transaction.get("Дата операции"), "%Y-%m-%d"
        )
        date_format = date_transaction.strftime("%Y-%m")
        if date_format == month_actual_format:
            date_list.append(transaction)
    sum_pay = []
    for i in date_list:
        if i.get("Сумма операции") <= limit:
            n = limit - i.get("Сумма операции")
            sum_pay.append(n)
        else:
            str_limit = str(limit)
            x = len(str_limit)
            str_last_digit = str(i.get("Сумма операции"))[-x:]
            if int(str_last_digit) < limit:
                n = limit - int(str_last_digit)
                sum_pay.append(n)
    logger.info("Успешное завершение функции")
    json_str = json.dumps(sum(sum_pay))
    return json_str
