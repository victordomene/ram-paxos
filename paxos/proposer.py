"""
This module implements a proposer, using the specified messenger.
"""

from proposal import Proposal

class Proposer():
    """
    Implementation of a Paxon proposer.

    @param messenger: the messenger instance that will be used
    """

    def __init__(self, messenger):
        self.messenger = messenger
        self.current_proposal = None
        self.highest_proposal = None
        self.promised_acceptors = set()
        self.proposal_sent = False

        self.min_quorum_size = len(self.messenger.get_quorum()) / 2 + 1
        return

    def propose(self, p, n, v, quorum):
        # cannot propose if we are currently proposing something else
        if self.current_proposal is not None:
            return False

        # create proposal with passed in information
        self.current_proposal = Proposal(p, n, v)

        # send the prepare message to everybody in the quorum
        self.prepare(p, n, quorum)

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
        print "PREPARING"

        self.messenger.send_prepare(p, n, quorum)
        return True

    def _check_promise_count(self):

        print "CHECKING COUNT: {}, {}".format(len(self.promised_acceptors), self.min_quorum_size)

        if len(self.promised_acceptors) >= self.min_quorum_size:
            # Proposal already sent
            if self.proposal_sent:
                return

            print "NOT SENT"

            # fetch the information that will be passed to acceptors
            p = self.current_proposal.p
            n = self.current_proposal.n
            v = self.current_proposal.v

            # the value must be the value corresponding to the highest-numbered
            # proposal we have seen in the quorum
            if self.highest_proposal is not None:
                v = self.highest_proposal.v

            print p, n, v

            # v could be None, if there was no previous value assigned to
            # this decree by any acceptor. In that case, we may propose
            # whatever we initially wanted to propose

            # send accept requests to a quorum
            print "SEND_ACCEPT_REQUEST CALLED"

            self.messenger.send_accept_request(p, n, v, self.promised_acceptors)

            self.proposal_sent = True

    def handle_promise(self, had_previous, p, n, v, acceptor):
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

        print "HANDLE PROMISE"

        # we must have a current proposal set in order to handle this request
        if self.current_proposal is None:
            return False

        print "NOT NONE PROPOSAL"

        # check if the message refers to the current proposal decree; if it
        # does not, we have nothing to do.
        
        if n != self.current_proposal.n:
            return False

        print "CORRECT DECREE"

        # if we had a previous proposal, update our highest_proposal accordingly
        if p is not None:
            assert(v is not None)

            # we may need to initiate the highest proposal here
            if self.highest_proposal is None:
                self.highest_proposal = Proposal(p, n, v)

            # update the value of the proposal according to the rules. Notice here
            # that p could be None
            if p > self.highest_proposal.p:
                self.highest_proposal.value = v
                self.highest_proposal.number = p
                self.highest_proposal.decree = n

        print "ADD ACCEPTOR TO PROMISED LIST"

        # update promised_acceptors and check whether we have enough
        self.promised_acceptors.add(acceptor)
        self._check_promise_count()

        return True

    def handle_refuse_promise(self, p, n, acceptor):
        """
        Handles a refusal of a promise given by an acceptor. In case this
        is received, we must stop working on the current proposal, since
        it will not be accepted anyway.

        @param p: the proposal number corresponding to the promise
        @param n: the decree number corresponding to the promise
        @param acceptor: the acceptor that responded with a promise

        @return XXX
        """

        # reset the state kept by proposer
        self.current_proposal = None
        self.highest_proposal = None
        self.promised_acceptors = set()

        return True
