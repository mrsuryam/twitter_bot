#!/bin/bash

pid=`/bin/ps -fu $USER| grep -i "bot" | grep -v "grep" | awk '{print $2}'`

if [ -z "$pid" ]; then
     echo "process is not running."
else
     kill -9 $pid
     sleep 1800
fi

python3 newBot.py &
