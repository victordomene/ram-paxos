"""
This module provides an implementation of the Receiver class using Google's
RPC Protocol (gRPC).

For the specific documentation of the arguments these methods take and 
what they do at a high level, refer to receiver.py.
"""

from grpc.beta import implementations
from receiver import Receiver

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from protobufs import paxos_pb2

TIMEOUT_SECONDS = 10
RECEIVER_DEBUG = False 

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

        return paxos_pb2.OKResponse(response = True)

    def handle_accept(self, request, context):
        p = request.proposal_number
        n = request.decree_number
        v = request.value
        proposer = request.proposer

        if RECEIVER_DEBUG:
            print "AcceptRequest received: p = {}, n = {}, v = {}, proposer = {}".format(p, n, v, proposer)

        success = self.acceptor.handle_accept(p, n, v, proposer)

        return paxos_pb2.OKResponse(response = True)

    def handle_promise(self, request, context):
        had_previous = request.had_previous

        # handle the case where we had no previous value set
        if had_previous:
            p = request.proposal_number
            proposer = request.proposer
            v = request.value
        else:
            p = None
            proposer = None
            v = None

        n = request.decree_number
        acceptor = request.acceptor

        if RECEIVER_DEBUG:
            print "PromiseRequest received: p = {}, proposer = {}, n = {}, v = {}, acceptor = {}".format(p, proposer, n, v, acceptor)

        success = self.proposer.handle_promise(p, proposer, n, v, acceptor)

        return paxos_pb2.OKResponse(response = True)

    def handle_refuse(self, request, context):
        p = request.proposal_number
        proposer = request.proposer
        n = request.decree_number
        acceptor = request.acceptor

        if RECEIVER_DEBUG:
            print "RefuseRequest received: p = {}, proposer = {}, n = {}, acceptor = {}".format(p, proposer, n, acceptor)

        success = self.proposer.handle_refuse(p, proposer, n, acceptor)

        return paxos_pb2.OKResponse(response = True)

    def handle_learn(self, request, context):
        p = request.proposal_number
        proposer = request.proposer
        n = request.decree_number
        v = request.value
        acceptor = request.acceptor

        if RECEIVER_DEBUG:
            print "LearnRequest received: p = {}, proposer = {}, n = {}, v = {}, acceptor = {}".format(p, proposer, n, v, acceptor)

        success = self.learner.handle_learn(p, proposer, n, v, acceptor)

        return paxos_pb2.OKResponse(response = True)
