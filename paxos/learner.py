"""
This module implements a learner, using the specified messenger.
"""

from proposal import Proposal

class Learner():
	"""
	Implementation of a Paxon learner.

	@param messenger: the messenger instance that will be used
	"""

	def __init__(self, messenger):
		self.messenger = messenger
		self.decree_to_value = {}
		self.proposal_and_decree_to_stats = {}
		return

	@property
	def messenger(self):
		"""
		The messenger instance used by this acceptor.
		"""
		return self.messenger

	@property
	def decree_to_value(self):
		"""
		The current state of the "law book", as seen from this learner's
		perspective. It is simply a dictionary that maps decree numbers to
		the values that were accepted.
		"""
		return self.decree_to_value

	@property
	def proposal_and_decree_to_stats(self):
		"""
		A dictionary that maps a tuple of (proposal number, decree number) to
		the statistics regarding that proposal number: how many acceptors
		voted for it and how many did not vote yet.

		This will be used, later, to verify whether a value has been agreed
		upon for this decree.
		"""
		return self.proposal_and_decree_to_stats

	def handle_accepted(self):
		"""
		Handles the event of an acceptor voting for a proposal.

		@param p: the proposal number in question
		@param n: the decree number in question
		@param v: the value accepted
		@param acceptor: the acceptor to whom this event refers

		Does not return.
		"""
		return
