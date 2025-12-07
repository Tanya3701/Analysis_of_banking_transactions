from src.views import main_page
from src.utils import read_excel
from src.services import prof_cashback, investment_bank, form_list_transactions
from src.reports import spending_by_weekday, spending_by_category

date = input()
main_page(date)
# Главная функция. Выводит json-ответ

data = read_excel()
year = input()
month = input()
prof_cashback(data, year, month)
# Выводит сумму кэшбэка для каждой категории на выбранный период

month = input()
transactions = form_list_transactions(read_excel())
limit = int(input())
investment_bank(month, transactions, limit)
# Выводит конечную сумму "инвесткопилки" за выбранный период

transactions = read_excel()
category = input()
date = input()
spending_by_category(transactions, category, date)
# Выводит общую сумму трат по выбранной категории за последние 3 месяца

transactions = read_excel()
date = input()
spending_by_weekday(transactions, date)
# Выводит среднюю сумму затрат для каждого дня недели, за последние три месяца
