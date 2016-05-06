"""
This module provides an implementation of the Receiver class using our own
RDTP Protocol, which we wrote for the Chat Assignment in CS262
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
    def usage_args(self, method, num, expected):
        if RECEIVER_DEBUG:
            print "RECEIVER_DEBUG: Received a {} request with {} arguments; expected {}".format(method, num, expected)

    def handle(self):
        while True:
            status, args = rdtp.recv(self.request)
            
            # in this application, the only valid status is 0
            if status != 0:
                if RECEIVER_DEBUG:
                    print "RECEIVER_DEBUG: Received a request with invalid status {}".format(status)

                return

            # in this application, all requests must come with more than 2 arguments
            if len(args) < 2:
                if RECEIVER_DEBUG:
                    print "RECEIVER_DEBUG: Received a request lacking arguments: {}".format(args)

                return

            # the first argument must be the method name
            method = args[0]
            
            if RECEIVER_DEBUG:
                print "RECEIVER_DEBUG: Received a request with method {} and arguments {}".format(method, args[1:])

            if method == 'send_prepare':
                if len(args) != 4:
                    self.usage_args(method, len(args), 4)
                    return

                p, n, proposer = int(args[1]), int(args[2]), args[3]
                self.server.receiver.handle_prepare(p, n, proposer)

            elif method == 'send_promise':
                if len(args) != 6:
                    self.usage_args(method, len(args), 6)
                    return

                had_previous, p, n, v, acceptor = bool(args[1]), int(args[2]), int(args[3]), int(args[4]), str(args[5])
                self.server.receiver.handle_promise(had_previous, p, n, v, acceptor)

            elif method == 'send_accept_request':
                if len(args) != 5:
                    self.usage_args(method, len(args), 5)
                    return

                p, n, v, proposer = int(args[1]), int(args[2]), int(args[3]), str(args[4])
                self.server.receiver.handle_accept_request(p, n, v, proposer)

            elif method == 'send_refuse_proposal':
                if len(args) != 4:
                    self.usage_args(method, len(args), 4)
                    return

                p, n, acceptor = int(args[1]), int(args[2]), str(args[3])
                self.server.receiver.handle_refuse_proposal(p, n, acceptor)

            elif method == 'send_accepted':
                if len(args) != 5:
                    self.usage_args(method, len(args), 5)
                    return

                p, n, v, acceptor = int(args[1]), int(args[2]), int(args[3]), str(args[4])
                self.server.receiver.handle_accepted(p, n, v, acceptor)

            # if none of the methods matched, we have an unknown request...
            else:
                if RECEIVER_DEBUG:
                    print "RECEIVER_DEBUG: Received an unknown request with method {}".format(method)

class rdtpReceiver():
    def __init__(self, proposer, acceptor, learner):
        self.proposer = proposer
        self.acceptor = acceptor
        self.learner = learner


    def serve(self, host, port):
        self.server = SocketServer.TCPServer((host, port), rdtpHandler, False)

        # !# HACK. Gross. Take this off Gabe. EW.
        self.server.receiver = self

        self.server.server_bind()
        self.server.server_activate()

        print 'Started listening on {}:{}'.format(host, port)

        thread.start_new_thread(self.serve_forever, ())

    def serve_forever(self):
        self.server.serve_forever()

    def handle_prepare(self, p, n, proposer):
        if RECEIVER_DEBUG:
            print "RECEIVER_DEBUG: PrepareRequest received: p = {}, n = {}, proposer = {}".format(p, n, proposer)

        return self.acceptor.handle_prepare(p, n, proposer)

    def handle_accept_request(self, p, n, v, proposer):
        if RECEIVER_DEBUG:
            print "RECEIVER_DEBUG: AcceptRequest received: p = {}, n = {}, v = {}, proposer = {}".format(p, n, v, proposer)

        return self.acceptor.handle_accept_request(p, n, v, proposer)

    def handle_promise(self, had_previous, p, n, v, acceptor):

        # handle the case where we had no previous value set
        if not had_previous:
            p = None
            v = None

        if RECEIVER_DEBUG:
            print "RECEIVER_DEBUG: PromiseRequest received: p = {}, n = {}, v = {}, acceptor = {}".format(p, n, v, acceptor)

        return self.proposer.handle_promise(had_previous, p, n, v, acceptor)

    def handle_refuse_promise(self, p, n, acceptor):
        if RECEIVER_DEBUG:
            print "RECEIVER_DEBUG: RefusePromiseRequest received: p = {}, n = {}, acceptor = {}".format(p, n, acceptor)

        return self.proposer.handle_refuse_promise(p, n, acceptor)

    def handle_accepted(self, p, n, v, acceptor):
        if RECEIVER_DEBUG:
            print "RECEIVER_DEBUG: AcceptedRequest received: p = {}, n = {}, v = {}, acceptor = {}".format(p, n, v, acceptor)

        return self.learner.handle_accepted(p, n, v, acceptor)
