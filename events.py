from datetime import datetime
import re

class CalendarEvent(object):
    """
    A timestamped event with a description
    """
    NLP_RG = "NLPRG"
    HACKY_HOUR = "HH"
    date_formatter = "%x (%A) @ %X"
    def __init__(self, title, kind, date, description):
        self.title = title
        self.kind = kind
        self.date = date
        # string representation of date
        self.date_str = self.date.strftime(CalendarEvent.date_formatter)
        self.summary = "\"{title}\"\n{time}!\nDescription: {about}".format(
                       title=self.title,
                       time=self.date_str,
                       about=description
                       )
    def __str__(self): return self.summary

    def __gt__(self, other):
        return other.date < self.date
    def __ge__(self, other):
        return other.date <= self.date
    def __lt__(self, other):
        return self.date < other.date
    def __le__(self, other):
        return self.date <= other.date

class Calendar(object):
    """
    Collection of events.
    TODO: add convenience methods for sorting/filtering events.
    """
    def __init__(self, events):
        self.events = sorted(events, key=lambda e: e.date)
    def following(self, other):
        if isinstance(other, datetime):
            candidates = [e for e in self.events if e.date > other]
        elif isinstance(other, CalendarEvent):
            candidates = [e for e in self.events if e > other]
        else:
            candidates = None
        return candidates

    def preceding(self, other):
        if isinstance(other, datetime):
            candidates = [e for e in self.events if e.date < other]
        elif isinstance(other, CalendarEvent):
            candidates = [e for e in self.events if e < other]
        else:
            candidates = None
        return candidates


class Patterns(object):
    HACKY_HOUR = re.compile(r"hacky[\-\s]?hour", re.IGNORECASE)
    NLP_RG = re.compile(r"nlprg|nlp reading group", re.IGNORECASE)

class Handler(object):
    '''
    All Handlers should have a respond method.
    '''
    def __init__(self):
        pass
    def respond():
        return ""
    @staticmethod
    def normalize_query(query):
        """
        Apply transformations on query to standardize
        """
        # TODO: remove @lingbot and punctuation?
        s0 = " ".join([term.lower() for term in query])
        s1 = re.sub(Patterns.HACKY_HOUR, CalendarEvent.HACKY_HOUR, s0)
        s2 = re.sub(Patterns.NLP_RG, CalendarEvent.NLP_RG, s1)
        return s2.split()

class EventQueryHandler(Handler):
    """
    Responds to queries concerning upcoming events.
    """
    NEXT = "next"
    PREVIOUS = "previous"
    ERROR_MSG = "No upcoming events matching that query"

    def __init__(self, calendar):
        self.calendar = calendar

    def respond(self, query):
        # get all future events
        now = datetime.now()
        # filter events based on left to right reading of query
        def parse_query(query, current):
            candidates = self.calendar.events
            #print("initial candidates: {}".format([e.title for e in candidates]))
            for q in query:
                if q == CalendarEvent.NLP_RG:
                    candidates = [e for e in candidates if e.kind == CalendarEvent.NLP_RG]
                # look forward in time
                elif q == EventQueryHandler.NEXT:
                    candidates = [e for e in candidates if e.date > current]
                    current = candidates[0].date if len(candidates) > 0 else current
                # look backward in time
                elif q == EventQueryHandler.PREVIOUS:
                    candidates = [e for e in candidates if e.date < current]
                    current = candidates[-1].date if len(candidates) > 0 else current
            #print("candidates: {}".format([e.title for e in candidates]))
            if len(candidates) == 0:
                return None
            return candidates[0]

        normalized_query = Handler.normalize_query(query)
        result = parse_query(normalized_query, now)
        response = ""
        if result == None:
            response = EventQueryHandler.ERROR_MSG
        else:
            response = result.summary
        return response

def demo_eqh():
    event0 = CalendarEvent(
        title="Out in vector space",
        kind=CalendarEvent.NLP_RG,
        date=datetime(2017, 1, 13, 15, 0, 0,0),
        description="blah blah blah"
        )
    event1 = CalendarEvent(
        title="Far out in vector space",
        kind=CalendarEvent.NLP_RG,
        date=datetime(2017, 1, 20, 15, 0, 0,0),
        description="blah blah blah"
        )
    event2 = CalendarEvent(
         title="Really far out in vector space",
         kind=CalendarEvent.NLP_RG,
         date=datetime(2017, 1, 27, 15, 0, 0,0),
         description="blah blah blah"
         )
    calendar = Calendar([event0, event1, event2])
    print("events: {}".format(["{}: {}".format(e.title, e.date_str) for e in calendar.events]))
    eqh = EventQueryHandler(calendar)
    answer_key = {
        "next":event1.summary,
        "next_nlprg":event1.summary,
        "previous": event0.summary,
        "previous_nlprg":event0.summary,
        "next_next":event2.summary,
        "nlprg_next":event1.summary,
        "nlprg_next_next":event2.summary,
    }
    queries = [
               ["next"], # should produce event1
               ["next", "nlprg"], # should produce event1
               ["next", "next"], # should produce event2
               ["nlprg", "next"], # should produce event1
               ["nlprg", "next", "next"], # should produce event2
               ["next", "next", "next"], # should produce nothing
               ["previous"], # should produce event0
               ["previous", "nlprg"], # should produce event0
              ]
    for q in queries:
        response = eqh.respond(q)
        print("{} -> {}".format(q, response))
        key = "_".join(q)
        correct_response = answer_key.get(key, EventQueryHandler.ERROR_MSG)
        if response == correct_response:
            print("\tCorrect!")
        else:
            print("\tIncorrect!")

if __name__ == "__main__":
    demo_eqh()
    # TODO: "nlprg following the next hacky hour" ->
    # step 1: identify event types:
    #    ["NLPRG_EVENT", "following", "the", "next", "HH_EVENT"]
    # def get_next_event(current_state: Date, filter: EventType): Event
    # step 2: parse natural language to create AST
    # get_next_event(current_state=get_next_event(current_state=CURRENT_TIME_AS_EVENT, filter=hack_hour), filter=hacky_hour)

