from threading import Lock, Condition
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from random import uniform

# To fix the bug from the buggy version
# we the generation number instead of can_cross boolean flag
# The generation would increment only when the last thread calls wait()
# on the barrier
# So we wait on the CV as long as curr_generation == the barrier's generation
# because as soon as the barrier's generation gets updated 
# it means the last thread called wait() => all threads from the 
# previous generation are free to cross 

class ReusableBarrier: 
    def __init__(self, n):
        self.n = n
        self.lock = Lock()
        self.cv = Condition(self.lock)
        self.num_threads_waiting = 0
        self.generation = 0

    def wait(self):
        with self.lock:
            # Increment the number of waiting threads and get the current generation       
            self.num_threads_waiting += 1
            curr_generation = self.generation

            # If this is the nth thread we can let all the threads through
            # so we can notify all of them and also exit the function
            # as we don't need this thread to wait
            if self.num_threads_waiting == self.n:
                # We also reset the num threads so that the barrier becomes reusable
                self.generation += 1
                self.num_threads_waiting = 0
                self.cv.notify_all()
                return

            # Mesa semantics, as long as can_cross is False, we keep waiting
            # on the condition variable
            while curr_generation == self.generation:
                # If one of the first n-1 threads run this
                # we have to block it, we do that using the cv's wait
                self.cv.wait()

NUM_THREADS = 5

def worker(id, barrier):
    # First phase of the work before the barrier
    print(f"Begin thread {id}")
    sleep(uniform(id + 1, id + 3))

    # Wait for all the threads to arrive at the barrier
    print(f"thread {id} arrived at the first barrier")
    barrier.wait()
    print(f"thread {id} crossed the first barrier")

    # Second phase of work
    sleep(uniform((NUM_THREADS - id) + 3, (NUM_THREADS - id) + 5))

    # Wait for all the threads to arrive at the barrier again
    print(f"thread {id} arrived at the second barrier")
    barrier.wait()
    print(f"thread {id} crossed the second barrier and done")

def main():
    barrier = ReusableBarrier(NUM_THREADS)
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(worker, id, barrier) for id in range(NUM_THREADS)]
        for future in futures:
            future.result()

    print("Main thread done!")

if __name__ == "__main__":
    main()


