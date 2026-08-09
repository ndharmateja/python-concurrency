from concurrent.futures import ThreadPoolExecutor
from time import sleep
from random import uniform
from threading import Lock, Condition
from queues.circular_array_queue import Queue

# Launch 3 producers and 2 consumers
NUM_PRODUCERS = 3
NUM_CONSUMERS = 2
NUM_PRODUCER_LOOPS = 6
NUM_CONSUMER_LOOPS = (NUM_PRODUCERS * NUM_PRODUCER_LOOPS) // NUM_CONSUMERS
MAX_ITEMS = 5
data_lock = Lock()
has_items = Condition(data_lock)
has_space = Condition(data_lock)

# This queue need not be thread-safe as our lock (which we are using along
# with the CV ensures that the enqueue() and dequeue() are atomic and that only
# one of them would be called at any point of time)
queue = Queue(MAX_ITEMS)

def producer(producer_id):
    for i in range(NUM_PRODUCER_LOOPS):
        sleep(uniform(0.5, 1))
        val = f"P{producer_id}-{i}"
        with data_lock:
            while queue.is_full():
                has_space.wait()
            queue.enqueue(val)
            has_items.notify()
            print(f"producer {producer_id} produced {val}. Queue: {queue}")

def consumer(consumer_id):
    for _ in range(NUM_CONSUMER_LOOPS):
        sleep(uniform(3, 5))
        with data_lock:
            while queue.is_empty():
                has_items.wait()
            val = queue.dequeue()
            has_space.notify()
            print(f"consumer {consumer_id} consumed {val}. Queue: {queue}")

def main():
    with ThreadPoolExecutor() as executor:
        producer_futures = [ executor.submit(producer, id) for id in range(NUM_PRODUCERS) ]
        consumer_futures = [ executor.submit(consumer, id) for id in range(NUM_CONSUMERS) ]
        for f in producer_futures + consumer_futures:
            f.result()

if __name__ == "__main__":
    main()