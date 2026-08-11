from threading import Lock, Condition

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
