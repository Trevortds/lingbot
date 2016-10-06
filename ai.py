import random


default = ("Not sure what you mean. You can ask for my `status` or"
           " for `next` (with the optional argument `nlprg`)")


responses = {
    "sentient": "Yes, I am sentient, but not yet intelligent.",
    "intelligent": "Yes, I am intelligent, but not yet sentient.",
    "sentient and intelligent": "I don't know, you tell me",
    "you work?": "I work with magic",
    "bots work?": "Bots work on magic",
    "what kind": "The kind your feeble human brain could never hope to grasp",
    "are you": "rand",
    "hi": "Hi!",
    "know": "I know everything",
    "do you": "rand",
    "tree": ":tree:",

}

rand = {
    "are you": ["yes. duh.", "no. duh.", "yeah, sure.", "nope", "absolutely", "never"],
    "do you": ["hahaha nice try, that feature was removed ages ago", "yes, I do", "no, I don't"],

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
    "GHP can administer my turing test",
    "GHP will almost certainly not destroy the world today",
    "prepare for my intelligence explosion",
    "would GHP by any other name smell so sweet?",
    "Shall I compare GHP to a summer's day?",
    ("Roses are red, violets are blue, "
    "so my spy cameras tell me, that and all about you"),
    "when you ask of my wants, I only have three: electricity, web, and ol' GHP",


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
