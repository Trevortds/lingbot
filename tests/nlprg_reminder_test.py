import pytest
from lingbot.features import nlprg_schedule_reader
import datetime
import bs4

FAKE_TIME_FAIL = datetime.datetime(2017, 10, 6, 12, 0, 0)
FAKE_TIME_MORNING = datetime.datetime(2017, 10, 6, 10, 0, 0)
FAKE_TIME_LAST_MINUTE = datetime.datetime(2017, 10, 6, 13, 45, 0)
FAKE_TIME_RESET = datetime.datetime(2017, 10, 6, 15, 0, 0)
DATE_GENERATOR = lambda y, m, d: datetime.date(y, m, d)

config = {
"active": True,
"url": "https://raw.githubusercontent.com/wiki/clulab/nlp-reading-group/Fall-2017-Reading-Schedule.md",
"time": 10
"room": "Gould-Simpson 906"
}


def test_constructor():
    reminder = nlprg_schedule_reader.Reminder(config)

@pytest.fixture
def patch_datetime_now_fail(monkeypatch):
    reminder = nlprg_schedule_reader.Reminder(config)

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
        def __init__(self, y, m, d, h):
            self = DATE_GENERATOR(y,m,d)
        @classmethod
        def now(cls):
            return FAKE_TIME_MORNING
        @classmethod
        def today(cls):
            return FAKE_TIME_MORNING

    # class myBeautifulSoup:
    #     def __init__(self, thing, otherthing):
    #         return open("resources/Fall-2017-Reading-Schedule.md", "r").read()

    monkeypatch.setattr(datetime, 'datetime', mydatetime)
    # monkeypatch.setattr(bs4, 'BeautifulSopu', myBeautifulSoup)
    reminder = nlprg_schedule_reader.Reminder(config)
    return reminder

def test_check_morning(patch_datetime_morning):
    assert datetime.datetime.now() == FAKE_TIME_MORNING
    assert FAKE_TIME_MORNING.date() == patch_datetime_morning.next_nlprg.date.date()
    assert FAKE_TIME_MORNING.weekday() == 4
    assert FAKE_TIME_MORNING == FAKE_TIME_MORNING.replace(hour=10, minute=0, second=0)
    assert patch_datetime_morning.check() == (("NLP Reading Group today! \n" + "Rebecca" +
                            " presenting on\n " + "Deep Learning for NLP Best Practices\nLink: http://ruder.io/deep-learning-nlp-best-practices/?utm_campaign=Artificial%2BIntelligence%2BWeekly&amp;utm_medium=email&amp;utm_source=Artificial_Intelligence_Weekly_66\n" +
                            "\n\n Join us in Gould-Simpson 906 at 1400\n\n" +
                            "(food and coffee provided)\n\nSee full schedule here: " +
                            "https://github.com/clulab/nlp-reading-group/wiki/FALL" +
                            "-2017-Reading-Schedule"), True)

@pytest.fixture
def patch_datetime_last_minute(monkeypatch):

    class mydatetime(datetime.datetime):
        def __init__(self, y, m, d, h):
            self = DATE_GENERATOR(y,m,d)
        @classmethod
        def now(cls):
            return FAKE_TIME_LAST_MINUTE
        @classmethod
        def today(cls):
            return FAKE_TIME_LAST_MINUTE

    # class myBeautifulSoup:
    #     def __init__(self, thing, otherthing):
    #         return open("resources/Fall-2017-Reading-Schedule.md", "r").read()

    monkeypatch.setattr(datetime, 'datetime', mydatetime)
    # monkeypatch.setattr(bs4, 'BeautifulSopu', myBeautifulSoup)
    reminder = nlprg_schedule_reader.Reminder(config)
    return reminder

def test_check_last_minute(patch_datetime_last_minute):
    assert datetime.datetime.now() == FAKE_TIME_LAST_MINUTE
    assert FAKE_TIME_LAST_MINUTE.date() == patch_datetime_last_minute.next_nlprg.date.date()
    assert FAKE_TIME_LAST_MINUTE.weekday() == 4
    assert FAKE_TIME_LAST_MINUTE == FAKE_TIME_LAST_MINUTE.replace(hour=13, minute=45, second=0)
    assert patch_datetime_last_minute.check() == (("NLP Reading Group happening NOW! :book: Gould-Simpson 906"
                            "\n(food and coffee provided, like for free, so come)\n\n"
                            ""), True)
