"""
This module implements a proposer, using the specified messenger.
"""

from proposal import Proposal
import threading

PROPOSER_DEBUG = True

class Proposer():
    """
    Implementation of a Paxon proposer.

    @param messenger: the messenger instance that will be used
    """

    def __init__(self, messenger):
        self.messenger = messenger

        self.min_quorum_size = len(self.messenger.get_quorum()) / 2 + 1

        self.init_decree()

        self.lock = threading.RLock()

        return

    def init_decree(self):
        self.init_proposal()
        self.proposal_counter = 0

    def init_proposal(self):
        self.current_proposal = None
        self.highest_proposal = None
        self.promised_acceptors = set()

    def propose(self, n, v, quorum):
        # everytime we propose something, we recalculate the quorum size.
        # this is not ideal, but it will work
        self.min_quorum_size = len(self.messenger.get_quorum()) / 2 + 1

        self.lock.acquire()

        # cannot propose if we are currently proposing something else
        if self.current_proposal is not None:

            # if we are starting a new proposal for the same decree...
            # notice that we do not want to set the counter to 0 here!
            if self.current_proposal.n == n:
                if PROPOSER_DEBUG:
                    print "PROPOSER_DEBUG: Attempt at proposing for decree {} when last proposal {} for decree was still in place. Restarting proposal.".format(n, self.current_proposal.p, self.current_proposal.n)
                self.init_proposal()

            # otherwise, we are starting a new decree
            else:
                if PROPOSER_DEBUG:
                    print "PROPOSER_DEBUG: Attempt at proposing for decree {} when last proposal {} for decree was still in place. Restarting proposal.".format(n, self.current_proposal.p, self.current_proposal.n)
                self.init_decree()

        # pick a proposal number from the counter, and add one
        p = self.proposal_counter
        self.proposal_counter += 1

        # create proposal with passed in information
        self.current_proposal = Proposal(p, n, v)

        # send the prepare message to everybody in the quorum
        self.prepare(p, n, quorum)

        self.lock.release()

    def prepare(self, p, n, quorum):
        """
        Wrapper on the messenger: simply sends a prepare message for the
        current proposal to a quorum.

        @param p: the proposal number in question
        @param n: the decree number in question
        @param quorum: the quorum to which the prepare will be sent

        @return True if message is sent successfully; False otherwise
        """

        # simply sends the RPC call
        self.messenger.send_prepare(p, n, quorum)

        if PROPOSER_DEBUG:
            print "PROPOSER_DEBUG: Proposal {} for decree {} initiated".format(p, n)

        return True

    def _check_promise_count(self):
        min_quorum = len(self.messenger.get_quorum()) / 2 + 1

        if PROPOSER_DEBUG:
            print "PROPOSER_DEBUG: Checking promise count: {}, when min_quorum_size is {}".format(len(self.promised_acceptors), self.min_quorum_size)

        if len(self.promised_acceptors) >= min_quorum:

            # fetch the information that will be passed to acceptors
            p = self.current_proposal.p
            n = self.current_proposal.n
            v = self.current_proposal.v

            # the value must be the value corresponding to the highest-numbered
            # proposal we have seen in the quorum (if any)
            if self.highest_proposal is not None:
                v = self.highest_proposal.v

                if PROPOSER_DEBUG:
                    print "PROPOSER_DEBUG: Proposal {} forced to take value {} by Paxos conditions".format(p, v)

            if PROPOSER_DEBUG:
                print "PROPOSER_DEBUG: Proposal {} with value {} sent to promised acceptors: {}".format(p, v, self.promised_acceptors)

            # send accept request to the promised acceptors !# ??
            self.messenger.send_accept(p, n, v, self.promised_acceptors)

            # reset the state kept by proposer
            self.init_proposal()


    def handle_promise(self, p, n, v, acceptor):
        """
        Handles a promise given by an acceptor. This must check the @param v
        (see below) and update our current proposal accordingly: the proposer
        is only allowed to propose the highest value received in the quorum
        (or anything, if no such value exists).

        This must also check if enough acceptors have responded, and if so,
        start the accept part of the algorithm.

        @param p: the highest-numbered proposal accepted by this acceptor in the past.
        This may be None.
        @param n: the decree number corresponding to the promise (and to @param p)
        @param v: the value corresponding to @param p. This may be None.
        @param acceptor: the acceptor that responded with a promise

        @return XXX
        """

        self.lock.acquire()

        # we must have a current proposal set in order to handle this request
        if self.current_proposal is None:
            if PROPOSER_DEBUG:
                print "PROPOSER_DEBUG: Promise received when no proposal is in place; ignoring it"

            self.lock.release()

            return False

        # check if the message refers to the current proposal decree; if it
        # does not, we have nothing to do.

        if n != self.current_proposal.n:
            if PROPOSER_DEBUG:
                print "PROPOSER_DEBUG: Promise received for a different decree {} than current one {}".format(n, self.current_proposal.n)

            self.lock.release()

            return False

        # if we had a previous proposal, update our highest_proposal accordingly
        if p is not None:
            assert(v is not None)

            if PROPOSER_DEBUG:
                print "PROPOSER_DEBUG: Promise received for decree {} up to proposal {} with value {}, from acceptor {}".format(n, p, v, acceptor)

            # we may need to initiate the highest proposal here
            if self.highest_proposal is None:
                self.highest_proposal = Proposal(p, n, v)

            # update the value of the proposal according to the rules. Notice here
            # that p could be None
            if p > self.highest_proposal.p:
                if PROPOSER_DEBUG:
                    print "PROPOSER_DEBUG: Updating highest_proposal to {} with value {}".format(p, v)

                self.highest_proposal.v = v
                self.highest_proposal.p = p
                self.highest_proposal.n = n

        if PROPOSER_DEBUG:
            print "PROPOSER_DEBUG: Added acceptor {} to list of promised acceptors".format(acceptor)

        # update promised_acceptors and check whether we have enough
        self.promised_acceptors.add(acceptor)
        self._check_promise_count()

        self.lock.release()

        return True

    def handle_refuse(self, p, n, acceptor):
        """
        Handles a refusal of a promise given by an acceptor. In case this
        is received, we must stop working on the current proposal, since
        it will not be accepted anyway.

        @param p: the proposal number corresponding to the promise
        @param n: the decree number corresponding to the promise
        @param acceptor: the acceptor that responded with a promise

        @return XXX
        """

        if PROPOSER_DEBUG:
            print "PROPOSER_DEBUG: Proposal {} for decree {} was refused by acceptor {}; aborting it".format(p, n, acceptor)

        self.lock.acquire()

        # reset the state kept by proposer
        self.init_proposal()

        self.lock.release()

        return True
