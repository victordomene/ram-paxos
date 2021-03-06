"""
This module implements an acceptor, using the specified messenger.
"""

from proposal import Proposal
import threading
import time
import os
import random

ACCEPTOR_DEBUG = False

class Acceptor():
    """
    Implementation of a Paxon acceptor. Using some optimizations, we need to
    keep track of (only) the highest proposal accepted by this acceptor for
    every decree that we have voted on (both its number and its value). We do
    this by keeping a dictionary that maps decrees to Proposal objects.

    @param messenger: the messenger instance that will be used
    """

    def __init__(self, messenger, use_disk):
        # messenger that is used for this acceptor
        self.messenger = messenger
        self.use_disk = use_disk

        # a dictionary that maps decree => latest proposal this machine
        # has accepted
        self.accepted_proposals = {}

        if self.use_disk:
            self.outfile = open(self.messenger.name + '-acceptor.out', 'w')
            self.infile = open('cat', 'r')

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

        self._latency()

        self.lock.acquire()

        # We have never replied to a prepare request for this decree
        if n not in self.promises:
            if ACCEPTOR_DEBUG:
                print "ACCEPTOR_DEBUG: First proposal {} for decree {}".format(p, n)

            # had_previous = False so p and v will be ignored
            self.messenger.send_promise(False, 0, "", n, 0, proposer)

            # Also we make a promise never to accept proposal numbered less than p
            self.promises[n] = (p, proposer)

            self._write('{},{},{}'.format(n, p, proposer))


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
            self._write('{},{},{}\n'.format(n, p, proposer))

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

        self._latency()

        self.lock.acquire()

        if self.use_disk:
            dumb = self.infile.read()
        
        # We promised not to accept any proposals less than promises[n]
        if n in self.promises and self.promises[n] < (p, proposer):
            if ACCEPTOR_DEBUG:
                print "ACCEPTOR_DEBUG: Promised not to answer proposals less than {} for decree {}".format(self.promises[n], n)

            self.messenger.send_refuse(p, proposer, n, proposer)

            self.lock.release()

            return False

        # If everything is fine, we proceed to accept
        if n in self.accepted_proposals:
            acc_p = self.accepted_proposals[n].p
            acc_proposer = self.accepted_proposals[n].proposer
            
            if ACCEPTOR_DEBUG:
                print "ACCEPTOR_DEBUG: Accepted proposal {} for proposer {}, which is higher than {} for {}".format(acc_p, acc_proposer, p, proposer)

            self.messenger.send_refuse(p, proposer, n, proposer)

            self.lock.release()

            return False

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

    def _latency(self):
        """
        Adds latency to this acceptor's receival of messages. This simply
        sleeps for a random amount of time centered around 0.005.
        
        To turn latency off, comment the early return; uncomment it to
        turn it on.
        """

        return
        time.sleep(0.005 + random.random() / 30.)

    def _sync(self):
        """
        Forces a sync of the outfile to disk. 

        Python has no clear interface to actually doing this nicely,
        so we force it by closing and opening the file.
        """

        self.outfile.close()
        self.outfile = open(self.messenger.name + '-acceptor.out', 'a+')

    def _write(self, what):
        """
        Write something to disk. This is a simple wrapper; to simulate
        proposals that are larger, we simply increase the number of times
        this method loops.
        """

        for i in xrange(5):
            if self.use_disk:
                # Write what to disk
                self.outfile.write(what)
            else:
                # Write what to RAM
                a = what[:]
        if self.use_disk:
            self._sync()
