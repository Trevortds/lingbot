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



def humor_handler(command):
	keys = responses.keys()
	random.shuffle(keys)
	for key in keys:
		if key in command:
			return responses[key]

	return default