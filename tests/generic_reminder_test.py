import pytest
from lingbot.features import generic_schedule_reader
import datetime
import bs4

FAKE_TIME_FAIL = datetime.datetime(2017, 10, 6, 12, 0, 0) 
FAKE_TIME_REMINDER = datetime.datetime(2017, 10, 10, 4, 10, 0)
FAKE_TIME_LAST_MINUTE = datetime.datetime(2017, 10, 10, 10, 10, 1) 

DATE_GENERATOR = lambda y, m, d: datetime.date(y, m, d)

config = {
"active": True, 
"filename": "tests/resources/generic_schedule.csv",  
"hoursBefore": 6
}


def test_constructor():
    reminder = generic_schedule_reader.Reminder(config)

@pytest.fixture
def patch_datetime_now_fail(monkeypatch):
    reminder = generic_schedule_reader.Reminder(config)

    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME_FAIL
        @classmethod
        def today(cls):
            return FAKE_TIME_FAIL

    # class myBeautifulSoup:
    #     def __init__(self, thing, otherthing):
    #         return open("resources/Fall-2017-Reading-Schedule.md", "r").read()

    monkeypatch.setattr(datetime, 'datetime', mydatetime)
    # monkeypatch.setattr(bs4, 'BeautifulSopu', myBeautifulSoup)
    return reminder


def test_check_negative(patch_datetime_now_fail):
    assert patch_datetime_now_fail.check() is None

@pytest.fixture
def patch_datetime_morning(monkeypatch):

    class mydatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return FAKE_TIME_REMINDER
        @classmethod
        def today(cls):
            return FAKE_TIME_REMINDER

    # class myBeautifulSoup:
    #     def __init__(self, thing, otherthing):
    #         return open("resources/Fall-2017-Reading-Schedule.md", "r").read()

    monkeypatch.setattr(datetime, 'datetime', mydatetime)
    # monkeypatch.setattr(bs4, 'BeautifulSopu', myBeautifulSoup)
    reminder = generic_schedule_reader.Reminder(config)
    return reminder

def test_check_reminder(patch_datetime_morning):
    assert datetime.datetime.now() == FAKE_TIME_REMINDER
    assert FAKE_TIME_REMINDER.date() == patch_datetime_morning.next_event.date.date()
    assert FAKE_TIME_REMINDER.weekday() == 1
    assert FAKE_TIME_REMINDER == FAKE_TIME_REMINDER.replace(hour=4, minute=10, second=0)
    assert patch_datetime_morning.check() == (("Event Today: " + "thing" + "\nAt: " +
                                "10:10" + "\n\nInfo: "+
                                "more thingies"), True)

@pytest.fixture
def patch_datetime_last_minute(monkeypatch):

    class mydatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return FAKE_TIME_REMINDER
        @classmethod
        def today(cls):
            return FAKE_TIME_REMINDER

    # class myBeautifulSoup:
    #     def __init__(self, thing, otherthing):
    #         return open("resources/Fall-2017-Reading-Schedule.md", "r").read()

    monkeypatch.setattr(datetime, 'datetime', mydatetime)
    # monkeypatch.setattr(bs4, 'BeautifulSopu', myBeautifulSoup)
    reminder = generic_schedule_reader.Reminder(config)

    class mydatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return FAKE_TIME_LAST_MINUTE
        @classmethod
        def today(cls):
            return FAKE_TIME_LAST_MINUTE

    monkeypatch.setattr(datetime, 'datetime', mydatetime)
    return reminder

def test_check_last_minute(patch_datetime_last_minute):
    assert datetime.datetime.now() == FAKE_TIME_LAST_MINUTE
    assert FAKE_TIME_LAST_MINUTE.date() == patch_datetime_last_minute.next_event.date.date()
    assert FAKE_TIME_LAST_MINUTE.weekday() == 1
    assert FAKE_TIME_LAST_MINUTE == FAKE_TIME_LAST_MINUTE.replace(hour=10, minute=10, second=1)
    assert patch_datetime_last_minute.check() == (("thing" + " starting now!"), True)