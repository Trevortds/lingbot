import os
import time
from slackclient import SlackClient
import datetime
import sys
from subprocess import call
import random
import re

from nlprgschedulereader import nlprg_meeting
import ai
import genericschedulereader

with open("api.txt", 'r') as f:
    api_token = f.readline()[:-1]
BOT_ID = os.environ.get("BOT_ID")
BOT_ID = "U25Q053D4"

version_number = "0.2.3"

AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
STATUS_COMMAND = "status"
RESTART_COMMAND = "restart"
MEETING_INFO_COMMAND = "next"
ADD_EVENT_COMMAND = "add event"
ELECTION_COMMAND = "election"

channel_codes = {"general": "C0AF685U7",
                 "bot_test": "C25NW0WN7",
                 "random": "C0AEYNKA4"}

general = "C0AF685U7"
bot_test = "C25NW0WN7"
randomchannel = "C0AEYNKA4"


gus = "U0AF1RAGZ"

event_patt = "add event \"(.*)\" \"(\d\d\d\d \d\d \d\d \d\d \d\d)\" \"(.*)\""

# insantiate slack and twilio clients
# wtf is twilio?
slack_client = SlackClient(api_token)

schedule_loc = ("https://raw.githubusercontent.com/wiki/clulab/nlp-reading-"
                "group/Fall-2016-Reading-Schedule.md")


def handle_command(command, channel, user, next_nlprg, next_event):
    '''
    recieves commands directed at the bot and tetermines if they are valid
                commands
    If so, then acts on the commands. If not, returns back what it needs for
            clarification
    '''

    response = ("Not sure what you mean. You can ask for my `status` or"
                " for `next`")
    print(datetime.datetime.now().isoformat())
    print("channel: ", channel)
    print("command: ", command)
    if command.startswith(STATUS_COMMAND):
        response = ("present instance started at " +
                    str(start_time.strftime("%A, %d. %B %Y %I:%M%p")) +
                    "\nVersion Number: " + version_number)
    elif command.startswith(RESTART_COMMAND):
        response = ("restarting. Ending instance started at " +
                    str(start_time.strftime("%A, %d. %B %Y %I:%M%p")))
        slack_client.api_call("chat.postMessage", channel=channel,
                              text=response, as_user=True)
        restart()
    elif command.startswith(MEETING_INFO_COMMAND):
        # TODO generic next meeting
        if next_event is None:
            response = ("Next NLPRG meeting info: \n" + next_nlprg.firstname +
                        " " +
                        next_nlprg.lastname + "\ntopic: \n" +
                        next_nlprg.paperinfo +
                        "\ndate: \n" + next_nlprg.date.strftime("%m/%d/%y") +
                        "\ncountdown: \n" + str(abs(next_nlprg.date -
                                                    datetime.datetime.now())) +
                        "\nSchedule here: https://github.com/clulab/nlp-read" +
                        "ing-group/wiki/Fall-2016-Reading-Schedule")
        elif "nlprg" in command or next_nlprg.date < next_event.date:
            response = ("Next NLPRG meeting info: \n" + next_nlprg.firstname +
                        " " +
                        next_nlprg.lastname + "\ntopic: \n" +
                        next_nlprg.paperinfo +
                        "\ndate: \n" + next_nlprg.date.strftime("%m/%d/%y") +
                        "\ncountdown: \n" + str(abs(next_nlprg.date -
                                                    datetime.datetime.now())) +
                        "\nSchedule here: https://github.com/clulab/nlp-read" +
                        "ing-group/wiki/Fall-2016-Reading-Schedule")
        else:
            response = ("Next event: " + next_event.name + "\ndate: " +
                        next_event.date.strftime("%A, %d. %B %Y %H:%M") +
                        "\nInfo: \n" + next_event.text)

    elif command.startswith(ADD_EVENT_COMMAND):
        match = re.search(event_patt, command)
        if match is None:
            response = ("Syntax: add event \"name\" \"yyyy mm dd hh mm\" " +
                        "\"information\"")
        else:
            new_date = datetime.datetime.strptime(match.group(2),
                                                  "%Y %m %d %H %M")
            genericschedulereader.add_event(match.group(1), new_date,
                                            match.group(3))
            next_event = genericschedulereader.get_next()
            response = "successfully added"
    elif command.startswith(ELECTION_COMMAND):
        response = "How did you find this feature? I didn't implement it yet"
    else:
        response = ai.humor_handler(command)

    if user == gus:
        random.shuffle(ai.gus_messages)
        response = response + "\n\n(P.S. " + ai.gus_messages[0] + ")"

    slack_client.api_call("chat.postMessage", channel=channel, text=response,
                          as_user=True)

    return next_event


def parse_slack_output(slack_rtm_output):
    '''
    The slack real time messaging API is an events firehose.
    This parsing function returns none unless a message is directed
    at the bot based on its id
    '''
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                    output['channel'], output['user']
    return None, None, None


def passive_check(next_nlprg, next_event):
    '''
    This function is run every second. If you have something you want to
    happen at a particular time, put it here, following the template of the
    others
    '''

    send = 0
    now = datetime.datetime.now().replace(microsecond=0)
    if now.weekday() == 3 and now == now.replace(hour=13, minute=0, second=0):
        # hacky hour reminder
        response = ("Hacky Hour today, at Gentle Ben's, starting at 1600! "
                    "Come, have a drink, talk to smart people, have fun!"
                    " :beers:")
        send = 1

    elif now.date() == next_nlprg.date.date() and \
            now == now.replace(hour=10, minute=0, second=0):
        # nlprg morning reminder
        response = ("NLP Reading Group today! \n" + next_nlprg.firstname +
                    " presenting on\n " + next_nlprg.paperinfo +
                    "\n\n Join us in Gould-Simpson 906 at 1400\n\n" +
                    "(food and coffee provided)\n\nSee full schedule here: " +
                    "https://github.com/clulab/nlp-reading-group/wiki/Fall" +
                    "-2016-Reading-Schedule")
        send = 1

    elif now.date() == next_nlprg.date.date() and \
            now == now.replace(hour=13, minute=45, second=0):
        # nlprg evening reminder
        response = ("NLP Reading Group happening NOW! :book: Gould-Simpson 906"
                    "\n(food and coffee provided, like for free, so come)\n\n"
                    "Afterwards, join us for drinks at Bear Tracks!")
        send = 1
    elif now.date() == next_nlprg.date.date() and \
            now == now.replace(hour=15, minute=0, second=0):
        # nlprg reset
        next_nlprg.refresh()
        send = 0

    elif next_event is not None:
        if next_event.date - now == datetime.timedelta(hours=6):
            response = ("Event Today: " + next_event.name + "\nAt: " +
                        next_event.date.strftime("%H:%M") + "\n\nInfo: " +
                        next_event.text)
            send = 1
        elif next_event.date + datetime.timedelta(seconds=1) == now:
            response = (next_event.name + " starting now!")
            next_event = genericschedulereader.get_next()
            send = 1

    if send == 1:
        slack_client.api_call("chat.postMessage", channel=general,
                              text=response, as_user=True)

    return next_event
    send = 0  # this should be redundant but just in case. I don't want to spam


def restart():
    '''
    pulls from the github and restarts the script
    '''
    call(["git", "pull"])
    # time.sleep(5)
    python = sys.executable
    os.execv(python, ['python3'] + sys.argv)


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    start_time = datetime.datetime.now()
    next_nlprg = nlprg_meeting(schedule_loc)
    next_event = genericschedulereader.get_next()

    if slack_client.rtm_connect():
        print("LingBot connected and running")
        while True:
            command, channel, user = parse_slack_output(
                slack_client.rtm_read())
            if command and channel:
                next_event = handle_command(command, channel, user,
                                            next_nlprg, next_event)
            else:
                passive_check(next_nlprg, next_event)
                pass
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("connection failed, invalid slack token or bot id?")


def send_message(channel, message):
    # if channel not in channel_codes.keys():
    #     print("channel doesn't exist, please pick from one of these")
    #     for key in channel_codes.keys():
    #         print(key)

    slack_client.api_call("chat.postMessage",
                          channel=channel, text=message, as_user=True)
