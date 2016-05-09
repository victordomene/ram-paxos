"""
This module implements an acceptor, using the specified messenger.
"""

from proposal import Proposal
import threading

ACCEPTOR_DEBUG = False

class Acceptor():
    """
    Implementation of a Paxon acceptor. Using some optimizations, we need to
    keep track of (only) the highest proposal accepted by this acceptor for
    every decree that we have voted on (both its number and its value). We do
    this by keeping a dictionary that maps decrees to Proposal objects.

    @param messenger: the messenger instance that will be used
    """

    def __init__(self, messenger):
        # messenger that is used for this acceptor
        self.messenger = messenger

        # a dictionary that maps decree => latest proposal this machine
        # has accepted
        self.accepted_proposals = {}

        # a dictionary that maps decree => latest promise this machine
        # has made
        self.promises = {}

        # lock to guarantee requests are atomic and that operations on
        # the sets (such as self.accepted_proposals) will not be conflicting
        self.lock = threading.Lock()

    def handle_prepare(self, p, n, proposer):
        """
        Handles a prepare request that has been received. This will succeed if
        the proposal number is higher than any other prepare request that we
        have already responded to. In case of success, this must promise the
        proposer that we will not accept any other proposal with lower number
        than this one.

        @param p: the proposal number in question
        @param n: the decree number in question
        @param proposer: the proposer to whom we must respond

        @return True if promise is made; False otherwise
        """

        self.lock.acquire()

        # We have never replied to a prepare request for this decree
        if n not in self.promises:
            if ACCEPTOR_DEBUG:
                print "ACCEPTOR_DEBUG: First proposal {} for decree {}".format(p, n)

            # had_previous = False so p and v will be ignored
            self.messenger.send_promise(False, 0, "", n, 0, proposer)

            # Also we make a promise never to accept proposal numbered less than p
            self.promises[n] = (p, proposer)

            self.lock.release()

            return True

        # We have made a promise but want to override it
        else:
            # if the promised proposal is smaller than the current proposal,
            # we refuse it
            if self.promises[n] < (p, proposer):
                if ACCEPTOR_DEBUG:
                    print "ACCEPTOR_DEBUG: Refused promise for proposal number {} from proposer {} for decree {}".format(p, proposer, n)

                self.messenger.send_refuse(p, proposer, n, proposer)

                self.lock.release()
                return False

            # otherwise, we want to accept it

            if ACCEPTOR_DEBUG:
                print "ACCEPTOR_DEBUG: Subsequent proposal number {} from proposer {} for decree {}".format(p, proposer, n)

            if n in self.accepted_proposals:
                highest_accepted = self.accepted_proposals[n]

                # had_previous = True so we'll send the current highest accepted value
                self.messenger.send_promise(True, highest_accepted.p, highest_accepted.proposer, n, highest_accepted.v, proposer)
            else:
                # We never accepted anything so we'll just send the empty promise
                self.messenger.send_promise(False, 0, "", n, 0, proposer)

            # Also we make a promise never to accept proposal numbered less than p
            self.promises[n] = (p, proposer)

            self.lock.release()

            return True

    def handle_accept(self, p, n, v, proposer):
        """
        Handles an accept request that has been received. This will always
        succeed, unless we promised a proposal with a higher number that we
        would not do so.

        @param p: the proposal number in question
        @param n: the decree number in question
        @param v: the value proposed
        @param proposer: the proposer to whom we must respond

        @return True if accepted; False otherwise
        """

        self.lock.acquire()

        # We promised not to accept any proposals less than promises[n]
        if n in self.promises and self.promises[n] < (p, proposer):
            if ACCEPTOR_DEBUG:
                print "ACCEPTOR_DEBUG: Promised not to answer proposals less than {} for decree {}".format(self.promises[n], n)

            self.messenger.send_refuse(p, proposer, n, proposer)

            self.lock.release()

            return False

        # If everything is fine, we proceed to accept
        # !# seems like there is an issue with < here...
        if n in self.accepted_proposals:
            acc_p = self.accepted_proposals[n].p
            acc_proposer = self.accepted_proposals[n].proposer

            assert((acc_p, acc_proposer) <= (p, proposer))

        self.accepted_proposals[n] = Proposal(p, proposer, n, v)

        if ACCEPTOR_DEBUG:
            print "ACCEPTOR_DEBUG: Accepted proposal {} for decree {} with value {}".format((p, proposer), n, v)

        # Finally we just send what we accepted to all learners
        # !# Everyone is a learner !!!!2!!
        learners = self.messenger.get_quorum()

        for learner in learners:
            if ACCEPTOR_DEBUG:
                print "ACCEPTOR_DEBUG: Reported acceptance of proposal {} and decree {} to learner {}".format((p, proposer), n, learner)

            self.messenger.send_learn(p, proposer, n, v, learner)

        self.lock.release()

        return True
