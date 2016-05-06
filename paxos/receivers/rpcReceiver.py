"""
This module provides an implementation of the Receiver class using Google's
RPC Protocol (gRPC).
"""

from grpc.beta import implementations
from receiver import Receiver

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from protobufs import paxos_pb2

TIMEOUT_SECONDS = 10
RECEIVER_DEBUG = True

class grpcReceiver(Receiver):
	def __init__(self, proposer, acceptor, learner):
		self.proposer = proposer
		self.acceptor = acceptor
		self.learner = learner
		self.server = None
		return

	def serve(self, host, port):
		self.server = paxos_pb2.beta_create_VM_server(self)
		self.server.add_insecure_port(host + ":" + str(port))
		self.server.start()

	def stop_server(self):
		self.server.stop(0)

	def handle_prepare(self, request, context):
		p = request.proposal_number
		n = request.decree_number
		proposer = request.proposer

		if RECEIVER_DEBUG:
			print "PrepareRequest received: p = {}, n = {}, proposer = {}".format(p, n, proposer)

		success = self.acceptor.handle_prepare(p, n, proposer)

		return paxos_pb2.OKResponse(response = success)

	def handle_accept_request(self, request, context):
		p = request.proposal_number
		n = request.decree_number
		v = request.value
		proposer = request.proposer

		if RECEIVER_DEBUG:
			print "AcceptRequest received: p = {}, n = {}, v = {}, proposer = {}".format(p, n, v, proposer)

		success = self.acceptor.handle_accept_request(p, n, v, proposer)

		return paxos_pb2.OKResponse(response = success)

	def handle_promise(self, request, context):
		had_previous = request.had_previous

		# handle the case where we had no previous value set
		if had_previous:
			p = request.proposal_number
			v = request.value
		else:
			p = None
			v = None

		n = request.decree_number
		acceptor = request.acceptor

		if RECEIVER_DEBUG:
			print "PromiseRequest received: p = {}, n = {}, highest_voted_value = {}, acceptor = {}".format(p, n, v, acceptor)

		success = self.proposer.handle_promise(p, n, highest_voted_value, acceptor)

		return paxos_pb2.OKResponse(response = success)

	def handle_refuse_promise(self, request, context):
		p = request.proposal_number
		n = request.decree_number
		acceptor = request.acceptor

		if RECEIVER_DEBUG:
			print "RefusePromiseRequest received: p = {}, n = {}, acceptor = {}".format(p, n, acceptor)

		success = self.proposer.handle_refuse_promise(p, n, acceptor)

		return paxos_pb2.OKResponse(response = success)

	def handle_accepted(self, request, context):
		p = request.proposal_number
		n = request.decree_number
		v = request.value
		acceptor = request.acceptor

		if RECEIVER_DEBUG:
			print "AcceptedRequest received: p = {}, n = {}, v = {}, acceptor = {}".format(p, n, v, acceptor)

		success = self.learner.handle_accept_request(p, n, v)

		return paxos_pb2.OKResponse(response = success)
