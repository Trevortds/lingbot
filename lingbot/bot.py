import os
import time
from slackclient import SlackClient
import datetime
import sys
from subprocess import call
import random
import re
import yaml


from lingbot.features.nlprg_schedule_reader import nlprg_meeting
from lingbot.features import ai
from lingbot.features import generic_schedule_reader
from lingbot import passive_feats


try:
    with open("api.txt", 'r') as f:
        api_token = f.readline()[:-1]
except FileNotFoundError:
    api_token = os.environ['SLACK_TOKEN']

if api_token == "":
    print("NO API TOKEN FOUND")
    sys.exit(1)

# BOT_ID = os.environ.get("BOT_ID")
BOT_ID = "U25Q053D4"

with open("config.yml", "r") as yamlfile:
    cfg = yaml.load(yamlfile)

version_number = "0.2.6"

AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
STATUS_COMMAND = "status"
RESTART_COMMAND = "restart"
MEETING_INFO_COMMAND = "next"
ADD_EVENT_COMMAND = "add event"
ELECTION_COMMAND = "election"
HELP_COMMAND = "help"

channel_codes = {"general": "C0AF685U7",
                 "bot_test": "C25NW0WN7",
                 "random": "C0AEYNKA4"}

general = "C0AF685U7"
bot_test = "C25NW0WN7"
randomchannel = "C0AEYNKA4"


gus = "U0AF1RAGZ"

event_patt = "add event \"(.*)\" \"(\d\d\d\d \d\d \d\d \d\d \d\d)\" \"([\s\S]*)\""

# insantiate slack and twilio clients
# wtf is twilio?
slack_client = SlackClient(api_token)

schedule_loc = cfg["features"]["passive"]["nlprgReminder"]["url"]

READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
start_time = datetime.datetime.now()
next_nlprg = nlprg_meeting(schedule_loc)

meeting_filename = cfg["features"]["passive"]["genericReminder"]["filename"]
next_event = generic_schedule_reader.get_next(meeting_filename)


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
    print("user: ", user)
    print("command: '", command, "'")

    # strip colon
    if command.startswith(":"):
        command = command[2:]
        print("stripped command: '", command, "'")

    # don't talk to yourself
    if user == BOT_ID:
        return next_event

    # check allowable channel
    if cfg["channels"]["restricted"] and not channel in cfg["channels"]["allowed"]:
        print("stopped because of restricted channel")
        print(channel)
        return next_event

    # adding note about scala channel
    if (("python" in command or "scala" in command) and channel != "\#scala" 
            and user != BOT_ID):

        # temporarily disabling until I can make this smarter
        
        # response = "Reminder: \#scala exists for conversation about programming!"
        
        # slack_client.api_call("chat.postMessage", channel=channel, text=response,
        #                   as_user=True)

        return next_event

    elif command.startswith(STATUS_COMMAND):
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
        if next_event is None:
            response = ("Next NLPRG meeting info: \n" + next_nlprg.firstname +
                        " " +
                        next_nlprg.lastname + "\ntopic: \n" +
                        next_nlprg.paperinfo +
                        "\ndate: \n" + next_nlprg.date.strftime("%m/%d/%y") +
                        "\ncountdown: \n" + str(abs(next_nlprg.date -
                                                    datetime.datetime.now())) +
                        "\nSchedule here: https://github.com/clulab/nlp-read" +
                        "ing-group/wiki/FALL-2017-Reading-Schedule")
        elif "nlprg" in command or next_nlprg.date < next_event.date:
            response = ("Next NLPRG meeting info: \n" + next_nlprg.firstname +
                        " " +
                        next_nlprg.lastname + "\ntopic: \n" +
                        next_nlprg.paperinfo +
                        "\ndate: \n" + next_nlprg.date.strftime("%m/%d/%y") +
                        "\ncountdown: \n" + str(abs(next_nlprg.date -
                                                    datetime.datetime.now())) +
                        "\nSchedule here: https://github.com/clulab/nlp-read" +
                        "ing-group/wiki/FALL-2017-Reading-Schedule")
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
            generic_schedule_reader.add_event(meeting_filename, match.group(1), new_date,
                                            match.group(3))
            next_event = generic_schedule_reader.get_next(meeting_filename)
            print(next_event)
            response = "successfully added"
    elif command.startswith(ELECTION_COMMAND):
        response = "How did you find this feature? I didn't implement it yet"
    elif command.startswith(HELP_COMMAND):
        response = ("You can ask for my `status`\n`add event`\nor `next` "+
                    "with the optional argument `nlprg`")

    else:
        response = ai.humor_handler(command)

    if user == gus:
        random.shuffle(ai.gus_messages)
        response = response + "\n\n(P.S. " + ai.gus_messages[0] + ")"

    slack_client.api_call("chat.postMessage", channel=channel, text=response,
                          as_user=True)

    return next_event



def restart():
    '''
    pulls from the github and restarts the script
    '''
    call(["git", "pull"])
    # time.sleep(5)
    python = sys.executable
    os.execv(python, ['python3'] + sys.argv)



def send_message(channel, message):
    # if channel not in channel_codes.keys():
    #     print("channel doesn't exist, please pick from one of these")
    #     for key in channel_codes.keys():
    #         print(key)

    slack_client.api_call("chat.postMessage",
                          channel=channel, text=message, as_user=True)

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
            elif (output and 'text' in output and 
                    ("scala" in output['text'] or "python" in output['text'])):
                return output['text'].strip().lower(), output['channel'], output['user']
    return None, None, None


def main(test = False): 
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    start_time = datetime.datetime.now()
    next_nlprg = nlprg_meeting(schedule_loc)
    next_event = generic_schedule_reader.get_next(meeting_filename)
    passive = passive_feats.Passive(slack_client, cfg["features"]["passive"])

    if slack_client.rtm_connect():
        print("LingBot connected and running")
        while True:
            command, channel, user = parse_slack_output(
                slack_client.rtm_read())
            if command and channel:
                next_event = handle_command(command, channel, user,
                                            next_nlprg, next_event)
            else:
                passive.check()
            time.sleep(READ_WEBSOCKET_DELAY)
            if test:
                return True
    else:
        print("connection failed, invalid slack token or bot id?")
        return False


if __name__ == "__main__":
    main()


