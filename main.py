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
            bot.polling(none_stop=False, interval=0, timeout=30)
            logger.info('Polling finished normally')
            # break
        except KeyboardInterrupt:
            logger.info('Polling stopped by user (Ctrl+C)')
            break
        except Exception as err:
            logger.exception('Polling error: %s', err)
            logger.info('Restarting polling in 5 seconds...')
            time.sleep(5)
        finally:
            bot.stop_polling()
            logger.info('Polling fully stopped')


if __name__ == '__main__':
    start_telegram_bot()