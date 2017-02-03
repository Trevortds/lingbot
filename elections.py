
import Hashids
import datetime
import hashlib



# TODO implement hashes-add-to-total thing


# Types of votes, each has a hash, this is how you confirm that your vote was counted. 

class vote:

	# vote abstract class. implements hashing method for all votes. Contains informatin about the 
	# user and the date, but not the vote value
	def generate_hash(self, username, datetime):
		datestring = datetime.strftime("%A, %d. %B %Y %I:%M%p")
		choices = " ".join(choices)
		hashystring = datestring + username + "four score and seven years ago"
		self.code = hashlib.mb5(hashystring).hexdigest()

class ranked_vote(vote):

	def __init__(self, choices, username, datetime):
		self.choices = choices
		self.down_ballot = 0
		self.top_choice = choices[down_ballot]
		self.code = self.generate_hash(username, datetime.datetime.now())



	def next_choice(self):
		self.down_ballot += 1
		self.top_choice = self.choices[down_ballot]
		return self.top_choice



class simple_vote(vote):

	def __init__(self, choice, username, datetime):
		if type(choice) == int:
			self.choice = choice
		elif type(choice) == str:
			self.choice = int(choice)

		self.generate_hash(username, datetime)


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
	# takes simplevotes, choices are either 0 or 1, 1 being a "no" vote

	def __init__(self):
		# 0 is yes, 1 is no. any 1 votes means failure
		self.votes = []

	def add(self, vote)
		if type(vote) != simple_vote:
			raise WrongVoteTypeError("spartan election requires simple vote")
		self.votes.add(vote)

	def count(self):
		for vote in self.votes:
			if vote.choice == 1:
				return "no"

		return "yes"


class fptp:


	def __init__(self, candidates):
		self.candidates = list()
		for candidate in candidates:

			self.candidates.add(candidate.lower())

		self.tally = [0]*len(candidates)


	def add(self, vote)
		if type(vote) != simple_vote:
			raise (WrongVoteTypeError("FTPT election requires simple vote!"))

		self.tally[vote.choice] += 1

	def count(self, winner_only = True):
		if winner_only:
			return self.candidates[self.tally.indexof(max(self.tally))]
		else:
			return zip(self.candidates, self.tally)
