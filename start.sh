#!/bin/bash

while true; do
	if pgrep "python3" > /dev/null
	then
		true
	else
		python3 /home/ubuntu/lingbot/lingbot.py > log.txt 2> err.txt &
	fi
	sleep 1
done
