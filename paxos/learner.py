"""
This module implements a learner, using the specified messenger.
"""

from proposal import Proposal

LEARNER_DEBUG = True

class Learner():
    """
    Implementation of a Paxon learner.

    @param messenger: the messenger instance that will be used
    """

    def __init__(self, messenger):
        self.messenger = messenger
        self.ledger = {}

        self.accepted = {}

        self.min_quorum_size = len(self.messenger.get_quorum()) / 2 + 1
        return

    def write_to_ledger(self, p, n, v):
        if LEARNER_DEBUG:
            print "LEARNER_DEBUG: Writing proposal {} for decree {} with value {} to learner {}".format(p, n, v, self.messenger.name)

        self.ledger[n] = Proposal(p, n, v)

    def handle_accepted(self, p, n, v, acceptor):
        """
        Handles the event of an acceptor voting for a proposal.

        @param p: the proposal number in question
        @param n: the decree number in question
        @param v: the value accepted
        @param acceptor: the acceptor who has accepted this value

        Does not return.
        """

        if LEARNER_DEBUG:
            print "LEARNER_DEBUG: Received an accepted notification for proposal {} and decree {} with value {} from acceptor {}".format(p, n, v, acceptor)

        if n not in self.accepted:
            self.accepted[n, p] = set()

        self.accepted[n, p].add(acceptor)

        if len(self.accepted[n, p]) >= self.min_quorum_size:
            self.write_to_ledger(p, n, v)


        return True

    def get_decree(self, n):
        if LEARNER_DEBUG:
            print "LEARNER_DEBUG: Getting the information in the ledger for decree {}".format(n)

        # Spinlock
        while n not in self.ledger:
        	pass
        return self.ledger[n]

