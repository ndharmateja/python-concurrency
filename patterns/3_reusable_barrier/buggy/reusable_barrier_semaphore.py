from threading import Semaphore

# ! This implementation is buggy as, if there are 2 threads (T0 and T1)
# ! T0 could first increment the num_threads to 1 and then get interrupted
# ! right before acquire() was called
# ! Now if T1 runs, it would increment num_threads to 2 and then reset
# ! the num_threads to 0 and release() which won't wake up any thread
# ! but the semaphore value becomes 1
# ! Now if T1 continues to run and calls wait() for the second time, it would
# ! increment the num_threads to 1 and call acquire which it would return
# ! immediately as the semaphore's value was 1 before the acquire() call
# ! letting it pass immediately

class ReusableBarrier: 
    def __init__(self, n):
        self.n = n
        self.num_threads_waiting = 0
        self.mutex = Semaphore(1)
        self.sem = Semaphore(0)

    def wait(self):
        with self.mutex:
            self.num_threads_waiting += 1

            # If this is the nth thread calling wait() then 
            # we would have to wake up all the remaining n-1 threads
            # and also reset the instance variables
            if self.num_threads_waiting == self.n:
                # ! We need to reset the num_threads to 0 first before releasing
                # ! to avoid race conditions as the one of the other threads could
                # ! immediately run the wait() method and would have a wrong
                # ! num_threads_waiting value
                # ! Actually it won't matter as we are using the mutex
                self.num_threads_waiting = 0
                for _ in range(self.n - 1):
                    self.sem.release()
                return

        # If this is called by one of the first n-1 threads
        # then we need to acquire (wait on) the semaphore which won't be
        # acquired as the initial value is 0
        self.sem.acquire()
