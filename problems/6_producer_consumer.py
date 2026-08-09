from concurrent.futures import ThreadPoolExecutor
from time import sleep
from random import uniform
from threading import Lock, Condition

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


data_lock = Lock()
has_items = Condition(data_lock)
has_space = Condition(data_lock)
queue = Queue(3)


def producer(producer_id):
    for i in range(6):
        sleep(uniform(0.5, 1))
        val = f"P{producer_id}-{i}"
        with data_lock:
            while queue.is_full():
                has_space.wait()
            queue.enqueue(val)
            has_items.notify()
            print(f"producer {producer_id} produced {val}. Queue: {queue}")

def consumer(consumer_id):
    for _ in range(9):
        sleep(uniform(3, 5))
        with data_lock:
            while queue.is_empty():
                has_items.wait()
            val = queue.dequeue()
            has_space.notify()
            print(f"consumer {consumer_id} consumed {val}. Queue: {queue}")

def main():
    # with ThreadPoolExecutor() as executor:
    #     pf = executor.submit(producer)
    #     cf = executor.submit(consumer)
    #     pf.result()
    #     cf.result()

    # Launch N Producer tasks
    NUM_PRODUCERS = 3
    NUM_CONSUMERS = 2
    with ThreadPoolExecutor() as executor:
        producer_futures = [
            executor.submit(producer, p_id) for p_id in range(NUM_PRODUCERS)
        ]
        consumer_futures = [
            executor.submit(consumer, c_id) for c_id in range(NUM_CONSUMERS)
        ]
        for f in producer_futures + consumer_futures:
            f.result()

if __name__ == "__main__":
    main()