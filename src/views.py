import json
from typing import Any

from utils import (
    currency_rate,
    date_transactions,
    filter_cards,
    greeting,
    list_cards,
    list_formatted,
    read_excel,
    read_json,
    stock_rate,
    top_transactions,
)


def main_page(date: str) -> Any:
    """Главная функция. Выводит json-ответ"""
    new_dict = {}
    actual_data = date_transactions(read_excel(), date)
    lists_cards = list_cards(filter_cards(actual_data))
    greet = greeting()
    top_transaction = list_formatted(top_transactions(actual_data))
    currency_rates = currency_rate(read_json())
    stock_prices = stock_rate(read_json())
    new_dict["greeting"] = greet
    new_dict["cards"] = lists_cards
    new_dict["top_transactions"] = top_transaction
    new_dict["currency_rates"] = currency_rates
    new_dict["stock_prices"] = stock_prices
    return json.dumps(new_dict, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    print(main_page("2019-04-15 13:00:00"))
