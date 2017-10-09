from lingbot.features import generic_schedule_reader, nlprg_schedule_reader, hacky_hour_reminder
import datetime

constructors = {
    "hackyHourReminder": lambda x: hacky_hour_reminder.Reminder(x),
    "nlprgReminder": lambda x: nlprg_schedule_reader.Reminder(x),
    "genericReminder": lambda x : generic_schedule_reader.Reminder(x)

}

general = "C0AF685U7"
bot_test = "C25NW0WN7"
randomchannel = "C0AEYNKA4"

class Passive():

    def __init__(self, slack_client, config):
        config = config["features"]["passive"]
        self.config = config
        self.reminder_objects = []
        for feat in config:
            self.reminder_objects.append(constructors[feat](config[feat]))
        self.slack_client = slack_client



    def check(self):
        '''
        This function is run every second. If you have something you want to
        happen at a particular time, put it here, following the template of the
        others
        '''

        send = 0
        now = datetime.datetime.now().replace(microsecond=0)
        

        for obj in self.reminder_objects:
            response = obj.check()
            if response is not None and response[1]:
                self.slack_client.api_call("chat.postMessage", channel=general,
                                  text=response[0], as_user=True)
        

        send = 0  # this should be redundant but just in case. I don't want to spam
