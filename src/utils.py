import datetime
import json
import os
from math import nan
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv


def date_transactions(excel_file_list: Any, date_actual: str) -> list[dict]:
    """Формирует список транзакций на заявленный месяц"""
    date_actual_d = datetime.datetime.strptime(date_actual, "%Y-%m-%d %H:%M:%S")
    start_date = date_actual_d.replace(day=1)
    new_list = []
    for transaction in excel_file_list:
        transaction_date = datetime.datetime.strptime(
            transaction.get("Дата операции"), "%d.%m.%Y %H:%M:%S"
        )
        if transaction_date >= start_date and transaction_date <= date_actual_d:
            new_list.append(transaction)
    return new_list


def greeting() -> str:
    """Функция выводит приветствие, в зависимости от времени суток"""
    date_now = datetime.datetime.now()
    if date_now.hour >= 0 and date_now.hour <= 5:
        greet = "Доброй ночи"
    elif date_now.hour >= 6 and date_now.hour <= 11:
        greet = "Доброе утро"
    elif date_now.hour >= 12 and date_now.hour <= 18:
        greet = "Добрый день"
    elif date_now.hour >= 19 and date_now.hour <= 23:
        greet = "Добрый вечер"
    return greet

def read_excel(excel_file: Any = "../data/operations.xlsx") -> list[dict]:
    """Преобразует файл xlsx в список словарей"""
    excel_file = pd.read_excel(excel_file)
    excel_file_list = excel_file.to_dict("records")
    return excel_file_list


def filter_cards(excel_file_list: list[dict], nan=None) -> list[dict]:
    """Фильтр списков по номерам карт"""
    list_cards = []
    list_transactions = []
    for transactions in excel_file_list:
        list_cards.append(transactions.get("Номер карты"))
    set_cards = set(list_cards)
    for card in set_cards:
        new_list = []
        for transactions in excel_file_list:
            if card == transactions.get("Номер карты"):
                new_list.append(transactions)
        list_transactions.append(new_list)
    return list_transactions


def list_cards(list_transactions: list[dict], nan: Any = None) -> list[dict]:
    """Формирует общие затраты по картам"""
    new_list = []
    for transactions in list_transactions:
        dict_card = {}
        for transaction in transactions:
            if transaction.get("Номер карты") != nan:
                last_digit = transaction.get("Номер карты")[-4:]
                dict_card["last_digits"] = last_digit
                spent_list = []
                spent_list.append(float(transaction.get("Сумма платежа")) * -1)
                total_spent = sum(spent_list)
                dict_card["total_spent"] = total_spent
                cashback = round(total_spent / 100, 2)
                dict_card["cashback"] = cashback
        if len(dict_card) != 0:
            new_list.append(dict_card)
    return new_list


def top_transactions(excel_file_list: list[dict]) -> list[dict]:
    """Определяет 5 самых крупных транзакций"""
    sorted_spent = sorted(
        excel_file_list, key=lambda transaction: transaction["Сумма платежа"]
    )
    top_spent = sorted_spent[:5]
    return top_spent


def list_formatted(top_spent: list[dict]) -> list[dict]:
    """Формирует список для вывода топ транзакций"""
    formatted_cards = []
    for transactions in top_spent:
        new_transaction = {}
        date = transactions.pop("Дата платежа")
        new_transaction["date"] = date
        amount = transactions.pop("Сумма платежа")
        new_transaction["amount"] = amount
        category_spent = transactions.pop("Категория")
        new_transaction["category"] = category_spent
        description = transactions.pop("Описание")
        new_transaction["description"] = description
        formatted_cards.append(new_transaction)
    return formatted_cards


def read_json(json_file: Any = "../user_settings.json") -> list[dict[Any, Any]]:
    """Преобразует Json файл в список"""
    with open(json_file, "r", encoding="utf-8") as file:
        currency = json.load(file)
    return currency


load_dotenv("../.env")
API_KEY = os.getenv("API_KEY")
url = "https://api.apilayer.com/exchangerates_data/convert"
header = {"apikey": API_KEY}


def currency_rate(user_settings: list[dict]) -> list[dict]:
    """Выводит актуальный обменный курс"""
    list_rate = []
    for data in user_settings:
        currency_list = data.get("user_currencies")
        for currency in currency_list:
            new_dict = {}
            payload = {"amount": 1, "from": currency, "to": "RUB"}
            response = requests.get(url, headers=header, params=payload)
            result = round(response.json()["result"], 2)
            new_dict["currency"] = currency
            new_dict["rate"] = result
            list_rate.append(new_dict)
    return list_rate


load_dotenv("../.env")
API_KEY_STOCK = os.getenv("API_KEY_STOCK")
headers = {"X-Api-Key": API_KEY_STOCK}


def stock_rate(user_settings: list[dict]) -> list[dict]:
    """Выводит актуальную стоимость акций"""
    list_rate = []
    for data in user_settings:
        stock_list = data.get("user_stocks")
        for stock in stock_list:
            new_dict = {}
            api_url = f"https://api.api-ninjas.com/v1/stockprice?ticker={stock}"
            response = requests.get(api_url, headers=headers)
            if response.status_code == requests.codes.ok:
                data = response.json()
                new_dict["stock"] = stock
                new_dict["price"] = data["price"]
                list_rate.append(new_dict)
    return list_rate


if __name__ == "__main__":
    print(filter_cards([{
            "Дата операции": "02.03.2019 14:02:30",
            "Дата платежа": "04.03.2019",
            "Номер карты": "*7198",
            "Статус": "OK",
            "Сумма операции": -167.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -167.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": nan,
            "Категория": "Фастфуд",
            "MCC": 5814.0,
            "Описание": "Крошка Картошка",
            "Бонусы (включая кэшбэк)": 3,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 167.0,
        },
        {
            "Дата операции": "02.03.2019 13:54:22",
            "Дата платежа": "04.03.2019",
            "Номер карты": "*7198",
            "Статус": "OK",
            "Сумма операции": -78.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -78.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": nan,
            "Категория": "Супермаркеты",
            "MCC": 5499.0,
            "Описание": "Колхоз",
            "Бонусы (включая кэшбэк)": 1,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 78.0,
        },
        {
            "Дата операции": "02.03.2019 12:49:51",
            "Дата платежа": "04.03.2019",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -350.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -350.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": nan,
            "Категория": "Фастфуд",
            "MCC": 5814.0,
            "Описание": "SUPERMANGO",
            "Бонусы (включая кэшбэк)": 7,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 350.0,
        },
        {
            "Дата операции": "01.03.2019 15:37:24",
            "Дата платежа": "04.03.2019",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -240.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -240.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": nan,
            "Категория": "Фастфуд",
            "MCC": 5814.0,
            "Описание": "Bufet 2",
            "Бонусы (включая кэшбэк)": 4,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 240.0,
        },
    ]))


