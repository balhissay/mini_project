import re
import argparse

parser = argparse.ArgumentParser(description = 'Name of the file with the NGROK tunnel information')
parser.add_argument('-f', '--file', help = None, type = None, required = True)
args = parser.parse_args()
filename = args.file

with open (filename, "r") as file:
    lines = file.readlines()
http_url, https_url = '', ''
for line in lines:
    match = re.match(r'Forwarding\s+(http:\S+)', line)
    if match:
        http_url = match.group(1)
    match = re.match(r'Forwarding\s+(https:\S+)', line)
    if match:
        https_url = match.group(1)

if not http_url:
    raise Exception('URL could not be found in file')
print(http_url)
