
import Hashids
import datetime
import hashlib


class vote:

	def generate_hash(self, username, datetime):
		datestring = datetime.strftime("%A, %d. %B %Y %I:%M%p")
		choices = " ".join(choices)
		hashystring = datestring + username + "four score and seven years ago"
		self.code = hashlib.mb5(hashystring).hexdigest()

class ranked_vote(vote):

	def __init__(self, choices, username,):
		self.choices = choices
		self.down_ballot = 0
		self.top_choice = choices[down_ballot]
		self.code = self.generate_hash(username, datetime.datetime.now())



	def next_choice(self):
		self.down_ballot += 1
		self.top_choice = self.choices[down_ballot]
		return self.top_choice


class simple_vote(vote):

	def __init__(self, choice):
		if type(choice) == int:
			self.choice = choice
		elif type(choice) == str:
			self.choice = int(choice)


class preferential_block_vote(vote):

	def __init__(self, first_votes, ranked)
		self.first_choices = first_votes
		self.ranked_votes = ranked
		self.down_ballot = 0

	def next_choice(self):
		output = self.ranked_votes[self.down_ballot]
		self.down_ballot += 1
		return self.down_ballot


class WrongVoteTypeError(Exception):
	pass


class spartan:

	def __init__(self):
		# 0 is yes, 1 is no. any 1 votes means failure
		self.votes = []

	def add(self, vote)
		if type(vote) != simple_vote:
			raise WrongVoteTypeError("spartan election requires simple vote")
		self.votes.add(vote)

	def count(self):
		for vote in self.votes:
			if vote.choice = 1
			return "no"

		return "yes"



