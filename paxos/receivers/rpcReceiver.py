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

        print "HANDLE PREPARE"

        if RECEIVER_DEBUG:
            print "PrepareRequest received: p = {}, n = {}, proposer = {}".format(p, n, proposer)

        success, p = self.acceptor.handle_prepare(p, n, proposer)

        if p is not None:
            assert(n == p.n)
            return paxos_pb2.PromiseResponse(promised = success, had_previous = True,
                    proposal_number = p.p, value = p.v, acceptor = self.name)
        else:
            return paxos_pb2.PromiseResponse(promised = success, had_previous = False,
                    proposal_number = p, value = 0, acceptor = self.name)

    def handle_accept(self, request, context):
        p = request.proposal_number
        n = request.decree_number
        v = request.value
        proposer = request.proposer

        print "HANDLE ACCEPT"

        if RECEIVER_DEBUG:
            print "AcceptRequest received: p = {}, n = {}, v = {}, proposer = {}".format(p, n, v, proposer)

        success = self.acceptor.handle_accept(p, n, v, proposer)

        print "SUCCESSFULLY HANDLED ACCEPT"

        return paxos_pb2.OKResponse(response = success)


    def handle_learn(self, request, context):
        print "HANDLE LEARN FINALLY OMGOMGOMGOMG"

        p = request.proposal_number
        n = request.decree_number
        v = request.value
        acceptor = request.acceptor

        print p, n, v, acceptor

        if RECEIVER_DEBUG:
            print "AcceptedRequest received: p = {}, n = {}, v = {}, acceptor = {}".format(p, n, v, acceptor)

        success = self.learner.handle_learn(p, n, v)

        return paxos_pb2.OKResponse(response = success)
