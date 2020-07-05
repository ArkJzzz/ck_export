#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging
from os import getenv

from dotenv import load_dotenv
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import ConversationHandler
from telegram.ext import RegexHandler

from qr_decode import decode_qr_from_photo
from tax_tools import get_receipt


logging.basicConfig(
    format='%(asctime)s %(name)s - %(funcName)s:%(lineno)d - %(message)s', 
    datefmt='%Y-%b-%d %H:%M:%S (%Z)',
)

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)



# KEYBOARD = [
#     ['Новый вопрос'],
#     ['Сдаться'],
# ]
# REPLY_MARKUP = ReplyKeyboardMarkup(
#     KEYBOARD, 
#     resize_keyboard=True,
#     one_time_keyboard=False,
# )


def start(update, context):
    logger.debug('new start')
    chat_id=update.effective_chat.id
    text='отправь сюда фото чека'
    context.bot.send_message(
        chat_id=chat_id,
        text=text, 
        # reply_markup=REPLY_MARKUP
    )


def photo(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('tax_image.jpeg')
    logger.info('Фото от {}: {}'.format(user.first_name, 'tax_image.jpeg'))
    qr_data = decode_qr_from_photo('tax_image.jpeg')
    update.message.reply_text('QR data: {}'.format(qr_data))
    receipt_data = get_receipt(qr_data)
    update.message.reply_text(receipt_data)


def main():
    load_dotenv()
    telegram_token = getenv('TELEGRAM_TOKEN')
    logger.debug(telegram_token)

    updater = Updater(
        telegram_token, 
        use_context=True,
    )
    
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            MessageHandler(Filters.photo, photo)

        ],

        states={},
        fallbacks=[]
    )

    updater.dispatcher.add_handler(conv_handler)

    try:
        logger.debug('Стартуем бота')
        updater.start_polling()

    except FileNotFoundError:
        logger.error('Ошибка: Файл не найден', exc_info=True)
    except redis.exceptions.AuthenticationError:
        logger.error('Подключение к базе данных: ошибка аутентификации')
    except Exception  as err:
        logger.error('Бот упал с ошибкой:')
        logger.error(err)
        logger.debug(err, exc_info=True)

    updater.idle()
    logger.info('Бот остановлен')

if __name__ == "__main__":
    main()


