import yaml
import json
import time
import os
import logging
from webexteamssdk import WebexTeamsAPI
from webexteamssdk import RateLimitWarning

bot_info_file = 'bot.yml'
message = f'Text message ({time.strftime("%Y%m%d-%H%M%S")})'
proxies = {
    'http': '127.0.0.1:63181',
    'https': '127.0.0.1:63181'
}

# Read bot info file
wt_bot_dir = os.path.abspath('wt_bot')
path = os.path.join(wt_bot_dir, bot_info_file)
with open(path, 'r') as handle:
    bot_info = yaml.safe_load(handle)

bot = WebexTeamsAPI(access_token=bot_info.get('bot_access_token'), proxies = None)
""" # Get all the rooms and ask for the room number to send the message to
room_dict = {}
for n, room in enumerate(bot.rooms.list()):
    room_dict[n] = {'title': room.title, 'id': room.id, 'ownerId': room.ownerId}
    print(n, room_dict[n]['title'])
#print(json.dumps(room_dict, indent = 4))
room_number = int(input('Select Room to send the message to:'))
bot.messages.create(room_dict[room_number]['id'], text = message)
 """
def send_message_all_spaces(message):
    # Send the message to all rooms the bot is in:
    for room in bot.rooms.list():
        logging.info(f'Sending message to room "{room.title}" ({room.id})')
        bot.messages.create(room.id, text = message)

def send_attachment_all_spaces(attachment_path):
    # Send the message to all rooms the bot is in:
    for room in bot.rooms.list():
        logging.info(f'Sending attachment to room "{room.title}" ({room.id})')
        bot.messages.create(room.id, files = attachment_path)
