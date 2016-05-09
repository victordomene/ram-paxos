"""
Plots a python pickle that represents a dictionary that is indexed into by a tuple of integers
"""
import sys
import matplotlib.pyplot as plt
import pickle

def usage():
    print "python graph.py filename"


if len(sys.argv) != 2:
    usage()
    sys.exit(1)

filename = sys.argv[1]


# first try to open the file
try:
    f = open(filename, "r")
except:
    print "Error opening file %s" % (filename)
    exit(2)

assert(f is not None)
# now try to depickle it

diff_dict = None

try:
    diff_dict = pickle.load(f)
except:
    print "Error depickling file %s" % (filename)
    exit(2)

diff_values = diff_dict.values()

plt.hist(diff_values, 20)
plt_title = "Learn time for %i different proposals" % (len(diff_values))
plt.title(plt_title)
plt.xlabel("Time in seconds")
plt.ylabel("Frequency")

plt.show()
