#!/bin/bash
FILE="tunnel_output"
SCHEME="http"
PYTHON_EXEC="/home/carlos/miniconda3/envs/pb377/bin/python"
PORT=5000

while getopts pfs option
do
case "${option}"
in
p) PORT=${OPTARG};;
f) FILE=${OPTARG};;
s) SCHEME=${OPTARG};;
esac
done
# Open Reverse SSH to NGROK for creating a tunnel to the specified port
ssh -o "StrictHostKeyChecking=no" -R 80:localhost:$PORT tunnel.eu.ngrok.com $SCHEME > $FILE &
# Sleep 1 second so the file is updated
sleep 2
# Python command to parse FILE for getting the URL
URL=$($PYTHON_EXEC 'parse_tunnel_info.py' -f $FILE)
# Python command to update the webhook URL in the testing service
$PYTHON_EXEC 'update_wt_webhook.py' -u $URL