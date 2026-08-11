from threading import Lock, Condition
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from random import uniform

# ! The bug here is that once T4 (assuming 5 total threads T0 to T4) calls wait()
# ! at the first barrier, num_threads will be set to 5 and can_cross to True
# ! and num_threads_waiting to 0 and it notifies all the other threads
# ! But if this thread continues and calls the wait() on the second barrier
# ! then num_threads will become 1 and can_cross is already set to False
# ! before any of the other threads could cross the first barrier

class ReusableBarrier: 
    def __init__(self, n):
        self.n = n
        self.lock = Lock()
        self.cv = Condition(self.lock)
        self.num_threads_waiting = 0
        self.can_cross = False

    def wait(self):
        with self.lock:
            # Increment the number of waiting threads            
            self.num_threads_waiting += 1

            # If this is the first thread we need the barrier to be reusable
            # so we make the can_cross to False as it could be True from
            # the previous use
            if self.num_threads_waiting == 1:
                self.can_cross = False

            # If this is the nth thread we can let all the threads through
            # so we can notify all of them and also exit the function
            # as we don't need this thread to wait
            if self.num_threads_waiting == self.n:
                # We also reset the num threads so that the barrier becomes reusable
                self.can_cross = True
                self.num_threads_waiting = 0
                self.cv.notify_all()
                return

            # Mesa semantics, as long as can_cross is False, we keep waiting
            # on the condition variable
            while not self.can_cross:
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


