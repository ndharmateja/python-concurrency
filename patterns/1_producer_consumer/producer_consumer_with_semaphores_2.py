from concurrent.futures import ThreadPoolExecutor
from time import sleep
from random import uniform
from threading import Semaphore
from queues.circular_array_queue_thread_safe import Queue

MAX_ITEMS = 5
queue = Queue(MAX_ITEMS)
has_space = Semaphore(MAX_ITEMS)
has_items = Semaphore(0)

# For this implementation of the producer-consumer (using semaphores)
# we need the Queue to be thread safe
# The print statements are just for reference, they need not be printed
# accurately as we don't have any locks to make sure that the production
# and the print statement are atomic

def producer(producer_id):
    for i in range(6):
        sleep(uniform(0.5, 1))
        val = f"P{producer_id}-{i}"
        has_space.acquire()
        queue.enqueue(val)
        print(f"producer {producer_id} produced {val}")
        has_items.release()

def consumer(consumer_id):
    for _ in range(8):
        sleep(uniform(3, 5))
        has_items.acquire()
        val = queue.dequeue()
        print(f"consumer {consumer_id} consumed {val}")
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