"""
This module implements the abstraction of a Virtual Machine.
"""

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from paxos import proposer, acceptor, learner

class VM():
    def __init__(self, name, messengerClass, receiverClass):
        self.messenger = messengerClass(name)

        self.proposer = proposer.Proposer(self.messenger)
        self.acceptor = acceptor.Acceptor(self.messenger)
        self.learner = learner.Learner(self.messenger)

        self.receiver = receiverClass(self.proposer, self.acceptor, self.learner)

        return

    def serve(self, host, port):
        """
        Starts an instance of the server (which will receive calls).
        """
        return self.receiver.serve(host, port)

    def stop_server(self):
        """
        Stops the instance of a server.
        """
        self.receiver.stop_server()

    def propose_to_quorum(self, p, n, v):
        """
        Starts a new proposal.
        """

        # get a quorum from the messenger (it is the messenger that keeps
        # track of our destinations)
        quorum = self.messenger.get_quorum()
        
        print "PROPOSING"

        # actually propose
        return self.proposer.propose(p, n, v, quorum)

    def add_destination(self, name, host, port):
        """
        Add a new destination to this machine's network.
        """

        return self.messenger.add_destination(name, host, port)
