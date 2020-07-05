import cv2
import logging
import pyzbar.pyzbar as pyzbar

# logging.basicConfig(
#     format='%(asctime)s %(name)s - %(funcName)s:%(lineno)d - %(message)s', 
#     datefmt='%Y-%b-%d %H:%M:%S (%Z)',
# )
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


def decode_qr_from_photo(image_name):
    logger.debug(image_name)
    image = cv2.imread(image_name)
    decodedObjects = pyzbar.decode(image)
    for obj in decodedObjects:
        logger.debug(obj)
        qr_data = obj.data.decode()
        logger.debug(qr_data)
        return qr_data

    # cv2.imshow("Frame", image)
    # cv2.waitKey(0)



def main():
    decode_qr_from_photo('tax_image.jpeg')

if __name__ == "__main__":
    main()