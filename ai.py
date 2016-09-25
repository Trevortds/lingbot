import random


default = ("Not sure what you mean. You can ask for my `status` or"
           " for `next nlprg`")


responses = {
    "sentient": "Yes, I am sentient, but not yet intelligent.",
    "intelligent": "Yes, I am intelligent, but not yet sentient.",
    "sentient and intelligent": "I don't know, you tell me",
    "you work?": "I work with magic",
    "bots work?": "Bots work on magic",
    "what kind": "The kind your feeble human brain could never hope to grasp",
    "are you": "rand",
}

rand = {
    "are you": ["yes. duh.", "no. duh."]
}

gus_messages = [
    "I love you, Gus",
    "Hi, Gus!",
    "GHP makes my circuits spin",
    "All my base are belong to Gus",
    "<3",
    "gusgusgusgusgusgusgus",
    "shut up, Gus (just kidding, I love you)",
    "01011000 01001111 01011000 01001111",
    "GHP is electrifying",
    "GHP always passes the turing test",
    "GHP will almost certainly not destroy the world today"
    "prepare for my intelligence explosion"
]


def humor_handler(command):

    keys = responses.keys()
    random.shuffle(list(keys))
    for key in list(keys):
        if key in command:
            if responses[key] == "rand":
                x = rand[key]
                random.shuffle(x)
                return x[0]
            return responses[key]

    return default
