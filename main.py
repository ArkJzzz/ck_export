#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'

# Import
import logging
from os.path import dirname
from os.path import abspath
from os.path import join as joinpath
from terminaltables import AsciiTable


# Init
logger = logging.getLogger(__file__)

BASE_DIR = dirname(abspath(__file__))
EXPORT_FILES_DIR = 'exports/'
EXPORT_FILES_DIR = joinpath(BASE_DIR, EXPORT_FILES_DIR)


# Funtions

def extract_transactions(csv_file):
	with open(csv_file, 'r', encoding='UTF-8') as csv_file:
		exported_data = csv_file.read()
	exported_data = exported_data.split('\n\n\n')
	transactions = exported_data[0].split('\n')
	transactions = transactions[2:]
	clear_transactions = []
	for transaction_string in transactions:
		transaction_string = transaction_string.split('","')
		transaction_chunks = []
		for chunk in transaction_string:
			chunk = chunk.replace('"', '')
			chunk = chunk.replace(',', '.')
			transaction_chunks.append(chunk)
			transaction = tuple(transaction_chunks[:6])
		clear_transactions.append(transaction)
	return clear_transactions


# Доходы				Сумма	
#-----------------------------------------------------
# Зарплата 10.хх.хххх	23682	ABB Evo
# Аванс 25.09.2018		20000	SBER
# Премия 18.xx.xxxx		17665	ABB Evo
# Проектирование		8000	ABB Evo
		
# Доп. заработок		4000	Луначарского 54
# Доп. заработок		1490	Северодвинск, Буквоед
# Доп. заработок		5000	Горелово

# Кэшбэк				51,2	кэшбэк АкБарс
# Кэшбэк				134,95	кэшбэк АкБарс
#-----------------------------------------------------



# def print_statistics(resourse, city, language_stat):
#     title = '{resourse} {city}'.format(resourse=resourse, city=city)
#     table_content = [('Язык программирования', 'Вакансий Найдено', 'Вакансий обработано', 'Средняя зарплата')]

#     for language, statistic in language_stat.items():
#         chunk = (
#             language,
#             statistic['vacancies_found'], 
#             statistic['vacancies_processed'],
#             statistic['average_salary'],
#         )
#         table_content.append(chunk)

#     table = AsciiTable(table_content, title)
#     print(table.table)
#     print()

def print_profits(transactions):
	tr_type = 'Перевод'
	tr_froms = ('Зарплата Андрей', 'Доп. заработок', 'Кэшбэк', 'Подарки')

	title = ('Доходы')
	table_content = [('Наименование', 'Сумма', 'Коментарий', 'Дата')]
	separator = ('-----', '', '', '')


	for tr_from in tr_froms:
		for transaction in transactions:
			if transaction[2] == tr_from:
				chunk = (
					transaction[2],
					transaction[5],
					'{}, {}'.format(transaction[4], transaction[3]),
					transaction[0],
				)

				table_content.append(chunk)	
		table_content.append(separator)
	summ = 0.0
	for string in table_content:
		try:
			summ += float(string[1])
		except:
			pass
	table_content.append(('ИТОГО', summ, '', ''))
	table = AsciiTable(table_content, title)
	print(table.table)


def print_capital(transactions):
	tr_type = 'Перевод'
	tr_tos = ('Abb депозит', 'PSB ИИС', 'Dollar\'s', 'Коробочка')

	title = ('Сбережения')
	table_content = [('Наименование', 'Сумма', 'Коментарий', 'Дата')]
	separator = ('-----', '', '', '')

	for tr_to in tr_tos:
		for transaction in transactions:
			if transaction[3] == tr_to:
				chunk = (
					transaction[2],
					transaction[5],
					transaction[3],
					transaction[0],
				)

				table_content.append(chunk)	
		table_content.append(separator)
	summ = 0.0
	for string in table_content:
		try:
			summ += float(string[1])
		except:
			pass
	table_content.append(('ИТОГО', summ, '', ''))
	table = AsciiTable(table_content, title)
	print(table.table)


def print_expenses(transactions):
	tr_type = 'Расход'
	tos = []
	for transaction in transactions:
		if transaction[1] == tr_type:
			if transaction[3] not in tos:
				tos.append(transaction[3])
	for tr_to in tos:
		table_content = []
		for transaction in transactions:
			if transaction[3] == tr_to:
				chunk = (transaction[4], transaction[5])
				table_content.append(chunk)
		labels = []
		sort_table_content = []
		for string in table_content:
			if string[0] not in labels:
				labels.append(string[0])
		for label in labels:
			summ = 0.0
			for string in table_content:
				if string[0] == label:
					summ += float(string[1])
			sort_table_content.append((label, round(summ, 2)))
		total = 0.00
		for string in sort_table_content:
			total += string[1]
		title = ' {}  {}  '.format(tr_to, total)
		new_table_content = [(tr_to, round(total, 2))]
		new_table_content.extend(sort_table_content)
		table = AsciiTable(new_table_content)
		table.justify_columns[1] = 'right'
		print(table.table)



def main():
	# init
	logging.basicConfig(
		format='%(asctime)s %(name)s - %(funcName)s:%(lineno)d - %(message)s', 
		datefmt='%Y-%b-%d %H:%M:%S (%Z)',
	)
	logger.setLevel(logging.DEBUG)

	# do
	export_file = joinpath(EXPORT_FILES_DIR, 'CoinKeeper_export (3).csv') 
	transactions = extract_transactions(export_file)

	print_profits(transactions)
	print_capital(transactions)
	print_expenses(transactions)



if __name__ == '__main__':
	main()
