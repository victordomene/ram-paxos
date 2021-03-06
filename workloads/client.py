"""
This file implements a set of tests for a server that uses the gRPC protocol
defined by paxos.proto.
"""

# import time
import socket

# attach the appropriate directories to sys.path
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from paxos.rdtp import rdtp

def init_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


def run():

    while True:
        host, port, comm = raw_input().split(":")
        sock = init_socket(host, int(port))
        rdtp.send(sock, 0, comm)



if __name__ == "__main__":
    run()
