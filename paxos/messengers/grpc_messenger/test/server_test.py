"""
This file implements a set of tests for a client that uses the gRPC protocol
defined by paxos.proto.
"""

import time

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from grpc_messenger import paxos_pb2

class VM(paxos_pb2.BetaVMServicer):
	def handle_prepare(self, request, context):
		print "PrepareRequest received: p = {}, n = {}, proposer = {}".format(request.proposal_number, request.decree_number, request.proposer)
		return paxos_pb2.OKResponse(response=True)

	def handle_accept_request(self, request, context):
		print "AcceptRequest received: p = {}, n = {}, v = {}, proposer = {}".format(request.proposal_number, request.decree_number, request.value, request.proposer)
		return paxos_pb2.OKResponse(response=True)

	def handle_promise(self, request, context):
		print "PromiseRequest received: p = {}, n = {}, highest_voted_value = {}".format(request.proposal_number, request.decree_number, request.highest_voted_value)
		return paxos_pb2.OKResponse(response=True)

	def handle_refuse_promise(self, request, context):
		print "RefuseRequest received: p = {}, n = {}".format(request.proposal_number, request.decree_number)
		return paxos_pb2.OKResponse(response=True)

	def handle_accepted(self, request, context):
		print "AcceptedRequest received: p = {}, n = {}, v = {}".format(request.proposal_number, request.decree_number, request.value)
		return paxos_pb2.OKResponse(response=True)

def run():
	server = paxos_pb2.beta_create_VM_server(VM())
	server.add_insecure_port("localhost:6666")
	server.start()

	try:
		while True:
			time.sleep(600)
			print "Woke up!"
	except KeyboardInterrupt:
		server.stop(0)

if __name__ == "__main__":
	run()
