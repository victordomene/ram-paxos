"""
This file implements a set of tests for a server that uses the gRPC protocol
defined by paxos.proto.
"""

import time

# attach the appropriate directories to sys.path
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.dirname(path.abspath(__file__))))))

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
    vm = initialize_rdtp_vm("2")
    vm.add_destination("1", "localhost", 6666)


    p = 10
    n = 1
    v = 100

    vm.propose_to_quorum(p, n, v)

if __name__ == "__main__":
    run()
