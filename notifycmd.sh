#!/bin/bash

EVENT_TYPE=$*
TOKEN="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
CHAT_ID="-YYYYYYYYYYYYYYYYYYYYYYYYYY"
URL="https://api.telegram.org/bot$TOKEN/sendMessage"

curl -s -X POST $URL -d chat_id=$CHAT_ID -d text="$EVENT_TYPE"
echo "$EVENT_TYPE" >> /home/andrew/Project/sai_log.txt
