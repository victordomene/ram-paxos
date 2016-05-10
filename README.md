# RAM Paxos: a performance comparison

This project presents a simple implementation of Paxos in Python, and several
workloads that are used to measure its performance with different configurations.
In particular, we will be measuring the performance of the algorithm when the
ledgers must be written to a durable and reliable storage (such as the disk),
and when it can remain in RAM.

## Components

For the architecture, check out `/writeup/final_paper.pdf`. The core code can be found in `/paxos/`.


## Setup instructions and Usage

This code has been tested on both Mac OS X El Capitan and the latest release of Ubuntu.

Clone this repository, and use Python on any of the workloads in `/workloads/` or the tests in `/paxos/test/` in order to test the implementation. Documentation on each workload/test is provided
inside its `.py` file.

This repository includes a compiled version of the Protocol Buffers used in
gRPC. If you want to compile it, follow the instructions in

`https://developers.google.com/protocol-buffers/`

In order to run the gRPC version of the code, you will also need to install
the gRPC library for Python:

`pip install grpcio`

This assumes you have `pip` installed; this is easy to get online.

## Using the Paxos client

Once you start up a Paxos workload (i.e. with `python sample_workload.py`) it will spawn a network of virtual machines talking to each other and passing greek decrees, but it will, by default, print nothing of what the Paxos agents are actually choosing. If you wish to see the ledger of one of the learners, you have to run the `client.py` found in `workloads/`. It accepts arguments of the type

`host:port:command`

sending a given command to the VM running at (host, port). The possible commands are

`print_ledger`
`print_differences`
`print_difference_mean`

Where `print_ledger` prints all of the passed decrees learned by the given VM. The other two commands are used to print the differences in time between the time a proposal is sent and the time the decree is passed.

A common usage would be to spawn a workload with some VM running in port 6666 in a terminal window, and then open the client in another window and invoke

`localhost:6666:print_ledger`


## Documentation

Documentation for the code can be found in the `/doc/` directory. It contains
HTML compiled by PyDoc.
