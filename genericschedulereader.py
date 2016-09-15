import csv
import datetime

filename = "generic_schedule.csv"

class meeting:
	def __init__(self, name, date, text):
		self.name = name
		self.date = date
		self.text = text


def gt(dt_str):
	'''
	stolen from stackoverflow
	'''
    dt, _, us= dt_str.partition(".")
    dt= datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    us= int(us.rstrip("Z"), 10)
    return dt + datetime.timedelta(microseconds=us)


def add_event(name, time, text):
	'''
	arguments:
	name: name of event
	time: datetime object for event
	text: text to display when event is ready to go. 
	'''
	times = datetime.datetime.now()
	with open(filename, newline='') as csvfile:
		calwriter = csv.writer(csvfile, delimiter=' ',
				uotechar='|', quoting=csv.QUOTE_MINIMAL)
		#TODO check for duplicates
		calwriter.writerow([name, times.isoformat(), text])


def delete_row()


def get_next():
	
