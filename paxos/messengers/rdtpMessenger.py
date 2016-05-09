"""
This module provides an implementation of the Messenger class using RDTP.
"""
import socket
from time import sleep
# import time

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from rdtp import rdtp
from messenger import Messenger

TIMEOUT_SECONDS = 10
BENCHMARK = True

class rdtpMessenger(Messenger):
    def __init__(self, name):
        Messenger.__init__(self)
        self.name = name
        self.destinations = {}
        self.sockets = {}


    def _fetch_stub(self, name):
        # fetch the stub for the proposer
        if name in self.sockets:
            return self.sockets[name]

        try:
            host, port = self.destinations[name]
            self.sockets[name] = self.connect(host, port)
            return self.sockets[name]
        except KeyError:
            print "_fetch_stub: Destination not found"
            return None
        except:
            print "_fetch_stub: unknown error"
            return None

    def get_quorum(self):
        return self.destinations.keys()

    def connect(self, host, port):
        while True:
            try:
                print 'Trying to connect to %s:%d' % (host, port)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((host, port))
                return sock
            except:
                sleep(1)

    def add_destination(self, name, host, port):
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

        # simply change the entry; do not check if it already exists
        self.destinations[name] = (host, port)

        # function always succeeds
        return True

    # Wrapper to rdtp.send
    def try_send(self, name, stub, *args):
        try:
            rdtp.send(stub, *args)
        except rdtp.ServerDead:
            del self.sockets[name]

            new_stub = self._fetch_stub(name)
            rdtp.send(new_stub, *args)

    def send_prepare(self, p, n, quorum):
        for acceptor in quorum:
            # fetch the stub for each of the acceptors
            stub = self._fetch_stub(acceptor)

            if stub is None:
                return False

            self.stamp_proposal(n, p)

            # create the appropriate request
            self.try_send(acceptor, stub, 0, "send_prepare", str(p), str(n), self.name)

        return True

    def send_accept(self, p, n, v, quorum):
        for acceptor in quorum:
            # fetch the stub for each of the acceptors
            stub = self._fetch_stub(acceptor)

            if stub is None:
                return False

            # create the appropriate request
            self.try_send(acceptor, stub, 0, "send_accept", str(p), str(n), str(v), self.name)

        return True

    def send_promise(self, had_previous, p, proposer, n, v, dest):
        # fetch the stub for the proposer
        stub = self._fetch_stub(dest)

        if stub is None:
            return False

        # create the appropriate request
        self.try_send(dest, stub, 0, "send_promise", str(had_previous), str(p), proposer, str(n), str(v), self.name)

        return True

    def send_refuse(self, p, proposer, n, dest):
        # fetch the stub for the proposer
        stub = self._fetch_stub(dest)

        if stub is None:
            return False

        # create the appropriate request
        self.try_send(dest, stub, 0, "send_refuse", str(p), proposer, str(n), self.name)

        return True

    def send_learn(self, p, proposer, n, v, dest):
        # fetch the stub for the learner
        stub = self._fetch_stub(dest)

        if stub is None:
            return False

        # create the appropriate request
        self.try_send(dest, stub, 0, "send_learn", str(p), proposer, str(n), str(v), self.name)

        return True
