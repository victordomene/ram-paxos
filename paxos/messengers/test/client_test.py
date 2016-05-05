"""
This file implements a set of tests for a client that uses the gRPC protocol
defined by paxos.proto.
"""

import time

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from messengers import rpcMessenger

def run():
	messenger = rpcMessenger.grpcMessenger("1")
	
	# wait for continue or something
	messenger.add_destination("2", "localhost", 6666)

	# send a prepare message to the destination
	dest = ["2"]
	messenger.send_prepare(100, 50, dest)
	messenger.send_accept_request(100, 50, 24, dest)
	messenger.send_promise(100, 50, 69, dest[0])
	messenger.send_refuse_proposal(100, 50, dest[0])
	messenger.send_accepted(100, 50, 24, dest[0])

if __name__ == "__main__":
	run()
