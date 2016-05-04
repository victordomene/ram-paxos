# List of TODOs

* Define each of the specific messengers, how they are supposed to be 
communicating.
	* gRPC seems like a very easy and trusty way to do this;
	* global shared queues also should work (even though this is kind of
cheating);
	* some kind of interprocess communication (pipes, or even files) to
simulate the network (especially in the beginning).
* Specify how exactly we are going to find quorums and how machines will be
added to the network. Maybe find a reference on how this is actually done.
	* So far, I think this will not be *that hard*.
* Write the *actual* implementations of the classes.
* Write a simple workload case so that Gabe & Brian can easily work on the
workloads in parallel, while Victor works on getting Paxos to work nicely and
beautifully.
