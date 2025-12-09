from src.reports import spending_by_category, spending_by_weekday
from src.services import form_list_transactions, investment_bank, prof_cashback
from src.utils import read_excel
from src.views import main_page

date = input()
main_page(date)
# Главная функция. Выводит json-ответ

data_excel = read_excel()
year = input()
month = input()
prof_cashback(data_excel, year, month)
# Выводит сумму кэшбэка для каждой категории на выбранный период

month = input()
transaction_list = form_list_transactions(read_excel())
limit = int(input())
investment_bank(month, transaction_list, limit)
# Выводит конечную сумму "инвесткопилки" за выбранный период

transactions_category = read_excel()
category = input()
date = input()
spending_by_category(transactions_category, category, date)
# Выводит общую сумму трат по выбранной категории за последние 3 месяца

transactions_week = read_excel()
date = input()
spending_by_weekday(transactions_week, date)
# Выводит среднюю сумму затрат для каждого дня недели, за последние три месяца
