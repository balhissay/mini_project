import argparse
from wt_bot import wt_bot

parser = argparse.ArgumentParser(description = 'URL of the webhook to be updated')
parser.add_argument('-u', '--url', help = None, type = None, required = True)
args = parser.parse_args()
url = args.url

wt_bot.update_webhook(url)