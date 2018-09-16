import os
import re
import datetime
import requests
from bs4 import BeautifulSoup

reader_pattern = r"\|\s*\d+\s*\|\s*(\w+)\s*([\w\s\-\.]*)\s*\|\s*\[(.*?)\]\((.*?)\)(?:\s*<br>\s*\[(.*?)\]\((.*?)\))?\s*\|\s*(\d+)/(\d+)/(\d+)"


class nlprg_meeting():
    # regex parser for reading schedule table
    # matches lines of the form
    # |1 | Firstname lastname | [nameofpaper](link) | m/d/y | GS 906 |
    # capture groups:
    # 1. firstname
    # 2. lastname
    # 3. papername
    # 4. paperlink
    # 5. papername2
    # 6. paperlink2
    # 5. month
    # 6. day
    # 7. year
    firstname = ''
    lastname = ''
    papername = ''
    paperlink = ''
    papername2 = ''
    paperlink2 = ''
    month = 0
    day = 0
    year = 0
        # declare instance variables (other)
    paperinfo = ''
    date = datetime.datetime.today()  # this is soon overwritten

    def __init__(self, schedule_loc="https://raw.githubusercontent.com/wiki/clulab/nlp-reading-group/Fall-2017-Reading-Schedule.md",
                 reader_pattern=reader_pattern):
        '''
        creates a meeting based on the information in the
            schedule file provided
        :schedule_loc: url of the .md file containing the schedule
        '''
        # with open(schedule_loc, 'r') as schedule_file:
        #     self.schedule_text = schedule_file.read()
        # declare instance variables (groups)
        self.reader_regex = re.compile(reader_pattern)
        self.schedule_loc = schedule_loc
        self.firstname = ''
        self.lastname = ''
        self.papername = ''
        self.paperlink = ''
        self.papername2 = ''
        self.paperlink2 = ''
        self.month = 0
        self.day = 0
        self.year = 0
        # declare instance variables (other)
        self.paperinfo = ''
        self.date = datetime.datetime.today()  # this is soon overwritten
        # initialize instance variables
        self.refresh()

    def refresh(self):
        req = requests.get(self.schedule_loc)
        self.schedule_text = str(BeautifulSoup(req.text, "lxml"))

        for m in re.finditer(self.reader_regex, self.schedule_text):
            self.year = int(m.group(9))
            self.month = int(m.group(7))
            self.day = int(m.group(8))
            self.date = datetime.datetime(self.year, self.month, self.day, 14)
            today = datetime.datetime.now()
            if self.date >= today:
                self.firstname = m.group(1)
                self.lastname = m.group(2)
                self.papername = m.group(3)
                self.paperlink = m.group(4)
                self.paperinfo = m.group(3) + "\nLink: " + m.group(4) + "\n"
                self.papername2 = m.group(5)
                self.paperlink2 = m.group(6)
                if m.group(5) is not None:
                    self.paperinfo = self.paperinfo + "and \n" + \
                        m.group(5) + "\nLink: " + m.group(6) + "\n"

                break

class Reminder():

    def __init__(self, config):
        self.active = config["active"]
        self.url = config["url"]
        self.remind_time = config["time"]
        self.next_nlprg = nlprg_meeting(self.url)

    def check(self):
        if not self.active:
            return None
        else:
            now = datetime.datetime.now().replace(microsecond=0)
            if now.date() == self.next_nlprg.date.date() and \
                now == now.replace(hour=self.remind_time, minute=0, second=0):
                # nlprg morning reminder
                response = ("NLP Reading Group today! \n" + self.next_nlprg.firstname +
                            " presenting on\n " + self.next_nlprg.paperinfo +
                            "\n\n Join us in Gould-Simpson 906 at 1400\n\n" +
                            "(food and coffee provided)\n\nSee full schedule here: " +
                            "https://github.com/clulab/nlp-reading-group/wiki/FALL" +
                            "-2017-Reading-Schedule")
                return response, True

            elif now.date() == self.next_nlprg.date.date() and \
                    now == now.replace(hour=13, minute=45, second=0):
                # nlprg evening reminder
                response = ("NLP Reading Group happening NOW! :book: Gould-Simpson 906"
                            "\n(food and coffee provided, like for free, so come)\n\n"
                            "")
                return response, True

            elif now.date() == self.next_nlprg.date and \
                    now == now.replace(hour=15, minute=0, second=0):
                # nlprg reset
                self.next_nlprg.refresh()
                return None

            if now.weekday() == 3 and now == now.replace(hour=13, minute=0, second=0):
                # hacky hour reminder
                response = ("Hacky Hour today, at {}, starting at {}! "
                            "Come, have a drink, talk to smart people, have fun!"
                            " :beers:").format(self.location, self.time)
                return response, True
            else:
                return None