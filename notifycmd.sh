#!/bin/bash

EVENT_TYPE=$*
TOKEN="5543492090:AAHzDvZ7vj0GFpzxKhwGPXWwJzL0U--N0aw"
CHAT_ID="-796955238"
URL="https://api.telegram.org/bot$TOKEN/sendMessage"

curl -s -X POST $URL -d chat_id=$CHAT_ID -d text="$EVENT_TYPE"
echo "$EVENT_TYPE" >> /home/andrew/Project/sai_log.txt
