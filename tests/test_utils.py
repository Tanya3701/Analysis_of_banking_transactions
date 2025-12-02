from unittest.mock import patch, Mock, mock_open
import os
from dotenv import load_dotenv

from src.utils import (date_transactions, greeting, read_excel, filter_cards, list_cards, top_transactions,
list_formatted, read_json, currency_rate, stock_rate)
import pandas as pd

from tests.conftest import spent_cards


def test_date_transactions(excel_file_list, excel_list_filter_date, nan = None):
    assert date_transactions(excel_file_list, '2019-03-15 13:00:00') == excel_list_filter_date


@patch("pandas.read_excel")
def test_read_excel(mock_read_excel):
    mock_data = [{"Номер карты": "*7197", "Сумма операции": -687.41, "Валюта операции": "RUB"}]
    mock_read_excel.return_value = pd.DataFrame(mock_data)
    result = read_excel("path")
    expected = mock_data
    assert result == expected


def test_filter_cards(cards, filter_for_cards, filter_for_card):
    assert filter_cards(cards) == filter_for_cards or filter_for_card


def test_list_cards(filter_list, spent_cards):
    assert list_cards(filter_list) == spent_cards


def test_top_transactions(example_list, top):
    assert top_transactions(example_list) == top


def test_list_formatted(example_list, top_list):
    assert list_formatted(example_list) == top_list


@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
@patch("os.path.exists")
@patch("os.path.getsize")
def test_load_operations_returns_dict(mock_getsize, mock_exists, mock_open):
    mock_exists.return_value = True
    mock_getsize.return_value = 1
    result = read_json("test_file.json")
    assert isinstance(result, dict)


@patch("requests.get")
def test_currency_rate(mock_get):
    mock_get.return_value.json.return_value = {"result": 50}
    assert (
        currency_rate(
            [{"user_currencies": ["USD", "EUR"]}])
        == [{'currency': 'USD', 'rate': 50}, {'currency': 'EUR', 'rate': 50}])


@patch("requests.get")
def test_stock_rate(mock_get):
    mock_get.return_value.json.return_value = {"result": 50}
    assert (
        stock_rate(
            [{"user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}])
        == [])
