from src.reports import spending_by_weekday, spending_by_category
import pytest


@pytest.mark.parametrize(
    "transactions, category, date, expected",
    [
        (
            [
                {
                    "Дата платежа": "04.03.2019",
                    "Сумма платежа": -167.0,
                    "Категория": "Фастфуд",
                    "Кэшбэк": 1.7,
                },
                {
                    "Дата платежа": "04.03.2019",
                    "Сумма платежа": -78.0,
                    "Категория": "Супермаркеты",
                    "Кэшбэк": 0.8,
                },
                {
                    "Дата платежа": "07.03.2019",
                    "Сумма платежа": -60.0,
                    "Категория": "Супермаркеты",
                    "Кэшбэк": 0.6,
                },
            ],
            "Супермаркеты",
            "2019-03-12",
            None,
        ),
        (
            [
                {
                    "Дата платежа": "04.03.2019",
                    "Сумма платежа": -167.0,
                    "Категория": "Фастфуд",
                    "Кэшбэк": 1.7,
                },
                {
                    "Дата платежа": "04.03.2019",
                    "Сумма платежа": -78.0,
                    "Категория": "Супермаркеты",
                    "Кэшбэк": 0.8,
                },
                {
                    "Дата платежа": "07.03.2019",
                    "Сумма платежа": -60.0,
                    "Категория": "Супермаркеты",
                    "Кэшбэк": 0.6,
                },
            ],
            "Фастфуд",
            "2019-03-12",
            None,
        ),
        (
            [
                {
                    "Дата платежа": "04.03.2019",
                    "Сумма платежа": -167.0,
                    "Категория": "Фастфуд",
                    "Кэшбэк": 1.7,
                },
                {
                    "Дата платежа": "04.03.2019",
                    "Сумма платежа": -78.0,
                    "Категория": "Супермаркеты",
                    "Кэшбэк": 0.8,
                },
                {
                    "Дата платежа": "07.03.2019",
                    "Сумма платежа": -60.0,
                    "Категория": "Супермаркеты",
                    "Кэшбэк": 0.6,
                },
            ],
            "Супермаркеты",
            "2021-03-12",
            None,
        ),
    ],
)
def test_spending_by_category(transactions, category, date, expected):
    assert spending_by_category(transactions, category, date) == expected


def test_spending_by_category_date(reports_example):
    assert spending_by_category(reports_example, "Супермаркеты") is None


def test_spending_by_weekday(reports_example_now):
    assert spending_by_weekday(reports_example_now) is None


def test_spending_by_weekday_date(reports_example):
    assert spending_by_weekday(reports_example, "2019-04-15") is None
