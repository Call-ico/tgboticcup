import os
import logging
import time
from logger import setup_logger
from bot import setup_bot
from config import token

def start_telegram_bot():
    # Initialize logger
    logger = setup_logger()

    if not token:
        logger.error('TELEGRAM_BOT_TOKEN not set!')
        return

    logger.info('Starting bot with provided token')

    while True:
        bot = setup_bot(token)
        bot.enable_save_next_step_handlers(delay=2)

        try:
            logger.info('Polling started')
            bot.polling(non_stop=False, none_stop=True, interval=0, timeout=30)
            logger.info('Polling finished normally')
            logger.info('You have 5 seconds to press Ctrl+C to stop the bot, otherwise it will restart.')
            time.sleep(5)
            #break
        except Exception as err:
            logger.exception('Polling error: %s', err)
            logger.info('Restarting polling in 5 seconds...')
            time.sleep(5)
        finally:
            bot.stop_polling()
            logger.info('Polling fully stopped')


if __name__ == '__main__':
    try:
        start_telegram_bot()
    except KeyboardInterrupt:
        print('Bot stopped by user (Ctrl+C)')


