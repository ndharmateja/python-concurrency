from threading import Lock

# Michael and Scott's version of the concurrent linked queue with
# two locks (see page 362 of OSTEP book) to improve concurrency
# enqueue() at tail and dequeue() at head
# The logic in the producer consumer (with semaphores) ensures that
# dequeue() won't be called when the queue is empty
# and that there won't be more than MAX_ITEMS (declared in the
# producer consumer file) enqueued at any point in time
class _Node:
    def __init__(self, val):
        self.val = val
        self.next: _Node = None

class Queue:
    def __init__(self):
        self.head = self.tail = _Node(None)
        self.head_lock = Lock()
        self.tail_lock = Lock()

    def enqueue(self, val):
        new_node = _Node(val)
        with self.tail_lock:
            self.tail.next = new_node
            self.tail = self.tail.next

    def dequeue(self):
        with self.head_lock:
            new_head = self.head.next
            self.head = self.head.next
        return new_head.val
