"""
This module provides an implementation of the Messenger class using Google's
RPC Protocol (gRPC).

For the specific documentation of the arguments these methods take and 
what they do at a high level, refer to messenger.py.
"""

from grpc.beta import implementations
from messenger import Messenger

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from protobufs import paxos_pb2

TIMEOUT_SECONDS = 10

def ignore(future):
    result = future.result()
    return

def ignore_accept(future):
    result = future.result()
    return

def ignore_promise(future):
    result = future.result()
    return

def ignore_learn(future):
    result = future.result()
    return

def ignore_refuse(future):
    result = future.result()
    return

class grpcMessenger(Messenger):
    def __init__(self, name):
        Messenger.__init__(self)
        self.name = name
        self.destinations = {}
        return

    def _fetch_stub(self, name):
        # fetch the stub for the proposer
        try:
            stub = self.destinations[name]
        except KeyError:
            print "_fetch_stub: could not find stub for {}".format(name)
            return None
        except:
            print "_fetch_stub: unknown error"
            return None

        return stub

    def get_quorum(self):
        return self.destinations.keys()

    def add_destination(self, name, host, port):
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
            response = stub.handle_prepare.future(request, TIMEOUT_SECONDS)

            response.add_done_callback(ignore)

        return True

    def send_accept(self, p, n, v, quorum):
        for acceptor in quorum:
            # fetch the stub for each of the acceptors
            stub = self._fetch_stub(acceptor)

            if stub is None:
                return False

            # create the appropriate request
            request = paxos_pb2.AcceptRequest(proposal_number = p,
                    decree_number = n, value = v, proposer = self.name)

            # finally send message to this acceptor
            response = stub.handle_accept.future(request, TIMEOUT_SECONDS)

            response.add_done_callback(ignore_accept)

        return True

    def send_promise(self, had_previous, p, proposer, n, v, dest):
        # fetch the stub for the proposer
        stub = self._fetch_stub(dest)

        if stub is None:
            return False

        # create the appropriate request
        request = paxos_pb2.PromiseRequest(had_previous = had_previous, proposal_number = p,
                proposer = proposer, decree_number = n, value = v, acceptor = self.name)

        # finally send promise back to proposer
        response = stub.handle_promise.future(request, TIMEOUT_SECONDS)

        response.add_done_callback(ignore_promise)

        return True

    def send_refuse(self, p, proposer, n, dest):
        # fetch the stub for the proposer
        stub = self._fetch_stub(dest)

        if stub is None:
            return False

        # create the appropriate request
        request = paxos_pb2.RefuseRequest(proposal_number = p,
                proposer = proposer, decree_number = n, acceptor = self.name)

        # finally send refusal back to proposer
        response = stub.handle_refuse.future(request, TIMEOUT_SECONDS)

        response.add_done_callback(ignore_refuse)

        return True

    def send_learn(self, p, proposer, n, v, learner):
        # fetch the stub for the learner
        stub = self._fetch_stub(learner)

        if stub is None:
            return False

        # create the appropriate request
        request = paxos_pb2.LearnRequest(proposal_number = p, proposer = proposer,
                decree_number = n, value = v, acceptor = self.name)

        # finally send message to learner
        response = stub.handle_learn.future(request, TIMEOUT_SECONDS)

        response.add_done_callback(ignore_learn)

        return True
