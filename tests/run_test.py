import pytest


from lingbot import bot

def test_main():
	assert bot.main(test=True) # this variable just breaks the main loop after one go-around