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
from paxos import proposer, acceptor, learner

def initialize_grpc_vm(name):
	return VM(name, rpcMessenger.grpcMessenger, rpcReceiver.grpcReceiver)

def run():
	vm = initialize_grpc_vm("1")
	vm.serve("localhost", 6666)

	try:
		while True:
			time.sleep(600)
			print "Woke up!"
	except KeyboardInterrupt:
		vm.stop_server()

if __name__ == "__main__":
	run()
