import pytest 

from lingbot import passive_feats

def test_constructor():
    passive = passive_feats.Passive({"hackyHourReminder": {"active": True, "location": "Pasco", "time": 16}})