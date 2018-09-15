import os
import time

import requests
from slackclient import SlackClient
import datetime
import sys
from subprocess import call
import random
import re
import yaml
import logging

from slackclient._server import SlackConnectionError

from lingbot.features.nlprg_schedule_reader import nlprg_meeting
from lingbot.features import ai
from lingbot.features import generic_schedule_reader
from lingbot import passive_feats, active_feats

logging.getLogger().setLevel(logging.INFO)

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

try:
    with open("config.yml", "r") as yamlfile:
        cfg = yaml.load(yamlfile)
except FileNotFoundError:
    with open("default-config.yml", "r") as yamlfile:
        cfg = yaml.load(yamlfile)

version_number = cfg["version"]

AT_BOT = "<@" + BOT_ID + ">"


channel_codes = {"general": "C0AF685U7",
                 "bot_test": "C25NW0WN7",
                 "random": "C0AEYNKA4"}

general = "C0AF685U7"
bot_test = "C25NW0WN7"
randomchannel = "C0AEYNKA4"


# insantiate slack and twilio clients
# wtf is twilio?
slack_client = SlackClient(api_token)

schedule_loc = cfg["features"]["passive"]["nlprgReminder"]["url"]

READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
start_time = datetime.datetime.now()
next_nlprg = nlprg_meeting(schedule_loc)

meeting_filename = cfg["features"]["passive"]["genericReminder"]["filename"]
next_event = generic_schedule_reader.get_next(meeting_filename)


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
    passive = passive_feats.Passive(slack_client, cfg)
    active = active_feats.Active(slack_client, cfg)

    if slack_client.rtm_connect():
        logging.info("LingBot connected and running")
        timeout = 1

        if "pytest" not in sys.modules:
            # do this only if you're not testing. got really spammy. 
            send_message(bot_test, "Lingbot started at " + str(start_time.strftime("%A, %d. %B %Y %I:%M%p")) + "\n version " + str(version_number))
        while True:
            if timeout != 1:
                send_message(bot_test, "Something went wrong, please check the logs")
            try:
                command, channel, user = parse_slack_output(
                    slack_client.rtm_read())
            except SlackConnectionError:
                logging.warning("Slack Connection Error: sleeping {} seconds".format(timeout))
                time.sleep(timeout)
                timeout = timeout * 2
                continue
            except requests.ConnectionError:
                logging.warning("Slack http Connection Error: sleeping {} seconds".format(timeout))
                time.sleep(timeout)
                timeout = timeout * 2
                continue
            except ConnectionResetError:
                logging.warning("Slack http Connection Reset: sleeping {} seconds".format(timeout))
                time.sleep(timeout)
                timeout = timeout * 2
                continue
            except Exception:
                logging.warning("Something else went wrong: sleeping {} seconds".format(timeout))
                logging.warning(sys.exc_info()[0])
                time.sleep(timeout)
                timeout = timeout * 2
                continue
            else:
                timeout = 1

            if command and channel:
                active.handle_command(command, channel, user)
            else:
                passive.check()
            time.sleep(READ_WEBSOCKET_DELAY)
            if test:
                return True
    else:
        logging.error("connection failed, invalid slack token or bot id?")
        return False


if __name__ == "__main__":
    main()


