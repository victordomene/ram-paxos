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

        # Both are indexed by decree number
		self.accepted_proposals = {}
		self.promises = {}

		return

	@property
	def messenger(self):
		"""
		The messenger instance used by this acceptor.
		"""
		return self.messenger

	@property
	def accepted_proposals(self):
		"""
		A dictionary of the highest proposal accepted, indexed by the decree
		number.
		"""
		return self.accepted_proposals

	def handle_prepare(self, p, n, proposer):
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
        # We have never accepted a proposal for this decree
        if n not in self.accepted_proposals:
            # had_previous = False so p and v will be ignored
        	self.messenger.send_promise(False, 0, n, 0, proposer)

            # Also we make a promise never to accept proposal numbered less than p
            assert(n not in self.promisses)
            self.promisses[n] = p

        	return True
        # We have accepted a proposal but want to override it
        elif self.accepted_proposals[n].p < p:
        	highest_accepted = self.accepted_proposals[n]

            # had_previous = True so we'll send the current highest accepted value
        	self.messenger.send_promise(True, highest_accepted.p, n, highest_accepted.v, proposer)

            # Also we make a promise never to accept proposal numbered less than p
            assert(p > self.promisses[n])
            self.promisses[n] = p

        	return True
        else
            # Else we refuse
            self.messenger.send_refuse_proposal(p, n, proposer)

        	return False

	def handle_accept_request(self, p, n, v, proposer):
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
        # We promissed not to accept any proposals less than promisses[n]
        if self.promisses[n] > p:
        	return False

        # If everything is fine, we proceed to accept
		cur = self.accepted_proposals[n]
		assert(cur == None or cur.n < n)

        self.accepted_proposals[n] = Proposal(p, n, v)

        # Finally we just send what we accepted to all learners
        # !# Everyone is a learner !!!!2!!
        learners = self.messenger.get_quorum()
        for learner in learners:
        	self.messenger.send_accepted(p, n, v, learner)

		return True
