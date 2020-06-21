#!/bin/bash
FILE="tunnel_output"

# Kill the SSH process against the ngrok host
kill $(ps aux | grep ngrok | grep -v "grep" | sed 's/^[[:alnum:]]*[[:blank:]]*\([[:alnum:]]*\).*/\1/')
echo '' > $FILE
# Optional: Restore the webhook URL to the previous value