"""
This module implements a proposer, using the specified messenger.
"""

from proposal import Proposal

class Proposer():
	"""
	Implementation of a Paxon proposer.

	@param messenger: the messenger instance that will be used
	"""

	def __init__(self, messenger):
		self.messenger = messenger
		self.current_proposal = None
		return

	@property
	def messenger(self):
		"""
		The messenger instance used by this acceptor.
		"""
		return self.messenger

	@property
	def current_proposal(self):
		"""
		The current proposal that we are trying to pass.
		"""
		return self.current_proposal

	def prepare(self):
		"""
		Wrapper on the messenger: simply sends a prepare message for the
		current proposal to a quorum.

		@param p: the proposal number in question
		@param n: the decree number in question
		@param quorum: the quorum to which the prepare will be sent

		@return True if message is sent successfully; False otherwise
		"""
		return

	def handle_promise(self):
		"""
		Handles a promise given by an acceptor. This must check the @param v
		(see below) and update our current proposal accordingly: the proposer
		is only allowed to propose the highest value received in the quorum
		(or anything, if no such value exists).

		This must also check if enough acceptors have responded, and if so,
		start the accept part of the algorithm.

		@param p: the proposal number corresponding to the promise
		@param n: the decree number corresponding to the promise
		@param v: the highest value accepted by this acceptor in the past
		@param acceptor: the acceptor that responded with a promise

		Does not return.
		"""
		return
