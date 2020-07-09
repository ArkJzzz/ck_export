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

logging.basicConfig(
    format='%(asctime)s %(name)s - %(funcName)s:%(lineno)d - %(message)s',
    datefmt='%Y-%b-%d %H:%M:%S (%Z)',
)
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

HOST = 'proverkacheka.nalog.ru:8888'
load_dotenv()
AUTHORIZATION = getenv('AUTHORIZATION')
DEVICE_ID = getenv('DEVICE_ID')
DEVICE_OS = getenv('DEVICE_OS')
HEADERS = {
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


def checking_existence(receipt_details):
    # 1. Отправляем запрос на проверку существования чека.
    # Если все хорошо, то получим код ответа сервера 204.

    url = 'http://{host}/v1/ofds/*/inns/*/fss/{fn}/operations/{n}/tickets/{i}'.format(
            host=HOST,
            fn=receipt_details['fn'],
            n=receipt_details['n'],
            i=receipt_details['i'],
        )
    headers = HEADERS
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
    # 2. Отправляем запрос на получение детальной информации по чеку.
    # Если все хорошо, то получим код ответа сервера 202.
    # 3. Отправляем еще запрос на получение детальной информации по чеку.
    # Вместе с кодом ответа сервера 200 вы получите json с данными чека.

    url = 'http://{host}/v1/inns/*/kkts/*/fss/{fn}/tickets/{i}'.format(
            host=HOST,
            fn=receipt_details['fn'],
            i=receipt_details['i'],
        )
    headers = HEADERS
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
                logger.debug(receipt_data)
                return receipt_data


def main():

    print('Этот модуль напрямую пока не запускается')

if __name__ == "__main__":
    main()