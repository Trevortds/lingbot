from lingbot.features import generic_schedule_reader, nlprg_schedule_reader, ai, next_event_tracker
import os
import sys
import datetime
from subprocess import call

constructors = {
    "meetingInfo": lambda x: next_event_tracker.NextEvent(x), 
    "addEvent" : lambda x: generic_schedule_reader.EventAdder(x),
}

STATUS_COMMAND = "status"
RESTART_COMMAND = "restart"
HELP_COMMAND = "help"
event_patt = "add event \"(.*)\" \"(\d\d\d\d \d\d \d\d \d\d \d\d)\" \"([\s\S]*)\""

general = "C0AF685U7"
bot_test = "C25NW0WN7"
randomchannel = "C0AEYNKA4"
BOT_ID = "U25Q053D4"


gus = "U0AF1RAGZ"


class Active():

    def __init__(self, slack_client, config):
        self.allconfig = config
        self.config = config["features"]["active"]
        self.slack_client = slack_client
        self.start_time = datetime.datetime.now()

        self.actors = {}

        for feat in self.config:
            if self.config[feat]["active"]:
                self.actors[self.config[feat]["command"]] = constructors[feat](self.config[feat])



    def handle_command(self, command, channel, user):
        '''
        recieves commands directed at the bot and tetermines if they are valid
                    commands
        If so, then acts on the commands. If not, returns back what it needs for
                clarification
        '''

        response = ("")
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
            return

        # check allowable channel
        if self.allconfig["channels"]["restricted"] and not channel in self.allconfig["channels"]["allowed"]:
            print("stopped because of restricted channel")
            print(channel)
            return

        elif command.startswith(HELP_COMMAND):
            response = self.help()

        elif command.startswith(STATUS_COMMAND):
            response = self.status()

        elif command.startswith(RESTART_COMMAND):
            response = ("restarting. Ending instance started at " +
                        str(self.start_time.strftime("%A, %d. %B %Y %I:%M%p")))
            self.slack_client.api_call("chat.postMessage", channel=channel,
                                  text=response, as_user=True)
            self.restart()

        else: 
            for trigger in self.actors:
                if command.startswith(trigger):
                    response = self.actors[trigger].handle(command, channel, user)   

        if response == '':
            response = ai.humor_handler(command)

        if user == gus:
            random.shuffle(ai.gus_messages)
            response = response + "\n\n(P.S. " + ai.gus_messages[0] + ")"

        self.slack_client.api_call("chat.postMessage", channel=channel, text=response,
                              as_user=True)

        return



    def status(self):
        response = ("present instance started at " +
                    str(self.start_time.strftime("%A, %d. %B %Y %I:%M%p")) +
                    "\nVersion Number: " + str(self.allconfig["version"]))
        return response


    def restart(self):
        '''
        pulls from the github and restarts the script
        '''
        call(["git", "pull"])
        # time.sleep(5)
        python = sys.executable
        os.execv(python, ['python3'] + sys.argv)


    def help(self):
        response = ("You can ask for my `status`\n`add event`\nor `next` "+
                        "with the optional argument `nlprg`")
        return response