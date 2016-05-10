"""
This workload presents a simple interface that can be reused in other workloads.
It summary, it runs several subprocesses using the multiprocessing package,
makes the connections between them, and then starts working.

This particular workload spawns NETWORK_SIZE machines, NUM_PROPOSERS of which are 
proposers. We can run with either gRPC or RDTP by changing start_vm or
proposer_entrypoint / replicas_entrypoint. Just make sure that the workload
does not start with replicas running gRPC and proposer running RDTP.
"""

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import time
from multiprocessing import Process
from paxos.vm import VM

from paxos.messengers import rpcMessenger
from paxos.receivers import rpcReceiver

from paxos.messengers import rdtpMessenger
from paxos.receivers import rdtpReceiver
from paxos import proposer, acceptor, learner

NETWORK_SIZE = 10
NUM_PROPOSERS = 3
HOST = "localhost"
START_PORT = 6666

def initialize_rdtp_vm(name, use_disk):
    return VM(name, rdtpMessenger.rdtpMessenger, rdtpReceiver.rdtpReceiver, use_disk)

def initialize_grpc_vm(name, use_disk):
    return VM(name, rpcMessenger.grpcMessenger, rpcReceiver.grpcReceiver, use_disk)

def start_vm(name, network, initialize_vm = initialize_rdtp_vm):
    """
    Starts a virtual machine with a given initializer.
    Already starts serving.

    @param name: the name of the machine that will be started
    @param network: a dictionary containing information on the machines in
    the network
    @param initialize_vm: an initializer for the VM; by default, RDTP

    @return: The instance of the RDTP virtual machine
    """

    # initialize the virtual machine with my name
    vm = initialize_vm(name, use_disk=False)

    # fetch the host/port information from the network for me
    host, port = network[name]
 
    # add other machines
    for friend_name, (friend_host, friend_port) in network.iteritems():
        # !# should we send it to ourselves?
        if friend_name == name:
            continue

        vm.add_destination(friend_name, friend_host, friend_port)
    
    # start serving
    vm.serve(host, port)

    return vm 

def proposer_entrypoint(name, network):
    """
    Thread entrypoint for a proposer.

    This must simply call start_rdtp_vm with our name and network. 
    """
    # start an rdtp VM with our name and start serving 
    vm = start_vm(name, network)

    # sleep a little bit before trying to send proposals
    # (cheating for bootstrap)
    time.sleep(2)

    # decree number and value; these will change
    n = 0
    v = 5000

    while True:
        # propose values
        vm.propose_to_quorum(n, v)

        # update values for next round
        n += 1
        v -= 1

        # give some time before proposing again
        time.sleep(1)

def replicas_entrypoint(name, network):
    # start an rdtp VM with our name and start serving
    vm = start_vm(name, network)

    # simply sleep forever, the server will handle the
    # necessary requests
    try:
        while True:
            time.sleep(600)
    except KeyboardInterrupt:
        vm.stop_server()

def main():
    """
    Main routine for this workload; spawn a single proposer and a variable
    number of acceptors (NETWORK_SIZE - 1).
    """

    # a network is a dictionary of names => (host, port)
    # we first build a network; then we spawn proposers, and finally
    # spawn replicas
    network = {}

    # initialize the network
    for i in xrange(NETWORK_SIZE):
        name = "M" + str(i)
        network[name] = (HOST, START_PORT + i)

    # initialize the proposer process
    for i in xrange(NUM_PROPOSERS):
        proposer = Process(target = proposer_entrypoint, args = ("M" + str(i), network))
        proposer.start()
    
    # initialize all the replicas
    for name in network.keys():
        # these are all proposers; ignore them here
        if name < "M" + str(NUM_PROPOSERS):
            print name
            continue

        replicas = Process(target = replicas_entrypoint, args = (name, network))
        replicas.start()

if __name__ == "__main__":
    main()
