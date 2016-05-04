"""
This module implements an acceptor, using the specified messenger.
"""

from proposal import Proposal

class Acceptor():
	"""
	Implementation of a Paxon acceptor. Using some optimizations, we need to
	keep track of (only) the highest proposal accepted by this acceptor for
	every decree that we have voted on (both its number and its value). We do
	this by keeping a dictionary that maps decrees to Proposal objects.

	@param messenger: the messenger instance that will be used
	"""

	def __init__(self, messenger):
		self.messenger = messenger
		self.decree_to_highest_proposal = {}
		return

	@property
	def messenger(self):
		"""
		The messenger instance used by this acceptor.
		"""
		return self.messenger

	@property
	def decree_to_highest_proposal(self):
		"""
		A dictionary of the highest proposal accepted, indexed by the decree
		number.
		"""
		return self.decree_to_highest_proposal

	def handle_prepare(self):
		"""
		Handles a prepare request that has been received. This will succeed if
		the proposal number is higher than any other prepare request that we
		have already responded to. In case of success, this must promise the
		proposer that we will not accept any other proposal with lower number
		than this one.

		@param p: the proposal number in question
		@param n: the decree number in question
		@param proposer: the proposer to whom we must respond

		@return True if promise is made; False otherwise
		"""
		return

	def handle_accept(self):
		"""
		Handles an accept request that has been received. This will always
		succeed, unless we promised a proposal with a higher number that we
		would not do so.

		@param p: the proposal number in question
		@param n: the decree number in question
		@param v: the value proposed
		@param proposer: the proposer to whom we must respond

		@return True if accepted; False otherwise
		"""
		return
