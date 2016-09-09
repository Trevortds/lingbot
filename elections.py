
import Hashids
import datetime

class ranked_vote:

	def __init__(self, choices, username,):
		self.choices = choices
		self.down_ballot = 0
		self.top_choice = choices[down_ballot]
		self.code = self.generate_hash(username, choices, datetime.datetime.now())



	def next_choice(self):
		self.down_ballot += 1
		self.top_choice = self.choices[down_ballot]
		return self.top_choice

	def generate_hash(self, username, choices, datetime):
		hashids = Hashids(salt="four score and seven years ago our forefathers brought fourth on this continent a great nation, concieved in liberty, and dedicated to the proposition that all men are created equal")
		

class simple_vote:

	def __init__(self, choice):
		self.choice = choice


class preferential_block_vote:

	def __init__(self, first_votes, ranked)
		self.first_choices = first_votes
		self.ranked_votes = ranked
		self.down_ballot = 0

	def next_choice(self):
		output = self.ranked_votes[self.down_ballot]
		self.down_ballot += 1
		return self.down_ballot



class spartan:

	def __init__(self):
		# 0 is yes, 1 is no. any 1 votes means failure
