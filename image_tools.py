#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging
import argparse
from os import listdir
from os.path import dirname
from os.path import abspath
from os.path import join as joinpath

import cv2
import pyzbar.pyzbar as pyzbar


logging.basicConfig(
    format='%(asctime)s %(name)s - %(funcName)s:%(lineno)d - %(message)s',
    datefmt='%Y-%b-%d %H:%M:%S (%Z)',
)
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


# Попробовал декодировать через cv2.QRCodeDetector(),
# он намного хуже справляется с этой задачей.
# из 20 чеков распознал qr-код только на одном.
# pyzbar.decode() не распознал 4

def qr_detect_and_decode(image_name):
    image = cv2.imread(image_name)
    decodedObjects = pyzbar.decode(image)

    if decodedObjects:
        for obj in decodedObjects:
            qr_data = obj.data.decode()
            logger.debug("QR Code data: {}".format(qr_data))
            return qr_data
    else:
        logger.debug("pyzbar: QR Code not detected")


def main():
    parser = argparse.ArgumentParser(
        description='Утилита для распознавания и расшифровки qr-кодов'
        )
    parser.add_argument('f', help='имя файла с изображением qr-кода')

    args = parser.parse_args()

    BASE_DIR = dirname(abspath(__file__))
    filename = joinpath(BASE_DIR, args.f)
    logger.debug('Filename: {}'.format(filename))

    try:
        qr_detect_and_decode(filename)
    except FileNotFoundError:
        logger.error('Ошибка: Файл не найден', exc_info=True)


if __name__ == "__main__":
    main()