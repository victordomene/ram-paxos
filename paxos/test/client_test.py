"""
This file implements a set of tests for a server that uses the gRPC protocol
defined by paxos.proto.
"""

import time

# attach the appropriate directories to sys.path
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from paxos.protobufs import paxos_pb2
from paxos.vm import VM
from paxos.messengers import rpcMessenger
from paxos.receivers import rpcReceiver
from paxos.messengers import rdtpMessenger
from paxos.receivers import rdtpReceiver
from paxos import proposer, acceptor, learner

def initialize_grpc_vm(name):
    return VM(name, rpcMessenger.grpcMessenger, rpcReceiver.grpcReceiver)

def initialize_rdtp_vm(name):
	return VM(name, rdtpMessenger.rdtpMessenger, rdtpReceiver.rdtpReceiver)

def run():
    vm = initialize_grpc_vm("2")
    vm.serve("localhost", 6667)
    vm.add_destination("1", "localhost", 6666)

    n = 0
    v = 100
    while True:
        time.sleep(1)

        vm.propose_to_quorum(n, v)
        n += 1
        v += 2


if __name__ == "__main__":
    run()
