import csv
import datetime

filename = "generic_schedule.csv"

# TODO make cleanup algorithm that eliminates events before the present by
# clearing the csv and repopulating it


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
    us = int(us.rstrip("Z"), 10)
    return dt + datetime.timedelta(microseconds=us)


def add_event(name, time, text):
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
        calwriter.writerow([name, time.isoformat(), text])


def get_next():
    with open(filename, newline='') as csvfile:
        schedulereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        soonest = next(schedulereader)
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
