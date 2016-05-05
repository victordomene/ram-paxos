"""
This module provides an implementation of the Messenger class using Google's
RPC Protocol (gRPC).
"""

from grpc.beta import implementations
from messenger import Messenger

import paxos_pb2

TIMEOUT_SECONDS = 10

class grpcMessenger(Messenger):
	def __init__(self, name):
		self.name = name
		self.destinations = {}
		return

	@property
	def name(self):
		"""
		The name through which this machine is recognized in the network.
		"""
		return self.name

	@property
	def destinations(self):
		"""
		A dictionary that maps names of machines to a stub corresponding
		to the machine we want to communicate to.
		"""
		return self.destinations

	def _fetch_stub(self, name):
		# fetch the stub for the proposer
		try:
			stub = self.destinations[name]
		except KeyError:
			print "send_promise: could not find stub for {}".format(name)
			return None
		except:
			print "send_promise: unknown error"
			return None

		return stub

	def add_destination(self, name, host, port):
		"""
		Adds a host/port combination to the list of possible destinations
		for messages. Basically, this tells our messenger where each machine
		can be found. It will store the host/port combination in a dictionary
		indexed by the given name.

		If a name already exists in the dictionary, this function will update
		the information for the name.

		@param name: the name given to this host/port combination
		@param host: the host to be added
		@param port: the port used in that host

		@return True if successfully added; False otherwise
		"""

		# uses gRPC to create a channel and a stub
		channel = implementations.insecure_channel(host, port)
		stub = paxos_pb2.beta_create_VM_stub(channel)

		# simply change the entry; do not check if it already exists
		self.destinations[name] = stub

		# function always succeeds
		return True

	def send_prepare(self, p, n, quorum):
		for acceptor in quorum:
			# fetch the stub for each of the acceptors
			stub = self._fetch_stub(acceptor)

			if stub is None:
				return False

			# create the appropriate request
			request = paxos_pb2.PrepareRequest(proposal_number = p,
					decree_number = n, proposer = self.name)

			# finally send message to this acceptor
			response = stub.handle_prepare(request, TIMEOUT_SECONDS)

		return True

	def send_accept_request(self, p, n, v, quorum):
		for acceptor in quorum:
			# fetch the stub for each of the acceptors
			stub = self._fetch_stub(acceptor)

			if stub is None:
				return False

			# create the appropriate request
			request = paxos_pb2.AcceptRequest(proposal_number = p,
					decree_number = n, value = v, proposer = self.name)

			# finally send message to this acceptor
			response = stub.handle_accept_request(request, TIMEOUT_SECONDS)

		return True

	def send_promise(self, p, n, v, proposer):
		# fetch the stub for the proposer
		stub = self._fetch_stub(proposer)

		if stub is None:
			return False

		# create the appropriate request
		request = paxos_pb2.PromiseRequest(proposal_number = p,
				decree_number = n, highest_voted_value = v)

		# finally send promise back to proposer
		response = stub.handle_promise(request, TIMEOUT_SECONDS)

		return True

	def send_refuse_proposal(self, p, n, proposer):
		# fetch the stub for the proposer
		stub = self._fetch_stub(proposer)

		if stub is None:
			return False

		# create the appropriate request
		request = paxos_pb2.RefusePromiseRequest(proposal_number = p,
				decree_number = n)

		# finally send refusal back to proposer
		response = stub.handle_refuse_promise(request, TIMEOUT_SECONDS)

		return True

	def send_accepted(self, p, n, v, learner):
		# fetch the stub for the learner
		stub = self._fetch_stub(learner)

		if stub is None:
			return False

		# create the appropriate request
		request = paxos_pb2.AcceptedRequest(proposal_number = p,
				decree_number = n, value = v)

		# finally send message to learner
		response = stub.handle_accepted(request, TIMEOUT_SECONDS)

		return True
