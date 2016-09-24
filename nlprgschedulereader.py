import os
import re
import datetime
import requests
from bs4 import BeautifulSoup


class nlprg_meeting():
    reader_pattern = re.compile(
        r"\|\s*\d+\s*\|\s*(\w+)\s*([\w\s\-\.]*)\s*\|\s*\[(.*?)\]\((.*?)\)(?:\s*<br>\s*\[(.*?)\]\((.*?)\))?\s*\|\s*(\d+)/(\d+)/(\d+)")
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

    def __init__(self, schedule_loc):
        '''
        creates a meeting based on the information in the
            schedule file provided
        :schedule_loc: url of the .md file containing the schedule
        '''
        # with open(schedule_loc, 'r') as schedule_file:
        #     self.schedule_text = schedule_file.read()
        # declare instance variables (groups)
        self.schedule_loc = schedule_loc
        self.firstname = ''
        self.lastname = ''
        self.papername = ''
        self.link = ''
        self.papername2 = ''
        self.link2 = ''
        self.month = 0
        self.day = 0
        self.year = 0
        # declare instance variables (other)
        self.paperinfo = ''
        self.date = datetime.date.today()  # this is soon overwritten
        # initialize instance variables
        self.refresh()

    def refresh(self):
        req = requests.get(self.schedule_loc)
        self.schedule_text = str(BeautifulSoup(req.text,))

        for m in re.finditer(self.reader_pattern, self.schedule_text):
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
