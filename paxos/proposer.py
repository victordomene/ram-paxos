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
		self.highest_proposal = None
		self.promised_acceptors = set()

		# how to initialize this?
		self.quorum_size = None
		return

	@property
	def messenger(self):
		"""
		The messenger instance used by this acceptor.
		"""
		return self.messenger

	@property
	def quorum_size(self):
		"""
		The size of a quorum.
		"""
		return self.quorum_size

	@property
	def promised_acceptors(self):
		"""
		A set of acceptors who have promised to us.
		"""
		return self.promised_acceptors

	@property
	def current_proposal(self):
		"""
		The current proposal that we are trying to pass.
		"""
		return self.current_proposal

	@property
	def highest_proposal(self):
		"""
		The highest proposal that was received within the promises.
		"""
		return self.current_proposal

	def prepare(self, p, n, quorum):
		"""
		Wrapper on the messenger: simply sends a prepare message for the
		current proposal to a quorum.

		@param p: the proposal number in question
		@param n: the decree number in question
		@param quorum: the quorum to which the prepare will be sent

		@return True if message is sent successfully; False otherwise
		"""

		# simply sends the RPC call
		self.messenger.send_prepare(p, n, quorum)
		return True

	def _check_promise_count(self):
		if len(self.promised_acceptors) >= self.quorum_size:
			# fetch the information that will be passed to acceptors
			p = self.current_proposal.number
			n = self.current_proposal.decree

			# the value must be the value corresponding to the highest-numbered
			# proposal we have seen in the quorum
			v = self.highest_proposal.value

			# v could be None, if there was no previous value assigned to
			# this decree by any acceptor. In that case, we may propose
			# whatever we initially wanted to propose
			if v is None:
				v = self.current_proposal.value

			# send accept requests to a quorum
			self.messenger.send_accept_request(p, n, v, self.quorum)

	def handle_promise(self, had_previous, p, n, v, acceptor):
		"""
		Handles a promise given by an acceptor. This must check the @param v
		(see below) and update our current proposal accordingly: the proposer
		is only allowed to propose the highest value received in the quorum
		(or anything, if no such value exists).

		This must also check if enough acceptors have responded, and if so,
		start the accept part of the algorithm.

		@param p: the highest-numbered proposal accepted by this acceptor in the past.
		This may be None.
		@param n: the decree number corresponding to the promise (and to @param p)
		@param v: the value corresponding to @param p. This may be None.
		@param acceptor: the acceptor that responded with a promise

		@return XXX
		"""

		# we must have a current proposal set in order to handle this request
		if self.current_proposal is None:
			return False

		# check if the message refers to the current proposal decree; if it
		# does not, we have nothing to do.
		if n != self.current_proposal.decree:
			return False

		# if we had a previous proposal, update our highest_proposal accordingly
		if p is not None:
			assert(v is not None)

			# we may need to initiate the highest proposal here
			if self.highest_proposal is None:
				self.highest_proposal = Proposal()

			# update the value of the proposal according to the rules. Notice here
			# that p could be None
			if p > self.highest_proposal.number:
				self.highest_proposal.value = v
				self.highest_proposal.number = p
				self.highest_proposal.decree = n

		# update promised_acceptors and check whether we have enough
		self.promised_acceptors.add(acceptor)
		self._check_promise_count()

		return True

	def handle_refuse_promise(self, p, n, acceptor):
		"""
		Handles a refusal of a promise given by an acceptor. In case this
		is received, we must stop working on the current proposal, since
		it will not be accepted anyway.

		@param p: the proposal number corresponding to the promise
		@param n: the decree number corresponding to the promise
		@param acceptor: the acceptor that responded with a promise

		@return XXX
		"""

		# reset the state kept by proposer
		self.current_proposal = None
		self.highest_proposal = None
		self.promised_acceptors = set()

		return True
