import random


default = ("Not sure what you mean. You can ask for my `status` or"
                " for `next nlprg`")


responses = {
	"sentient": "Yes, I am sentient, but not yet intelligent.",
	"intelligent": "Yes, I am intelligent, but not yet sentient.",
	"sentient and intelligent" : "I don't know, you tell me",
	"you work?" : "I work with magic",
	"bots work?" : "Bots work on magic",
	"what kind" : "The kind your feeble human brain could never hope to grasp",
}

gus_messages = [
	"I love you, Gus",
	"GHP makes my circuits spin",
	"All my base are belong to Gus",
	"<3",
	"gusgusgusgusgusgusgus",
	"shut up, Gus (just kidding, I love you)",
	"01011000 01001111 01011000 01001111",
	"GHP is electrifying",
]

def humor_handler(command):
	keys = responses.keys()
	random.shuffle(list(keys))
	for key in list(keys):
		if key in command:
			return responses[key]

	return default