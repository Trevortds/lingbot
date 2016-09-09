import os
import time
from slackclient import SlackClient
import datetime
import sys
from subprocess import call
from schedulereader import meeting
import ai


BOT_ID = os.environ.get("BOT_ID")
BOT_ID = "U25Q053D4"

AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
STATUS_COMMAND = "status"
RESTART_COMMAND = "restart"
MEETING_INFO_COMMAND = "next nlprg"

channel_codes = {"general":"C0AF685U7",
                 "bot_test":"C25NW0WN7",
                 "random":"C0AEYNKA4"}

general = "C0AF685U7"
bot_test = "C25NW0WN7"
random = "C0AEYNKA4"

# insantiate slack and twilio clients
# wtf is twilio?
slack_client = SlackClient("xoxb-73816173446-K1KCFywSvpmw4Toyrg2eKZGa")

schedule_loc = ("https://raw.githubusercontent.com/wiki/clulab/nlp-reading-"
                "group/Fall-2016-Reading-Schedule.md")


def handle_command(command, channel):
    '''
    recieves commands directed at the bot and tetermines if they are valid
                commands
    If so, then acts on the commands. If not, returns back what it needs for
            clarification
    '''

    response = ("Not sure what you mean. You can ask for my `status` or"
                " for `next nlprg`")
    print(datetime.datetime.now().isoformat())
    print("channel: ", channel)
    print("command: ", command)
    if command.startswith(STATUS_COMMAND):
        response = ("present instance started at " +
                    str(start_time.strftime("%A, %d. %B %Y %I:%M%p")))
    elif command.startswith(RESTART_COMMAND):
        response = ("restarting. Ending instance started at " +
                    str(start_time.strftime("%A, %d. %B %Y %I:%M%p")))
        slack_client.api_call("chat.postMessage", channel=channel,
                              text=response, as_user=True)
        restart()
    elif command.startswith(MEETING_INFO_COMMAND):
        response = ("Next meeting info: \n" + next_meeting.firstname + " " +
                    next_meeting.lastname + "\ntopic: \n" +
                    next_meeting.paperinfo +
                    "\ndate: \n" + next_meeting.date.strftime("%m/%d/%y") +
                    "\ncountdown: \n" + str(abs(next_meeting.date -
                                                datetime.datetime.now())))
    else:
        response = ai.humor_handler(command)

    slack_client.api_call("chat.postMessage", channel=channel, text=response,
                          as_user=True)


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
                    output['channel']
    return None, None


def passive_check():
    '''
    This function is run every second. If you have something you want to
    happen at a particular time, put it here, following the template of the
    others
    '''
    send = 0
    now = datetime.datetime.now()
    if now.weekday() == 3 and now == now.replace(hour=13, minute=0, second=0):
        # hacky hour reminder
        response = ("Hacky Hour today, at Frog & Firkin, starting at 1600! "
                    "Come, have a drink, talk to smart people, have fun!"
                    " :beers:")
        send = 1

    elif now.date() == next_meeting.date.date() and \
            now == now.replace(hour=10, minute=0, second=0):
        # nlprg morning reminder
        response = ("NLP Reading Group today! \n" + next_meeting.firstname +
                    "presenting on\n " + next_meeting.paperinfo +
                    "\n\n Join us in Gould-Simpson 906 at 1400\n\n" +
                    "(food and coffee provided)")
        send = 1

    elif now.date() == next_meeting.date.date() and \
            now == now.replace(hour=13, minute=45, second=0):
        # nlprg evening reminder
        response = ("NLP Reading Group happening NOW! :book: Gould-Simpson 906"
                    "\n(food and coffee provided, like for free, so come)\n\n"
                    "Afterwards, join us for drinks at Bear Tracks!")
        send = 1
    elif now.date() == next_meeting.date.date() and \
            now == now.replace(hour=15, minute=0, second=0):
        # nlprg reset
        next_meeting.refresh()
        send = 0

    if send == 1:
        slack_client.api_call("chat.postMessage", channel=general,
                              text=response, as_user=True)

    send = 0  # this should be redundant but just in case. I don't want to spam


def restart():
    '''
    pulls from the github and restarts the script
    '''
    call(["git", "pull"])
    python = sys.executable
    os.execl(python, python, * sys.argv)




if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    start_time = datetime.datetime.now()
    next_meeting = meeting(schedule_loc)

    if slack_client.rtm_connect():
        print("LingBot connected and running")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            else:
                passive_check()
                pass
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("connection failed, invalid slack token or bot id?")



def send_message(channel, message):
    if channel not in channel_codes.keys():
        print("channel doesn't exist, please pick from one of these")
        for key in channel_codes.keys():
            print(key)

    slack_client.api_call("chat.postMessage", channel=channel_codes[channel], text=message, as_user=True)