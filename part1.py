import requests
import ssl
import json
import yaml
import urllib3
import logging
from wt_bot import wt_bot
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

server = 'sandboxdnac2.cisco.com:443'
username = 'devnetuser'
password = 'Cisco123!'
yaml_filename = 'DNAC_devices.yml'
logging_level = logging.INFO

token_url = f'https://{server}/dna/system/api/v1/auth/token'
devices_url = f'https://{server}/dna/intent/api/v1/network-device'

logging.basicConfig(format='%(levelname)s (%(asctime)s): %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging_level)

# Allow insecure connections
if hasattr(ssl, '_create_unverified_context'):
	ssl._create_default_https_context = ssl._create_unverified_context
	ssl._DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
urllib3.disable_warnings(InsecureRequestWarning)

def jprint(json_object):
    print(json.dumps(json_object, indent=4))

def get_token():
    token = requests.post(
       token_url,
       auth=HTTPBasicAuth(username=username, password=password),
       headers={'content-type': 'application/json'},
       verify=False,
    )
    data = token.json()
    return data['Token']

def get_devices():
    response = requests.get(
        devices_url,
        headers={
            "X-Auth-Token": '{}'.format(token),
            "Content-type": "application/json",
        },
        verify=False
    )
    return response

logging.info('Getting token from DNA Center')
token = get_token()
logging.info('Getting device list from DNA Center')
response = get_devices()

# Get required parsed output
logging.info('Parsing device list')
devices = response.json()['response']
#jprint(devices)
output = ''
for device in devices:
    output += f'hostname: {device.get("hostname", "NA")}, serial: {device.get("serialNumber", "NA")}, platform: {device.get("platformId", "NA")}\n'
print(output)

# Save inventory to YAML file
logging.info('Saving output to YAML file')
output_yaml = yaml.dump(devices)
with open(yaml_filename, "w") as file:
    file.write(output_yaml)

# Send output to WT
logging.info('Sending output to WebEx Teams')
wt_bot.send_message_all_spaces(output)

# Send YAML file as attachment
logging.info('Sending file to WebEx Teams')
wt_bot.send_attachment_all_spaces([yaml_filename])
