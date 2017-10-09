import pytest
from lingbot.features import hacky_hour_reminder
import datetime

FAKE_TIME_SUCCESS = datetime.datetime(2017, 10, 5, 13, 0, 0)
FAKE_TIME_FAIL = datetime.datetime(2017, 10, 5, 12, 0, 0)


def test_constructor():
    reminder = hacky_hour_reminder.Reminder({"active": True, "location": "Pasco",  "time": 16})

@pytest.fixture
def patch_datetime_now_fail(monkeypatch):

    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME_FAIL

    monkeypatch.setattr(datetime, 'datetime', mydatetime)


def test_check_negative(patch_datetime_now_fail):
    reminder = hacky_hour_reminder.Reminder({"active": True, "location": "Pasco",  "time": 16})
    assert reminder.check() is None

@pytest.fixture
def patch_datetime_now(monkeypatch):

    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME_SUCCESS

    monkeypatch.setattr(datetime, 'datetime', mydatetime)

def test_check_positive(patch_datetime_now):
    reminder = hacky_hour_reminder.Reminder({"active": True, "location": "Pasco",  "time": 16})
    assert datetime.datetime.now() == FAKE_TIME_SUCCESS
    assert FAKE_TIME_SUCCESS.weekday() == 3
    assert FAKE_TIME_SUCCESS == FAKE_TIME_SUCCESS.replace(hour=13, minute=0, second=0)
    assert reminder.check() == (("Hacky Hour today, at Pasco, starting at 16! "
                            "Come, have a drink, talk to smart people, have fun!"
                            " :beers:"), True)