"""
This module implements a proposal.
"""

class Proposal():
	"""
	Implementation of a Paxon proposal. Instead of simply keeping a number
	and a value (as in the Synod algorithm, described by Lamport), we also
	keep the decree number.
	"""

	def __init__(self):
		self.number = None
		self.decree = None
		self.value = None
		return

	@property
	def number(self):
		"""
		The number of this proposal.
		"""
		return self.number

	@property
	def decree(self):
		"""
		The decree number to which this proposal refers to.
		"""
		return self.decree

	@property
	def value(self):
		"""
		The value proposed.
		"""
		return self.value
