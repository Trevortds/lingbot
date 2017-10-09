import pytest 

from lingbot import passive_feats
from slackclient import SlackClient
import os

def test_constructor():
    try:
        with open("api.txt", 'r') as f:
            api_token = f.readline()[:-1]
    except FileNotFoundError:
        api_token = os.environ['SLACK_TOKEN']

    if api_token == "":
        print("NO API TOKEN FOUND")
        sys.exit(1)

    passive = passive_feats.Passive(SlackClient(api_token), {"features" : {"passive": {"hackyHourReminder": {"active": True, "location": "Pasco", "time": 16}}}})