"""
This module defines the abstract class of a messenger. It provides all of
the functionality that is implemented by a specific type of messenger. In
Paxos, we will allow some different types of communication, but all of them
must present this interface.

Notice that a single machine may need to use all of the functionality of a
Proposer, Learner or Acceptor. For this reason, these methods are all
accessible.
"""

from abc import abstractmethod
import time

class Messenger():
    def __init__(self):
        # messages sent, indexed by decree and proposal number
        self.sent = {}
        return

    @abstractmethod
    def get_quorum(self):
        """
        Returns a quorum from the destination list.
        """
        return

    @abstractmethod
    def add_destination(self):
        """
        Adds a host/port combination to the list of possible destinations
        for messages. Basically, this tells our messenger where each machine
        can be found. It will store the host/port combination in a dictionary
        indexed by the given name.

        If a name already exists in the dictionary, this function will update
        the information for the name.

        @param name: the name given to this host/port combination
        @param host: the host to be added
        @param port: the port used in that host

        @return True if successfully added; False otherwise
        """
        return

    @abstractmethod
    def send_prepare(self):
        """
        This method should be used exclusively by a Proposer.

        Sends a prepare message for everyone who is in a given quorum. This
        message will contain simply the number of the proposal and the number
        of the decree that is being voted.

        @param p: the proposal number in question
        @param n: the decree number in question
        @param quorum: the quorum to which message will be sent

        @return True if message is sent; False otherwise """
        return

    @abstractmethod
    def send_accept(self):
        """
        This method should be used exclusively by a Proposer.

        Sends an accept request for everyone who is in a given quorum. This
        should be called after a proposer sees a majority of promises (say, if
        everybody in the quorum made the promise).

        @param p: the proposal number in question
        @param n: the decree number in question
        @param v: the value proposed
        @param quorum: the quorum to which message will be sent

        @return True if message is sent; False otherwise
        """
        return

    @abstractmethod
    def send_promise(self):
        """
        This method should be used exclusively by an Acceptor.

        Sends a promise back to the proposer, which guarantees that this
        acceptor will not accept any proposals with number less than some
        number. Also sends back the value for the highest numbered proposal for
        which this acceptor has responded.

        @param p: the proposal number in question
        @param n: the decree number in question
        @param v: the value of the highest-numbered proposal voted
        @param proposer: the proposer to whom the message will be sent

        @return True if message is sent; False otherwise
        """
        return

    @abstractmethod
    def send_refuse(self):
        """
        This method should be used exclusively by an Acceptor.

        Sends a message to the proposer saying that this acceptor will not
        accept this proposal (probably, because it has already taken a promise
        for a higher-number proposal).

        @param p: the proposal number in question
        @param n: the decree number in question
        @param proposer: the proposal to whom the message will be sent

        @return True if message is sent; False otherwise
        """
        return

    @abstractmethod
    def send_learn(self):
        """
        This method should be used exclusively by an Acceptor.

        Sends a message to a set of learners saying that a given proposal has
        been accepted by this acceptor.

        @param p: the proposal number in question
        @param n: the decree number in question
        @param v: the value accepted
        @param learners: the set of learners to which the message will be sent

        @return True if message is sent; False otherwise
        """
        return

    def fetch_proposal(self, n, p):
        """
        For benchmarking purposes, retrieve the timestamp associated with this value

        @param n: the decree number
        @param p: the proposal number

        @return the timestamp given in seconds
        """
        if (n, p) in self.sent:
            return self.sent[n, p]
        else:
        	return None

    def stamp_proposal(self, n, p):
        """
        For benchmarking purposes, adds a given proposal number and a decree number to a dictionary
        and adds a timestamp

        @param n: the decree number
        @param p: the proposal number

        @return None
        """
        self.sent[n, p] = time.time()
