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
    vm = initialize_rdtp_vm("1")

    vm.serve("localhost", 6666)
    vm.add_destination("2", "localhost", 6667)

    while True:
        time.sleep(600)
        print "Woke up!"

if __name__ == "__main__":
    run()
