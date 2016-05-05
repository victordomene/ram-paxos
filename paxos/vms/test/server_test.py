"""
This file implements a set of tests for a server that uses the gRPC protocol
defined by paxos.proto.
"""

import time

# attach the appropriate directories to sys.path
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from protobufs import paxos_pb2
from vms import rpcVM

def run():
	vm = rpcVM.grpcVM("FIRST MACHINE")

	server = paxos_pb2.beta_create_VM_server(vm)
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
