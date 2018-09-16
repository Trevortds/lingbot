
from lingbot.features import generic_schedule_reader, nlprg_schedule_reader
import datetime
'''
singleton. tracks the next generic and nlprg event, on handle it returns the next one unless nlprg is called specifically
'''

class NextEvent:
    class __NextEvent:
        config = {}
        def __init__(self, config):
            self.config = config 
            self.update()
        def update(self):
            self.next_generic = generic_schedule_reader.get_next(self.config["filename"])
            self.next_nlprg = nlprg_schedule_reader.nlprg_meeting(self.config["nlprg_url"])
        def handle(self, command, channel, user):
            response = ""
            if self.next_generic is None:
                response = ("Next NLPRG meeting info: \n" + self.next_nlprg.firstname +
                            " " +
                            self.next_nlprg.lastname + "\ntopic: \n" +
                            self.next_nlprg.paperinfo +
                            "\ndate: \n" + self.next_nlprg.date.strftime("%m/%d/%y") +
                            "\ncountdown: \n" + str(abs(self.next_nlprg.date -
                                                        datetime.datetime.now())) +
                            "\nSchedule here: https://github.com/clulab/nlp-read" +
                            "ing-group/wiki/FALL-2017-Reading-Schedule")
            elif "nlprg" in command or self.next_nlprg.date < self.next_generic.date:
                response = ("Next NLPRG meeting info: \n" + self.next_nlprg.firstname +
                            " " +
                            self.next_nlprg.lastname + "\ntopic: \n" +
                            self.next_nlprg.paperinfo +
                            "\ndate: \n" + self.next_nlprg.date.strftime("%m/%d/%y") +
                            "\ncountdown: \n" + str(abs(self.next_nlprg.date -
                                                        datetime.datetime.now())) +
                            "\nSchedule here: https://github.com/clulab/nlp-read" +
                            "ing-group/wiki/FALL-2017-Reading-Schedule")
            else:
                response = ("Next event: " + self.next_generic.name + "\ndate: " +
                            self.next_generic.date.strftime("%A, %d. %B %Y %H:%M") +
                            "\nInfo: \n" + self.next_generic.text)
            return response


    instance = None

    def __new__(cls, config=None):
        if not NextEvent.instance:
            NextEvent.instance = NextEvent.__NextEvent(config)
        if config is not None:
            NextEvent.instance.config = config
        return NextEvent.instance
    def update(self):
        NextEvent.instance.update()
    def handle(self , command, channel, user):
        return NextEvent.instance.handle(command, channel, user)