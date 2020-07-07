import cv2
import logging
import pyzbar.pyzbar as pyzbar

from os import listdir

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

def decode_qr_from_photo(image_name):
    image = cv2.imread(image_name)
    decodedObjects = pyzbar.decode(image)

    if decodedObjects:
        for obj in decodedObjects:
            qr_data = obj.data.decode()
            logger.debug("pyzbar: {}".format(qr_data))
            return qr_data
    else:
        logger.debug("pyzbar: QR Code not detected")



def main():
    photos_dir = 'receipts_photos'
    files = listdir(photos_dir)


    for image in files:
        print(image)
        decode_qr_from_photo('{}/{}'.format(photos_dir, image))


    # print(decode_qr_from_photo('receipts_photos/tax_image9.jpeg'))

if __name__ == "__main__":
    main()