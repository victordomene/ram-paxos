"""
This module defines the abstract class of a VM. It provides all of
the functionality that is implemented by a specific type of VM. In
Paxos, we will allow some different types of communication, but all of them
must present this interface.

Notice that a single machine may need to use all of the functionality of a
Proposer, Learner or Acceptor. For this reason, these methods are all
accessible.
"""

from abc import abstractmethod

class VM():
	def __init__(self):
		return

	@property
	def messenger(self):
		"""
		The messenger instance of this VM. Ideally this would not need
		to be exposed; however, we must cheat on bootstrap, and we do this
		by exposing the messenger.
		"""
		return self.messenger

	@property
	def proposer(self):
		"""
		The proposer instance of this VM.
		"""
		return self.proposer

	@property
	def acceptor(self):
		"""
		The acceptor instance of this VM.
		"""
		return self.acceptor

	@property
	def learner(self):
		"""
		The learner instance of this VM.
		"""
		return self.learner

	@abstractmethod
	def serve(self):
		"""
		Instantiates a server that will be able to receive requests
		and respond appropriately.
		"""
		return

	@abstractmethod
	def handle_prepare(self):
		"""
		This method should be used exclusively by an Acceptor.

		Responds appropriately to a prepare request. This will send back
		a promise or a refusal of a promise.
		"""
		return

	@abstractmethod
	def handle_accept_request(self):
		"""
		This method should be used exclusively by an Acceptor.

		Responds appropriately to an accept request. This will send Accepted
		requests to the learners (or do nothing if we cannot accept).
		"""
		return

	@abstractmethod
	def handle_promise(self):
		"""
		This method should be used exclusively by a Proposer.

		Responds appropriately to a promise. It must keep track of the promises
		this proposer has seen so far, and if everyone in the quorum accepts,
		it must issue Accept Requests.
		"""
		return

	@abstractmethod
	def handle_refuse_proposal(self):
		"""
		This method should be used exclusively by a Proposer.

		Responds appropriately to a refusal of a promise. This must stop
		the current proposal.
		"""
		return

	@abstractmethod
	def handle_accepted(self):
		"""
		This method should be used exclusively by a Learner.

		Responds appropriately to an accepted request. This must check that
		enough people have accepted this value for this decree, and if so, it 
		must add the decree to a "law book".
		"""
		return
