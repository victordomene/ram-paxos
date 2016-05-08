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

        # calculate the quorum size; notice that this may change as we
        # add destinations to the messenger
        self.min_quorum_size = len(self.messenger.get_quorum()) / 2 + 1

        # initializes the current & highest proposals to None
        self.current_proposal = None
        self.highest_proposal = None

        # initialize the set of promised acceptors for the current proposal
        self.promised_acceptors = set()

        # initialize the proposal counter; this will be reset everytime
        # a decree is agreed upon. !# This may not be necessary/desired.
        self.proposal_counter = 0

        # lock to guarantee requests are atomic and that operations on
        # the sets (such as self.promised_acceptors) will not be conflicting
        self.lock = threading.Lock()

    def _init_proposal(self):
        """
        Helper method that initializes a proposal (by clearing the useful
        instance variables).

        Does not return.
        """

        self.current_proposal = None
        self.highest_proposal = None
        self.promised_acceptors = set()

    def propose(self, n, v, quorum):
        """
        Interface to start a Paxos proposal. Simply does a lot of
        initialization steps and sends the prepare requests. Notice that
        the proposal number is handled internally, and if we propose in
        the middle of another proposal, we simply stop the previous proposal.

        @param n: the decree number in question
        @param v: the proposed value for this decree
        @param quorum: the quorum to which the prepare will be sent

        Does not return.
        """

        # recalculate the quorum size on every proposal; doing this on
        # init is not good enough, since we may add destinations to the
        # messenger
        self.min_quorum_size = len(self.messenger.get_quorum()) / 2 + 1

        self.lock.acquire()

        # cannot propose if we are currently proposing something else
        if self.current_proposal is not None:
            if PROPOSER_DEBUG:
                print "PROPOSER_DEBUG: Attempt at proposing for decree {} when last proposal {} for decree was still in place. Restarting proposal.".format(n, self.current_proposal.p, self.current_proposal.n)

            self._init_proposal()

        # pick a proposal number from the counter, and add one
        p = self.proposal_counter
        self.proposal_counter += 1

        # create proposal with passed in information
        self.current_proposal = Proposal(p, self.messenger.name, n, v)

        # send the prepare message to everybody in the quorum
        self.messenger.send_prepare(p, n, quorum)

        if PROPOSER_DEBUG:
            print "PROPOSER_DEBUG: Proposal {} for decree {} initiated".format(p, n)

        self.lock.release()

    def _check_promise_count(self):
        """
        Helper function that checks the current promise count, and sends
        accept requests to a quorum if we have enough promises.

        Does not return.
        """

        if PROPOSER_DEBUG:
            print "PROPOSER_DEBUG: Checking promise count: {}, when min_quorum_size is {}".format(len(self.promised_acceptors), self.min_quorum_size)

        if len(self.promised_acceptors) >= self.min_quorum_size:

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
            self._init_proposal()

    def handle_promise(self, p, proposer, n, v, acceptor):
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

        @return True if promise can be handled; False if it cannot (i.e., there
        is no proposal in place, or the current decree we are handling
        is not the one to which the promise refers to)
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
            assert(proposer is not None)

            if PROPOSER_DEBUG:
                print "PROPOSER_DEBUG: Promise received for decree {} up to proposal {} with value {}, from acceptor {}".format(n, p, v, acceptor)

            # we may need to initiate the highest proposal here
            if self.highest_proposal is None:
                self.highest_proposal = Proposal(p, proposer, n, v)

            # update the value of the proposal according to the rules. Notice here
            # that p could be None
            high_p = self.highest_proposal.p
            high_proposer = self.highest_proposal.proposer

            if (p, proposer) > (high_p, high_proposer):
                if PROPOSER_DEBUG:
                    print "PROPOSER_DEBUG: Updating highest_proposal to {} with value {}".format(p, v)

                self.highest_proposal.v = v
                self.highest_proposal.p = p
                self.highest_proposal.proposer = proposer
                self.highest_proposal.n = n

        if PROPOSER_DEBUG:
            print "PROPOSER_DEBUG: Added acceptor {} to list of promised acceptors".format(acceptor)

        # update promised_acceptors and check whether we have enough
        self.promised_acceptors.add(acceptor)
        self._check_promise_count()

        self.lock.release()

        return True

    def handle_refuse(self, p, proposer, n, acceptor):
        """
        Handles a refusal of a proposal by an acceptor. In case this
        is received, we must stop working on the current proposal, since
        it will not be accepted anyway.

        @param p: the proposal number corresponding to the refusal
        @param proposer: the proposer who initiated this proposal
        @param n: the decree number corresponding to the refusal
        @param acceptor: the acceptor that responded with a refusal

        @return True if we could abort proposal; False otherwise 
        """

        if self.current_proposal is None or self.current_proposal.p != p or self.current_proposal.proposer != proposer:
            if PROPOSER_DEBUG:
                print "PROPOSER_DEBUG: Proposal {} for proposer {} was refused by acceptor {}, but this is not our current proposal; ignoring it".format(p, proposer, acceptor)

            return False

        self.lock.acquire()

        # reset the state kept by proposer
        self._init_proposal()

        if PROPOSER_DEBUG:
            print "PROPOSER_DEBUG: Proposal {} for proposer {} refused by acceptor {}; aborting".format(p, proposer, acceptor)

        self.lock.release()

        return True
