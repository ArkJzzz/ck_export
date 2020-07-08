#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import requests
import logging

# import pandas
import re
# import openpyxl
from os import getenv
from os import walk as walkpath
from os.path import join as joinpath
from os.path import dirname
from os.path import abspath
from time import sleep


from dotenv import load_dotenv


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

HOST = 'proverkacheka.nalog.ru:8888'
load_dotenv()
AUTHORIZATION = getenv('AUTHORIZATION')
DEVICE_ID = getenv('DEVICE_ID')
DEVICE_OS = getenv('DEVICE_OS')


# 1. Отправляем запрос на проверку существования чека. 
# Если все хорошо, то получим код ответа сервера 204.
# 2. Отправляем запрос на получение детальной информации по чеку. 
# Если все хорошо, то получим код ответа сервера 202.
# 3. Отправляем еще запрос на получение детальной информации по чеку. 
# Вместе с кодом ответа сервера 200 вы получите json с данными чека.



def checking_existence(receipt_details):

    url = 'http://{host}/v1/ofds/*/inns/*/fss/{fn}/operations/{n}/tickets/{i}'.format(
            host=HOST,
            fn=receipt_details['fn'],
            n=receipt_details['n'],
            i=receipt_details['i'],
        )
    headers = {
            'User-Agent': 'OkHttp 3.3',
            'Authorization': AUTHORIZATION,
            'Device-Id': DEVICE_ID, 
            'Device-OS': DEVICE_OS, 
            'Version': '2', 
            'ClientVersion': '1.4.2', 
            'Host': 'proverkacheka.nalog.ru:8888', 
            'Connection': 'Keep-Alive', 
            'Accept-Encoding': 'gzip',
        }
    payload = {
        'fiscalSign': receipt_details['fp'],
        'date': receipt_details['t'],
        'sum': receipt_details['s'],
    }
    response = requests.get(url, headers=headers, params=payload)
    logger.debug(response.status_code)
    if response.status_code == 204:
        return response.ok


def get_receipt_data(receipt_details):

    url = 'http://{host}/v1/inns/*/kkts/*/fss/{fn}/tickets/{i}'.format(
            host=HOST,
            fn=receipt_details['fn'],
            i=receipt_details['i'],
        )
    headers = {
        'User-Agent': 'OkHttp 3.3',
        'Authorization': AUTHORIZATION,
        'Device-Id': DEVICE_ID, 
        'Device-OS': DEVICE_OS, 
        'Version': '2', 
        'ClientVersion': '1.4.2', 
        'Host': 'proverkacheka.nalog.ru:8888', 
        'Connection': 'Keep-Alive', 
        'Accept-Encoding': 'gzip',
    }
    payload = {
        'fiscalSign': receipt_details['fp'],
        'sendToEmail': 'no',
    }

    response = requests.get(url, headers=headers, params=payload)
    logger.debug(response.status_code)

    if response.status_code == 202:
        sleep(5)
    response = requests.get(url, headers=headers, params=payload)
    if response.status_code == 200:
        return response.json()
    else: 
        logger.debug('Не удалось загрузить чек')
        

def print_receipt(receipt_data):

    data_to_print = '''
    Дата: {dateTime}
    Сумма чека: {totalSum}
    -----
    Товары:
    '''.format(
            dateTime=receipt_data['document']['receipt']['dateTime'],
            totalSum=receipt_data['document']['receipt']['totalSum']/100,
            # items=receipt_data['document']['receipt']['items']
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


def get_receipt(qr_data):
        receipt = qr_data.split('&')
        receipt_details = {}
        for item in receipt:
            key, value = item.split('=')
            receipt_details[key] = value.replace('.', '')

        logger.debug(receipt_details)

        if checking_existence(receipt_details):
            receipt_data = get_receipt_data(receipt_details)

            if receipt_data:
                logger.debug(print_receipt(receipt_data))
                return print_receipt(receipt_data)


def main():

    receipts = [
        't=20200610T1936&s=309.00&fn=9287440300116906&i=132373&fp=2411058669&n=1',
        't=20200612T1740&s=440.00&fn=9283440300083150&i=15421&fp=4184806037&n=1',
        't=20200620T1543&s=129.80&fn=9289000100476486&i=8598&fp=2244516407&n=1',
        't=20200621T1906&s=199.98&fn=9289000100476486&i=9380&fp=2183116907&n=1',
        't=20200617T2017&s=499.00&fn=9251440300183590&i=10386&fp=3013850763&n=1',
        't=20200207T1516&s=1386.00&fn=9282000100333614&i=55650&fp=1136766986&n=1',
        't=20200513T1812&s=288.00&fn=9280440300479432&i=19441&fp=2095343795&n=1',
        # 't=20200125T170200&s=1339.78&fn=9285000100129803&i=18155&fp=3876454150&n=1',
    ]

    for receipt in receipts:

        receipt = receipt.split('&')
        receipt_details = {}
        for item in receipt:
            key, value = item.split('=')
            receipt_details[key] = value.replace('.', '')

        print(receipt_details)

        if checking_existence(receipt_details):
            receipt_data = get_receipt_data(receipt_details)

            if receipt_data:
                print(print_receipt(receipt_data))

 
if __name__ == "__main__":
    main()










