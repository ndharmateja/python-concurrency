from concurrent.futures import ThreadPoolExecutor
from time import sleep
from random import uniform
from threading import Semaphore, Lock
from queues.circular_array_queue import Queue

MAX_ITEMS = 5
queue = Queue(MAX_ITEMS)
has_space = Semaphore(MAX_ITEMS)
has_items = Semaphore(0)
lock = Lock()

# For this implementation of the producer-consumer (using semaphores)
# we DO NOT need the Queue to be thread safe as we are using our own lock

def producer(producer_id):
    for i in range(6):
        sleep(uniform(0.5, 1))
        val = f"P{producer_id}-{i}"

        has_space.acquire()
        with lock:
            queue.enqueue(val)
            print(f"producer {producer_id} produced {val}. Queue: {queue}")
        has_items.release()

def consumer(consumer_id):
    for _ in range(8):
        sleep(uniform(3, 5))

        has_items.acquire()
        with lock:
            val = queue.dequeue()
            print(f"consumer {consumer_id} consumed {val}. Queue: {queue}")
        has_space.release()

def main():
    # Launch 3 producers and 2 consumers
    NUM_PRODUCERS = 4
    NUM_CONSUMERS = 3
    with ThreadPoolExecutor() as executor:
        producer_futures = [ executor.submit(producer, id) for id in range(NUM_PRODUCERS) ]
        consumer_futures = [ executor.submit(consumer, id) for id in range(NUM_CONSUMERS) ]
        for f in producer_futures + consumer_futures:
            f.result()

if __name__ == "__main__":
    main()