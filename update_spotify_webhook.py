import argparse
import spotify_util

parser = argparse.ArgumentParser(description = 'URL of the webhook to be updated')
parser.add_argument('-u', '--url', help = None, type = None, required = True)
args = parser.parse_args()
url = args.url

spotify_util.update_webhook_in_file(url)