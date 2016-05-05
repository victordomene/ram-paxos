"""
This module defines the abstract class of a messenger. It provides all of
the functionality that is implemented by a specific type of messenger. In
Paxos, we will allow some different types of communication, but all of them
must present this interface.

Notice that a single machine may need to use all of the functionality of a
Proposer, Learner or Acceptor. For this reason, these methods are all
accessible.
"""

from abc import abstractmethod

class Messenger():
	def __init__(self):
		return

	@abstractmethod
	def send_prepare(self):
		"""
		This method should be used exclusively by a Proposer.

		Sends a prepare message for everyone who is in a given quorum. This
		message will contain simply the number of the proposal and the number
		of the decree that is being voted.

		@param p: the proposal number in question
		@param n: the decree number in question
		@param quorum: the quorum to which message will be sent

		@return True if message is sent; False otherwise """
		return

	@abstractmethod
	def send_accept_request(self):
		"""
		This method should be used exclusively by a Proposer.

		Sends an accept request for everyone who is in a given quorum. This
		should be called after a proposer sees a majority of promises (say, if
		everybody in the quorum made the promise).

		@param p: the proposal number in question
		@param n: the decree number in question
		@param v: the value proposed
		@param quorum: the quorum to which message will be sent

		@return True if message is sent; False otherwise
		"""
		return

	@abstractmethod
	def send_promise(self):
		"""
		This method should be used exclusively by an Acceptor.

		Sends a promise back to the proposer, which guarantees that this
		acceptor will not accept any proposals with number less than some
		number. Also sends back the value for the highest numbered proposal for
		which this acceptor has responded.

		@param p: the proposal number in question
		@param n: the decree number in question
		@param v: the value of the highest-numbered proposal voted
		@param proposer: the proposer to whom the message will be sent

		@return True if message is sent; False otherwise
		"""
		return

	@abstractmethod
	def send_refuse_proposal(self):
		"""
		This method should be used exclusively by an Acceptor.

		Sends a message to the proposer saying that this acceptor will not
		accept this proposal (probably, because it has already taken a promise
		for a higher-number proposal).

		@param p: the proposal number in question
		@param n: the decree number in question
		@param proposer: the proposal to whom the message will be sent

		@return True if message is sent; False otherwise
		"""
		return

	@abstractmethod
	def send_accepted(self):
		"""
		This method should be used exclusively by an Acceptor.

		Sends a message to a set of learners saying that a given proposal has
		been accepted by this acceptor.

		@param p: the proposal number in question
		@param n: the decree number in question
		@param v: the value accepted
		@param learners: the set of learners to which the message will be sent

		@return True if message is sent; False otherwise
		"""
		return
