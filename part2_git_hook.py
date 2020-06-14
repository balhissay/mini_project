from wt_bot import wt_bot
import logging

logging_level = logging.INFO

logging.basicConfig(format='%(levelname)s (%(asctime)s): %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging_level)

# Send notification to WT
logging.info('Sending notification to WebEx Teams')
wt_bot.send_message_all_spaces('Commit created in GIT')