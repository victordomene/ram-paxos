"""
This module implements a learner, using the specified messenger.
"""

from proposal import Proposal
import threading
import time
import pickle

LEARNER_DEBUG = False 
BENCHMARK = False

class Learner():
    """
    Implementation of a Paxon learner.

    @param messenger: the messenger instance that will be used
    """

    def __init__(self, messenger, use_disk):
        # messenger that is used for this learner
        self.messenger = messenger
        self.use_disk = use_disk

        # the ledger, where accepted decrees will be written
        self.ledger = {}

        if self.use_disk:
        	self.outfile = open('ledger-{}.out'.format(self.messenger.name), 'w')

        # a dictionary that maps (decree, proposal) => set of machines
        # that have accepted that proposal for that decree
        self.accepted = {}

        # calculate the quorum size; notice that this may change as we
        # add destinations to the messenger
        self.min_quorum_size = len(self.messenger.get_quorum()) / 2 + 1

        # lock to guarantee requests are atomic and that operations on
        # the sets (such as self.accepted) will not be conflicting
        self.lock = threading.Lock()

        # keep track of the differences between sending and learning
        # proposals. indexed by decree number and by p
        self.differences = {}

    def write_to_ledger(self, p, proposer, n, v):
        """
        Write a chosen value to the learner's ledger. If we are supposed
        to write to disk (by passing in the appropriate parameters),
        then we do so here.

        @param p: the proposal number chosen
        @param proposer: the proposer who proposed the chosen p
        @param n: the decree this refers to
        @param v: the value chosen

        Does not return.
        """

        if LEARNER_DEBUG:
            print "LEARNER_DEBUG: Writing proposal {} from proposer {} for decree {} with value {} to learner {}".format(p, proposer, n, v, self.messenger.name)

        if self.use_disk:
        	self.outfile.write('%d,%s,%d,%d\n'.format(p, proposer, n, v))

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
            # want to calculate the difference between when the proposal
            # was sent and when it was learned
            if BENCHMARK:
                old_time = self.messenger.fetch_proposal(n, p)
                if old_time is not None:
                    self.differences[n, p] = time.time() - old_time

            self.write_to_ledger(p, proposer, n, v)

        self.lock.release()

        return True

    def handle_print_ledger(self):
        """
        Simply prints out this learner's current ledger.

        Does not return.
        """

        print "##########################"
        print 'Learner {} printing Ledger'.format(self.messenger.name)

        self.lock.acquire()

        for decree in self.ledger:
            print "Decree: {}, Value: {}, Proposal {} from {}".format(decree, self.ledger[decree].v, self.ledger[decree].p, self.ledger[decree].proposer)

        self.lock.release()

    def handle_print_differences(self):
        """
        Prints the mean of the time differences for this learner. This time
        difference refers to the same time differences in handle_diff_file:
        it is the difference between the time when a proposer started a proposal,
        and the time when the corresponding learner learnt it.
        
        Does not return.
        """

        print "##########################"
        print "Learner {} printing time differences".format(self.messenger.name)

        self.lock.acquire()

        for diff in self.differences:
            print "Difference: {}, Proposal {}, Decree number {}".format(self.differences[diff], diff[1], diff[0])

        self.lock.release()

    def handle_print_difference_mean(self):
        """
        Prints the mean of the time differences for this learner. This time
        difference refers to the same time differences in handle_diff_file:
        it is the difference between the time when a proposer started a proposal,
        and the time when the corresponding learner learnt it.

        This is the difference between the time a proposal starts, and the
        time the learner (in the same VM) actually learned that the proposal
        passed.

        Notice that this is not a necessary function to Paxos; it only does
        benchmarking.

        Does not return.
        """

        print "##########################"
        print "Learner {} printing MEAN of time differences".format(self.messenger.name)
        if self.use_disk:
            print "Use Disk: TRUE"
        else:
            print "User Disk: FALSE"

        self.lock.acquire()

        total = 0.
        for diff in self.differences:
        	total += self.differences[diff]

        if len(self.differences) > 0:
            print "Mean of Differences: {}. Sample size: {}".format(total / len(self.differences), len(self.differences))
        else:
        	print "Division by 0 in handle_print_difference_mean"

        self.lock.release()

    def handle_diff_file(self):
        """
        Prints the timing differences to a file for this given learner.

        This is the difference between the time a proposal starts, and the
        time the learner (in the same VM) actually learned that the proposal
        passed.

        Notice that this is not a necessary function to Paxos; it only does
        benchmarking.

        Does not return.
        """

        print "##########################"
        print "Learner {} printing time differences to file".format(self.messenger.name)

        filename = "../bench_data/" + str(time.time())

        diff_file = open(filename, "w+")
        pickle.dump(self.differences, diff_file)
        diff_file.close()
