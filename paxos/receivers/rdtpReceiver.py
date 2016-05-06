"""
This module provides an implementation of the Receiver class using Google's
RPC Protocol (gRPC).
"""

import SocketServer
import thread

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from rdtp import rdtp

TIMEOUT_SECONDS = 10
RECEIVER_DEBUG = True

class rdtpHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            status, args = rdtp.recv(self.request)

            assert(status == 0)
            assert(len(args) >= 2)

            method = args[0]

            print 'Received rdtp.recv with method:' + method
            if method == 'send_prepare':
                assert(len(args) == 4)
                p, n, proposer = int(args[1]), int(args[2]), args[3]
                self.server.receiver.handle_prepare(p, n, proposer)

            if method == 'send_promise':
                assert(len(args) == 6)
                had_previous, p, n, v, acceptor = bool(args[1]), int(args[2]), int(args[3]), int(args[4]), str(args[5])
                self.server.receiver.handle_promise(had_previous, p, n, v, acceptor)

            if method == 'send_accept_request':
                assert(len(args) == 5)
                p, n, v, proposer = int(args[1]), int(args[2]), int(args[3]), str(args[4])
                self.server.receiver.handle_accept_request(p, n, v, proposer)

            if method == 'send_refuse_proposal':
                assert(len(args) == 4)
                p, n, acceptor = int(args[1]), int(args[2]), str(args[3])
                self.server.receiver.handle_refuse_proposal(p, n, acceptor)

            if method == 'send_accepted':
                assert(len(args) == 5)
                p, n, v, acceptor = int(args[1]), int(args[2]), int(args[3]), str(args[4])
                self.server.receiver.handle_accepted(p, n, v, acceptor)


class rdtpReceiver():
    def __init__(self, proposer, acceptor, learner):
        self.proposer = proposer
        self.acceptor = acceptor
        self.learner = learner


    def serve(self, host, port):
        self.server = SocketServer.TCPServer((host, port), rdtpHandler, False)
        self.server.receiver = self
        self.server.server_bind()
        self.server.server_activate()

        print 'Started listening on %s:%d' % (host, port)
        thread.start_new_thread(self.serve_forever, ())

    def serve_forever(self):
        self.server.serve_forever()

    def handle_prepare(self, p, n, proposer):
        if RECEIVER_DEBUG:
            print "PrepareRequest received: p = {}, n = {}, proposer = {}".format(p, n, proposer)

        return self.acceptor.handle_prepare(p, n, proposer)

    def handle_accept_request(self, p, n, v, proposer):
        if RECEIVER_DEBUG:
            print "AcceptRequest received: p = {}, n = {}, v = {}, proposer = {}".format(p, n, v, proposer)

        return self.acceptor.handle_accept_request(p, n, v, proposer)

    def handle_promise(self, had_previous, p, n, v, acceptor):

        # handle the case where we had no previous value set
        if not had_previous:
            p = None
            v = None

        if RECEIVER_DEBUG:
            print "PromiseRequest received: p = {}, n = {}, v = {}, acceptor = {}".format(p, n, v, acceptor)

        return self.proposer.handle_promise(had_previous, p, n, v, acceptor)

    def handle_refuse_promise(self, p, n, acceptor):
        if RECEIVER_DEBUG:
            print "RefusePromiseRequest received: p = {}, n = {}, acceptor = {}".format(p, n, acceptor)

        return self.proposer.handle_refuse_promise(p, n, acceptor)

    def handle_accepted(self, p, n, v, acceptor):
        if RECEIVER_DEBUG:
            print "AcceptedRequest received: p = {}, n = {}, v = {}, acceptor = {}".format(p, n, v, acceptor)

        return self.learner.handle_accepted(p, n, v, acceptor)
