# This queue implementation is not thread safe
class Queue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.count = 0
        self.items = [None for _ in range(self.capacity)]
        self.fill_ptr = self.use_ptr = 0

    def enqueue(self, item):
        self.items[self.fill_ptr] = item
        self.fill_ptr = (self.fill_ptr + 1) % self.capacity
        self.count += 1

    def dequeue(self):
        val = self.items[self.use_ptr]
        self.use_ptr = (self.use_ptr + 1) % self.capacity
        self.count -= 1
        return val

    def is_full(self): return self.count == self.capacity
    def is_empty(self): return self.count == 0

    def __str__(self):
        result = "front <- [ "
        for i in range(self.count):
            result += str(self.items[(i + self.use_ptr) % self.capacity])
            result += " "
        result += "] <- back"
        return result