"""
This module provides an implementation of the Receiver class using our own
RDTP Protocol, which we wrote for the Chat Assignment in CS262
"""

import socket
import select
import thread

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from rdtp import rdtp

TIMEOUT_SECONDS = 10
RECEIVER_DEBUG = True

MAX_PENDING_CLIENTS = 50


class rdtpReceiver():
    def __init__(self, proposer, acceptor, learner):
        self.proposer = proposer
        self.acceptor = acceptor
        self.learner = learner


    def serve(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(0)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))

        self.sockets = [self.socket]

        print 'Started listening on {}:{}'.format(host, port)

        thread.start_new_thread(self.serve_forever, ())

    def serve_forever(self):
        self.socket.listen(MAX_PENDING_CLIENTS)

        while 1:
            # This blocks until we are ready to read some socket
            ready_to_read,_,_ = select.select(self.sockets,[],[],3)

            for sock in ready_to_read:
                # New client connection!
                # we accept the connection and get a new socket
                # for it
                if sock == self.socket:
                    new_client_sock, client_addr = sock.accept()
                    self.sockets.append(new_client_sock)
                    print 'New client connection with address [%s:%s]' % client_addr
                # Old client wrote us something. It must be
                # a message!
                else:
                    try:
                        status, args = rdtp.recv(sock)
                    except rdtp.ClientDead:
                        print "Client died"
                        self.sockets.remove(sock)
                        continue

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
                        self.handle_prepare(p, n, proposer)

                    elif method == 'send_promise':
                        if len(args) != 6:
                            self.usage_args(method, len(args), 6)
                            return

                        had_previous, p, n, v, acceptor = 'True' == args[1], int(args[2]), int(args[3]), int(args[4]), str(args[5])
                        self.handle_promise(had_previous, p, n, v, acceptor)

                    elif method == 'send_accept_request':
                        if len(args) != 5:
                            self.usage_args(method, len(args), 5)
                            return

                        p, n, v, proposer = int(args[1]), int(args[2]), int(args[3]), str(args[4])
                        self.handle_accept_request(p, n, v, proposer)

                    elif method == 'send_refuse_proposal':
                        if len(args) != 4:
                            self.usage_args(method, len(args), 4)
                            return

                        p, n, acceptor = int(args[1]), int(args[2]), str(args[3])
                        self.handle_refuse_promise(p, n, acceptor)

                    elif method == 'send_accepted':
                        if len(args) != 5:
                            self.usage_args(method, len(args), 5)
                            return

                        p, n, v, acceptor = int(args[1]), int(args[2]), int(args[3]), str(args[4])
                        self.handle_accepted(p, n, v, acceptor)

                    # if none of the methods matched, we have an unknown request...
                    else:
                        if RECEIVER_DEBUG:
                            print "RECEIVER_DEBUG: Received an unknown request with method {}".format(method)


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
