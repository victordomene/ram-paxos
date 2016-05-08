"""
This module implements a learner, using the specified messenger.
"""

from proposal import Proposal
import threading

LEARNER_DEBUG = True

class Learner():
    """
    Implementation of a Paxon learner.

    @param messenger: the messenger instance that will be used
    """

    def __init__(self, messenger):
        # messenger that is used for this learner
        self.messenger = messenger

        # the ledger, where accepted decrees will be written
        self.ledger = {}

        # a dictionary that maps (decree, proposal) => set of machines
        # that have accepted that proposal for that decree
        self.accepted = {}

        # calculate the quorum size; notice that this may change as we
        # add destinations to the messenger
        self.min_quorum_size = len(self.messenger.get_quorum()) / 2 + 1

        # lock to guarantee requests are atomic and that operations on
        # the sets (such as self.accepted) will not be conflicting
        self.lock = threading.Lock()

    def write_to_ledger(self, p, proposer, n, v):
        if LEARNER_DEBUG:
            print "LEARNER_DEBUG: Writing proposal {} from proposer {} for decree {} with value {} to learner {}".format(p, proposer, n, v, self.messenger.name)

        self.ledger[n] = Proposal(p, proposer, n, v)

    def handle_learn(self, p, proposer, n, v, acceptor):
        """
        Handles the event of an acceptor voting for a proposal.

        @param p: the proposal number in question
        @param n: the decree number in question
        @param v: the value accepted
        @param acceptor: the acceptor who has accepted this value

        Does not return.
        """

        # recalculate the quorum size on every learn request; doing this on
        # init is not good enough, since we may add destinations to the
        # messenger
        self.min_quorum_size = len(self.messenger.get_quorum()) / 2 + 1

        self.lock.acquire()

        if LEARNER_DEBUG:
            print "LEARNER_DEBUG: Received an accepted notification for proposal {} from proposer {} and decree {} with value {} from acceptor {}".format(p, proposer, n, v, acceptor)

        # initialize the set of machines that accepted this decree and
        # proposal
        if (n, p) not in self.accepted:
            self.accepted[n, p] = set()

        # add this acceptor to the set
        self.accepted[n, p].add(acceptor)

        # if we have enough acceptors, write to ledger
        if len(self.accepted[n, p]) >= self.min_quorum_size:
            self.write_to_ledger(p, proposer, n, v)

        self.lock.release()

        return True

    def handle_print_ledger(self):
        print "##########################"
        print 'Learner {} printing Ledger'.format(self.messenger.name)

        self.lock.acquire()

        for decree in self.ledger:
            print "Decree: {}, Value: {}, Proposal {} from {}".format(decree, self.ledger[decree].v, self.ledger[decree].p, self.ledger[decree].proposer)

        self.lock.release()
