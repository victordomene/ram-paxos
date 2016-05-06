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
		self.ledger = {}
		return

	@property
	def messenger(self):
		"""
		The messenger instance used by this acceptor.
		"""
		return self.messenger

	def handle_accepted(self, p, n, v, acceptor):
		"""
		Handles the event of an acceptor voting for a proposal.

		@param p: the proposal number in question
		@param n: the decree number in question
		@param v: the value accepted
		@param acceptor: the acceptor who has accepted this value

		Does not return.
		"""
		self.ledger[n] = Proposal(p, n, v)

		return True
