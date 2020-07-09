#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'



def print_receipt(receipt_data):
    receipt_data_receipt = receipt_data['document']['receipt']
    receipt_datetime = receipt_data_receipt['dateTime'].split('T')

    data_to_print = '''
    Дата: {date}
    Время: {time}
    Сумма чека: {totalSum}
    -----
    ФН: {fiscalDriveNumber}
    ФД: {fiscalDocumentNumber}
    ФП: {fiscalSign}
    -----

    Товары:
    '''.format(
            date=receipt_datetime[0],
            time=receipt_datetime[1],
            totalSum=receipt_data_receipt['totalSum']/100,
            fiscalDriveNumber=receipt_data_receipt['fiscalDriveNumber'],
            fiscalDocumentNumber=receipt_data_receipt['fiscalDocumentNumber'],
            fiscalSign=receipt_data_receipt['fiscalSign'],
        )

    commodity_items = receipt_data['document']['receipt']['items']

    for item in commodity_items:
        item = '''
    Наименование: {name}
    Цена: {price}
    Количество: {quantity}
    Сумма: {sum}
        '''.format(
                name=item['name'],
                price=item['price']/100,
                quantity=item['quantity'],
                sum=item['sum']/100,
            )
        data_to_print += item

    return data_to_print



def add_to_xlsx_file(receipt_data):
    workbook = openpyxl.load_workbook(applicants_file, read_only=False)
    sheet_names = workbook.get_sheet_names()
    sheet_name = sheet_names[0]
    excel_data = workbook.get_sheet_by_name(sheet_name)
    last_column = excel_data.max_column
    cell = excel_data.cell(row=1, column=last_column)

    for row in list(excel_data.rows)[1:]:
        replace_noncyrillic_characters(row[1].value)

    if cell.value != 'Статус выгрузки':
        last_column += 1
    excel_data.cell(row=1, column=last_column).value = 'Статус выгрузки'

if __name__ == "__main__":
    main()




