1. circular array queue with 2 locks as enqueue() won't be called on a full queue and dequeue() won't be called on an empty queue.
2. instead of hardcoding the number of consumer threads and number of loops per consumer (which would mean that each consumer runs for a fixed number of times), stop the consumers once all the producers are done.
   1. use one sentinel (which once a consumer finds can stop that thread and re-enqueue the sentinel for the next consumer)
   2. sentinel per consumer 