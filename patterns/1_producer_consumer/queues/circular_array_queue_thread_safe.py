from threading import Lock

# Thread safe Circular Array Queue
# The logic in the producer consumer ensures that
# enqueue() won't be called when the queue is full
# and dequeue() won't be called when the queue is empty
# so we don't need the count variable
# And we don't also need the is_full() and is_empty() methods
# as the number of items are tracked by the semaphore
class Queue:
    def __init__(self, capacity):
        self.items = [None for _ in range(capacity)]
        self.fill_ptr = self.use_ptr = 0
        self.lock = Lock()

    def enqueue(self, item):
        with self.lock:
            self.items[self.fill_ptr] = item
            self.fill_ptr = (self.fill_ptr + 1) % len(self.items)

    def dequeue(self):
        with self.lock:
            val = self.items[self.use_ptr]
            self.use_ptr = (self.use_ptr + 1) % len(self.items)
        return val