import datetime


class Reminder():

    def __init__(self, config):
        self.active = config["active"]
        self.location = config["location"]
        self.time = config["time"]

    def check(self):
        if not self.active:
            return None
        else:
            now = datetime.datetime.now().replace(microsecond=0)
            if now.weekday() == 3 and now == now.replace(hour=13, minute=0, second=0):
                # hacky hour reminder
                response = ("Hacky Hour today, at {}, starting at {}! "
                            "Come, have a drink, talk to smart people, have fun!"
                            " :beers:").format(self.location, self.time)
                return response, True
            else:
                return None