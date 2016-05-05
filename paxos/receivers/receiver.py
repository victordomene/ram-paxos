"""
This module defines the abstract class of a receiver. It provides all of
the functionality that is implemented by a specific type of receiver. In
Paxos, we will allow some different types of communication, but all of them
must present this interface.

Notice that a single machine may need to use all of the functionality of a
Proposer, Learner or Acceptor. For this reason, these methods are all
accessible.
"""

from abc import abstractmethod

class Receiver():
	def __init__(self):
		return

	@abstractmethod
	def serve(self):
		"""
		Starts an instance of the server defined by Receiver.

		@param host: the host in which server will run
		@param port: the port in the given host
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
