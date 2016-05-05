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
	vm = rpcVM.grpcVM("SECOND MACHINE")
	vm.messenger.add_destination("FIRST MACHINE", "localhost", 6666)
	vm.messenger.send_prepare(100, 50, ["FIRST MACHINE"])

if __name__ == "__main__":
	run()
