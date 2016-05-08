"""
This module implements a proposal.
"""

class Proposal():
    """
    Implementation of a Paxon proposal. Instead of simply keeping a number
    and a value (as in the Synod algorithm, described by Lamport), we also
    keep the decree number.
    """

    def __init__(self, p, proposer, n, v):
        self.p = p
        self.proposer = proposer
        self.n = n
        self.v = v
        return
