#!/bin/bash
FILE="tunnel_output"
SCHEME="http"
PYTHON_EXEC="/home/carlos/miniconda3/envs/pb377/bin/python"
PORT=5000
REGION="eu"

while getopts pfsr option
do
case "${option}"
in
p) PORT=${OPTARG};;
f) FILE=${OPTARG};;
s) SCHEME=${OPTARG};;
r) REGION=${OPTARG};;
esac
done
# Open Reverse SSH to NGROK for creating a tunnel to the specified port
ssh -o "StrictHostKeyChecking=no" -R 80:localhost:$PORT tunnel.$REGION.ngrok.com $SCHEME > $FILE &
# Sleep 1 second so the file is updated
sleep 3
# Python command to parse FILE for getting the URL
URL=$($PYTHON_EXEC 'parse_tunnel_info.py' -f $FILE)
# Python command to update the webhook URL in the testing service
$PYTHON_EXEC 'update_wt_webhook.py' -u $URL
# Update webhook in Spotify App and in spotify.yml
$PYTHON_EXEC 'update_spotify_webhook.py' -u $URL
echo "Update webhook in spotify App settings manually: https://developer.spotify.com/dashboard/applications"