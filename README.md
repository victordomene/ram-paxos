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

## Documentation

Documentation for the code can be found in the `/doc/` directory. It contains
HTML compiled by PyDoc.
