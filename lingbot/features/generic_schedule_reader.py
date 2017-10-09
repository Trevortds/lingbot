import csv
import datetime
from lingbot.features import next_event_tracker
import re

# TODO make cleanup algorithm that eliminates events before the present by
# clearing the csv and repopulating it
event_patt = "add event \"(.*)\" \"(\d\d\d\d \d\d \d\d \d\d \d\d)\" \"([\s\S]*)\""


class meeting:
    def __init__(self, name, date, text):
        self.name = name
        self.date = date
        self.text = text


def gt(dt_str):
    '''
    stolen from stackoverflow
    '''
    dt, _, us = dt_str.partition(".")
    dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    return dt


def add_event(filename, name, time, text):
    '''
    arguments:
    name: name of event
    time: datetime object for event
    text: text to display when event is ready to go. 
    '''
    with open(filename, 'a', newline='') as csvfile:
        calwriter = csv.writer(csvfile, delimiter=' ',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # TODO check for duplicates
        print(calwriter.writerow([name, time.isoformat(), text]))

def get_next(filename):
    try:
        with open(filename, newline='') as csvfile:
            schedulereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            try:
                soonest = next(schedulereader)
            except StopIteration:
                return None
            soonest_time = gt(soonest[1])
            while soonest_time < datetime.datetime.now():
                try:
                    soonest = next(schedulereader)
                except:
                    return None
                soonest_time = gt(soonest[1])
            for row in schedulereader:
                time = gt(row[1])
                if time > datetime.datetime.now():
                    if time < soonest_time:
                        soonest = row
                        soonest_time = time
            return meeting(soonest[0], soonest_time, soonest[2])
    except FileNotFoundError:
        return 4




class EventAdder():
    def __init__(self, config):
        self.config = config
    def handle(self, command, channel, user):
        match = re.search(event_patt, command)
        if match is None:
            response = ("Syntax: add event \"name\" \"yyyy mm dd hh mm\" " +
                        "\"information\"")
        else:
            new_date = datetime.datetime.strptime(match.group(2),
                                                  "%Y %m %d %H %M")
            add_event(self.config["filename"], match.group(1), new_date,
                                            match.group(3))
            next_event_tracker.NextEvent().update()
            
            response = "successfully added"
        return response
        



    
class Reminder():
    def __init__(self, config):
        self.active = config["active"]
        self.hours_before = config["hoursBefore"]
        self.filename = config["filename"]
        self.next_generic = get_next(self.filename)

    def check(self):
        if not self.active:
            return None
        else:
            now = datetime.datetime.now().replace(microsecond=0)
            

            if self.next_generic is not None:
                if self.next_generic.date - now == datetime.timedelta(hours=self.hours_before):
                    response = ("Event Today: " + self.next_generic.name + "\nAt: " +
                                self.next_generic.date.strftime("%H:%M") + "\n\nInfo: "+

                                self.next_generic.text)
                    return response, True
                elif self.next_generic.date + datetime.timedelta(seconds=1) == now:
                    response = (self.next_generic.name + " starting now!")
                    self.next_generic = get_next(self.filename)
                    next_event_tracker.NextEvent().update()
                    return response, True

            else:
                return None