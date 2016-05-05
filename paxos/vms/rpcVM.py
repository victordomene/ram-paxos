"""
This module provides an implementation of the VM class using Google's
RPC Protocol (gRPC).
"""

# attach the appropriate directories to sys.path
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from grpc.beta import implementations
from messengers import rpcMessenger
from paxos import proposer, acceptor, learner
from vm import VM
from protobufs import paxos_pb2

VM_DEBUG = True

class grpcVM(VM):
	def __init__(self, name):
		# creates a new messenger with a given name; this is the messenger
		# that will be used by Proposer, Acceptor and Learner
		self.messenger = rpcMessenger.grpcMessenger(name)

		# initializes the VM's properties
		self.proposer = proposer.Proposer(self.messenger)
		self.acceptor = acceptor.Acceptor(self.messenger)
		self.learner = learner.Learner(self.messenger)
		return

	def handle_prepare(self, request, context):
		p = request.proposal_number
		n = request.decree_number
		proposer = request.proposer

		if VM_DEBUG:
			print "PrepareRequest received: p = {}, n = {}, proposer = {}".format(p, n, proposer)

		success = self.acceptor.handle_prepare(p, n, proposer)

		return paxos_pb2.OKResponse(response = success)

	def handle_accept_request(self, request, context):
		p = request.proposal_number
		n = request.decree_number
		v = request.value
		proposer = request.proposer

		if VM_DEBUG:
			print "AcceptRequest received: p = {}, n = {}, v = {}, proposer = {}".format(p, n, v, proposer)

		success = self.acceptor.handle_accept_request(p, n, v, proposer)

		return paxos_pb2.OKResponse(response = success)

	def handle_promise(self, request, context):
		p = request.proposal_number
		n = request.decree_number
		highest_voted_value = request.highest_voted_value
		acceptor = request.acceptor

		if VM_DEBUG:
			print "PromiseRequest received: p = {}, n = {}, highest_voted_value = {}, acceptor = {}".format(p, n, highest_voted_value, acceptor)

		success = self.proposer.handle_promise(p, n, highest_voted_value, acceptor)

		return paxos_pb2.OKResponse(response = success)

	def handle_refuse_promise(self, request, context):
		p = request.proposal_number
		n = request.decree_number
		acceptor = request.acceptor

		if VM_DEBUG:
			print "RefusePromiseRequest received: p = {}, n = {}, acceptor = {}".format(p, n, acceptor)

		success = self.proposer.handle_refuse_promise(p, n, acceptor)

		return paxos_pb2.OKResponse(response = success)

	def handle_accepted(self, request, context):
		p = request.proposal_number
		n = request.decree_number
		v = request.value
		acceptor = request.acceptor

		if VM_DEBUG:
			print "AcceptedRequest received: p = {}, n = {}, v = {}, acceptor = {}".format(p, n, v, acceptor)

		success = self.learner.handle_accept_request(p, n, v)

		return paxos_pb2.OKResponse(response = success)
