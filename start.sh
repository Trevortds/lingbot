#!/bin/bash

while true; do
	if pgrep "python3" > /dev/null
	then
		true
	else
		python3 ./lingbot/bot.py &
	fi
	sleep 1
done
